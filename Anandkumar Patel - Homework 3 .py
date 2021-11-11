#!/usr/bin/env python
# coding: utf-8

# # Homework 3
# 
# 
# Name: Anandkumar Patel
# 
# Date: 10/8/2021
# 
# UMID: 6417 7534

#GSI Comments

##Q1: -2 for not actually using the exists function


# #### Question 0 - RECS and Replicates Weights 
# 
# 
# ###### Data Files
# 
# 
# recs data 2009 = https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public.csv
# 
# recs data 2009 weights = https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public_repweights.csv
# 
# recs data 2015 = https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv
# 
# 2009 codebook = https://www.eia.gov/consumption/residential/data/2009/xls/recs2009_public_codebook.xlsx
# 
# 2015 codebook = https://www.eia.gov/consumption/residential/data/2015/xls/codebook_publicv4.xlsx
# 
# using rep weights = https://www.eia.gov/consumption/residential/data/2015/pdf/microdata_v3.pdf

# ###### Variables
# 
# 
# * DOEID (id)
# * NWEIGHT (weights)
# * HDD65 (heating days)
# * CDD65 (cooling days)
# * REGIONC

# ###### Weights and Replicate Weights
# 
# Using Replicate Weights = https://www.eia.gov/consumption/residential/data/2015/pdf/microdata_v3.pdf
# 
# $ \hat{V}(\tilde{\theta})  = \frac{1}{R(1 - \epsilon)^2} \sum_{r = 1}^{R} (\hat{\theta_r} - \hat{\theta})$
# 
# * $\theta$ = population parameter of interest
# * $\hat{\theta}$ = estimate for the full sample 
# * $\hat{\theta_r}$ = estimate for the r-th subsample replicate
# * $\epsilon$ = Fayes coefficient
#     * $0 < \epsilon < 1$ 
#     * For this data, $\epsilon = 0.5$ 
# * R = Number of Replicates
# 
# $ SE = \sqrt{\hat{V}} $
# 

# #### Question 1 - Data Preperation

# *Loading Packages*

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as stat
import math
from os.path import exists
from scipy.stats import norm


# *Setting Up Files*

# *Reading In 2009 Data* 

# In[2]:


rec_data_2009_url = 'https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public.csv'


# In[3]:


recs_2009_data = pd.read_csv(rec_data_2009_url)


# In[4]:


rec_2009_data_mini = pd.DataFrame(
    recs_2009_data[[
        'DOEID', 
        'REGIONC', 
        'HDD65', 
        'CDD65', 
        'NWEIGHT' ]]).copy()


# In[5]:


rec_2009_data_mini = rec_2009_data_mini.astype(
    {'DOEID' : 'int64',
     'REGIONC' : 'category',
     'HDD65' : 'int64',
     'CDD65' : 'int64',
     'NWEIGHT': 'float'})


# In[6]:


rec_2009_data_mini['RegionName'] = pd.Categorical(
    rec_2009_data_mini['REGIONC'].replace(
        {1: 'Northeast Census Region',
         2: 'Midwest Census Region',
         3: 'South Census Region',
         4: 'West Census Region',
       }))


# In[7]:


rec_2009_data_mini = pd.DataFrame(rec_2009_data_mini)


# In[8]:


rec_2009_data_mini.to_csv('local_rec_2009_data_final.csv')


# In[9]:


def local_data(data_file, url, columns_needed):
    file_exists = exists(data_file)
    if file_exists == True:
        data = pd.read_csv(data_file)
        
    else:
        data = pd.read_csv(url)
        data = data[columns_needed]
    return data


# In[10]:


# local_data('local_rec_2009_data_final.csv',
#           rec_data_2009_url,
#           ['DOEID', 'REGIONC', 'HDD65', 'CDD65', 'NWEIGHT' ])


# *Reading in 2015 Data* 

# In[11]:


rec_data_2015_url = 'https://www.eia.gov/consumption/residential/data/2015/csv/recs2015_public_v4.csv'


# In[12]:


recs_2015_data = pd.read_csv(rec_data_2015_url)


# In[13]:


recs_2015_data_mini= recs_2015_data.filter(
    regex = r'(DOEID|REGIONC|HDD65|CDD65|NWEIGHT|BRRWT.)').copy()


# In[14]:


recs_2015_data_mini.drop(
    columns=recs_2015_data_mini.columns[-1], 
    axis=1, 
    inplace=True)


# In[15]:


recs_2015_data_cleaned = recs_2015_data_mini.drop(
    recs_2015_data_mini.iloc[:, 3:99], axis = 1).reset_index()


