


from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
import numpy as np
#import MySQLdb.cursors
import pyodbc as pyodbc 
import shutil
import urllib.request
from pathlib import Path

def initialize():
    path_to_file = 'skirt-flipkart-final-final.csv'
    path = Path(path_to_file)

    if path.is_file():     
        print(f'The file {path_to_file} exists')
        insertcsvdata()
    else:
        Scrapper()

def connection():
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
        conn = pyodbc.connect(conn_string)
        return conn
    except Exception as e:
        print(e)
        print('task is terminated')
        sys.exit()
    

def Scrapper():
    #The url for flipkart>tshirts.
    url="https://www.flipkart.com/clothing-and-accessories/bottomwear/skirts/pr?sid=clo,vua,iku&otracker=categorytree"
    #url="https://www.amazon.com/b/ref=s9_acss_bw_cg_MLDTSBC_2b1_w?node=1258644011&ref=lp_1040658_nr_n_1&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-7&pf_rd_r=HRC7K6SFZY6FNSECGNQR&pf_rd_t=101&pf_rd_p=3254816d-1451-4e02-8410-e252015abaa8&pf_rd_i=7147441011"
    x= requests.get(url)
    soup= bs(x.content, "html.parser")

    page=soup.findAll("a", {"class": "_2UzuFa"})

    #Getting links for all pages. Each page has 40 items
    page_links=[]
    for p in page:
        page_links.append(p.get('href'))
    page_links=['https://flipkart.com'+p for p in page_links ]
    print(page_links)

    # linkss=[]
    # for p in page_links:
    #     url=p
    #    # print(url)
    #     x= requests.get(url)
    #     soup= bs(x.content, "html.parser")
    #     linkss=soup.findAll("div",{"class":"aMaAEs"})
    #     #links=soup.find_all({"xpath":'//*[@id="container"]/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/a'})
    #     #print("links", linkss)
    
        
    # len(linkss)



    # linkss[0]

    def download_img(url,file_name,File_path):
        full_path = File_path + file_name + '.jpg'
        urllib.urlretrieve(url,full_path)


    #Extracts the following features from each item and stores them in a list, to be stored as dataframe later on
    urls=[]
    brands=[]
    item_names=[]
    disc_prices=[]
    mrp_prices=[]
    stars=[]
    ratings=[]
    reviews=[]
    text_reviews=[]
    type_=[]
    sleeve_=[]
    fit_=[]
    fabric_=[]
    neck_=[]
    pattern_=[]
    brand_fit_=[]
    brand_color_=[]

    # shirts=linkss

    #for i in range(len(shirts)): 
     #       print(i)
     #       url=shirts[i]
     #       print(url)

    # print(len(shirts))
    for i in range(len(page_links)): 
            url=page_links[i]
            x= requests.get(url,stream=True)
            soup= bs(x.content, "html.parser")
            try:
                imghref = soup.find("img",{"class":"_2r_T1I _396QI4"})
            except:
                imghref=' '
            try:
                brand=soup.find("span", {"class": "G6XhRU"}).text
                print(brand)
            except:
                brand=' '
            finally: 
                try:           
                    item=soup.find("span", {"class": "B_NuCI"}).text
                    print(item)
                    download_img(imghref,item,'D:/Downloads/GriD_Fashion-master/GriD_Fashion-master/static/New Images/')
                    print(item)
                except:
                    item = ' '
                finally:
                    try:
                        disc_price=soup.find("div", {"class": "_30jeq3 _16Jk6d"}).text
                        print(disc_price)
                    except:
                        disc_price= ''
                    finally: 
                        try:
                            mrp=soup.find("div", {"class": "_3I9_wc _2p6lqe"}).text
                            print(mrp)
                        except:
                            mrp='0' 
                        finally:   
                            try:
                                star=soup.find("div", {"class": "_3LWZlK _3uSWvT"}).text
                                print(type(star))
                                print(star)
                                rating_number=soup.find("span",{"class":"_2_R_DZ"}).text
                                print(rating_number) 
                                ratings_num=(rating_number[0:rating_number.find('ratings')-1])
                                print(ratings_num)   
                                reviews_num=rating_number[rating_number.find('and')+4:rating_number.find('reviews')-1]
                                print(reviews_num)
                            except:
                                star = '0'
                                print(star)
                                reviews_num = '0' 
                                print(reviews_num)
                                ratings_num = '0' 
                                print(ratings_num)
                                print("Incomplete details for item"+str(i)+url)
                            finally:
                                review=[]
                                x=soup.findAll("div", {"class": "_6K-7Co"})
                                for i in range(len(x)):
                                    review.append(x[i].text)
                            
                            
                                feat=soup.findAll("div", {"class": "col col-3-12 _2H87wv"})
                                feat_ans=soup.findAll("div", {"class": "col col-9-12 _2vZqPX"})
                                features={}
                                for x in range(len(feat)):
                                    features[feat[x].text]=feat_ans[x].text
                                urls.append(url)
                                brands.append(brand)
                                item_names.append(item)
                                disc_prices.append(disc_price)
                                mrp_prices.append(mrp)
                                stars.append(star)
                                ratings.append(ratings_num)
                                reviews.append(reviews_num)
                                text_reviews.append(review)
                                # type_.append(features['Type'])
                                # sleeve_.append(features['Brand Color'])
                                # fabric_.append(features['Fabric'])
                                # pattern_.append(features['Color'])
                                print("task finish...")        
    #convert ratings,reviews, stars to int and floats for easy calculation later
    y=[int(r.replace(',','')) for r in ratings]
    ratings=y
    reviews=[(r.replace(',','')) for r in reviews]
    stars=[float(r) for r in stars]




    #creating a dataframe and saving it to csv
    table={'URL':urls,'BRAND':brands,'ITEM':item_names,'DISCOUNTED PRICE':disc_prices,'MRP':mrp_prices,'STARS':stars,'NUMBER OF RATINGS':ratings,'NUMBER OF REVIEWS':reviews,'LIST OF REVIEWS':text_reviews}
    print(type(table))
    df=pd.DataFrame(table)
    df.to_csv(r'skirt-flipkart-final-final.csv')

    insertcsvdata()



