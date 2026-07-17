# 🚦 Ahmedabad Smart Traffic Signal Management System (ASTMS)

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-orange?logo=pytorch)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap)

</p>

---

## 📌 Overview

The **Ahmedabad Smart Traffic Signal Management System (ASTMS)** is an AI-powered intelligent traffic management prototype that dynamically allocates traffic signals using real-time vehicle detection.

Unlike traditional traffic lights that operate on fixed timers, ASTMS analyzes live camera feeds using **YOLOv8**, calculates traffic congestion, prioritizes lanes based on vehicle density, and automatically determines the optimal green signal duration.

The project demonstrates how Artificial Intelligence and Computer Vision can improve urban traffic flow while reducing waiting time, congestion, and fuel consumption.

---

# 🎯 Problem Statement

Traditional traffic signal systems rely on **fixed timing schedules**, regardless of the actual number of vehicles waiting.

This leads to:

- 🚗 Long waiting times
- 🚦 Unnecessary congestion
- ⛽ Increased fuel consumption
- 🌍 Higher carbon emissions
- 🚑 Delayed emergency vehicles

---

# 💡 Solution

ASTMS replaces static timers with an AI-based decision engine.

The system:

- Detects vehicles using YOLOv8
- Counts vehicles in every lane
- Calculates congestion scores
- Prioritizes traffic dynamically
- Allocates optimized green signal durations
- Prevents lane starvation using fairness logic

---

# ✨ Features

- 🔐 Secure Login Authentication
- 🖥 Smart Traffic Control Dashboard
- 📹 Live CCTV Video Streaming
- 🤖 YOLOv8 Vehicle Detection
- 🚗 Automatic Vehicle Counting
- 🚦 Dynamic Traffic Signal Allocation
- 📊 AI Decision Panel
- 📈 Traffic Analytics
- 📝 Decision History Logging
- ⚡ Real-Time Updates
- 🧠 Intelligent Priority-Based Scheduling

---

# 🏗 System Architecture

```
User Login
     │
     ▼
Dashboard
     │
     ▼
Select Junction
     │
     ▼
Camera Streams
     │
     ▼
Frame Capture
     │
     ▼
YOLOv8 Detection
     │
     ▼
Vehicle Counting
     │
     ▼
Priority Score Calculation
     │
     ▼
Traffic Decision Engine
     │
     ▼
Signal Allocation
     │
     ▼
Frontend Update
     │
     ▼
Decision History
```

---

# 🧠 AI Workflow

1. Capture image from live camera.
2. Detect vehicles using YOLOv8.
3. Count:

- Cars
- Motorcycles
- Buses
- Trucks

4. Calculate weighted congestion score.
5. Compare all lanes.
6. Select highest priority lane.
7. Allocate green signal.
8. Repeat continuously.

---

# 🚗 Traffic Decision Logic

Vehicle weights:

| Vehicle | Weight |
|----------|---------|
| Car | 1 |
| Motorcycle | 1 |
| Bus | 4 |
| Truck | 5 |

Additional rules:

✅ Waiting Bonus (+10)

- Prevents starvation.

✅ Recently Served Penalty (-50)

- Prevents giving consecutive green signals.

Green Signal Duration:

- Minimum: **20 sec**
- Maximum: **60 sec**

---

# 📂 Project Structure

```
ASTMS/
│
├── app.py
├── config.py
├── requirements.txt
│
├── models/
├── videos/
├── processed/
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   └── junction.py
│
├── utils/
│   ├── detector.py
│   ├── scheduler.py
│   ├── traffic.py
│   └── video_stream.py
│
├── static/
│
├── templates/
│
└── README.md
```

---

# ⚙️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Flask | Web Framework |
| OpenCV | Image Processing |
| YOLOv8 | Vehicle Detection |
| PyTorch | Deep Learning |
| Bootstrap 5 | UI |
| HTML/CSS | Frontend |
| JavaScript | Dynamic Dashboard |

---

# 📡 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Login Page |
| `/dashboard` | GET | Dashboard |
| `/logout` | GET | Logout |
| `/junction/<junction>` | GET | Junction View |
| `/stream/<junction>/<direction>` | GET | Live Camera Feed |
| `/api/traffic_state/<junction>` | GET | Live Traffic Data |

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/ASTMS.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

> Replace these placeholders with your screenshots.

```
📷 Login Page

📷 Dashboard

📷 Live Camera Feed

📷 AI Detection

📷 Signal Controller

📷 Analytics
```

---

# 🎥 Demo

You can also upload a demo GIF.

```
assets/demo.gif
```

---

# 📈 Future Enhancements

- 🌐 Real CCTV Integration
- 📡 RTSP Camera Support
- 🗺 Live City Map
- 📊 Analytics Dashboard
- 🗄 PostgreSQL Database
- 🔔 Emergency Vehicle Detection
- 📱 Mobile Application
- ☁ Cloud Deployment
- 🔄 WebSocket Communication

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 👨‍💻 Developer

**Yash Joshi**

B.Tech Computer Engineering (AI & ML)

Silver Oak University

Ahmedabad, Gujarat

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

# ⭐ Support

If you like this project,

⭐ Star the repository

🍴 Fork it

💬 Share your feedback

---

## 📜 License

This project is developed for educational and research purposes.