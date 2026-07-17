"""
AI Detection utility module.
Handles YOLOv8 object detection, counting, and frame annotation.
"""

import time
import threading
from ultralytics import YOLO
from utils.traffic import traffic_state_manager

class VehicleDetector:
    """Singleton YOLO wrapper to load model only once and ensure thread safety."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VehicleDetector, cls).__new__(cls)
            # Load model lazily
            cls._instance.model = None
            # Restrict detections to only relevant COCO classes: car, motorcycle, bus, truck
            cls._instance.target_classes = [2, 3, 5, 7]
            # Since Flask runs streams in background threads, we must lock YOLO inference
            cls._instance.lock = threading.Lock()
        return cls._instance
        
    def detect(self, frame):
        with self.lock:
            if self.model is None:
                from ultralytics import YOLO
                self.model = YOLO('yolov8n.pt')
            # verbose=False prevents console spam for every frame
            results = self.model(frame, classes=self.target_classes, verbose=False)
            return results[0]

class TrafficAnalyzer:
    """Calculates density and updates state based on detections."""
    
    def __init__(self):
        self.detector = VehicleDetector()
        
    def process_frame(self, frame, junction: str, direction: str):
        start_time = time.time()
        
        # 1. YOLO Inference
        result = self.detector.detect(frame)
        
        # 2. Count and Classify Vehicles
        vehicle_count = len(result.boxes)
        cars = motorcycles = bus = truck = 0
        confidences = []
        
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            confidences.append(conf)
            
            if cls_id == 2: cars += 1
            elif cls_id == 3: motorcycles += 1
            elif cls_id == 5: bus += 1
            elif cls_id == 7: truck += 1
            
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
        
        # 3. Calculate Congestion according to rules
        # 0-15 LOW, 16-35 MEDIUM, 36+ HIGH
        if vehicle_count <= 15:
            congestion_level = 'LOW'
        elif vehicle_count <= 35:
            congestion_level = 'MEDIUM'
        else:
            congestion_level = 'HIGH'
            
        density = min((vehicle_count / 35.0) * 100, 100.0)
        
        # 4. Draw Bounding Boxes on Frame
        # Remove confidence labels, displaying only the vehicle class
        annotated_frame = result.plot(conf=False)
        
        fps = 1.0 / (time.time() - start_time + 0.001)
        
        # 5. Update Global TrafficState
        traffic_state_manager.update_camera(junction, direction, {
            'vehicle_count': vehicle_count,
            'cars': cars,
            'motorcycles': motorcycles,
            'bus': bus,
            'truck': truck,
            'density': density,
            'congestion_level': congestion_level,
            'average_confidence': avg_conf,
            'fps': round(fps, 1),
            'ai_status': 'Active'
        })
        
        # 6. Return Annotated Frame
        return annotated_frame

class VisionEngine:
    """Orchestrates detection and analysis."""
    def __init__(self):
        self.analyzer = TrafficAnalyzer()
        
    def process(self, frame, junction: str, direction: str):
        return self.analyzer.process_frame(frame, junction, direction)

# Singleton Vision Engine instance
vision_engine = VisionEngine()
