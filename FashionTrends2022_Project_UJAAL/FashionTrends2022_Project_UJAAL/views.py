"""
Routes and views for the flask application.
"""
from datetime import datetime        
from flask import Flask,session,render_template,request,redirect,url_for,flash
import pyodbc  
from FashionTrends2022_Project_UJAAL import app

app.secret_key='asdsdfsdfs13sdf_df%&'
# creating connection Object which will contain SQL Server Connection    
connection = pyodbc.connect('Driver={SQL Server};Server=.;Database=Fashion_Trends_2022;uid=sa;pwd=Test@1234')# Creating Cursor    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']  
        res = connection.execute("SELECT * FROM User_login WHERE Email ='"+username+"'"+"AND Password ='"+ password+"'").fetchone()
        if res is None:
            flash("no email found","danger")
            return render_template('login.html')
        else:
            return redirect(url_for('home'))
        connection.close() 
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    login=False
    if 'username' in session:
        login=True
    return render_template('login_home.html',login=login)

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
