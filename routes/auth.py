"""
Authentication routing module.
Handles login and logout functionality using mock credentials.
"""

from flask import render_template, request, redirect, url_for, session

def register_auth_routes(app):
    """Registers authentication routes on the given Flask app instance."""
    
    @app.route('/', methods=['GET', 'POST'])
    def login():
        """Handle user login."""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Verify against hardcoded credentials in config
            if username == app.config['DUMMY_USERNAME'] and password == app.config['DUMMY_PASSWORD']:
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))
                
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        """Handle user logout."""
        session.clear()
        return redirect(url_for('login'))
