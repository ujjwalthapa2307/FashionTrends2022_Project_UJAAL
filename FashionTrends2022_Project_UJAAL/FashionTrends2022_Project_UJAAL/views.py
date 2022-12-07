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
from .Review_scrape import *
import glob
import random
import json

app.secret_key='asdsdfsdfs13sdf_df%&'
# creating connection Object which will contain SQL Server Connection    
# connection = pyodbc.connect('Driver={SQL Server};Server=.;Database=Fashion_Trends_2022;uid=sa;pwd=Test@1234')
# Creating Cursor    
DRIVER = 'SQL Server'
SERVER_NAME = 'localhost'
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

# Registration
@app.route('/register', methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        password=request.form.get("password")
        #secure_password=sha256_crypt.encrypt(str(password))
        try:
            if password == "":
                get_flashed_message("password did not match","danger")
                return redirect(url_for('register'))
            else:
                try:
                    connection.execute("INSERT INTO User_login(Email,Password,name) VALUES('"+email+"','"+password+"','"+name+"')")
                    connection.commit()                    
                    return redirect(url_for('login'))
                except:
                    return redirect(url_for('register'))
        except:
            return redirect(url_for('register'))

    return render_template('register.html')

        

# Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']  
        
        res = connection.execute("SELECT * FROM User_login WHERE Email ='"+username+"'"+"AND Password ='"+ password+"'").fetchone()
        session['username'] = request.form['username']
        if res is None:
            flash("no email found","danger")
            return render_template('login.html')
        else:
            return render_template('present.html')

        connection.close() 

    return render_template('login.html')

# Map Fashion Trends by Brands and Sales
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
    initialize()

    country_sales = connection.execute("SELECT TOP 1 WITH TIES T.Name AS Territory, B.Brand_Name, MAX(S.SALES) AS Sales FROM TERRITORY_SALES AS TS INNER JOIN TERRITORY AS T ON TS.TERRITORY_ID=T.TERRITORY_ID INNER JOIN SALES AS S ON TS.SALES_ID=S.SALES_ID INNER JOIN SKU AS SK ON S.SKU_ID=SK.SKU_ID INNER JOIN BRAND AS B ON SK.BRAND_ID=B.BRAND_ID GROUP BY T.Name, B.Brand_Name ORDER BY ROW_NUMBER() OVER(PARTITION BY T.Name ORDER BY MAX(S.Sales) DESC);").fetchall()
    country_name = [row[0] for row in country_sales]
    country_sales_number = [row[1] for row in country_sales]
    country_brand = [row[2] for row in country_sales]

    login=False

    if 'username' in session:
        login=True

    return render_template('login_home.html',login=login,country_name = country_name, country_sales_number = country_sales_number, country_brand = country_brand, country_sales = country_sales)

# Home Page
@app.route('/home',methods=['GET','POST'])
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

# Present Analysis Page
@app.route('/present')
def present():
    """Renders the Fashion Present Analysis page."""
    return render_template(
        'present.html',
        title='Present Page',
        year=datetime.now().year,
    )

# Past Analysis Page
@app.route('/past')
def past():
    """Renders the Fashion Past Analysis page."""
    return render_template(
        'past.html',
        title='Past Page',
        year=datetime.now().year,
    )

# Future Analysis Page
@app.route('/future')
def future():
    """Renders the Fashion Future Analysis page."""
    return render_template(
        'future.html',
        title='Future Page',
        year=datetime.now().year,
    )

# Contact Page
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

# About Us Page
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='About Us Page'
    )

# Subscription Page
@app.route('/subscription')
def subscription():
    """Renders the subscription page."""
    return render_template(
        'subscription.html',
        title='Subscription',
        year=datetime.now().year,
        message='Subscription Page'
    )

class DataStore():
    Prod= None
    Prod2=None
    Prod3=None
data=DataStore()

