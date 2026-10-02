import requests
import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="Cardiovascular 3D Risk Visualizer",
    page_icon="🫀",
    layout="wide",
)

st.title("🫀 3D Cardiac Risk & Coronary Artery Stenosis Predictor")
st.markdown(
    "Adjust clinical metrics in the sidebar to dynamically generate 3D vessel risk visualizations."
)

# 2. Sidebar Inputs (Patient Clinical Parameters)
st.sidebar.header("📋 Patient Clinical Features")

age = st.sidebar.slider("Age", 30, 90, 58)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
bmi = st.sidebar.slider("BMI", 15.0, 45.0, 28.5)
bp = st.sidebar.slider("Systolic BP (mmHg)", 90, 200, 130)
fbs = st.sidebar.slider("Fasting Blood Sugar (FBS)", 70, 300, 110)
ef_tte = st.sidebar.slider("Ejection Fraction (EF-TTE %)", 15, 70, 50)

htn = st.sidebar.selectbox("Hypertension (HTN)", [0, 1], index=1)
dm = st.sidebar.selectbox("Diabetes Mellitus (DM)", [0, 1], index=0)
current_smoker = st.sidebar.selectbox("Current Smoker", [0, 1], index=0)
typical_cp = st.sidebar.selectbox("Typical Chest Pain", [0, 1], index=1)
vhd = st.sidebar.selectbox(
    "Valvular Heart Disease (VHD)", ["N", "mild", "Severe"], index=0
)


# 3. Dynamic 3D Model Renderer Function with Real-Time Colors & Coordinates
def render_3d_heart_with_hotspots(
    lad_risk, lcx_risk, rca_risk, lad_color, lcx_color, rca_color
):
  html_code = f"""
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
    
    <style>
      .hotspot {{
        display: block;
        width: 16px;
        height: 16px;
        border-radius: 8px;
        border: 2px solid white;
        box-sizing: border-box;
        cursor: pointer;
        transition: transform 0.2s;
      }}
      
      .hotspot:hover {{
        transform: scale(1.3);
      }}

      /* Dynamically inject risk colors returned by backend model */
      .hotspot[slot="hotspot-lad"] {{ background-color: {lad_color}; }}
      .hotspot[slot="hotspot-lcx"] {{ background-color: {lcx_color}; }}
      .hotspot[slot="hotspot-rca"] {{ background-color: {rca_color}; }}

      .annotation {{
        background-color: rgba(15, 23, 42, 0.9);
        color: white;
        position: absolute;
        transform: translate(15px, -15px);
        border-radius: 6px;
        padding: 8px 12px;
        font-family: sans-serif;
        font-size: 14px;
        border: 1px solid #444;
        display: none;
        white-space: nowrap;
        pointer-events: none;
        z-index: 10;
      }}
      
      .hotspot:hover .annotation {{
        display: block;
      }}
    </style>

    <div style="width: 100%; height: 500px;">
        <model-viewer 
            src="http://localhost:8000/static/heart.glb" 
            alt="3D Heart Model" 
            auto-rotate 
            camera-controls 
            style="width: 100%; height: 100%; background-color: transparent;">
            
            <!-- LAD Hotspot -->
            <button class="hotspot" slot="hotspot-lad" data-position="0.16755185357773228m -0.156195866205191m -0.22095659286859315m" data-normal="0.9672626258336271m 0.1480235666039187m -0.20613596579755866m">
                <div class="annotation"><strong>LAD Risk:</strong> {lad_risk:.1f}%</div>
            </button>
            
            <!-- LCX Hotspot -->
            <button class="hotspot" slot="hotspot-lcx" data-position="-0.14760723150383215m -0.03315664008045538m 0.07581237825668452m" data-normal="-0.7441572966679513m 0.29130026735339676m 0.6011439694912412m">
                <div class="annotation"><strong>LCX Risk:</strong> {lcx_risk:.1f}%</div>
            </button>
            
            <!-- RCA Hotspot -->
            <button class="hotspot" slot="hotspot-rca" data-position="0.2182989211104156m -0.13248988640234505m 0.10984203945245175m" data-normal="0.5708740360735403m 0.21053483495421774m -0.7935854826090927m">
                <div class="annotation"><strong>RCA Risk:</strong> {rca_risk:.1f}%</div>
            </button>
            
        </model-viewer>
    </div>
    """
  components.html(html_code, height=550)


# 4. Payload & API Request
payload = {
    "Age": age,
    "Sex": sex,
    "BMI": bmi,
    "Systolic_BP": bp,
    "FBS": fbs,
    "EF_TTE": ef_tte,
    "HTN": htn,
    "DM": dm,
    "Current_Smoker": current_smoker,
    "Typical_Chest_Pain": typical_cp,
    "VHD": vhd,
}

API_URL = "http://localhost:8000/predict"

col1, col2 = st.columns([1, 2])

try:
  response = requests.post(API_URL, json=payload)

  if response.status_code == 200:
    data = response.json()["results"]

    with col1:
      st.subheader("📊 Diagnostic Summary")
      st.metric(
          "Overall CAD Risk (Cath)",
          f"{data['cath']['risk_score']}%",
          delta=data["cath"]["status"],
          delta_color=(
              "inverse" if data["cath"]["probability"] >= 0.5 else "normal"
          ),
      )
      st.write("---")
      st.write(
          f"**LAD Vessel Risk:** <span style='color:{data['lad']['color']};font-weight:bold;'>{data['lad']['risk_score']}% ({data['lad']['status']})</span>",
          unsafe_allow_html=True,
      )
      st.write(
          f"**LCX Vessel Risk:** <span style='color:{data['lcx']['color']};font-weight:bold;'>{data['lcx']['risk_score']}% ({data['lcx']['status']})</span>",
          unsafe_allow_html=True,
      )
      st.write(
          f"**RCA Vessel Risk:** <span style='color:{data['rca']['color']};font-weight:bold;'>{data['rca']['risk_score']}% ({data['rca']['status']})</span>",
          unsafe_allow_html=True,
      )

    with col2:
      st.subheader("🫀 Interactive 3D Cardiac Vessel Visualization")
      # Pass both probabilities and backend-determined colors directly into the 3D renderer
      render_3d_heart_with_hotspots(
          lad_risk=data["lad"]["risk_score"],
          lcx_risk=data["lcx"]["risk_score"],
          rca_risk=data["rca"]["risk_score"],
          lad_color=data["lad"]["color"],
          lcx_color=data["lcx"]["color"],
          rca_color=data["rca"]["color"],
      )
  else:
    st.error(f"API Error ({response.status_code}): {response.text}")

except requests.exceptions.ConnectionError:
  st.error(
      "🚨 Cannot connect to FastAPI backend. Ensure `app.py` is running on `http://localhost:8000`."
  )