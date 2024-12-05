from app import create_app

"""
This file is the entry point for running the Flask application.
It creates an app instance using the factory method from app.py and starts the server
"""

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
