


# 3D Cardiac Risk Visualizer (CAD Prediction System)

An end-to-end machine learning application and interactive web interface designed to predict Coronary Artery Disease (CAD) and vessel-specific risks (such as LAD and LCX blockages) using clinical health parameters.

---

## 🚀 Key Features

* **Machine Learning Pipelines**: Integrates pre-trained XGBoost models for targeted vessel risk assessment trained on clinical metrics.
* **Interactive 3D Visualizer**: A custom web dashboard powered by a Python backend (`app.py`), static assets, and 3D asset bundles (`cad_models_bundle/`) to render interactive anatomical heart models and risk hotspots.
* **Research & Analysis**: Includes a complete Jupyter notebook (`Copy of CAD prediction.ipynb`) detailing data preprocessing, exploration, and model training.

---

## 📁 Project Structure

```text
Cad/
├── app.py                                   # Python/Web backend application
├── Copy of CAD prediction.ipynb             # Jupyter notebook for model training & evaluation
├── extention of Z-Alizadeh sani dataset.xlsx # Clinical dataset source file
├── cad_models_bundle/                       # 3D anatomical model assets and bundles
├── static/                                  # Frontend assets (CSS, JS, 3D .glb models)
├── .vscode/                                 # Workspace configuration settings
├── requirements.txt                         # Python package dependencies
└── README.md                                # Project documentation


## ⚙️ Setup Instructions & Execution

git clone [https://github.com/Aprio-wile/Cad.git](https://github.com/Aprio-wile/Cad.git)
cd Cad
python -m venv venv

# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app:app --reload
streamlit run streamlit_app.py
