"""
Dashboard routing module.
Handles the main global dashboard view.
"""

from flask import render_template, redirect, url_for, session

def register_dashboard_routes(app):
    """Registers dashboard routes on the given Flask app instance."""
    
    @app.route('/dashboard')
    def dashboard():
        """Render the global dashboard page."""
        # Ensure user is authenticated
        if not session.get('logged_in'):
            return redirect(url_for('login'))
            
        return render_template('dashboard.html')
