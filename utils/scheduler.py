"""
Scheduler utility module.
Implements the Traffic Decision Engine for dynamic signal timing.
"""

import time
import threading
import datetime
from utils.video_stream import video_manager
from utils.detector import vision_engine
from utils.traffic import traffic_state_manager

class TrafficDecisionEngine:
    def __init__(self):
        self.lock = threading.Lock()
        self.junctions = {}
        
    def start_junction(self, junction: str):
        with self.lock:
            if junction not in self.junctions:
                self.junctions[junction] = {
                    'thread': threading.Thread(target=self._run_cycle, args=(junction,), daemon=True),
                    'active': True,
                    'current_green': 'north',
                    'time_left': 5, # Start with a short timer to trigger the first snapshot quickly
                    'wait_times': {'north': 0, 'east': 0, 'west': 0, 'south': 0},
                    'logs': [],
                    'history': [],
                    'snapshot_metrics': {'cars': 0, 'motorcycles': 0, 'bus': 0, 'truck': 0, 'autos': 0, 'total': 0},
                    'priority_ranking': [],
                    'ai_recommendation': {},
                    'cycle_count': 1,
                    'total_processed': 0,
                    'total_green': 0
                }
                self._log(junction, "Traffic Decision Engine initialized.")
                self.junctions[junction]['thread'].start()
                
    def _log(self, junction: str, msg: str):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.junctions[junction]['logs'].append(f"{now} - {msg}")
        if len(self.junctions[junction]['logs']) > 30:
            self.junctions[junction]['logs'].pop(0)

    def _run_cycle(self, junction: str):
        state = self.junctions[junction]
        directions = ['north', 'east', 'west', 'south']
        
        while state['active']:
            if state['time_left'] > 0:
                time.sleep(1)
                state['time_left'] -= 1
                continue
                
            # Timer reached zero
            self._log(junction, "Traffic Snapshot Captured")
            
            # 1. Capture snapshot and run YOLO once per cycle
            scores = {}
            total_cars = total_moto = total_bus = total_truck = 0
            
            for d in directions:
                frame = video_manager.get_latest_frame(junction, d)
                if frame is not None:
                    # Run YOLO and update TrafficState synchronously
                    vision_engine.process(frame, junction, d)
                
                # Retrieve updated state
                cam_state = traffic_state_manager.get_junction_state(junction)[d]
                
                c = cam_state['cars']
                m = cam_state['motorcycles']
                b = cam_state['bus']
                t = cam_state['truck']
                a = 0 # Autos are implicitly wrapped into cars in standard YOLO COCO classes
                
                total_cars += c
                total_moto += m
                total_bus += b
                total_truck += t
                
                # Calculate Priority Score based on requested weights
                wait_bonus = state['wait_times'][d] * 10
                recent_penalty = 50 if state['current_green'] == d else 0
                    
                score = c + m + a + (b * 4) + (t * 5) + wait_bonus - recent_penalty
                scores[d] = score

            # Update fresh snapshot metrics (Do not accumulate forever)
            total_snap = total_cars + total_moto + total_bus + total_truck
            state['snapshot_metrics'] = {
                'cars': total_cars, 'motorcycles': total_moto, 'bus': total_bus, 'truck': total_truck, 'autos': 0,
                'total': total_snap
            }
            
            self._log(junction, "Priority Calculated")
            
            # 2. Choose next road
            # Prevent consecutive greens unless all other roads have 0 priority
            candidates = {k: v for k, v in scores.items() if k != state['current_green']}
            if all(v <= 0 for v in candidates.values()):
                next_green = max(scores, key=scores.get)
            else:
                next_green = max(candidates, key=candidates.get)
            
            
            # Create priority ranking
            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            state['priority_ranking'] = [{'direction': k.upper(), 'score': v} for k, v in ranked]
            
            # 3. Calculate dynamic green time
            next_count = traffic_state_manager.get_junction_state(junction)[next_green]['vehicle_count']
            green_time = min(max(30 + next_count, 20), 60)
            
            self._log(junction, f"Green Allocated ({next_green.upper()})")
            self._log(junction, f"Countdown Started ({green_time} sec)")
            
            # 4. Update state variables and historical arrays
            for d in directions:
                if d == next_green:
                    state['wait_times'][d] = 0
                else:
                    state['wait_times'][d] += 1
                    
            state['ai_recommendation'] = {
                'priority_lane': next_green.upper(),
                'traffic_volume': next_count,
                'congestion': traffic_state_manager.get_junction_state(junction)[next_green]['congestion_level'],
                'priority_score': scores[next_green],
                'adaptive_green': green_time,
                'reason': f"Highest priority score ({scores[next_green]}) after weighted vehicle analysis."
            }
            
            now = datetime.datetime.now().strftime("%H:%M:%S")
            state['history'].insert(0, {
                'time': now,
                'road': next_green.upper(),
                'score': scores[next_green],
                'duration': green_time,
                'reason': state['ai_recommendation']['reason']
            })
            if len(state['history']) > 5:
                state['history'].pop()
                
            # Apply decisions and loop
            state['current_green'] = next_green
            state['time_left'] = green_time
            state['cycle_count'] += 1
            state['total_processed'] += total_snap
            state['total_green'] += green_time
            
    def get_decision_state(self, junction: str):
        if junction not in self.junctions:
            self.start_junction(junction)
        
        state = self.junctions[junction]
        avg_green = state['total_green'] // max(1, state['cycle_count'] - 1)
        avg_wait = avg_green * 2  # Simple heuristic for avg wait time 
        
        return {
            'current_green': state['current_green'],
            'time_left': state['time_left'],
            'logs': state['logs'],
            'history': state['history'],
            'snapshot_metrics': state['snapshot_metrics'],
            'priority_ranking': state['priority_ranking'],
            'ai_recommendation': state['ai_recommendation'],
            'stats': {
                'cycle': state['cycle_count'],
                'processed': state['total_processed'],
                'avg_green': avg_green,
                'avg_wait': avg_wait
            }
        }

# Singleton Controller Instance
decision_engine = TrafficDecisionEngine()
