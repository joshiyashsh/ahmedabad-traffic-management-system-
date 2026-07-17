"""
Video streaming module.
Handles frame ingestion and MJPEG HTTP streaming.
"""

import cv2
import threading
import time

class VideoManager:
    """Manages video capture objects and streams frames."""
    
    def __init__(self):
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Clean mapping for all 8 local videos using absolute paths
        self.video_paths = {
            'iskcon': {
                'north': os.path.join(base_dir, 'videos', 'part1.mp4'),
                'east': os.path.join(base_dir, 'videos', 'part2.mp4'),
                'west': os.path.join(base_dir, 'videos', 'part3.mp4'),
                'south': os.path.join(base_dir, 'videos', 'part4.mp4'),
            },
            'shivranjani': {
                'north': os.path.join(base_dir, 'videos', 'part5.mp4'),
                'east': os.path.join(base_dir, 'videos', 'part6.mp4'),
                'west': os.path.join(base_dir, 'videos', 'part7.mp4'),
                'south': os.path.join(base_dir, 'videos', 'part8.mp4'),
            }
        }
        
        self.captures = {}
        self.lock = threading.Lock()
        
    def _get_capture(self, junction: str, direction: str):
        """Retrieve or initialize the cv2.VideoCapture object."""
        import os
        key = f"{junction}_{direction}"
        
        with self.lock:
            path = self.video_paths.get(junction, {}).get(direction)
            if not path:
                return None
                
            if key not in self.captures or not self.captures[key].isOpened():
                print(f"Opening video:\n{path}")
                
                if not os.path.exists(path):
                    print("Video not found")
                    print(f"Current working directory\n{os.getcwd()}")
                    print(f"Absolute path\n{path}")
                    return None
                    
                cap = cv2.VideoCapture(path)
                
                if not cap.isOpened():
                    print("Video not found")
                    print(f"Current working directory\n{os.getcwd()}")
                    print(f"Absolute path\n{path}")
                    return None
                    
                self.captures[key] = cap
                
            return self.captures[key]

    def get_latest_frame(self, junction: str, direction: str):
        """Grabs a single synchronized snapshot for the decision engine."""
        cap = self._get_capture(junction, direction)
        if cap:
            with self.lock:
                success, frame = cap.read()
                if not success:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    success, frame = cap.read()
                if success:
                    return cv2.resize(frame, (640, 360))
        return None

    def generate_frames(self, junction: str, direction: str):
        """Generator function for MJPEG streaming."""
        cap = self._get_capture(junction, direction)
        
        if not cap:
            # Yield a blank frame if the path doesn't exist in mapping
            yield self._generate_blank_frame("Invalid Camera Feed")
            return
            
        while True:
            # Lock the read operation to ensure thread safety
            with self.lock:
                success, frame = cap.read()
                
                # Loop forever: Restart video automatically when it ends
                if not success:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    success, frame = cap.read()
                    
            if not success or frame is None:
                # Fallback if video file is missing or unreadable
                yield self._generate_blank_frame("NO SIGNAL")
                time.sleep(1)
                continue
                
            # Resize every frame to 640x360 as requested
            try:
                frame = cv2.resize(frame, (640, 360))
            except Exception:
                yield self._generate_blank_frame("RESIZE ERROR")
                time.sleep(1)
                continue
                
            # Note: YOLO is explicitly NOT run here to preserve performance.
            # Inference is handled dynamically by the TrafficDecisionEngine.
            
            # Return JPEG encoded frames
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()
            
            # Yield multipart format for MJPEG
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Small delay to approximate 30 FPS playback locally
            time.sleep(0.033)

    def _generate_blank_frame(self, text: str):
        """Helper to generate a blank black frame with centered text."""
        import numpy as np
        frame = np.zeros((360, 640, 3), dtype=np.uint8)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        color = (255, 255, 255)
        thickness = 2
        
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (640 - text_size[0]) // 2
        text_y = (360 + text_size[1]) // 2
        
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        return (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Singleton instance to manage all feeds across requests
video_manager = VideoManager()
