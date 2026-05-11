"""
RetiNexAI - Flask Application Entry Point

This is the main Flask application for the RetiNexAI system.
Routes and business logic are organized in the backend module.
"""

from flask import Flask
from backend import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
