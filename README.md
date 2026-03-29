[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Flutter](https://img.shields.io/badge/Flutter-3.10+-02569B.svg)](https://flutter.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)](https://scikit-learn.org/)

> **"Solving hardware failures in space with software intelligence on Earth."**

## About the Project

In the harsh environment of space, high-energy cosmic radiation particles can temporarily alter the state of memory bits (flipping 0s to 1s) in satellite computers. This phenomenon, known as a **Single Event Upset (SEU)**, causes massive, physically impossible spikes in telemetry data from sensors, jeopardizing mission safety and operational integrity.

**Perfectum Pipeline** is a hybrid artificial intelligence and statistical filtering system developed to solve this critical issue. The system ingests radiation-corrupted telemetry data, autonomously detects anomalies using Machine Learning (Isolation Forest), and mathematically reconstructs the damaged data points via linear interpolation with over 99% accuracy.

## Key Features

- ** AI-Based Anomaly Detection:** Utilizes `Scikit-Learn`'s Isolation Forest algorithm to mathematically identify and isolate sudden voltage/sensor spikes caused by cosmic radiation.
- ** Autonomous Data Repair:** Corrupted data points are purged and seamlessly reconstructed using Linear Interpolation, restoring the telemetry's natural trajectory.
- ** High-Speed Microservice:** A `FastAPI`-based backend processes raw telemetry data in milliseconds, serving cleaned JSON payloads ready for visualization.
- ** Real-Time Ground Control Station:** A modern, cross-platform dashboard built with `Flutter` and `fl_chart` that simultaneously visualizes raw, corrupted data alongside the AI-filtered safe data.
- ** Disaster Simulator:** Includes a custom Python data generation engine capable of simulating various space hazards (Classic SEUs, Solar Flare Noise, and Sensor Blackouts).

## Tech Stack

* **Backend & Data Science:** Python, Pandas, NumPy, Scikit-Learn
* **API & Server:** FastAPI, Uvicorn
* **Frontend & Data Visualization:** Flutter, Dart, fl_chart, http

---

## Installation & Execution

Follow these steps to run the project locally. The system architecture is divided into a Backend (Python) and a Frontend (Flutter).

### 1. Starting the Python Backend Server

First, install the required Python dependencies:

```bash
pip install pandas numpy scikit-learn fastapi uvicorn matplotlib
```
Generate the simulated test data (uydu_telemetri.csv) by running the disaster simulator:

```bash
python data_generator.py
```
Launch the FastAPI server:
```bash
python -m uvicorn api:app --reload
(The server will start running locally at http://127.0.0.1:8000)
```
2. Launching the Flutter Ground Control Dashboard
Open a new terminal session, navigate to the root directory of your Flutter project, and fetch the required packages:

```bash
flutter pub get
```
Run the application (on Web, Windows, or a connected mobile device/emulator):

```bash
flutter run
Note: If you are testing on an Android Emulator, make sure to update the API URL in main.dart to http://10.0.2.2:8000/telemetri_getir to properly route localhost traffic.
```

## Screenshots

Left/Red Line: Raw telemetry data suffering from cosmic radiation damage, spiking up to dangerous 30V levels.

Right/Blue Line: The smooth, safe telemetry trajectory instantly repaired by the Perfectum Pipeline using the Isolation Forest algorithm.
