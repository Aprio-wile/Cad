# 3D Cardiac Risk Visualizer (CAD Prediction System)

An end-to-end machine learning application that predicts Coronary Artery Disease (CAD) and vessel-specific risks (such as LAD and LCX blockages) using clinical indicators. It features an interactive **3D Cardiac Risk Visualizer** web interface powered by a Python backend.

---

## Features

* **Predictive Modeling**: Utilizes pre-trained machine learning and XGBoost models (`model_cath.pkl`, `model_xgb_lad.pkl`, `model_xgb_lcx.pkl`) trained on clinical health parameters (based on the [Z-Alizadeh Sani dataset](https://github.com/Aprio-wile/Cad/blob/master/extention%20of%20Z-Alizadeh%20sani%20dataset.xlsx)).
* **Interactive 3D Visualizer**: A web interface (`app.py` and static assets) providing real-time risk estimation and anatomical visualization.
* **Jupyter Notebook Research**: Includes experimentation and training workflows (`CAD_prediction.ipynb`).

---

## Project Structure

```text
├── app.py                      # Flask/Web backend application
├── CAD_prediction.ipynb        # Jupyter notebook for model training & evaluation
├── extention of Z-Alizadeh sani dataset.xlsx # Clinical dataset file
├── model_cath.pkl              # Serialized main CAD prediction model
├── model_xgb_lad.pkl           # Serialized XGBoost LAD model
├── model_xgb_lcx.pkl           # Serialized XGBoost LCX model
├── static/                     # Frontend assets (CSS, JS, 3D models)
└── .vscode/                    # Workspace configuration

```

---

# 3D Cardiac Risk Visualizer (CAD Prediction System)

An end-to-end machine learning application that predicts Coronary Artery Disease (CAD) and vessel-specific risks (such as LAD and LCX blockages) using clinical indicators. It features an interactive **3D Cardiac Risk Visualizer** web interface powered by a Python backend.

---

## Features

* **Predictive Modeling**: Utilizes pre-trained machine learning and XGBoost models (`model_cath.pkl`, `model_xgb_lad.pkl`, `model_xgb_lcx.pkl`) trained on clinical health parameters (based on the [Z-Alizadeh Sani dataset](https://github.com/Aprio-wile/Cad/blob/master/extention%20of%20Z-Alizadeh%20sani%20dataset.xlsx)).
* **Interactive 3D Visualizer**: A web interface (`app.py` and static assets) providing real-time risk estimation and anatomical visualization.
* **Jupyter Notebook Research**: Includes experimentation and training workflows (`CAD_prediction.ipynb`).

---

## Project Structure

```text
├── app.py                      # Flask/Web backend application
├── CAD_prediction.ipynb        # Jupyter notebook for model training & evaluation
├── extention of Z-Alizadeh sani dataset.xlsx # Clinical dataset file
├── model_cath.pkl              # Serialized main CAD prediction model
├── model_xgb_lad.pkl           # Serialized XGBoost LAD model
├── model_xgb_lcx.pkl           # Serialized XGBoost LCX model
├── static/                     # Frontend assets (CSS, JS, 3D models)
└── .vscode/                    # Workspace configuration
