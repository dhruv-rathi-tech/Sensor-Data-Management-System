# 📊 Smart Home Sensors Data Management System

This project is a **Database Management System (DBMS)** application designed to process, store, and visualize data from smart home sensors. It features a Python-based preprocessing pipeline to clean raw CSV data, loads the data into an **Oracle Database**, and provides an interactive web interface using **Streamlit** to query and export the data.

## 🚀 Features
- **Data Preprocessing Pipeline:** Cleans raw sensor data, removes duplicates/nulls, and formats the dataset.

- **Oracle Database Integration:** Automatically creates tables and inserts processed data securely into a local Oracle Database.

- **Interactive Web Interface:** A beautifully styled Streamlit frontend with a custom splash screen.

- **Custom SQL Queries:** Run arbitrary SQL commands directly from the UI and view the results in real-time.

- **Query Shortcuts:** Quick one-click buttons for common analytics like calculating average temperature/humidity, top active sensors, and tracking the latest records.

- **Export Capabilities:** Download query results easily as a CSV file.

## 🛠️ Tech Stack
- **Python 3.x**
- **Pandas & NumPy** (Data Processing)
- **Oracle Database (`oracledb`)** (Data Storage)
- **Streamlit** (Frontend Interface)

## 📁 Project Structure
```text
.
├── backend/
│   └── preprocessing.py       # Script for cleaning data and pushing to Oracle DB
├── frontend/
│   └── app.py                 # Streamlit web application
├── data/
│   ├── dataset.csv            # Raw dataset
│   └── processed_dataset.csv  # Cleaned dataset (generated via preprocessing.py)
└── README.md                  # Project documentation
```

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dhruv-rathi-tech/Sensor-Data-Management-System.git
   cd Sensor-Data-Management-System
   ```

2. **Install Required Packages:**
   Install the required dependencies:
```bash
   pip install pandas numpy oracledb streamlit
```

3. 3. **Database Configuration:**
   - Ensure **Oracle Database (XE)** is installed and running locally.
   - Update your credentials (username/password) in `backend/preprocessing.py` and `frontend/app.py` to match your local Oracle setup.

## ▶️ Running the Application

### Step 1: Process and Load the Data
Run the preprocessing script to clean the data and create the tables in your database:
```bash
python backend/preprocessing.py
```

### Step 2: Start the Web Interface
Run the Streamlit app to launch the dashboard in your browser:
```bash
streamlit run frontend/app.py
```

## 👥 Contributors
This project was developed for the DBMS course, submitted to **Dr. Sobitha Ahila**.
- **Aman Gupta**
- **Dhruv Rathi**
