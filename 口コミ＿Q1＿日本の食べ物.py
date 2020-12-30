#!/usr/bin/env python
# coding: utf-8

# # 口コミ（食べログ）

# we will try to find about "When I visit Japan (or particular town in Japan) what kind of food that is recomended by Japanese that should I try?"
# 
# This code will contain of the data scraping and data cleaning part

# # Data Scraping

# In[ ]:


#import the library

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import string


# In[ ]:


#define the scraping path
#put your own User-Agent

headers = {'User-Agent': '...'}
rstlst_all=[]

def getRstlst(town,page):
    url = f'https://tabelog.com/{town}/rstLst/{page}/'
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    rstlsts = soup.find_all('div', {'class':'list-rst__contents'})
    for item in rstlsts:
        rstlst = {
            'town' : town,
            'rst_kind' : item.find('div', {'class':'list-rst__area-genre cpy-area-genre'}).text,
            'rst_star' : item.find('span', {'class':'c-rating__val c-rating__val--strong list-rst__rating-val'}),
            'rst_rvwcnt' : item.find('em',{'class':'list-rst__rvw-count-num cpy-review-count'}).text
        }
        rstlst_all.append(rstlst)
    return


# In[ ]:


##try the function for 1 town at first
##here, we want to obtain the data for Tokyo in the page 1 to 50
for n in range (1,50):
    getRstlst('tokyo',n)

print(len(rstlst_all))


# In[ ]:


##apply to multiple town

towns = ['tokyo','osaka','kyoto']
for town in towns:
    n in range(1,50)
    getRstlst(town,n)

print(len(rstlst_all))


# In[ ]:


##store the data into Pandas dataframe for easiness
##you can export the data first as well 
data = pd.DataFrame(rstlst_all)
print(data.head())
#data.to_excel('ロコミ＿Q1.xlsx')
#print('done')


# # Data Cleaning

# in this case, data cleaning only necessary for the 'rst_kind' part

# In[ ]:


#read the data
#data = pd.read_excel('ロコミ＿Q1.xlsx')


# In[ ]:


def clean_kind(text):
    text = re.sub('その他','',text)
    text = re.sub('\n','',text)
    text = re.sub('・',' ',text)
    text = re.sub('、',' ',text)
    text = re.sub('[（）]','', text)
    return text

data['rst_kind'] = data['rst_kind'].apply(clean_kind)
new = data['rst_kind'].str.split('/', n = 1,expand=True)
data['rst_loc'] = new[0]
data['rst_kind'] = new[1]
print(data.head())


# In[ ]:


# Saving your data for further analysis
data.to_excel('ロコミ＿Q1_clean.xlsx')
print('done')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




