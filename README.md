# Lie Detector with ARDUINO and ML

This project implements a basic **lie detection system** using Arduino and Machine Learning. It combines real-time biosignal acquisition from sensors connected to an Arduino board, and classification of truthful vs. deceptive responses using machine learning models trained in Python.

## 🚀 Features

- Real-time data acquisition using Arduino
- Signal preprocessing and feature extraction
- Supervised machine learning for binary classification (Lie / Truth)
- Simple, interpretable output
- Modular design for extensibility

## 🛠️ Components Used

- **Hardware:**
  - Arduino Uno
  - Galvanic Skin Response (GSR) sensor
  - Pulse Sensor
  - Jumper wires and breadboard
  - USB cable for serial communication

- **Software:**
  - Arduino IDE
  - Python 3.x
  - Libraries: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `serial`

## 📁 Project Structure

Lie-Detector-with-ARDUINO-and-ML/
│
├── Arduino_Code/ # Code to collect sensor data from Arduino
│ └── lie_detector.ino
│
├── Data/ # Raw and preprocessed datasets
│ ├── raw_data.csv
│ └── cleaned_data.csv
│
├── ML_Model/ # Jupyter notebooks and scripts for ML
│ ├── preprocessing.ipynb
│ ├── train_model.ipynb
│ └── model.pkl # Serialized trained model
│
├── Results/ # Plots and evaluation results
│ └── accuracy_plot.png
│
└── README.md # Project overview and instructions


## 📊 Working Principle

1. **Data Collection:** Arduino collects GSR and heart rate values during questioning.
2. **Data Logging:** Sensor values are sent via serial port and saved into a CSV.
3. **Feature Extraction:** Extract statistical features like mean, variance, peaks.
4. **Model Training:** A binary classifier (e.g., SVM, Decision Tree) is trained.
5. **Prediction:** New input data is classified as Lie or Truth in real time.

## 🔧 Setup Instructions

### Hardware

1. Connect the GSR sensor and Pulse sensor to Arduino Uno as per your wiring diagram.
2. Upload the `lie_detector.ino` sketch from `Arduino_Code/` using the Arduino IDE.

### Software

1. Clone this repository:
   ```bash
   git clone https://github.com/kanakroy13/Lie-Detector-with-ARDUINO-and-ML.git
   cd Lie-Detector-with-ARDUINO-and-ML

2.Install required Python packages:
 pip install -r requirements.txt

3. Run the data collection and ML training notebooks located in ML_Model/.


##🧠 Machine Learning Models
Several classifiers were tested, including:

Decision Tree

Support Vector Machine (SVM)

K-Nearest Neighbors (KNN)

Final model selection is based on accuracy, F1-score, and inference speed.

📌 Notes
This system is experimental and not suitable for legal or forensic use.

Data quality depends heavily on sensor placement and subject conditions.

Can be extended with more biosensors like EEG or facial emotion analysis.

📷 Sample Output

![Screenshot 2025-04-11 100356](https://github.com/user-attachments/assets/034741ec-0126-43e2-a4ae-47a5d3ae3472)

![Screenshot 2025-03-31 194355](https://github.com/user-attachments/assets/eefa0ceb-f900-476a-b379-9c7c3969d76d)

