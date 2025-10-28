# ReCore — Processor Lifecycle Estimator

**ReCore** is an AI-powered desktop analytics system that predicts and visualizes the **lifecycle and performance health** of GPUs or processors based on their operational metrics.  
It combines **Machine Learning**, **Data Visualization**, and **Full-Stack Integration** to deliver insights into hardware longevity and efficiency.

---

## Project Overview

ReCore consists of three main modules:

1. 🧮 **Backend (Flask)** — Handles CSV file uploads, processes them using a pre-trained ML model, and optionally stores results in MongoDB.  
2. 💻 **Frontend (React.js)** — User interface where CSVs are uploaded, analyzed, and linked to the dashboard.  
3. 📊 **Dashboard (Streamlit)** — Interactive visualization layer that displays performance trends, lifecycle predictions, and allows PDF report downloads.

---

## ⚙️ Key Features

✅ Upload GPU/processor usage data (CSV format)  
✅ Predict processor lifecycle class using **K-Means Clustering**  
✅ Visualize metrics such as average power, memory, and thermal performance  
✅ Generate and download analytical **PDF reports**  
✅ MongoDB integration for result storage
✅ Interactive and modern UI built with React  

---

##  Tech Stack

### **Machine Learning**
- Scikit-learn (K-Means Clustering)
- Joblib (for saving trained models)
- Pandas, NumPy (data preprocessing)

### **Backend**
- Flask (REST API)
- Flask-CORS for API Integration
- MongoDB (via PyMongo)

### **Frontend**
- React.js (Vite)
- Typescript
- Tailwind CSS
- Framer Motion
- Lucide React Icons

### **Dashboard**
- Streamlit
- Plotly / Matplotlib
- ReportLab (for PDF generation)

--

