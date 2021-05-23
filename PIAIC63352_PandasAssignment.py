#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from glob import glob


# # **Part1**

# Inspect the Data!
# 1.
# The first visualization your boss wants you to make is a scatterplot that shows average income in a state vs proportion of women in that state.
# 
# Open some of the census csv files in the navigator. How are they named? What kind of information do they hold? Will they help us make this graph?
# 

# In[10]:


states1 = pd.read_csv('states1.csv')
states1


# 2.
# It will be easier to inspect this data once we have it in a DataFrame. You can’t even call .head() on these csvs! How are you supposed to read them?
# 
# Using glob, loop through the census files available and load them into DataFrames. Then, concatenate all of those DataFrames together into one DataFrame, called something like us_census.
# 

# In[11]:


data = glob('states*')
us_census = pd.concat((pd.read_csv(file) for file in data), ignore_index=True)


# 3.
# Look at the .columns and the .dtypes of the us_census DataFrame. Are those datatypes going to hinder you as you try to make histograms?

# In[12]:


us_census.columns


# In[13]:


us_census.dtypes


# 4.
# Look at the .head() of the DataFrame so that you can understand why some of these dtypes are objects instead of integers or floats.
# 
# Start to make a plan for how to convert these columns into the right types for manipulation.
# 

# In[14]:


us_census.head()


# 5.
# Use regex to turn the Income column into a format that is ready for conversion into a numerical type.
# 

# In[15]:


us_census["Income"] = us_census["Income"].str.replace("$","",regex = True)
us_census["Income"] = pd.to_numeric(us_census["Income"])


# In[16]:


us_census.dtypes


# 6.
# Look at the GenderPop column. We are going to want to separate this into two columns, the Men column, and the Women column.
# 
# Split the column into those two new columns using str.split and separating out those results.
# 

# In[17]:


us_census[["the Men","the Women"]] = us_census["GenderPop"].str.split("_",expand = True)


# In[18]:


us_census.head()


# 7.Convert both of the columns into numerical datatypes.
# 
# There is still an M or an F character in each entry! We should remove those before we convert.

# In[19]:


us_census["the Men"] = us_census["the Men"].str.replace("M","")
us_census["the Men"] = pd.to_numeric(us_census["the Men"])


# In[20]:


us_census["the Women"] = us_census["the Women"].str.replace("F","")
us_census["the Women"] = pd.to_numeric(us_census["the Women"])


# 8.
# Now you should have the columns you need to make the graph and make sure your boss does not slam a ruler angrily on your desk because you’ve wasted your whole day cleaning your data with no results to show!
# 
# Use matplotlib to make a scatterplot!
# 
# plt.scatter(the_women_column, the_income_column) 
# Remember to call plt.show() to see the graph!
# 

# In[21]:


plt.scatter(us_census["the Women"], us_census["Income"])
plt.show()


# 9.
# Did you get an error? These monstrous csv files probably have nan values in them! Print out your column with the number of women per state to see.
# 
# We can fill in those nans by using pandas’ .fillna() function.
# 
# You have the TotalPop per state, and you have the Men per state. As an estimate for the nan values in the Women column, you could use the TotalPop of that state minus the Men for that state.
# 
# Print out the Women column after filling the nan values to see if it worked!
# 

# In[22]:


us_census["the Women"] = us_census["the Women"].fillna(us_census["TotalPop"]-us_census["the Men"]).astype(int)


# 10.
# We forgot to check for duplicates! Use .duplicated() on your census DataFrame to see if we have duplicate rows in there.
# 

# In[23]:


us_census.duplicated()


# 11.
# Drop those duplicates using the .drop_duplicates() function.
# 

# In[24]:


us_census.drop_duplicates(inplace = True)


# 12.Make the scatterplot again. Now, it should be perfect! Your job is secure, for now.
# 
# 

# In[25]:


plt.scatter(us_census["the Women"], us_census["Income"])
plt.show()


# 13.
# Now, your boss wants you to make a bunch of histograms out of the race data that you have. Look at the .columns again to see what the race categories are.
# 

# In[26]:


us_census.columns


# 14.
# Try to make a histogram for each one!
# 
# You will have to get the columns into numerical format, and those percentage signs will have to go.
# 
# Don’t forget to fill the nan values with something that makes sense! You probably dropped the duplicate rows when making your last graph, but it couldn’t hurt to check for duplicates again.
# 
# 

# In[27]:


def remove_sign(Name):
  us_census[Name] = us_census[Name].str.replace("%","").astype(float)
remove_sign("Hispanic")
remove_sign("White")
remove_sign("Black")
remove_sign("Native")
remove_sign("Asian")            
remove_sign("Pacific")


# In[28]:


us_census.isnull().sum()


# In[29]:


def fill(Name):
  us_census[Name] = us_census[Name].fillna(us_census[Name].mean())
fill("Pacific")


# In[35]:


us_census.duplicated()


# In[30]:


x = ["Hispanic","White","Black","Native","Asian","Pacific"]
plt.hist(x,bins=10)


# # ***Part2***

# 1.
# Data for all of the locations of Petal Power is in the file inventory.csv. Load the data into a DataFrame called inventory.

# In[31]:


inventory = pd.read_csv("inventory.csv")


# 2.
# Inspect the first 10 rows of inventory.

# In[32]:


inventory.head(10)


# 3.
# The first 10 rows represent data from your Staten Island location. Select these rows and save them to staten_island.

# In[33]:


staten_island = inventory.iloc[:10,:]
staten_island


# 4.
# A customer just emailed you asking what products are sold at your Staten Island location. Select the column product_description from staten_island and save it to the variable product_request.

# In[34]:


product_request = staten_island["product_description"]
product_request


# 5.
# Another customer emails to ask what types of seeds are sold at the Brooklyn location.
# 
# Select all rows where location is equal to Brooklyn and product_type is equal to seeds and save them to the variable seed_request

# In[35]:


seed_request = inventory.loc[(inventory["location"] == "Brooklyn")& (inventory["product_type"] == "seeds")]
seed_request


# Inventory
# 6.
# Add a column to inventory called in_stock which is True if quantity is greater than 0 and False if quantity equals 0.

# In[36]:


a = lambda x: "True" if x>0 else "False"
inventory["in_stock"] = inventory.quantity.apply(a) 
inventory.head(10)


# 7.
# Petal Power wants to know how valuable their current inventory is.
# 
# Create a column called total_value that is equal to price multiplied by quantity.

# In[37]:


inventory["total_value"] = inventory["price"] * inventory["quantity"]
inventory.head()


# 8.
# The Marketing department wants a complete description of each product for their catalog.
# 
# The following lambda function combines product_type and product_description into a single string:
# 
# combine_lambda = lambda row: \
#     '{} - {}'.format(row.product_type,
#                      row.product_description)
# Paste this function into script.py.
# 

# In[38]:


combine_lambda = lambda row: '{} - {}'.format(row.product_type, row.product_description)


# 
# 9.
# Using combine_lambda, create a new column in inventory called full_description that has the complete description of each product.

# In[39]:


inventory["full_description"] = combine_lambda(inventory)


# In[40]:


inventory.head(10)

