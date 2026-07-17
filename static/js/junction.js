// static/js/junction.js
document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-scroll terminal log to bottom on load
    const eventLog = document.getElementById('event-log');
    if (eventLog) {
        eventLog.scrollTop = eventLog.scrollHeight;
    }

    // 2. Poll API for Live AI Traffic Statistics & Decision State
    const pathParts = window.location.pathname.split('/');
    const junctionName = pathParts[pathParts.length - 1];
    
    if (junctionName && junctionName !== 'junction') {
        setInterval(() => {
            fetch(`/api/traffic_state/${junctionName}`)
                .then(res => res.json())
                .then(data => {
                    if (data.error) return;
                    
                    const traffic = data.traffic;
                    const decision = data.decision;
                    const directions = ['north', 'east', 'west', 'south'];
                    
                    // --- UPDATE CAMERAS & CONTROLLER ---
                    directions.forEach(dir => {
                        const state = traffic[dir];
                        if (state) {
                            // Update Volume
                            const volEl = document.getElementById(`vol-${dir}`);
                            if (volEl) volEl.innerText = state.vehicle_count;
                            
                            // Update Congestion
                            const congEl = document.getElementById(`cong-${dir}`);
                            if (congEl) {
                                congEl.innerText = state.congestion_level;
                                congEl.className = 'cam-stat-val text-end ' + 
                                    (state.congestion_level === 'LOW' ? 'text-success' : 
                                    (state.congestion_level === 'MEDIUM' ? 'text-warning' : 'text-danger'));
                            }
                            
                            // Update HUD
                            const aiEl = document.getElementById(`ai-status-${dir}`);
                            if (aiEl) aiEl.innerHTML = `<i class="fa-solid fa-microchip text-primary"></i> ${state.ai_status}`;
                            
                            const fpsEl = document.getElementById(`fps-${dir}`);
                            if (fpsEl) fpsEl.innerText = `FPS: ${state.fps}`;
                            
                            const confEl = document.getElementById(`conf-${dir}`);
                            if (confEl) confEl.innerText = `Conf: ${(state.average_confidence * 100).toFixed(0)}%`;
                        }
                        
                        // Signal Controller & Queue Logic
                        const timerEl = document.getElementById(`timer-${dir}`);
                        const lightEl = document.getElementById(`light-${dir}`);
                        const boxEl = document.getElementById(`box-${dir}`);
                        
                        if (decision.current_green === dir) {
                            if (decision.time_left <= 2 && decision.time_left > 0) {
                                // Yellow Transition Phase
                                if (lightEl) {
                                    lightEl.className = 'signal-light';
                                    lightEl.style.background = '#F59E0B';
                                    lightEl.style.boxShadow = '0 0 20px rgba(245, 158, 11, 0.8)';
                                }
                                if (timerEl) {
                                    timerEl.className = 'signal-timer text-warning';
                                    timerEl.innerText = decision.time_left.toString().padStart(2, '0');
                                }
                            } else {
                                // Green Phase
                                if (lightEl) {
                                    lightEl.className = 'signal-light green';
                                    lightEl.style.background = '';
                                    lightEl.style.boxShadow = '';
                                }
                                if (timerEl) {
                                    timerEl.className = 'signal-timer text-success';
                                    timerEl.innerText = decision.time_left.toString().padStart(2, '0');
                                }
                            }
                            if (boxEl) boxEl.classList.add('active');
                            
                        } else {
                            // Red Phase
                            if (lightEl) {
                                lightEl.className = 'signal-light red';
                                lightEl.style.background = '';
                                lightEl.style.boxShadow = '';
                            }
                            if (timerEl) {
                                timerEl.className = 'signal-timer text-muted';
                                timerEl.innerText = '--';
                            }
                            if (boxEl) boxEl.classList.remove('active');
                        }
                    });
                    
                    // --- UPDATE AI RECOMMENDATION ---
                    if (decision.ai_recommendation && decision.ai_recommendation.priority_lane) {
                        const ai = decision.ai_recommendation;
                        document.getElementById('ai-rec-lane').innerText = ai.priority_lane;
                        document.getElementById('ai-rec-vol').innerText = `${ai.traffic_volume} v/cycle`;
                        document.getElementById('ai-rec-cong').innerText = ai.congestion;
                        document.getElementById('ai-rec-score').innerText = ai.priority_score;
                        document.getElementById('ai-rec-green').innerText = `${ai.adaptive_green} sec`;
                        document.getElementById('ai-rec-reason').innerText = ai.reason;
                    }
                    
                    // --- UPDATE TERMINAL LOGS ---
                    const logContainer = document.getElementById('event-log');
                    if (logContainer && decision.logs.length > 0) {
                        let logHtml = '';
                        decision.logs.forEach(log => {
                            const parts = log.split(' - ');
                            const time = parts[0] || '';
                            const msg = parts[1] || '';
                            
                            let levelClass = 'text-info';
                            let levelText = '[INFO]';
                            if (msg.includes("Snapshot Captured")) {
                                levelClass = 'text-primary';
                                levelText = '[CAMERA]';
                            } else if (msg.includes("Priority Calculated")) {
                                levelClass = 'text-warning';
                                levelText = '[CALC]';
                            } else if (msg.includes("Allocated")) {
                                levelClass = 'text-success';
                                levelText = '[DECISION]';
                            } else if (msg.includes("Countdown")) {
                                levelClass = 'text-danger';
                                levelText = '[TIMER]';
                            }
                            
                            logHtml += `<div class="log-line"><span class="log-time">${time}</span><span class="log-level ${levelClass}">${levelText}</span><span class="log-msg text-white">${msg}</span></div>`;
                        });
                        logContainer.innerHTML = logHtml;
                        logContainer.scrollTop = logContainer.scrollHeight; // Auto-scroll
                    }
                    
                    // --- UPDATE HISTORY TABLE ---
                    const historyBody = document.getElementById('decision-history-body');
                    if (historyBody && decision.history.length > 0) {
                        let histHtml = '';
                        decision.history.forEach(h => {
                            histHtml += `
                            <tr>
                                <td><span class="text-secondary">${h.time}</span></td>
                                <td><span class="badge bg-success bg-opacity-25 text-success border border-success">${h.road}</span></td>
                                <td class="font-monospace text-primary">${h.score}</td>
                                <td><small class="text-muted">${h.reason}</small></td>
                            </tr>
                            `;
                        });
                        historyBody.innerHTML = histHtml;
                    }

                })
                .catch(err => console.error("Error polling decision state", err));
        }, 1000);
    }
});