# Current Trends
@app.route('/currenttrends', methods=["GET","POST"])
def api_currenttrends():
    if 'tshirts' in request.args:
#        Insert code here/ information to retrieve
        top1_name=[]
        top1_description=[]
        top1_score=[]
        bottom1_name=[]
        bottom1_description=[]
        bottom1_score=[]
        
        images_path=[]
        imagestshirts = glob.glob('/static/images/current_trends/shirt+' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        imagestshirts = glob.glob('/static/images/current_trends/shirt-' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        
        colnames=['sno','URL','id','desc','stars','num_ratings','num_reviews','reviews','vader_score','final_score']
        reqdcolnames=['id','stars','desc','URL','final_score']  
        dataset_csv = pd.read_csv('FashionTrends2022_Project_UJAAL/CurrentTrends/final_csv/tshirts/tshirts_csv_final.csv',names=colnames, delimiter=',', error_bad_lines=False, 
                                  header=None,usecols=reqdcolnames, na_values=" NaN")
        dataset_csv = dataset_csv.dropna()
        dataset_csv2=dataset_csv.sort_values(by='final_score', ascending=False)
        dataset_csv2=dataset_csv2.reset_index()
        #print(dataset_csv2.head())
        for i in range(1, 6):
            top1_name.append(dataset_csv2['desc'][i])
            top1_description.append(dataset_csv2['URL'][i])
            top1_score.append(dataset_csv2['final_score'][i])
        for i in range((len(dataset_csv2)-5),len(dataset_csv2)):
            bottom1_name.append(dataset_csv2['desc'][i])
            bottom1_description.append(dataset_csv2['URL'][i])
            bottom1_score.append(dataset_csv2['final_score'][i])
            
        
        df = pd.read_csv('FashionTrends2022_Project_UJAAL/CurrentTrends/Leaderboard/tshirt_colour_top_bottom.csv')
        #print(df.head())
        df = df[["Bigram", "Rating", "Count"]]
        
        # order in the groupby here matters, it determines the json nesting
        # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
        df1 = df.groupby(['Bigram', 'Rating'])['Count'].sum()
        df1 = df1.reset_index()
        
        
        # start a new flare.json document
        flare = dict()
        d = {"name": "flare", "children": []}
        i=0
        for line in df1.values:
            Bigram = line[0]
            Rating = line[1]
            Count = line[2]
            # make a list of keys
            keys_list = []
            for item in d['children']:
                keys_list.append(item['name'])
    
            # if 'the_parent' is NOT a key in the flare.json yet, append it
            if not Bigram in keys_list:
                d['children'].append({"name": Bigram, "children": [{"name": Rating, "size": Count}]})
                
    
            # if 'the_parent' IS a key in the flare.json, add a new child to it
            else:
                d['children'][keys_list.index(Bigram)]['children'].append({"name": Rating, "size": Count})
                
    
        flare = d
        e = json.dumps(flare)
        data.Prod = json.loads(e)
        Prod=data.Prod
        
        
        
        df = pd.read_csv('FashionTrends2022_Project_UJAAL/CurrentTrends/Leaderboard/tshirt_neck_top_bottom.csv')
        #print(df.head())
        df = df[["Bigram", "Rating", "Count"]]
    
        # order in the groupby here matters, it determines the json nesting
        # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
        df1 = df.groupby(['Bigram', 'Rating'])['Count'].sum()
        df1 = df1.reset_index()
    
        # start a new flare.json document
        flare = dict()
        d = {"name": "flare", "children": []}
    
        for line in df1.values:
            Bigram = line[0]
            Rating = line[1]
            Count = line[2]
    
            # make a list of keys
            keys_list = []
            for item in d['children']:
                keys_list.append(item['name'])
    
            # if 'the_parent' is NOT a key in the flare.json yet, append it
            if not Bigram in keys_list:
                d['children'].append({"name": Bigram, "children": [{"name": Rating, "size": Count}]})
    
            # if 'the_parent' IS a key in the flare.json, add a new child to it
            else:
                d['children'][keys_list.index(Bigram)]['children'].append({"name": Rating, "size": Count})
    
        flare = d
        e = json.dumps(flare)
        data.Prod2 = json.loads(e)
        Prod2=data.Prod2
        
        
        
        df = pd.read_csv('FashionTrends2022_Project_UJAAL/CurrentTrends/Leaderboard/tshirt_print_top_bottom.csv')
        #print(df.head())
        df = df[["Bigram", "Rating", "Count"]]
    
        # order in the groupby here matters, it determines the json nesting
        # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
        df1 = df.groupby(['Bigram', 'Rating'])['Count'].sum()
        df1 = df1.reset_index()
    
        # start a new flare.json document
        flare = dict()
        d = {"name": "flare", "children": []}
    
        for line in df1.values:
            Bigram = line[0]
            Rating = line[1]
            Count = line[2]
    
            # make a list of keys
            keys_list = []
            for item in d['children']:
                keys_list.append(item['name'])
    
            # if 'the_parent' is NOT a key in the flare.json yet, append it
            if not Bigram in keys_list:
                d['children'].append({"name": Bigram, "children": [{"name": Rating, "size": Count}]})
    
            # if 'the_parent' IS a key in the flare.json, add a new child to it
            else:
                d['children'][keys_list.index(Bigram)]['children'].append({"name": Rating, "size": Count})
    
        flare = d
        e = json.dumps(flare)
        data.Prod3 = json.loads(e)
        Prod3=data.Prod3
        
        
        
        
        
        return render_template("website_currenttrends_tshirts.html",images_path=images_path,Prod=Prod, Prod2=Prod2,Prod3=Prod3, top1_name=top1_name,top1_description=top1_description,top1_score=top1_score,bottom1_name=bottom1_name,bottom1_description=bottom1_description,bottom1_score=bottom1_score)
    if 'dresses' in request.args:
#        Insert code here/ information to retrieve
        top1_name=[]
        top1_description=[]
        top1_score=[]
        bottom1_name=[]
        bottom1_description=[]
        bottom1_score=[]
        
        images_path=[]
        imagestshirts = glob.glob('/static/images/current_trends/dress+' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        imagestshirts = glob.glob('/static/images/current_trends/dress-' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        
        colnames=['sno','URL','id','desc','stars','num_ratings','num_reviews','reviews','vader_score','final_score']
        reqdcolnames=['id','stars','desc','URL','final_score'] 
        
        dataset_csv = pd.read_csv('FashionTrends2022_Project_UJAAL/CurrentTrends/final_csv/dresses/dresses_csv_final.csv',names=colnames, delimiter=',', error_bad_lines=False, 
                                  header=None,usecols=reqdcolnames, na_values=" NaN")
        dataset_csv = dataset_csv.dropna()
        dataset_csv2=dataset_csv.sort_values(by='final_score', ascending=False)
        dataset_csv2=dataset_csv2.reset_index()
        #print(dataset_csv2.head())
        for i in range(1, 6):
            top1_name.append(dataset_csv2['desc'][i])
            top1_description.append(dataset_csv2['URL'][i])
            top1_score.append(dataset_csv2['final_score'][i])
        for i in range((len(dataset_csv2)-5),len(dataset_csv2)):
            bottom1_name.append(dataset_csv2['desc'][i])
            bottom1_description.append(dataset_csv2['URL'][i])
            bottom1_score.append(dataset_csv2['final_score'][i])
        
        df = pd.read_csv('FashionTrends2022_Project_UJAAL/CurrentTrends/Leaderboard/dress_top_bottom.csv')
        #print(df.head())
        df = df[["Bigram", "Rating", "Count"]]
    
        # order in the groupby here matters, it determines the json nesting
        # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
        df1 = df.groupby(['Bigram', 'Rating'])['Count'].sum()
        df1 = df1.reset_index()
    
        # start a new flare.json document
        flare = dict()
        d = {"name": "flare", "children": []}
    
        for line in df1.values:
            Bigram = line[0]
            Rating = line[1]
            Count = line[2]
    
            # make a list of keys
            keys_list = []
            for item in d['children']:
                keys_list.append(item['name'])
    
            # if 'the_parent' is NOT a key in the flare.json yet, append it
            if not Bigram in keys_list:
                d['children'].append({"name": Bigram, "children": [{"name": Rating, "size": Count}]})
    
            # if 'the_parent' IS a key in the flare.json, add a new child to it
            else:
                d['children'][keys_list.index(Bigram)]['children'].append({"name": Rating, "size": Count})
    
        flare = d
        e = json.dumps(flare)
        data.Prod = json.loads(e)
        Prod=data.Prod
        return render_template("website_currenttrends.html",images_path=images_path,Prod=Prod, top1_name=top1_name,top1_description=top1_description,top1_score=top1_score,bottom1_name=bottom1_name,bottom1_description=bottom1_description,bottom1_score=bottom1_score)
    if 'skirts' in request.args:
#        Insert code here/ information to retrieve
        top1_name=[]
        top1_description=[]
        top1_score=[]
        bottom1_name=[]
        bottom1_description=[]
        bottom1_score=[]
        
        images_path=[]
        imagestshirts = glob.glob('/static/images/current_trends/skirt+' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        imagestshirts = glob.glob('/static/images/current_trends/skirt-' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        
        colnames=['sno','URL','id','desc','stars','num_ratings','num_reviews','reviews','vader_score','final_score']
        reqdcolnames=['id','stars','desc','URL','final_score']  
        dataset_csv = pd.read_csv('CurrentTrends/final_csv/skirts/skirts_csv_final.csv',names=colnames, delimiter=',', error_bad_lines=False, 
                                  header=None,usecols=reqdcolnames, na_values=" NaN")
        dataset_csv = dataset_csv.dropna()
        dataset_csv2=dataset_csv.sort_values(by='final_score', ascending=False)
        dataset_csv2=dataset_csv2.reset_index()
        #print(dataset_csv2.head())
        for i in range(1, 6):
            top1_name.append(dataset_csv2['desc'][i])
            top1_description.append(dataset_csv2['URL'][i])
            top1_score.append(dataset_csv2['final_score'][i])
        for i in range((len(dataset_csv2)-5),len(dataset_csv2)):
            bottom1_name.append(dataset_csv2['desc'][i])
            bottom1_description.append(dataset_csv2['URL'][i])
            bottom1_score.append(dataset_csv2['final_score'][i])
        
        df = pd.read_csv('CurrentTrends/Leaderboard/skirt_top_bottom.csv')
        #print(df.head())
        df = df[["Bigram", "Rating", "Count"]]
    
        # order in the groupby here matters, it determines the json nesting
        # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
        df1 = df.groupby(['Bigram', 'Rating'])['Count'].sum()
        df1 = df1.reset_index()
    
        # start a new flare.json document
        flare = dict()
        d = {"name": "flare", "children": []}
    
        for line in df1.values:
            Bigram = line[0]
            Rating = line[1]
            Count = line[2]
    
            # make a list of keys
            keys_list = []
            for item in d['children']:
                keys_list.append(item['name'])
    
            # if 'the_parent' is NOT a key in the flare.json yet, append it
            if not Bigram in keys_list:
                d['children'].append({"name": Bigram, "children": [{"name": Rating, "size": Count}]})
    
            # if 'the_parent' IS a key in the flare.json, add a new child to it
            else:
                d['children'][keys_list.index(Bigram)]['children'].append({"name": Rating, "size": Count})
    
        flare = d
        e = json.dumps(flare)
        data.Prod = json.loads(e)
        Prod=data.Prod
        return render_template("website_currenttrends.html",images_path=images_path,Prod=Prod, top1_name=top1_name,top1_description=top1_description,top1_score=top1_score,bottom1_name=bottom1_name,bottom1_description=bottom1_description,bottom1_score=bottom1_score)
    if 'footwear' in request.args:
#        Insert code here/ information to retrieve
        top1_name=[]
        top1_description=[]
        top1_score=[]
        bottom1_name=[]
        bottom1_description=[]
        bottom1_score=[]
        
        images_path=[]
        imagestshirts = glob.glob('/static/images/current_trends/skirt+' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        imagestshirts = glob.glob('/static/images/current_trends/skirt-' + '*.jpeg')
        for i in range(0,len(imagestshirts)):
            images_path.append(imagestshirts[i])
        
        colnames=['sno','URL','id','desc','stars','num_ratings','num_reviews','reviews','vader_score','final_score']
        reqdcolnames=['id','stars','desc','URL','final_score']  
        dataset_csv = pd.read_csv('CurrentTrends/final_csv/skirts/skirts_csv_final.csv',names=colnames, delimiter=',', error_bad_lines=False, 
                                  header=None,usecols=reqdcolnames, na_values=" NaN")
        dataset_csv = dataset_csv.dropna()
        dataset_csv2=dataset_csv.sort_values(by='final_score', ascending=False)
        dataset_csv2=dataset_csv2.reset_index()
        #print(dataset_csv2.head())
        for i in range(1, 6):
            top1_name.append(dataset_csv2['desc'][i])
            top1_description.append(dataset_csv2['URL'][i])
            top1_score.append(dataset_csv2['final_score'][i])
        for i in range((len(dataset_csv2)-5),len(dataset_csv2)):
            bottom1_name.append(dataset_csv2['desc'][i])
            bottom1_description.append(dataset_csv2['URL'][i])
            bottom1_score.append(dataset_csv2['final_score'][i])
        
        df = pd.read_csv('CurrentTrends/Leaderboard/skirt_top_bottom.csv')
        #print(df.head())
        df = df[["Bigram", "Rating", "Count"]]
    
        # order in the groupby here matters, it determines the json nesting
        # the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
        df1 = df.groupby(['Bigram', 'Rating'])['Count'].sum()
        df1 = df1.reset_index()
    
        # start a new flare.json document
        flare = dict()
        d = {"name": "flare", "children": []}
    
        for line in df1.values:
            Bigram = line[0]
            Rating = line[1]
            Count = line[2]
    
            # make a list of keys
            keys_list = []
            for item in d['children']:
                keys_list.append(item['name'])
    
            # if 'the_parent' is NOT a key in the flare.json yet, append it
            if not Bigram in keys_list:
                d['children'].append({"name": Bigram, "children": [{"name": Rating, "size": Count}]})
    
            # if 'the_parent' IS a key in the flare.json, add a new child to it
            else:
                d['children'][keys_list.index(Bigram)]['children'].append({"name": Rating, "size": Count})
    
        flare = d
        e = json.dumps(flare)
        data.Prod = json.loads(e)
        Prod=data.Prod
        return render_template("website_currenttrends.html",images_path=images_path,Prod=Prod, top1_name=top1_name,top1_description=top1_description,top1_score=top1_score,bottom1_name=bottom1_name,bottom1_description=bottom1_description,bottom1_score=bottom1_score)


@app.route("/currenttrendsget-data",methods=["GET","POST"])
def returnProdDatacurrenttrends():
    f=data.Prod
    return jsonify(f)


@app.route("/currenttrendsgetdata2",methods=["GET","POST"])
def returnProdDatacurrenttrends2():
    f=data.Prod2
    return jsonify(f)

@app.route("/currenttrendsgetdata3",methods=["GET","POST"])
def returnProdDatacurrenttrends3():
    f=data.Prod3
    return jsonify(f)