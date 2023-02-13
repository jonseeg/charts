#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

# import libraries for data visualization
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


df_orig = pd.read_csv("/Users/bossm/CIS3920/data/food_order.csv")

df = df_orig.copy()

# returns the first 5 rows
df.head()


# In[3]:


# to restrict the float value to 2 decimal places
pd.set_option('display.float_format', lambda x: '%.2f' % x)

# using describe function to get a 5 number statistical summary with round to restrict decimal places and transpose
df.describe().round(2).T


# In[4]:


df.rating.value_counts(1)


# In[5]:



# we will make 2 lists of restaurant names, old values and new values, then iterate the list to replace old values with new values in dataframe
old_values = ['Big Wong Restaurant \x8c_¤¾Ñ¼', 'Empanada Mama (closed)', 'Chipotle Mexican Grill $1.99 Delivery', "Joe's Shanghai \x8e_À\x8eü£¾÷´", 'Dirty Bird To Go (archived)', 'CafÌ© China']
new_values = ['Big Wong Restaurant', 'Empanada Mama', 'Chipotle Mexican Grill', "Joe's Shanghai", 'Dirty Bird To Go', 'Cafe China']

# iterating the list of old restaurant names to find their index values
for i, name in enumerate(old_values):
  
  index_value = df[df['restaurant_name'] == name].index

# iterating the index values and replacing the old name with new name
  for x in index_value:

    df.loc[x,'restaurant_name'] = new_values[i]


# removing minor typing anomalies by applying strip and capitalize using lambda
df['restaurant_name'] = df['restaurant_name'].apply(lambda x : x.strip().capitalize())

# checking restaurant names again for verifying changes
df['restaurant_name'].nunique()


# In[6]:


df['rating_new'] = df['rating'].replace('Not given', np.nan).astype(float)

# adding a new column in the dataframe which will be the sum of food preparation time and delivery time
df['order_completion_time'] = df['food_preparation_time'] + df['delivery_time']

# creating a copy of dataframe before imputing rating values
df_original_file = df.copy()

# Imputing Nan values with mean rating of the respective restaurant
df['rating_new'] = df['rating_new'].fillna(value = df.groupby(['restaurant_name'])['rating_new'].transform('mean'))

# copying dataframe with imputed ratings to new dataframe
df_modified_rating = df.copy()

# copying original dataframe with unimputed values to df
df = df_original_file.copy()

df.head()


# In[7]:


df_modified_rating.isnull().sum()


# In[23]:


# checking histogram for cost of order
plt.figure(figsize=(15,10))
sns.histplot(data=df, x='cost_of_the_order', kde=True, color='orange')
plt.xlabel('Dollar Cost')
plt.ylabel('Order Count')
plt.title('Distribution of Cost of the Order')
plt.grid(axis = 'y', color = 'red', linestyle = '--', linewidth = 0.4)
plt.show()

#checking boxplot for cost of order
plt.figure(figsize=(15,10))
sns.boxplot(data=df, x='cost_of_the_order', color='lightblue')
plt.xlabel('Dollar Cost')
plt.title('Boxplot of Cost of the Order')
plt.show()


# In[20]:


# checking count plot of day of the week
plt.figure(figsize=(15,10))
sns.countplot(data=df, y='day_of_the_week')
plt.xlabel('Count')
plt.ylabel('Day of the Week')
plt.title('Count of Day of the Week')
plt.grid(axis = 'x', color = 'green', linestyle = '--', linewidth = 0.5)
plt.show()


# In[24]:


# storing the name of top 5 restaurants 
top5_restaurant_names = df['restaurant_name'].value_counts().reset_index().iloc[0:5,0]

# creating a seperate dataframe of top 5 restaurants
df_top5_restaurants = df[df['restaurant_name'].isin(top5_restaurant_names)]

# displaying top 5 restaurants
df['restaurant_name'].value_counts().iloc[0:5]


# In[26]:


df.restaurant_name.value_counts(1)*100


# In[ ]:


Cuisine Analysis


# In[36]:


# using barplot to display distribution of cuisine type
plt.figure(figsize=(15,10))
sns.countplot(data=df, y='cuisine_type', hue='day_of_the_week')
plt.xlabel('Order Count')
plt.ylabel('Cuisine Type')
plt.title('Orders per Cuisine Type by Day of the Week')
plt.grid(axis = 'x', color = 'green', linestyle = '--', linewidth = 0.5)
plt.show()


# In[34]:


sns.heatmap(df.corr(), annot=True)
plt.show()


# In[37]:


# checking order count per cuisine
df2 = df.groupby(['cuisine_type'])['order_id'].nunique().sort_values(ascending=False).reset_index()
df2.rename(columns={'order_id': 'order_count'}, inplace=True)

# checking barplot of order count vs cuisines
plt.figure(figsize=(10,5))
sns.barplot(data=df2, y='cuisine_type', x='order_count')
plt.xlabel('Number of Orders')
plt.ylabel('Cuisine Type')
plt.xticks(np.arange(0,650,50))
plt.title('Number of Orders per Cuisine Type')
plt.grid(axis = 'x', linestyle = '--', linewidth = 0.5)
plt.show()

df2.head()

