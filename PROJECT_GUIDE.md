# Ahmedabad Smart Traffic Signal Management System

The Ahmedabad Smart Traffic Signal Management System (ASTMS) is an intelligent traffic operations center prototype designed to revolutionize urban mobility. 

**Problem Statement:** Traditional traffic signal systems rely on hard-coded static timers. This inflexible approach inherently leads to unnecessary congestion, extended wait times, and increased vehicle emissions when traffic density varies unpredictably.

**Project Objective:** Develop a dynamic, AI-driven traffic signal allocation system capable of understanding real-time intersection congestion and making autonomous decisions to optimize traffic flow.

**Real-world Motivation:** Rapidly growing metropolitan cities like Ahmedabad require scalable smart-city infrastructure. By maximizing intersection throughput using visual intelligence, authorities can significantly improve urban mobility without the immediate need for expensive physical road expansion.

---

## Project Overview

The ASTMS is a comprehensive prototype built specifically for traffic officers and urban planners. It provides a centralized command center interface to monitor active junctions. Instead of relying on blind timers, the system dynamically allocates green signals by processing live camera feeds using an AI-assisted vehicle detection pipeline. The engine evaluates traffic volume across all approaches of an intersection simultaneously, ranks them by priority, and allocates proportional green light durations to alleviate congestion organically.

---

## Complete System Flow

The execution of the application follows a robust, cyclical flow:

**Login** (Authentication into the Command Center)
↓
**Dashboard** (Overview of all city junctions)
↓
**Select Junction** (Officer drills down into a specific intersection)
↓
**Open Camera Streams** (Browser connects to MJPEG video feeds)
↓
**Traffic Snapshot** (Backend periodically captures a single frame from all cameras)
↓
**YOLO Vehicle Detection** (AI locates bounding boxes for all vehicles)
↓
**Vehicle Counting** (System tallies Cars, Motorcycles, Buses, and Trucks)
↓
**Priority Score Calculation** (Weighted math is applied to the vehicle counts)
↓
**Traffic Decision Engine** (Compares priorities and enforces fairness logic)
↓
**Signal Allocation** (Engine selects the winning lane and determines green duration)
↓
**UI Update** (Frontend fetches the new state and updates the Signal Controller)
↓
**Decision History** (The rationale is logged in the analytics table)
↓
**Repeat** (Countdown completes, next cycle begins)

---

## Folder Structure

*   **`app.py`**: The application entry point. It initializes the Flask server and registers all routes.
*   **`config.py`**: Contains global configuration variables (application name, secret keys, dummy credentials).
*   **`routes/`**: Contains the modular routing files that handle HTTP requests and view rendering.
*   **`templates/`**: Holds all Jinja2 HTML templates (`login.html`, `dashboard.html`, etc.) for the frontend.
*   **`static/`**: Stores static assets including custom CSS stylesheets, vanilla JavaScript files, and images.
*   **`utils/`**: The core backend logic directory containing modules for video streaming, AI detection, and scheduling.
*   **`videos/`**: Local storage directory containing pre-recorded `.mp4` video files representing live CCTV camera feeds.
*   **`models/`**: Stores the downloaded YOLOv8 weights (e.g., `yolov8n.pt`) to prevent continuous re-downloading.
*   **`processed/`**: An optional directory for saving annotated frames or analytical output if configured.

---

## File-by-File Explanation

### `app.py`
*   **Purpose**: The central bootstrap file for the Flask application.
*   **Responsibilities**: Configures the Flask instance, applies application secrets, and calls modular route registration functions.
*   **How it interacts**: Imports registration functions from the `routes` directory to bind URLs to backend Python logic.

### `config.py`
*   **Purpose**: Centralized configuration management.
*   **Responsibilities**: Defines `SECRET_KEY`, `APPLICATION_NAME`, and hardcoded `VALID_CREDENTIALS` for the prototype.

### `routes/auth.py`
*   **Purpose**: Handles user authentication.
*   **Responsibilities**: Processes login forms, verifies credentials against `config.py`, manages Flask sessions, and handles logouts.

### `routes/dashboard.py`
*   **Purpose**: Manages the main operations center view.
*   **Responsibilities**: Ensures the user is authenticated and renders the `dashboard.html` template.

### `routes/junction.py`
*   **Purpose**: Manages the individual junction monitoring interface and its data feeds.
*   **Responsibilities**: Renders the junction UI, provides the MJPEG streaming endpoints, and exposes the JSON API for live traffic state.

