


from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
import numpy as np
import pyodbc as pyodbc 




def connection():
    DRIVER_NAME = 'SQL Server'
    s = 'localhost' #Your server name 
    d = 'Fashion_Trends_2022' 
    u = "DESKTOP-JBUBG3B" #Your login
    p = ' ' #Your login password
    conn_string = f"""
        Driver={{{DRIVER_NAME}}};
        Server={s};
        Database={d};
        Trust_Connection=yes;"""
    conn = pyodbc.connect(conn_string)
    return conn

#The url for flipkart>tshirts.
url="https://www.flipkart.com/mens-footwear/sports-shoes/pr?sid=osp,cil,1cu&otracker=nmenu_sub_Men_0_Sports%20Shoes"
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
weight_=[]
sleeve_=[]
fit_=[]
fabric_=[]
neck_=[]
pattern_=[]
brand_fit_=[]
brand_color_=[]
Inner_mat=[]
Outer_mat=[]
Sole_material=[]

# shirts=linkss

#for i in range(len(shirts)): 
 #       print(i)
 #       url=shirts[i]
 #       print(url)

# print(len(shirts))
for i in range(len(page_links)): 
    
   
        
        url=page_links[i]
        x= requests.get(url)
        soup= bs(x.content, "html.parser")
        try:
            brand=soup.find("span", {"class": "G6XhRU"}).text
            print(brand)
        except:
            brand=' '
        finally: 
            try:           
                item=soup.find("span", {"class": "B_NuCI"}).text
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
                            print(features)
                            urls.append(url)
                            brands.append(brand)
                            item_names.append(item)
                            disc_prices.append(disc_price)
                            mrp_prices.append(mrp)
                            stars.append(star)
                            ratings.append(ratings_num)
                            reviews.append(reviews_num)
                            text_reviews.append(review)
                            # weight_.append(features['Weight'])
                            # Inner_mat.append(features['Inner material'])
                            # Outer_mat.append(features['Outer material'])
                            # Sole_material.append(features['Sole material'])
                            # brand_color_.append(features['Color'])
                            print("task finish...")        
#convert ratings,reviews, stars to int and floats for easy calculation later
y=[int(r.replace(',','')) for r in ratings]
ratings=y
reviews=[(r.replace(',','')) for r in reviews]
stars=[float(r) for r in stars]

#creating a dataframe and saving it to csv
table={'URL':urls,'BRAND':brands,'ITEM':item_names,'DISCOUNTED PRICE':disc_prices,'MRP':mrp_prices,'STARS':stars,'NUMBER OF RATINGS':ratings,'NUMBER OF REVIEWS':reviews,'LIST OF REVIEWS':text_reviews}
df=pd.DataFrame(table)
df.to_csv(r'Footwear-flipkart-final-final.csv')


#creating a dataframe and saving it to csv
table={'URL':urls,'BRAND':brands,'ITEM':item_names,'DISCOUNTED PRICE':disc_prices,'MRP':mrp_prices,'STARS':stars,'NUMBER OF RATINGS':ratings,'NUMBER OF REVIEWS':reviews,'LIST OF REVIEWS':text_reviews}
print(type(table))
df=pd.DataFrame(table)
df.to_csv(r'skirt-flipkart-final-final.csv')

#Database

csv_Data=pd.read_csv("D:/Downloads/GriD_Fashion-master/GriD_Fashion-master/skirt-flipkart-final-final.csv")
dataframe1 = pd.DataFrame(csv_Data)
df.rename(columns = {'ID':'id','ITEM':'desc', 'LIST OF REVIEWS':'reviews','NUMBER OF REVIEWS':'num_reviews','STARS':'stars','NUMBER OF RATINGS':'num_ratings','DISCOUNTED PRICE':'DISCOUNTEDPRICE'}, inplace=True)

conn = connection()
cursor = conn.cursor()

# Insert DataFrame to Table
for row in dataframe1.itertuples():
    stars=str(row.stars)
    num_ratings = str(row.num_ratings)
    num_reviews = str(row.num_reviews)
    cursor.execute('''INSERT INTO Product_Details (URL,Brands,ITEM_NAME,DISCOUNTED_PRICE,MRP,STARS,No_Rating,No_Reviews,List_Reviews)VALUES (?,?,?,?,?,?,?,?,?)''',row.URL,row.BRAND,row.desc,row.DISCOUNTEDPRICE,row.MRP,stars,num_ratings,num_reviews,row.reviews)
    # cursor.execute('INSERT INTO Product_data (ID,URL,Brands,ITEM_NAME,DISCOUNTED_PRICE,MRP,STARS,No_Rating,No_Reviews,List_Reviews)VALUES ('
    #                     +id+','+row.URL+','+row.BRAND+','+row.desc+','+row.DISCOUNTEDPRICE+','+ row.MRP +','+ stars +','+ num_ratings +','+ num_reviews +','+ row.reviews +')')
    cursor.commit()



cursor.execute('''SELECT * FROM Product_Details''')
results = cursor.fetchall()
print(results)




