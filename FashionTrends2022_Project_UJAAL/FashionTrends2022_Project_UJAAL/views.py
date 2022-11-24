"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FashionTrends2022_Project_UJAAL import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/present')
def present():
    """Renders the home page."""
    return render_template(
        'present.html',
        title='Present Page',
        year=datetime.now().year,
    )

@app.route('/past')
def past():
    """Renders the home page."""
    return render_template(
        'past.html',
        title='Past Page',
        year=datetime.now().year,
    )

@app.route('/future')
def future():
    """Renders the home page."""
    return render_template(
        'future.html',
        title='Future Page',
        year=datetime.now().year,
    )
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