### `utils/video_stream.py`
*   **Purpose**: Simulates live hardware cameras using local video files.
*   **Responsibilities**: Maps junction directions to specific `.mp4` files, manages `cv2.VideoCapture` objects, loops videos endlessly, and yields JPEG frames.

### `utils/detector.py`
*   **Purpose**: The AI Vision Engine.
*   **Responsibilities**: Loads the YOLOv8n model as a singleton, runs inference on image frames, filters for specific vehicle classes, and updates the shared memory state with vehicle counts.

### `utils/traffic.py`
*   **Purpose**: Thread-safe memory storage for traffic data.
*   **Responsibilities**: Maintains a globally accessible dictionary of vehicle counts, congestion levels, and AI statuses across all junctions and directions.

### `utils/scheduler.py`
*   **Purpose**: The Traffic Decision Engine (The "Brain").
*   **Responsibilities**: Runs an asynchronous background loop that orchestrates snapshots, calculates priority math, allocates green timers, logs decision history, and prevents lane starvation.

---

## Function Responsibilities

### `VideoManager.get_latest_frame(junction, direction)`
*   **Purpose**: Retrieves a single, current snapshot for the AI to process.
*   **Input**: Junction ID and Direction (e.g., "iskcon", "north").
*   **Output**: A numpy array representing the image frame.
*   **When it is called**: Triggered by the Scheduler precisely when a countdown timer reaches zero.
*   **Dependencies**: Relies on OpenCV to successfully read the video file.

### `VisionEngine.process(frame, junction, direction)`
*   **Purpose**: Detects vehicles and updates analytics.
*   **Input**: An image frame, junction name, and direction.
*   **Output**: None directly (mutates global state).
*   **When it is called**: Triggered by the Scheduler immediately after capturing a snapshot.
*   **Dependencies**: Requires the YOLO model to be loaded; `TrafficStateManager` relies on this to have accurate data.

### `TrafficDecisionEngine._run_cycle(junction)`
*   **Purpose**: The continuous, autonomous loop managing the traffic lights.
*   **Input**: Junction ID.
*   **Output**: None (mutates global state and updates the active signal).
*   **When it is called**: Triggered as a daemon thread the first time a user requests data for a junction.
*   **Dependencies**: Relies on `VideoManager` for frames and `VisionEngine` for inference.

---

## Traffic Decision Engine

The Decision Engine replaces static timers with dynamic, mathematics-based logic. 

*   **Priority Score**: Vehicles are weighted by size and impact. (e.g., Trucks=5 points, Buses=4 points, Cars=1 point, Motorcycles=1 point). The total sum creates a base score.
*   **Waiting Bonus**: To prevent starvation, lanes receive a +10 point bonus for every consecutive cycle they are forced to wait on red.
*   **Recently Served Penalty**: The lane that just had a green light receives a massive -50 point penalty to heavily discourage the system from giving the same lane back-to-back green lights.
*   **Green Time Allocation**: Once a lane wins the priority ranking, its green duration is calculated dynamically based on its vehicle count (minimum 20 seconds, maximum 60 seconds).
*   **Signal Rotation**: The system naturally cycles through lanes organically based on which lane mathematically demands the most immediate attention.

---

## Video Processing Pipeline

1.  **Video Loading**: `cv2.VideoCapture` connects to a local `.mp4` file via an absolute system path.
2.  **Frame Capture**: A separate generator loop continuously reads and yields frames to the browser for visual monitoring.
3.  **Snapshot**: The backend `Scheduler` asks the `VideoManager` for exactly one frame exactly when a cycle ends.
4.  **YOLO**: The `VisionEngine` receives this single frame and performs a forward pass through the neural network.
5.  **Vehicle Counting**: Bounding boxes are filtered; the system counts occurrences of classes 2 (Car), 3 (Motorcycle), 5 (Bus), and 7 (Truck).
6.  **Traffic State**: The tallies are saved into `TrafficStateManager` memory.
7.  **Signal Decision**: The `Scheduler` retrieves these tallies to calculate the next signal phase.

---

## Frontend Flow

*   **Login Page**: A standalone, full-screen glassmorphism interface. It submits credentials via POST to the backend.
*   **Dashboard**: The operations center. It provides entry points to specific junctions. Uses `base_dashboard.html` for layout.
*   **Junction View**: The primary command interface.
*   **Live Camera Feeds**: Standard `<img>` tags whose source attributes point to the MJPEG streaming API endpoints.
*   **AI Decision Panel**: Dynamically updated via JavaScript polling to show the winning lane, score, and explanation.
*   **Signal Controller**: Visual representation of red/green lights and countdowns. JavaScript applies CSS classes based on API state.
*   **Decision History / Terminal Log**: Displays historical logs of the system's autonomous choices.

JavaScript heavily relies on `fetch()` to hit the `/api/traffic_state/<junction>` endpoint every 1000ms. It dynamically manipulates DOM element text, colors, and widths without reloading the page.

---

## API Endpoints

| Endpoint | Method | Purpose |
| :--- | :--- | :--- |
| `/` | GET | Redirects users to the login page or dashboard. |
| `/dashboard` | GET | Renders the main command center interface. |
| `/logout` | GET | Clears session data and redirects to login. |
| `/junction/<junction>` | GET | Renders the HTML interface for a specific intersection. |
| `/stream/<junction>/<direction>` | GET | Yields continuous MJPEG frames for a single camera feed. |
| `/api/traffic_state/<junction>` | GET | Returns a comprehensive JSON payload containing YOLO metrics, timer state, historical logs, and priority rankings. |

---

## Technologies Used

*   **Flask (Python)**: Chosen for its lightweight, modular nature. Perfect for quickly scaffolding robust API endpoints and managing MJPEG streaming.
*   **OpenCV (`cv2`)**: Industry standard for computer vision; used for efficient frame extraction and image resizing.
*   **YOLOv8 (Ultralytics)**: Chosen for its state-of-the-art speed-to-accuracy ratio. Essential for real-time inference without high-end GPU requirements.
*   **PyTorch**: The deep learning backend powering the YOLO model.
*   **Bootstrap 5**: Provides a rapid, responsive CSS grid framework, allowing the dashboard to scale gracefully across monitors and tablets.
*   **JavaScript / HTML / CSS**: Vanilla web technologies were utilized to avoid the overhead of heavy SPA frameworks (like React/Vue), keeping the prototype extremely lean and fast.

---

## How to Run

1.  **Clone Project**: Download the repository to your local machine.
2.  **Virtual Environment**: 
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
3.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Server**:
    ```bash
    python app.py
    ```
5.  **Access Application**: Open a web browser and navigate to `http://127.0.0.1:5000`.
6.  **Login**: Use the dummy credentials provided in the `config.py` file.

---

## Common Problems

*   **Video showing "NO SIGNAL" / Blank**: Verify that the `.mp4` files exist exactly as named in the `utils/video_stream.py` mapping logic. The system uses absolute pathing, so ensure the `videos/` directory sits in the project root.
*   **Slow initial startup**: The application must download the `yolov8n.pt` weights file on its very first inference pass. Subsequent runs will use the cached local model.
*   **Missing Requirements Error**: Ensure you have activated your virtual environment before running `pip install`.
*   **Port 5000 already in use**: Another Flask/Node app is running. Kill the process or run Flask on a different port via `app.run(port=5001)`.

---

## Future Improvements

*   **Persistent Database**: Transition from in-memory state tracking to a PostgreSQL or SQLite database for long-term historical analytics.
*   **Real CCTV Hardware**: Replace local `.mp4` video reading with RTSP network streams from physical IP cameras.
*   **City Map Integration**: Add a live, interactive map to the Dashboard showing congestion heatmaps across the city.
*   **Multi-Officer Sessions**: Implement role-based access control and WebSockets to synchronize dashboard state across multiple logged-in officer screens instantly.
*   **Advanced Analytics Dashboard**: Implement the currently deactivated "Analytics" sidebar route with Chart.js line graphs comparing weekly traffic density.

---

## Important Notes

*   **This is a Prototype**: The system is designed to simulate hardware interactions via software.
*   **Pre-recorded Videos**: The cameras do not currently connect to physical hardware. They loop high-quality local recordings.
*   **Discrete AI Execution**: To drastically save CPU/GPU overhead, YOLO does *not* run on every single video frame. It purposefully runs *only once* at the exact moment a traffic signal countdown hits zero. This guarantees maximum efficiency.
*   **Weighted Priorities**: The system does not merely look at raw vehicle count. It gives emergency/heavy vehicles (Buses, Trucks) higher mathematical importance to quickly clear large blockages.

---

## Conclusion

The Ahmedabad Smart Traffic Signal Management System bridges the gap between static infrastructure and dynamic artificial intelligence. By cleanly separating the heavy AI inference loop from the fast UI rendering cycle, the architecture remains highly responsive and extensible. This documentation equips any incoming developer with the structural understanding necessary to confidently maintain, refactor, and expand upon this intelligence platform.
