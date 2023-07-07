# importing required python libraries
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

# Required Flipkart page
url = "https://www.flipkart.com/food-products/pr?sid=eat"

urls = []

for var in range(1,16):
    url = ["https://www.flipkart.com/food-products/pr?sid=eat=%i"%(var)]
    urls.append(url[0])


urls

con_urls = connect(urls[0])


for i in range(0,15):
    con = connect(urls[i])
    for container in con:
        product_name = container.div.img["alt"]
        print(product_name)

for container in con:
    s_price = container.findAll("div",{"class":"_30jeq3 _1_WHN1"})
    actual_price = container.findAll("div",{"class":"_3I9_wc _27UcVY"})
    ratting = container.findAll("div",{"class":"_3LWZlK"})
    p_retting = container.findAll("span",{"class":"_2_R_DZ"})
    offer = container.findAll("div",{"class":"_3Ay6Sb"})
    print(offer)

def dataframe(containers):
    data = {"Product_name":[],"Sale price":[],"Actual Price":[],"Ratting":[],"Person Ratting":[],"Offer":[]}
    for i in range(0,15):
        con = connect(containers[i])
        for container in con:
            #Product Name
            product_name = container.div.img["alt"]
            data["Product_name"].append(product_name)
            
            #Sale price
            s_price = container.findAll("div",{"class":"_30jeq3 _1_WHN1"})
            s_p = s_price[0].text
            data["Sale price"].append(s_p)
            
            #Actual Price
            try:
                actual_price = container.findAll("div",{"class":"_3I9_wc _27UcVY"})
                a_p = actual_price[0].text
                data["Actual Price"].append(a_p)
            except IndexError:
                print("Same as sale price")
                data["Actual Price"].append("Same Price")
            
            #Ratting
            try:
                ratting = container.findAll("div",{"class":"_3LWZlK"})
                r = ratting[0].text
                data["Ratting"].append(r)
            except IndexError:
                data["Ratting"].append("No Ratting")
            
            #No of person given ratting
            try:
                p_retting = container.findAll("span",{"class":"_2_R_DZ"})
                p_r = p_retting[0].text
                data["Person Ratting"].append(p_r)
            except IndexError:
                data["Person Ratting"].append("No Ratting")
                        
            
            #Offer
            try:
                offer = container.findAll("div",{"class":"_3Ay6Sb"})
                off = offer[0].text
                data["Offer"].append(off)
            except IndexError:
                data["Offer"].append("No offer this product")
            
        print("done",i)
        
    return data

dataset = dataframe(urls)

df = pd.DataFrame(dataset)
df.dtypes


df["Ratting"] = pd.to_numeric(df["Ratting"])

df.dtypes

df[["No of Ratting","No of Reviews"]] = df["Person Ratting"].str.split("&",1,expand=True)

df["No of Ratting"] = df["No of Ratting"].str.split(" ").str[0]

df["No of Reviews"] = df["No of Reviews"].str.split(" ").str[0]

df["No of Reviews"] = df["No of Reviews"].str.split(" ").str[0]

df

# Storing Data in CSV
df.to_csv("Food_Data.csv")

# Storing Data in MongoDB
import pymongo #!pip install pymongo


def dftomonogdb(dataset):
    import pymongo
    connect = pymongo.MongoClient(host="localhost",port=27017)
    database = connect["flipkartDB"]
    collection = database["iphone"]


    for (row,rs) in dataset.iterrows():
        #print(row)
        #r = rs
        Product_Name = rs[0]
        Sale_Price = rs[1]
        Actual_Price = rs[2]
        Ratting = rs[3]
        Offer = rs[4]
        n_ratting = rs[5]
        n_review = rs[6]
        d = {"Product_Name":Product_Name,"Ratting":Ratting,"Sale_Price":Sale_Price,
             "Actual_Price":Actual_Price,"Offer":Offer,"No of Ratting":n_ratting,"No of Reviews":n_review}
        
        collection.insert_one(d)
        
        
        
    print("Done")

dftomonogdb(df)


