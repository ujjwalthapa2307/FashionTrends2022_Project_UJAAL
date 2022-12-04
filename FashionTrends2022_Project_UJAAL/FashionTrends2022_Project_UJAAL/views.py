"""
Routes and views for the flask application.
"""
from ast import IsNot
from asyncio.windows_events import NULL
from datetime import datetime
import sys        
from flask import Flask,session,render_template,request,redirect,url_for,flash,jsonify
import pyodbc  
from FashionTrends2022_Project_UJAAL import app

app.secret_key='asdsdfsdfs13sdf_df%&'
# creating connection Object which will contain SQL Server Connection    
#connection = pyodbc.connect('Driver={SQL Server};Server=.;Database=Fashion_Trends_2022;uid=sa;pwd=Test@1234')# Creating Cursor    
DRIVER = 'SQL Server'
SERVER_NAME = 'LOVELEEN\LKSQL'
DATABASE_NAME = 'Fashion_Trends_2022'

conn_string = f"""
    Driver={{{DRIVER}}};
    Server={SERVER_NAME};
    Database={DATABASE_NAME};
    Trust_Connection=yes;
"""

try:
    connection = pyodbc.connect(conn_string)
except Exception as e:
    print(e)
    print('task is terminated')
    sys.exit()
else:
    cursor = connection.cursor()

# Registeration
@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        #secure_password=sha256_crypt.encrypt(str(password))

        if password == "":
            get_flashed_message("password did not match","danger")
            return redirect(url_for('register'))

        else:
            connection.execute("INSERT INTO User_login(Email,Password,name) VALUES('"+email+"','"+password+"','"+name+"')")
            connection.commit()
            #get_flashed_message("registration succesfull","success")
            return redirect(url_for('login'))
    
    else:
        return render_template('register.html')

# Login
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
            return render_template('present.html')

        connection.close() 
    return render_template('login.html')

# Map Population
@app.route('/_populate_map')
def populate_map():
    territorydata = connection.execute("SELECT TOP 1 WITH TIES T.Name AS Territory, B.Brand_Name, MAX(S.SALES) AS Sales FROM TERRITORY_SALES AS TS INNER JOIN TERRITORY AS T ON TS.TERRITORY_ID=T.TERRITORY_ID INNER JOIN SALES AS S ON TS.SALES_ID=S.SALES_ID INNER JOIN SKU AS SK ON S.SKU_ID=SK.SKU_ID INNER JOIN BRAND AS B ON SK.BRAND_ID=B.BRAND_ID GROUP BY T.Name, B.Brand_Name ORDER BY ROW_NUMBER() OVER(PARTITION BY T.Name ORDER BY MAX(S.Sales) DESC);").fetchall()
    return jsonify(territorydata)

# Logout
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

# Default Page
@app.route('/')
def index():
    login=False
    if 'username' in session:
        login=True
    return render_template('login_home.html',login=login)

# Home Page
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
