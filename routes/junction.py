"""
Junction routing module.
Handles the junction detail view and MJPEG video streaming endpoints.
"""

from flask import render_template, redirect, url_for, session, Response, jsonify
from utils.video_stream import video_manager
from utils.traffic import traffic_state_manager
from utils.scheduler import decision_engine

def register_junction_routes(app):
    """Registers junction and streaming routes on the given Flask app instance."""
    
    @app.route('/junction/<junction_name>')
    def junction(junction_name: str):
        """Render the junction detail dashboard."""
        if not session.get('logged_in'):
            return redirect(url_for('login'))
            
        return render_template('junction.html', junction_name=junction_name)

    @app.route('/stream/<junction>/<direction>')
    def stream(junction: str, direction: str):
        """
        MJPEG streaming endpoint for specific camera feeds.
        Continuously yields frames from the VideoManager.
        """
        if not session.get('logged_in'):
            return Response("Unauthorized", status=401)
            
        return Response(
            video_manager.generate_frames(junction, direction),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )

    @app.route('/api/traffic_state/<junction>')
    def api_traffic_state(junction: str):
        """Provides a JSON feed of the real-time AI traffic statistics and decisions."""
        if not session.get('logged_in'):
            return jsonify({"error": "Unauthorized"}), 401
            
        return jsonify({
            'traffic': traffic_state_manager.get_junction_state(junction),
            'decision': decision_engine.get_decision_state(junction)
        })