# In[16]:


recs_2015_data_cleaned = recs_2015_data_cleaned.sort_values('DOEID')


# In[17]:


recs_2015_data_cleaned = recs_2015_data_cleaned.astype(
    {'DOEID' : 'int64',
     'REGIONC' : 'category',
     'HDD65' : 'int64',
     'CDD65' : 'int64',
     'NWEIGHT': 'float'}
)


# In[18]:


recs_2015_data_cleaned['RegionName'] = pd.Categorical(
    recs_2015_data_cleaned['REGIONC'].replace(
        {1: 'Northeast Census Region',
         2: 'Midwest Census Region',
         3: 'South Census Region',
         4: 'West Census Region',
       }))


# In[19]:


recs_2015_data_cleaned.to_csv('local_rec_2015_data_final.csv')


# In[20]:


def local_data(data_file, url, columns_needed):
    file_exists = exists(data_file)
    if file_exists == True:
        data = pd.read_csv(data_file)
        
    else:
        data = pd.read_csv(url)
        data = data[columns_needed]
    return data

# In[21]:


file_exists('local_rec_2015_data_final.csv',
            rec_data_2009_url,
            regex = r'(DOEID|REGIONC|HDD65|CDD65|NWEIGHT|BRRWT.)')


# **Part B - Replicate Weights**

# *2009 Replicate Weights*

# In[22]:


replicate_2009_url = 'https://www.eia.gov/consumption/residential/data/2009/csv/recs2009_public_repweights.csv'


# In[23]:


recs_2009_replicate_weights = pd.read_csv(
    replicate_2009_url)


# In[24]:


recs_2009_replicate_weights = recs_2009_replicate_weights.drop(
['NWEIGHT'],
axis = 1)


# In[25]:


long_rep_weights_2009 = pd.melt(
    recs_2009_replicate_weights,
    id_vars = ['DOEID'],
    var_name = 'rep'
).reset_index()


# In[26]:


long_rep_weights_2009.to_csv('long_weights_2009.csv')


# *2015 Replicate Weights*

# In[27]:


rep_ids = pd.DataFrame(
    recs_2015_data_mini.iloc[:, 0]
    .copy())


# In[28]:


rep_weights_2015 = recs_2015_data_mini.iloc[:, 3: 99].copy()


# In[29]:


rep_weights_2015 = pd.DataFrame(
    rep_ids.join(
        rep_weights_2015))


# In[30]:


long_rep_weights = pd.wide_to_long(
    rep_weights_2015, 
    stubnames = ['BRRWT'],
    i = 'DOEID',
    j = 'rep')


# In[31]:


long_rep_weights= pd.DataFrame(
    long_rep_weights).reset_index()


# In[32]:


long_rep_weights_2015 = long_rep_weights.sort_values('DOEID')


# In[33]:


long_rep_weights_2015.to_csv('long_rep_weights_2015.csv')


# In[34]:


# long_weights_2015 = 'long_rep_weights_2015.csv'

# if exists(long_weights_2015)==True:
#     pd.read_csv(long_weights_2015)
# else:
#     pd.read_csv(replicate_2009_url)


# #### Construct and Report the Estimates

# **Point Estimates for 2009**

# In[35]:


rec_2009_data_mini['HeatedWeights'] = (
    rec_2009_data_mini.HDD65 * rec_2009_data_mini.NWEIGHT
)

rec_2009_data_mini['CoolWeights'] = (
    rec_2009_data_mini.CDD65 * rec_2009_data_mini.NWEIGHT
)


# In[36]:


rec_2009_sum = (rec_2009_data_mini
                .groupby('REGIONC')
                .agg('sum'))

rec_2009_sum['Weight_Avg_Heat_2009'] = (
    rec_2009_sum.HeatedWeights / rec_2009_sum.NWEIGHT
)

rec_2009_sum['Weight_Avg_Cool_2009'] = (
    rec_2009_sum.CoolWeights / rec_2009_sum.NWEIGHT
)


avg_temp_2009 = rec_2009_sum.iloc[:,-2:].reset_index()


# **Constructing the CI** 

# In[37]:


rec_full_data_w_weights = pd.merge(rec_2009_data_mini,
                                   long_rep_weights_2009,
                                   how = 'left', 
                                   on = ['DOEID'])


rec_full_data_w_weights['multi_rep_heat'] = (
    rec_full_data_w_weights.HDD65 * rec_full_data_w_weights.value)

rec_full_data_w_weights['multi_rep_cool'] = (
    rec_full_data_w_weights.CDD65  * rec_full_data_w_weights.value)


# In[38]:


rec_full_data_w_weights_sum = (rec_full_data_w_weights[
    ['REGIONC',
     'rep',
     'multi_rep_heat',
     'multi_rep_cool',
     'value']]
    .groupby(['REGIONC', 'rep'])
    .agg('sum')
    .reset_index())

rec_full_data_w_weights_sum['Weight_Avg_Heat_replicates'] = (
    rec_full_data_w_weights_sum.multi_rep_heat \
    / rec_full_data_w_weights_sum.value)

rec_full_data_w_weights_sum['Weight_Avg_Cool_replicates'] = (
    rec_full_data_w_weights_sum.multi_rep_cool \
    / rec_full_data_w_weights_sum.value)


# In[39]:


avg_temp_2009_replicates = rec_full_data_w_weights_sum[
    ['REGIONC',
     'Weight_Avg_Heat_replicates',
     'Weight_Avg_Cool_replicates']
]


# In[40]:


epsilon = 0.5


# In[41]:


replicates_and_avg_2009 = pd.merge(
    avg_temp_2009, 
    avg_temp_2009_replicates,
    how="left",
    on=['REGIONC']
)


# In[42]:


replicates_and_avg_2009['square_diff_heat'] = (
    (replicates_and_avg_2009.Weight_Avg_Heat_2009 - \
     replicates_and_avg_2009.Weight_Avg_Heat_replicates)**2)
replicates_and_avg_2009['square_diff_cool'] = (
    (replicates_and_avg_2009.Weight_Avg_Cool_2009 - \
     replicates_and_avg_2009.Weight_Avg_Cool_replicates)**2)


# In[43]:


mean_sq_diff_ht = pd.DataFrame(
    (replicates_and_avg_2009
     .groupby('REGIONC')['square_diff_heat']
     .mean()).reset_index())

mean_sq_diff_co = pd.DataFrame(
    replicates_and_avg_2009
    .groupby('REGIONC')['square_diff_cool']
    .mean()).reset_index()


mean_sq_diff_ht['se_heat'] = np.sqrt(
    (mean_sq_diff_ht['square_diff_heat'] / 
     ((1 - epsilon)**2)))

mean_sq_diff_co['se_cool'] = np.sqrt(
    (mean_sq_diff_co['square_diff_cool'] / 
     ((1 - epsilon)**2)))


se_table_2009 = pd.merge(
    mean_sq_diff_ht,
    mean_sq_diff_co,
    how = 'left',
    on = 'REGIONC')


# In[44]:


final_data_2009 = pd.merge(avg_temp_2009,
                          se_table_2009,
                          how = 'left',
                          on = 'REGIONC')


# In[45]:


final_data_2009_clean = final_data_2009[
    ['REGIONC',
     'Weight_Avg_Heat_2009',
     'Weight_Avg_Cool_2009',
     'se_heat',
     'se_cool']].copy()


# In[46]:


crit = norm.ppf(.975)


# In[47]:


final_data_2009_clean['lower_heat'] = (
    final_data_2009_clean.Weight_Avg_Heat_2009 -\
    crit * final_data_2009_clean.se_heat
)


final_data_2009_clean['upper_heat'] = (
    final_data_2009_clean.Weight_Avg_Heat_2009 +\
    crit * final_data_2009_clean.se_heat
)


final_data_2009_clean['lower_cool'] = (
    final_data_2009_clean.Weight_Avg_Cool_2009 -\
    crit * final_data_2009_clean.se_cool
)


final_data_2009_clean['upper_cool'] = (
    final_data_2009_clean.Weight_Avg_Cool_2009 +\
    crit * final_data_2009_clean.se_cool
)


# In[48]:


final_report_2009 = final_data_2009_clean[['REGIONC',
                                          'Weight_Avg_Heat_2009',
                                          'lower_heat',
                                          'upper_heat',
                                          'Weight_Avg_Cool_2009',
                                          'lower_cool',
                                          'upper_cool']].rename(
    columns = {'REGIONC':'census region',
               'Weight_Avg_Heat_2009' : 'average heating days 2009',
               'lower_heat': 'lower bound heating days 2009',
               'upper_heat': 'upper bound heating days 2009',
               'Weight_Avg_Cool_2009': 'average cooling days 2009',
               'lower_cool': 'lower bound cooling days 2009',
               'upper_cool': 'upper bound cooling days 2009'})


# In[49]:


final_report_2009['census reg names'] = pd.Categorical(
    final_report_2009['census region'].replace(
        {1: 'Northeast Census Region',
         2: 'Midwest Census Region',
         3: 'South Census Region',
         4: 'West Census Region',
       }))


# In[50]:


final_report_2009 = final_report_2009.round(2)


# In[51]:


final_table = final_report_2009.copy()


# In[52]:


final_table['heat bounds'] = (
    final_table['lower bound heating days 2009'].
    astype(str) + ' - ' + final_table['upper bound heating days 2009']
    .astype(str))


final_table['cold bounds'] = (
    final_table['lower bound cooling days 2009']
    .astype(str) + ' - ' + final_table['upper bound cooling days 2009']
    .astype(str))


# In[53]:


final_table = final_table.drop(
   columns = ['lower bound heating days 2009',
     'upper bound heating days 2009',
     'lower bound cooling days 2009',
     'upper bound cooling days 2009'])


# In[54]:


final_table = final_table[['census reg names',
                          'average heating days 2009',
                          'heat bounds',
                          'average cooling days 2009',
                          'cold bounds']]


# In[55]:


from IPython.core.display import display, HTML
display(HTML(final_table.to_html(index=False)))


# **Point Estimates for the 2015 Data**

# In[56]:


recs_2015_data_cleaned['HeatedWeights'] = (
    recs_2015_data_cleaned.HDD65 * recs_2015_data_cleaned.NWEIGHT
)

recs_2015_data_cleaned['CoolWeights'] = (
    recs_2015_data_cleaned.CDD65 * recs_2015_data_cleaned.NWEIGHT
)


# In[57]:


rec_2015_sum = (recs_2015_data_cleaned.
                groupby('REGIONC').
                agg('sum'))

rec_2015_sum['Weight_Avg_Heat_2015'] = (
    rec_2015_sum.HeatedWeights \
    / rec_2015_sum.NWEIGHT)

rec_2015_sum['Weight_Avg_Cool_2015'] = (
    rec_2015_sum.CoolWeights \
    / rec_2015_sum.NWEIGHT)


# In[58]:


avg_temp_2015 = rec_2015_sum.iloc[:,-2:].reset_index()


# In[59]:


temp_data_needed = recs_2015_data_cleaned[
    ['DOEID',
     'REGIONC',
     'HDD65',
     'CDD65',
     'HeatedWeights',
     'CoolWeights']]


# In[60]:


rec_full_data_w_weights_2015 = pd.merge(
    temp_data_needed,
    long_rep_weights_2015,
    how = 'left', 
    on = ['DOEID'])


# In[61]:


rec_full_data_w_weights_2015['multi_rep_heat'] = (
    rec_full_data_w_weights_2015.HDD65 \
    * rec_full_data_w_weights_2015.BRRWT)

rec_full_data_w_weights_2015['multi_rep_cool'] = (
    rec_full_data_w_weights_2015.CDD65  \
    * rec_full_data_w_weights_2015.BRRWT)


# In[62]:


rec_full_data_w_weights_sum_2015 = (rec_full_data_w_weights_2015
                                    .groupby(
                                        ['REGIONC', 'rep'])
                                    .agg('sum')).reset_index()


# In[63]:


rec_full_data_w_weights_sum_2015['Weight_Avg_Heat_replicates_2015'] = (
    rec_full_data_w_weights_sum_2015.multi_rep_heat \
    / rec_full_data_w_weights_sum_2015.BRRWT)

rec_full_data_w_weights_sum_2015['Weight_Avg_Cool_replicates_2015'] = (
    rec_full_data_w_weights_sum_2015.multi_rep_cool \
    / rec_full_data_w_weights_sum_2015.BRRWT)


# In[64]:


avg_temp_2015_replicates = rec_full_data_w_weights_sum_2015[
    ['REGIONC',
     'Weight_Avg_Heat_replicates_2015',
     'Weight_Avg_Cool_replicates_2015']].reset_index()


# In[65]:


replicates_and_avg_2015 = pd.merge(
    avg_temp_2015, 
    avg_temp_2015_replicates,
    how="left",
    on=['REGIONC'])


# In[66]:


replicates_and_avg_2015['square_diff_heat_2015'] = (
    (replicates_and_avg_2015.Weight_Avg_Heat_2015 - \
     replicates_and_avg_2015.Weight_Avg_Heat_replicates_2015)**2)
replicates_and_avg_2015['square_diff_cool_2015'] = (
    (replicates_and_avg_2015.Weight_Avg_Cool_2015 - \
     replicates_and_avg_2015.Weight_Avg_Cool_replicates_2015)**2)


# In[67]:


mean_sq_diff_ht_2015 = pd.DataFrame(
    replicates_and_avg_2015
    .groupby('REGIONC')['square_diff_heat_2015']
    .mean()).reset_index()

mean_sq_diff_co_2015 = pd.DataFrame(
    replicates_and_avg_2015
    .groupby('REGIONC')['square_diff_cool_2015']
    .mean()).reset_index()


mean_sq_diff_ht_2015['se_heat_2015'] = np.sqrt(
    (mean_sq_diff_ht_2015['square_diff_heat_2015'] / 
     ((1 - epsilon)**2)))

mean_sq_diff_co_2015['se_cool_2015'] = np.sqrt(
    (mean_sq_diff_co_2015['square_diff_cool_2015'] / 
     ((1 - epsilon)**2)))



se_table_2015 = pd.merge(
    mean_sq_diff_ht_2015,
    mean_sq_diff_co_2015,
    how = 'left',
    on = 'REGIONC')


# In[68]:


final_data_2015 = pd.merge(avg_temp_2015,
                          se_table_2015,
                          how = 'left',
                          on = 'REGIONC')


# In[69]:


final_data_2015_clean = final_data_2015[
    ['REGIONC',
     'Weight_Avg_Heat_2015',
     'Weight_Avg_Cool_2015',
     'se_heat_2015',
     'se_cool_2015']].copy()


# In[70]:


final_data_2015_clean['lower_heat_2015'] = (
    final_data_2015_clean.Weight_Avg_Heat_2015 -\
    crit * final_data_2015_clean.se_heat_2015)

final_data_2015_clean['upper_heat_2015'] = (
    final_data_2015_clean.Weight_Avg_Heat_2015 +\
    crit * final_data_2015_clean.se_heat_2015)

final_data_2015_clean['lower_cool_2015'] = (
    final_data_2015_clean.Weight_Avg_Cool_2015 -\
    crit * final_data_2015_clean.se_cool_2015)
                                       
final_data_2015_clean['upper_cool_2015'] = (
    final_data_2015_clean.Weight_Avg_Cool_2015 +\
    crit * final_data_2015_clean.se_cool_2015)


# In[71]:


final_report_2015 = final_data_2015_clean[
    ['REGIONC',
     'Weight_Avg_Heat_2015',
     'lower_heat_2015',
     'upper_heat_2015',
     'Weight_Avg_Cool_2015',
     'lower_cool_2015',
     'upper_cool_2015']].rename(
    columns = {
        'REGIONC':'census region',
        'Weight_Avg_Heat_2015' : 'average heating days 2015',
        'lower_heat_2015': 'lower bound heating days 2015',
        'upper_heat_2015': 'upper bound heating days 2015',
        'Weight_Avg_Cool_2015': 'average cooling days 2015',
        'lower_cool_2015': 'lower bound cooling days 2015',
        'upper_cool_2015': 'upper bound cooling days 2015'})


# In[72]:


final_report_2015['census reg names'] = pd.Categorical(
    final_report_2015['census region'].replace(
         {1: 'Northeast Census Region',
         2: 'Midwest Census Region',
         3: 'South Census Region',
         4: 'West Census Region',
       }))


# In[73]:


final_report_2015 = final_report_2015.round(2)


# In[74]:


final_table_2015 = final_report_2015.copy()


# In[75]:


final_table_2015['heat bounds'] = (
    final_table_2015['lower bound heating days 2015']
    .astype(str) + ' - ' + final_table_2015['upper bound heating days 2015']
    .astype(str))


final_table_2015['cold bounds'] = (
    final_table_2015['lower bound cooling days 2015']
    .astype(str) + ' - ' + final_table_2015['upper bound cooling days 2015']
    .astype(str))


# In[76]:


final_table_2015 = final_table_2015.drop(
   columns = ['lower bound heating days 2015',
     'upper bound heating days 2015',
     'lower bound cooling days 2015',
     'upper bound cooling days 2015'])


# In[77]:


final_table_2015 = final_table_2015[['census reg names',
                          'average heating days 2015',
                          'heat bounds',
                          'average cooling days 2015',
                          'cold bounds']]


# In[78]:


display(HTML(final_table_2015.to_html(index=False)))


# **Part B**

# In[79]:


whole_data = pd.merge(final_data_2009_clean,
                     final_data_2015_clean,
                     how = 'left',
                     on = 'REGIONC')


# In[80]:


whole_data['temp_difference_heat'] = (whole_data.Weight_Avg_Heat_2015 -                                      whole_data.Weight_Avg_Heat_2009) 

whole_data['temp_difference_cool'] = (whole_data.Weight_Avg_Cool_2015 -                                      whole_data.Weight_Avg_Cool_2009) 

whole_data['joint_se_heat'] = np.sqrt(((whole_data.se_heat ** 2) +                                (whole_data.se_heat_2015 ** 2)))

whole_data['joint_se_cool'] = np.sqrt(((whole_data.se_cool ** 2) +                                (whole_data.se_cool_2015 ** 2)))


# In[81]:


difference_data = whole_data[[
    'REGIONC',
    'temp_difference_heat',
    'joint_se_heat',
    'temp_difference_cool',
    'joint_se_cool']].copy()


# In[82]:


difference_data['lower_diff_heat'] = (
    difference_data.temp_difference_heat -\
    crit * difference_data.joint_se_heat)

difference_data['upper_diff_heat'] = (
    difference_data.temp_difference_heat +\
    crit * difference_data.joint_se_heat)

difference_data['lower_diff_cool'] = (
    difference_data.temp_difference_cool-\
    crit * difference_data.joint_se_cool)

difference_data['upper_diff_cool'] = (
    difference_data.temp_difference_cool +\
    crit * difference_data.joint_se_cool)


# In[83]:


diff_ci = difference_data[['REGIONC',
                           'temp_difference_heat',
                           'lower_diff_heat',
                           'upper_diff_heat',
                           'temp_difference_cool',
                           'lower_diff_cool',
                           'upper_diff_cool']]


# In[84]:


final_difference_data = diff_ci[[
    'REGIONC',
    'temp_difference_heat',
    'lower_diff_heat',
    'upper_diff_heat',
    'temp_difference_cool',
    'lower_diff_cool',
    'upper_diff_cool']].rename(
    columns = {
        'REGIONC':'census region',
        'temp_difference_heat': 'average difference in heating days',
        'lower_diff_heat': 'lower bound of diff in heating days',
        'upper_diff_heat': 'upper bound of diff in heating days',
        'temp_difference_cool':'average difference in cooling days',
        'lower_diff_cool':'lower bound of diff in cooling days',
        'upper_diff_cool': 'upper bound of diff in cooling days'})


# In[85]:


final_difference_data = final_difference_data.round(2)


# In[86]:


final_difference_data['census reg names'] = pd.Categorical(
    final_difference_data['census region'].replace(
        {1: 'Northeast Census Region',
         2: 'Midwest Census Region',
         3: 'South Census Region',
         4: 'West Census Region',
       }))


# In[87]:


final_difference_table = final_difference_data.copy()


# In[88]:


final_difference_table['difference heating bounds'] = (
final_difference_table[
    'lower bound of diff in heating days']
    .astype(str) + ' - ' + final_difference_table[
        'upper bound of diff in heating days'].astype(str))

final_difference_table['difference cooling bounds'] = (
final_difference_table[
    'lower bound of diff in cooling days']
    .astype(str) + ' - ' + final_difference_table[
        'upper bound of diff in cooling days'].astype(str))


# In[89]:


final_difference_table = final_difference_table.drop(
    columns = [
        'lower bound of diff in heating days',
        'upper bound of diff in heating days',
        'lower bound of diff in cooling days',
        'upper bound of diff in cooling days',
    ])


# In[90]:


final_difference_table = final_difference_table[
    ['census region',
     'census reg names',
     'average difference in heating days',
     'difference heating bounds',
     'average difference in cooling days',
     'difference cooling bounds'
    
]]


# In[91]:


display(HTML(final_difference_table.to_html(index=False)))


# #### Question 3 - Graphical Representations

# In[92]:


fig1, ax1 = plt.subplots(nrows=1, ncols=1)

_ = plt.errorbar(
    x = final_difference_data['average difference in heating days'],
    y = final_difference_data['census reg names'],
    xerr = (final_difference_data['average difference in heating days'] \
            - final_difference_data['lower bound of diff in heating days']),
    marker = 'o',
    ls = 'none',
    capsize = 6,
    ecolor = 'red'
)


_ = ax1.set_xlabel('Mean and 95% CI (F units)')
_ = ax1.set_title('Average Difference in Heating Days (2015 - 2009)')

fig1.set_size_inches(15.5, 8.5)


# *Figure 1 - Average Difference in Heating Days (2015 - 2009)*
# 
# From the above graph, we can see that the difference in heating days is signifcantly different between the years of 2015 and 2009 for all regions except for the Northeast Census Region. This is evident by looking at the intervals. If the number of heating days between both year are approximatley the same, one should expect the interval to be centered around 0. However, in the plot above, we see that only the Northeast Census region has an interval around 0. This indicated that the there was a significant difference in the number of heating days between 2015 and 2009. 
# 
# 

# In[93]:


fig2, ax2 = plt.subplots(nrows=1, ncols=1)
_ = plt.errorbar(
    x = final_difference_data['average difference in cooling days'],
    y = final_difference_data['census reg names'],
    xerr = (final_difference_data['average difference in cooling days']\
            - final_difference_data['lower bound of diff in cooling days']),
    marker = 'x',
    ls = 'none',
    capsize = 6,
    ecolor = 'orange'
)
_ = ax2.set_xlabel('Mean and 95% CI (F units)')
_ = ax2.set_title('Average Difference in Cooling Days (2015 - 2009)')

fig2.set_size_inches(15.5, 8.5)


# *Figure 2 - Average Difference in Cooling Days (2015 - 2009)*
# 
# From the above graph, we can see that the difference in cool days is signifcantly different between the years of 2015 and 2009 for all regions. This is evident by looking at the intervals. If the number of coolings days between both year are approximatley the same, one should expect the interval to be centered around 0. However, in the plot above, we see that only the Northeast Census region has an interval around 0. This indicated that the there was a significant difference in the number of heating days between 2015 and 2009. 

# In[94]:


fig3, ax3 = plt.subplots(nrows=1, ncols=1)
_ = plt.errorbar(
    x = final_report_2015['average heating days 2015'],
    y = final_report_2015['census reg names'],
    xerr = (final_report_2015['average heating days 2015'] \
            - final_report_2015['lower bound heating days 2015']),
    marker = 'o',
    ls = 'none',
    capsize = 6,
    ecolor = 'red'
)
_ = ax3.set_xlabel('Mean and 95% CI (F units)')
_ = ax3.set_title('Average Heating Days (2015)')

fig3.set_size_inches(15.5, 8.5)


# *Figure 3 - Average Number of Heating Day 2015*
# 
# The above graph shows the average number of heating days for each region followed by a 95% confidence interval. We can see that the Northeast and the Midwest have the highest number of heating days(as expected). On the contrary, the south had the least number of heating days. 
# 

# In[95]:


fig4, ax4 = plt.subplots(nrows=1, ncols=1)
_ = plt.errorbar(
    x = final_report_2015['average cooling days 2015'],
    y = final_report_2015['census reg names'],
    xerr = (final_report_2015['average cooling days 2015']
            - final_report_2015['lower bound cooling days 2015']),
    marker = 'x',
    ls = 'none',
    capsize = 6,
    ecolor = 'orange'
)
_ = ax4.set_xlabel('Mean and 95% CI (F units)')
_ = ax4.set_title('Average Cooling Days (2015)')

fig4.set_size_inches(15.5, 8.5)


# *Figure 4 - Average Number of Cooling Day 2015*
# 
# The above graph shows the average number of cooling days for each region followed by a 95% confidence interval. We can see that the Northeast and the Midwest have the least number of heating days(as expected). On the contrary, the south had the least number of cooling days. 
# 

# In[96]:


fig6, ax6 = plt.subplots(nrows=1, ncols=1)
_ = plt.errorbar(
    x = final_report_2009['average heating days 2009'],
    y = final_report_2009['census reg names'],
    xerr = (final_report_2009['average heating days 2009'] \
            - final_report_2009['lower bound heating days 2009']),
    marker = 'o',
    ls = 'none',
    capsize = 6,
    ecolor = 'red'
)
_ = ax6.set_xlabel('Mean and 95% CI (F units)')
_ = ax6.set_title('Average Heating Days (2009)')

fig6.set_size_inches(15.5, 8.5)


# *Figure 5 - Average Number of Heating Day 2015*
# 
# The above graph shows the average number of heating days for each region followed by a 95% confidence interval. We can see that the Northeast and the Midwest have the highest number of heating days(as expected). On the contrary, the south had the least number of heating days. 

# In[97]:


fig5, ax5 = plt.subplots(nrows=1, ncols=1)
_ = plt.errorbar(
    x = final_report_2009['average cooling days 2009'],
    y = final_report_2009['census reg names'],
    xerr = (final_report_2009['average cooling days 2009'] \
            - final_report_2009['lower bound cooling days 2009']),
    marker = 'x',
    ls = 'none',
    capsize = 6,
    ecolor = 'orange'
)
_ = ax5.set_xlabel('Mean and 95% CI (F units)')
_ = ax5.set_title('Average Cooling Days (2009)')

fig5.set_size_inches(15.5, 8.5)


# *Figure 6 - Average Number of Cooling Day 2015*
# 
# The above graph shows the average number of cooling days for each region followed by a 95% confidence interval. We can see that the Northeast and the Midwest have the least number of heating days(as expected). On the contrary, the south had the least number of cooling days. 
# 

# In[98]:


fig8, axes = plt.subplots(nrows=2, ncols=1, sharex= True)

_ = axes[0].errorbar(
    x = final_report_2009['average heating days 2009'],
    y = final_report_2009['census reg names'],
    xerr = (final_report_2009['average heating days 2009'] \
            - final_report_2009['lower bound heating days 2009']),
    marker = 'o',
    ls = 'none',
    capsize = 6,
    ecolor = 'red'
)
_ = axes[0].set_xlabel('Mean and 95% CI (F units)')
_ = axes[0].set_title('Average Heating Days (2009)')

_ = axes[1].errorbar(
    x = final_report_2015['average heating days 2015'],
    y = final_report_2015['census reg names'],
    xerr = (final_report_2015['average heating days 2015'] \
            - final_report_2015['lower bound heating days 2015']),
    marker = 'x',
    ls = 'none',
    capsize = 6,
    ecolor = 'green'
)
_ = axes[1].set_xlabel('Mean and 95% CI (F units)')
_ = axes[1].set_title('Average Heating Days 2015')


fig8.set_size_inches(15.5, 8.5)


# *Figure 7 - Comparison of Heating Days for 2009 and 2015* 
# 
# From the above plots, we can see that the average number of heating days for all of the regions has decreased between 2009 and 2015. The south region seems to have the biggest change while the northeast region seems to have the smallest change. 

# In[99]:


fig9, axes = plt.subplots(nrows=2, ncols=1, sharex= True)

_ = axes[0].errorbar(
    x = final_report_2009['average cooling days 2009'],
    y = final_report_2009['census reg names'],
    xerr = (final_report_2009['average cooling days 2009'] \
            - final_report_2009['lower bound cooling days 2009']),
    marker = 'o',
    ls = 'none',
    capsize = 6,
    ecolor = 'red'
)
    
_ = axes[0].set_xlabel('Mean and 95% CI (F units)')
_ = axes[0].set_title('Average Cooling Days 2009')


_ = axes[1].errorbar(
    x = final_report_2015['average cooling days 2015'],
    y = final_report_2015['census reg names'],
    xerr = (final_report_2015['average cooling days 2015'] \
            - final_report_2015['lower bound cooling days 2015']),
    marker = 'x',
    ls = 'none',
    capsize = 6,
    ecolor = 'green'
)
_ = axes[1].set_xlabel('Mean and 95% CI (F units)')
_ = axes[1].set_title('Average Cooling Days 2015')

fig9.set_size_inches(15.5, 8.5)


# *Figure 8 - Comparison of Cooling Days for 2009 and 2015* 
# 
# From the above plots, we can see that the average number of cooling days for all of the regions has increased between 2009 and 2015. The south and midwest region seems to have the biggest change while the northeast region seems to have the smallest change. (Interesting to see this relationship with climate change). 

# In[100]:


fig7, axes = plt.subplots(nrows=2, ncols=1, sharex= True)

_ = axes[0].errorbar(
    x = final_difference_data['average difference in heating days'],
    y = final_difference_data['census reg names'],
    xerr = (final_difference_data['average difference in heating days']\
            -final_difference_data['lower bound of diff in heating days']),
    marker = 'o',
    ls = 'none',
    capsize = 6,
    ecolor = 'red'
)
_ = axes[0].set_xlabel('Mean and 95% CI (F units)')
_ = axes[0].set_title('Average Heating Difference Days (2015 - 2009)')

_ = axes[1].errorbar(
    x = final_difference_data['average difference in cooling days'],
    y = final_difference_data['census reg names'],
    xerr = (final_difference_data['average difference in cooling days']\
            - final_difference_data['lower bound of diff in cooling days']),
    marker = 'x',
    ls = 'none',
    capsize = 6,
    ecolor = 'green'
)
_ = axes[1].set_xlabel('Mean and 95% CI (F units)')
_ = axes[1].set_title('Average Cooling Difference Days (2015 - 2009)')

fig7.set_size_inches(15.5, 8.5)


# *Figure 9 - Comparison of Difference in Heating and Cooling Days for 2009 and 2015* 
# 
# From the above plot, we can see that that Northest region had the lowest difference in heating days between 2015 and 2009, while the Midwest had the most. On the contrary, the south had the greatest difference in cooling days between 2009 and 2015. Again, it would be interesting to see the relationship between these values and climate change. 
