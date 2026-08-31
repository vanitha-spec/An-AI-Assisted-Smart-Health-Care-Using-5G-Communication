# AI-Assisted Smart Healthcare System Using 5G Communication

An intelligent healthcare monitoring framework that combines **IoT sensing, 5G communication, fog/cloud computing, and machine learning** to enable real-time patient monitoring and health condition prediction.

## 📌 Overview

Traditional healthcare monitoring systems rely on manual observation, delayed diagnosis, and slow data transmission over legacy 4G networks — making it hard to track patients continuously, especially the elderly, chronically ill, or those in remote areas. This project addresses that gap by building a simulated smart healthcare ecosystem where IoT sensor nodes continuously capture vital signs (heart rate, temperature, blood pressure), transmit them through fog nodes over a 5G-simulated network, and use hybrid machine learning models on the cloud side to classify patient health status in real time — with encrypted storage to protect sensitive medical data.

## 🎯 Key Features

- **IoT Health Network Simulation** – Simulated sensor nodes, fog nodes, and a cloud/central processing unit that mimic a real hospital-grade IoT monitoring setup.
- **5G vs 4G Performance Comparison** – Visualizes and compares packet delivery ratio and throughput to demonstrate 5G's advantage in low-latency medical data transmission.
- **Hybrid ML-Based Health Prediction** – Combines Random Forest and XGBoost in an ensemble model to classify patient health status, alongside a baseline SVM model for comparison.
- **Encrypted Data Storage** – Patient vitals are encrypted before being stored in the cloud database, decrypted only for authorized access.
- **Interactive Dashboard** – Web interface to view IoT network status, run predictions, view AI explanations, chat with a health assistant, analyze medical reports, and locate nearby hospitals.

## 🧠 Machine Learning Models

| Model | Role | Accuracy |
|---|---|---|
| SVM (baseline) | Classifies patient vitals into normal/abnormal categories | ~86% |
| Random Forest + XGBoost (hybrid ensemble) | Combines multiple learners for robust health condition classification | ~98% |

The hybrid ensemble approach significantly outperforms the standalone SVM model by reducing overfitting and better capturing complex, non-linear relationships in physiological data.

## 🏗️ System Architecture

The system follows a layered **IoT → Fog → Cloud** architecture:

1. **IoT Layer** – Sensor nodes continuously capture vital parameters from patients.
2. **Fog Layer** – Handles intermediate communication, reducing load on the cloud and enabling faster local processing.
3. **Cloud Layer** – Stores encrypted patient data, runs the trained ML models, and serves predictions to the web dashboard.
4. **Communication Layer** – Simulated 5G network transmission is benchmarked against 4G to demonstrate improvements in throughput and packet delivery.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 4
- **Database:** MySQL / SQLite
- **Machine Learning:** scikit-learn (SVM, Random Forest), XGBoost, NumPy, Pandas
- **Other:** Data encryption for secure storage, simulation scripts for IoT/5G network behavior

## 📂 Repository Structure

```
├── Dataset/           # Health datasets used for training/testing
├── Health/            # Core application logic
├── HealthApp/         # Django app configuration
├── model/             # Trained ML models
├── Simulation.py       # IoT/5G network simulation script
├── manage.py           # Django management script
├── db.sqlite3           # Application database
├── runServer.bat        # Script to launch the web server
├── runSimulation.bat    # Script to launch the network simulation
└── DatasetLink.txt      # Link to the source dataset
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/vanitha-spec/An-AI-Assisted-Smart-Health-Care-Using-5G-Communication.git
   cd An-AI-Assisted-Smart-Health-Care-Using-5G-Communication
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(If a `requirements.txt` isn't present yet, install Flask/Django, scikit-learn, xgboost, pandas, and numpy manually.)*

3. **Run the IoT/5G network simulation**
   ```bash
   runSimulation.bat
   ```

4. **Start the web application**
   ```bash
   runServer.bat
   ```
   or
   ```bash
   python manage.py runserver
   ```

5. Open your browser at `http://127.0.0.1:8000/` to access the dashboard.

## 📊 Results

- The 5G-simulated network achieved **over 90% packet delivery ratio** with higher throughput compared to a simulated 4G network.
- The hybrid Random Forest + XGBoost model achieved **~98% classification accuracy**, compared to **~86%** for the standalone SVM model.

## 🔮 Future Scope

- Integrate deep learning models (LSTM / Transformers) to capture temporal patterns in patient vitals.
- Add federated learning for privacy-preserving, decentralized model training across hospitals.
- Deploy lightweight models directly on IoT edge devices to cut latency.
- Use reinforcement learning for adaptive 5G network slicing based on healthcare traffic priority.
- Combine physiological signals with medical imaging and EHR data for improved diagnostic accuracy.

## 📄 License

This project was developed as an academic project. Feel free to explore, learn from, and build on it.

---

⭐ If you found this project useful, consider starring the repo!
