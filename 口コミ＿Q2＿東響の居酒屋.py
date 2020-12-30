#!/usr/bin/env python
# coding: utf-8

# # 東響の居酒屋口コミ（食べログ）

# we will try to find about "how was people sentiment towards izakaya in Tokyo from time to time?"

# # Data Scraping

# In[ ]:


#import the library

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt


# In[ ]:


#define the scraping path
#put your own User-Agent

headers = {'User-Agent': '...'}
linklist = []

def geturl(page):
    url = f'https://tabelog.com/tokyo/rstLst/izakaya/{page}/'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    rstlsts = soup.find_all('div', {'class':'list-rst__contents'})
    for item in rstlsts:
        rstlst = item.find('a',{'class':'list-rst__rst-name-target cpy-rst-name'})['href']
        rvw_links = rstlst + 'dtlrvwlst/'
        linklist.append(rvw_links)
    return 
#print(len(rvws))


# In[ ]:


#scrape the data from page 1 to 50

for n in range(1,50):
    geturl(n)
    
print(len(linklist))


# In[ ]:


#define to get the review location
#the location will be station (駅) based
def getloc(rvw):
    page = requests.get(rvw)
    soup = BeautifulSoup(page.text, 'html.parser')
    rst_loc = soup.find(class_='linktree__parent-target-text').text
    #print(rst_loc)
    return rst_loc


# In[ ]:


#define to get the average star from each restaurant 
#on the corresponding location

def getstar(rvw):
    page = requests.get(rvw)
    soup = BeautifulSoup(page.text, 'html.parser')
    rst_star = soup.find(class_='rdheader-rating__score-val-dtl').text
    rvw_count = soup.find(class_='num').text
    #print(rst_star)
    return rst_star


# In[ ]:


#define to get the review date

def getdate(rvw):
    page = requests.get(rvw)
    soup = BeautifulSoup(page.text, 'html.parser')
    rvw_date = soup.find(class_='rvw-item__date').find_all('p')
    #print(rvw_date)
    return rvw_date


# In[ ]:


#define to get the review content (口コミ)

def getrvw(rvw):
    page = requests.get(rvw)
    soup = BeautifulSoup(page.text, 'html.parser')
    rvw_cmt = soup.find(class_='rvw-item__rvw-comment').text
    #print(rvw_cmt)
    return rvw_cmt


# In[ ]:


#apply the 2 above functions to obtain the 
#data set

rvw_item = []
for r in linklist:
    item = {
        'rst_loc':getloc(r),
        'rst_stavg':getstar(r),
        'rvw_date':getdate(r),
        'rvw_content':getrvw(r)
    }
    rvw_item.append(item)


# In[ ]:


#store in the Pandas dataframe for convenient way
#you can export the data first as well 

data = pd.DataFrame(rvw_item)
print(len(data))
#data.to_excel('ロコミ＿Q2.xlsx')
#print('done')


# # Data Cleaning

# In[ ]:


#read the data
#data = pd.read_excel('ロコミ＿Q2.xlsx')


# In[ ]:


#define to clean the 'rvw_content' part 

def clean_content(text):
    text = re.sub('\n','',text)
    text = re.sub('、',' ',text)
    text = re.sub('[（）.。■？！・＾】【円×♪:]','', text)
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


# In[ ]:


def clean_date(text):
    text = re.sub('\n','',text)
    text = re.sub('\[.*?\]','',text)
    text = re.sub('[訪問]','', text)
    return text


# In[ ]:


data['rvw_content'] = data['rvw_content'].apply(clean_content)
data['rvw_date'] = data['rvw_date'].apply(clean_content)
data.head()


# In[ ]:


# Saving your data for further analysis
data.to_excel('ロコミ＿Q2_clean.xlsx')
print('done')


# In[ ]:





# In[ ]:




