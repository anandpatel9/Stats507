#!/usr/bin/env python
# coding: utf-8

# ## Pandas Topic ##
# 
# ### pd. query ##
# 
# ###### Name: Anandkumar Patel
# ###### Email: patelana@umich.edu
# ###### Unique ID: patelana

# ### Arguments and Output
# 
# **Arguments** 
# 
# * expression (expr) 
# * inplace (default = False) 
#     * Do you want to operate directly on the dataframe or create new one
# * kwargs (keyword arguments)
# 
# **Returns** 
# * Dataframe from provided query

# ## Why
# 
# * Similar to an SQL query 
# * Can help you filter data by querying
# * Returns a subset of the DataFrame
# * loc and iloc can be used to query either rows or columns

# ## Query Syntax
# 
# * yourdataframe.query(expression, inplace = True/False

# ## Code Example

# In[2]:


import pandas as pd
df = pd.DataFrame({'A': range(1, 6),
                   'B': range(10, 0, -2),
                   'C C': range(10, 5, -1)})
print(df)

print('Below is the results of the query')

print(df.query('A > B'))