def insertcsvdata():
    #Database
    csv_Data=pd.read_csv("skirt-flipkart-final-final.csv")
    dataframe1 = pd.DataFrame(csv_Data)
    dataframe1.rename(columns = {'ID':'id','ITEM':'desc', 'LIST OF REVIEWS':'reviews','NUMBER OF REVIEWS':'num_reviews','STARS':'stars','NUMBER OF RATINGS':'num_ratings','DISCOUNTED PRICE':'DISCOUNTEDPRICE'}, inplace=True)

    conn = connection()
    cursor = conn.cursor()

    # Insert DataFrame to Table
    for row in dataframe1.itertuples():
        stars=str(row.stars)
        num_ratings = str(row.num_ratings)
        num_reviews = str(row.num_reviews)
        cursor.execute('''INSERT INTO Dress_Data (URL,Brands,ITEM_NAME,DISCOUNTED_PRICE,MRP,STARS,No_Rating,No_Reviews,List_Reviews)VALUES (?,?,?,?,?,?,?,?,?)''',row.URL,row.BRAND,row.desc,row.DISCOUNTEDPRICE,row.MRP,stars,num_ratings,num_reviews,row.reviews)
        # cursor.execute('INSERT INTO Product_data (ID,URL,Brands,ITEM_NAME,DISCOUNTED_PRICE,MRP,STARS,No_Rating,No_Reviews,List_Reviews)VALUES ('
        #                     +id+','+row.URL+','+row.BRAND+','+row.desc+','+row.DISCOUNTEDPRICE+','+ row.MRP +','+ stars +','+ num_ratings +','+ num_reviews +','+ row.reviews +')')
        cursor.commit()



    cursor.execute('''SELECT * FROM Dress_Data''')
    results = cursor.fetchall()
    print(results)



