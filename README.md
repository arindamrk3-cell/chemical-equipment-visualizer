# Chemical Equipment Parameter Visualizer
(Hybrid Web + Desktop Application)

## 📌 Project Overview
The Chemical Equipment Parameter Visualizer is a hybrid analytics application that runs as both a **Web Application** and a **Desktop Application**.  
Users can upload CSV files containing chemical equipment parameters, and the system performs analytics and visualizations using a shared Django backend.

The project demonstrates:
- Data processing with Pandas
- REST API design using Django REST Framework
- Web visualization using React + Chart.js
- Desktop visualization using PyQt5 + Matplotlib
- Multi-client architecture with a single backend

---

## 🧱 Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- Pandas
- SQLite
- ReportLab (PDF generation)

### Frontend (Web)
- React.js (Vite)
- Chart.js
- Fetch API

### Frontend (Desktop)
- PyQt5
- Matplotlib
- Requests

---

## 📂 Project Structure

chemical-equipment-visualizer/
│
├── backend/
│   ├── equipment_backend/
│   ├── analytics/
│   ├── manage.py
│   ├── requirements.txt
│
├── web/
│   ├── src/
│   ├── package.json
│
├── desktop/
│   ├── main.py
│   ├── api_client.py
│   ├── charts.py
│   ├── requirements.txt
│
├── sample_equipment_data.csv
└── README.md

⚙️ Backend Setup
1️⃣ Create & Activate Virtual Environment
cd backend
python -m venv venv
venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Apply Migrations
python manage.py migrate

4️⃣ Create Admin User
python manage.py createsuperuser

5️⃣ Run Backend Server
python manage.py runserver


Backend URL:  http://127.0.0.1:8000/


🔐 Authentication

Implemented using Django REST Framework Basic Authentication
Required for:
/api/history/
/api/report/<id>/
Example
curl -u admin:password http://127.0.0.1:8000/api/history/

🌍 Web Frontend Setup (React)
cd web
npm install
npm run dev


Web App URL:
http://localhost:5173

Web Features
CSV upload
Summary cards (total & averages)
Chart.js bar chart
Dataset history dropdown
Uses backend APIs only

🖥️ Desktop Application Setup (PyQt5)
Activate backend virtual environment first:
cd backend
venv\Scripts\activate
python desktop/main.py

Desktop Features
CSV upload via file picker
Summary analytics display
Matplotlib bar chart
Uses same backend APIs as web app

📄 PDF Report Generation
Generated on backend using ReportLab
Contains:
    Dataset name
    Upload date
    Summary statistics
    Equipment type distribution

Download via:   /api/report/<dataset_id>/