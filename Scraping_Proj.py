#!/usr/bin/env python
# coding: utf-8

# Using BeautifulSoup to scrap the data from the Web page

# In[1]:


from bs4 import BeautifulSoup
import urllib.request as urllib
import re
import pandas as pd


# In[2]:


html_page = urllib.urlopen("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
soup = BeautifulSoup(html_page)


# In[3]:


soup


# In[4]:


My_table = soup.find('table',{'class':'wikitable sortable'})
My_table


# In[5]:


My_table.find_all('th')


# In[6]:


col_names = []
for col in My_table.find_all('th'):
    col = str(col)
    col = col.replace("<th>","")
    col = col.replace("</th>","")
    col = col.replace("\n","")
    col_names.append(col)
print(col_names)


# Extracting Data from Table of the Wikipedia page

# In[41]:



li_post = []
li_boro = []
li_neigh = []
count=0
for row in My_table.find_all('td'):
    row = str(row)
    row = row.replace("<td>","")
    row = row.replace("</td>","")
    row = row.replace("\n","")
    if row.startswith("<a"):
     #  row = re.sub("<a *","", row)
     #  row = re.sub("href=*", "", row)
     #  row = re.sub("/wiki*/*", "", row)
     #  row = re.sub("</a>", "", row)
     #  row = re.sub(">", "", row)
     #  row = re.sub("title=", "", row)
     #  row = re.split(",",row)
        row = re.split(">", row)
        row = row[1]
        row = re.sub("</a", "", row)
    
    if count ==0:
        li_post.append(row)
        count=count+1
    
    elif count== 1:
        li_boro.append(row)
        count=count+1
    
    else:
        li_neigh.append(row)
        count=0
    



data = {'Postcode': li_post[:],
        'Borough': li_boro[:],
        'Neighbourhood': li_neigh[:]
        }

df = pd.DataFrame(data, columns = col_names)
df
    


# Data Cleaning

# In[42]:



df['Postcode'] = df['Postcode'].sort_values()
df


# In[43]:


df = df[df['Borough']!='Not assigned']
df

li_count = []
li_count = df.groupby(['Postcode'])['Neighbourhood'].count().tolist()

#df.groupby(['Postcode'])['Neighbourhood'].count()

#print(li_count)

k=0

#li_merge = []
#li_merge = df['Neighbourhood'][df['Postcode'] == 'M5A'].tolist()

li_code = []
for index,row in df.iterrows():
    if li_count[k] == 1:
        continue
    else:
        i = 0
        li_merge = []
        li_merge = df['Neighbourhood'][df['Postcode'] == row['Postcode']].tolist()
        
        while i< len(li_merge):
            if i!=0 and row['Postcode'] not in li_code:
                li_merge[0] = li_merge[0] + ", "+ li_merge[i]
            i = i+1
    row['Neighbourhood'] = li_merge[0]
    li_code.append(row['Postcode'])
df


# In[44]:



df.drop_duplicates(subset ="Postcode", 
                     keep = "first", inplace = True)
df


# Updating Not assigned rows in Neighbourhood column

# In[57]:


import numpy as np
df = df.sort_values('Postcode', axis=0, ascending=True, inplace=False, kind='quicksort')

df['Neighbourhood'] = np.where(df['Neighbourhood']== 'Not assigned', df['Borough'], df['Neighbourhood'])
df


# Extracting Latitude and Longitude data

# In[48]:


df_new = pd.read_csv(r'C:\Users\sahit\Downloads\Geospatial_Coordinates.csv')
df_new


# Creating DataFrame in the Specified format

# In[58]:



li_new_code = []
li_new_boro = []
li_new_neigh = []
li_new_lat = []
li_new_long = []

li_new_code = df['Postcode'].tolist()
li_new_boro = df['Borough'].tolist()
li_new_neigh = df['Neighbourhood'].tolist()
li_new_lat = df_new['Latitude'].tolist()
li_new_long = df_new['Longitude'].tolist()

data_cleaned = {'Postcode': li_new_code[:],
        'Borough': li_new_boro[:],
        'Neighbourhood': li_new_neigh[:], 
        'Latitude' : li_new_lat[:],
        'Longitude' : li_new_long[:]
        }

new_col_names = ['Postcode', 'Borough', 'Neighbourhood', 'Latitude', 'Longitude']

df_cleaned = pd.DataFrame(data_cleaned, columns = new_col_names)

df_cleaned


# In[ ]:




