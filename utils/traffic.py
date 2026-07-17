"""
Traffic utility module.
Helper functions and state management for traffic data.
"""

import time
import threading

class TrafficState:
    """Manages the real-time state of all traffic cameras globally."""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.state = {}
        
    def _init_camera(self, junction: str, direction: str):
        key = f"{junction}_{direction}"
        if key not in self.state:
            self.state[key] = {
                'vehicle_count': 0,
                'cars': 0,
                'motorcycles': 0,
                'bus': 0,
                'truck': 0,
                'density': 0.0,
                'congestion_level': 'LOW',
                'average_confidence': 0.0,
                'fps': 0.0,
                'last_updated': time.time(),
                'ai_status': 'Init...'
            }
        return key
            
    def update_camera(self, junction: str, direction: str, data: dict):
        """Thread-safe update of camera metrics."""
        with self.lock:
            key = self._init_camera(junction, direction)
            self.state[key].update(data)
            self.state[key]['last_updated'] = time.time()
            
    def get_junction_state(self, junction: str):
        """Returns the full 4-direction state for a specific junction."""
        with self.lock:
            return {
                dir_name: self.state.get(f"{junction}_{dir_name}", self._default_state())
                for dir_name in ['north', 'east', 'west', 'south']
            }
            
    def _default_state(self):
        return {
            'vehicle_count': 0,
            'cars': 0,
            'motorcycles': 0,
            'bus': 0,
            'truck': 0,
            'density': 0.0,
            'congestion_level': 'Detecting...',
            'average_confidence': 0.0,
            'fps': 0.0,
            'last_updated': 0,
            'ai_status': 'Offline'
        }

# Singleton instance
traffic_state_manager = TrafficState()
