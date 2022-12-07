import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords 
import re

analyser = SentimentIntensityAnalyzer()

data=pd.read_csv("D:/Downloads/GriD_Fashion-master/GriD_Fashion-master/CurrentTrends/final_code/dress-flipkart-final-final.csv")
data.head()
data=data[['URL','ID','ITEM','STARS','NUMBER OF RATINGS','NUMBER OF REVIEWS', 'LIST OF REVIEWS']]

data.rename(columns = {'ID':'id','ITEM':'desc', 'LIST OF REVIEWS':'reviews','NUMBER OF REVIEWS':'num_reviews','STARS':'stars','NUMBER OF RATINGS':'num_ratings'}, inplace=True)
data.head()

data.reviews = data.reviews.str.lower()
data.reviews = data.reviews.str.replace('\n','').str.replace('[\'!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~]','')


data['vader_score'] = 1.0
for ind in data.index: 
    rev=data['reviews'][ind]
    x = rev.split()
#     print(x)
    sum_score=0.0
    for i in x:
        score = analyser.polarity_scores(i)
        sum_score=sum_score+score['compound']
    data['vader_score'][ind] =sum_score

total_star_givers = data['num_ratings'].sum()     
total_review_givers = data['num_reviews'].sum()
# print(total_star_givers)
# print(total_review_givers)

data['final_score'] = ((data['stars']*data['num_ratings'])/total_star_givers)+((data['vader_score']*data['num_reviews'])/total_review_givers)

data.head()
data.to_csv('D:/Downloads/GriD_Fashion-master/GriD_Fashion-master/CurrentTrends/final_code/dress-flipkart-final-final.csv')

dict_bigram={}
item_bigram={}
stop_words = set(stopwords.words('english')) 
for ind in data.index:
    d=data['desc'][ind][6:-5]
    d= re.sub(r'[^\w\s]', '', d) 
    nltk_tokens = nltk.word_tokenize(d)
    nltk_tokens = [w for w in nltk_tokens if not w in stop_words] 
    arr=list(nltk.bigrams(nltk_tokens))
    for i in arr:
        if i in dict_bigram:
            dict_bigram[i]=dict_bigram[i]+1
            item_bigram[" ".join(i)].append(ind)
        else:
            dict_bigram[i]=1
            item_bigram[" ".join(i)]=[]
            item_bigram[" ".join(i)].append(ind)
print(item_bigram) 

dict_bigram_sorted= sorted(dict_bigram, key=dict_bigram.get, reverse=True)
print(dict_bigram_sorted)

row=dict_bigram_sorted[0:5]+dict_bigram_sorted[-5:]
print(row)

res = [] 
for el in row: 
#         sub = el.split(', ')
    sub=" ".join(el)
    res.append(list(sub.split("*"))) 
print(res)


import csv
with open('dress_top_bottom.csv', 'w', newline='') as file:
    res = [] 
    for el in row: 
#         sub = el.split(', ')
        sub=" ".join(el)
        res.append(list(sub.split("*"))) 

    for i in range(len(res)):
        res[i]=res[i]+item_bigram[res[i][0]]

    print(res)
    writer = csv.writer(file)
    writer.writerows(res)