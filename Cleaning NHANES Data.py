#!/usr/bin/env python
# coding: utf-8

# ## Stats 507 - HW 6

# #### Problem 1: Using Git

# In[ ]:


import pandas as pd


# In[ ]:


demo_data_2012 = pd.read_sas('Demo_G.XPT')
demo_data_2012['cohort'] = [2012 for i in range(demo_data_2012.shape[0])]

demo_data_2014 = pd.read_sas('Demo_H.XPT')
demo_data_2014['cohort'] = [2014 for i in range(demo_data_2014.shape[0])]

demo_data_2016 = pd.read_sas('Demo_I.XPT')
demo_data_2016['cohort'] = [2016 for i in range(demo_data_2016.shape[0])]

demo_data_2018 = pd.read_sas('Demo_J.XPT')
demo_data_2018['cohort'] = [2018 for i in range(demo_data_2018.shape[0])]


# In[ ]:


subset_data = pd.DataFrame()
for i in [demo_data_2012,
          demo_data_2014,
          demo_data_2016,
          demo_data_2018]:
    subset_data = subset_data.append(i)

deom_subset_data = subset_data[['cohort',
                                'SEQN',
                                'RIAGENDR',
                                'RIDAGEYR',
                                'RIDRETH3',
                                'DMDEDUC2',
                                'DMDMARTL',
                                'RIDSTATR',
                                'SDMVPSU',
                                'SDMVSTRA',
                                'WTMEC2YR',
                                'WTINT2YR']]

demographic_data = deom_subset_data.drop_duplicates(
    subset = 'SEQN').copy()

demographic_data = demographic_data.rename(
    {'SEQN':'ids',
     'RIDAGEYR': 'age',
     'RIAGENDR': 'gender',
     'RIDRETH3': 'race and ethnicity',
     'DMDEDUC2': 'education',
     'DMDMARTL': 'marital status',
     'RIDSTATR': 'examination status',
     'SDMVPSU': 'pseudo psu variance',
     'SDMVSTRA': 'pseudo stratum variance',
     'WTMEC2YR': 'full 2 year mec exam weight',
     'WTINT2YR' : 'full 2 year mec interview weight'},
    axis = 1)

demographic_data_2 = demographic_data.fillna(-1).copy()

demographic_data_2 = demographic_data_2.astype(
    {'age': 'int',
     'gender': 'category',
     'race and ethnicity': 'int',
     'marital status': 'int',
     'education': 'int',
     'age': 'int',
     'ids': 'int',
     'examination status':'int'
    })


# In[ ]:


demographic_data_2['education level'] = pd.Categorical(
    demographic_data_2['education'].replace(
        {1 : 'Less than 9th Grade',
         2: '9 - 11 Grade - No Diploma',
         3: 'High School Graduate/GED',
         4: 'Some College',
         5: 'College Graduate',
         7: 'Refused',
         9: 'Do not know',
         -1: 'Missing'}))
demographic_data_2['marital status 2'] = pd.Categorical(
    demographic_data_2['marital status'].replace(
        {1: 'Married',
         2: 'Widowed',
         3: 'Divorced',
         4: 'Separated',
         5: 'Never Married',
         6: 'Living with Partner',
         77: 'Refused',
         99: 'Do not know',
         -1 : 'Missing'}))
                                                  
demographic_data_2['race and ethnicity 2'] = pd.Categorical(
    demographic_data_2['race and ethnicity'].replace(
        {1: 'Mexican American',
         2: 'Other Hispanic',
         3: 'Non Hispanic White',
         4: 'Non Hispanic Black',
         6: 'Non Hispanic Asian',
         7: 'Other',
         -1: 'Missing'}))
demographic_data_2['examination status 2'] = pd.Categorical(
    demographic_data_2['examination status'].replace(
        {1: 'Interview Only',
         2: 'Interview and MEC',
         -1: 'Missing'}))


# In[ ]:


demographic_data_2.to_pickle('./cleaned_demo_data.pkl')


# *Part B*

# In[ ]:


oral_2012 = pd.read_sas('OHXDEN_G.XPT')
oral_2014 = pd.read_sas('OHXDEN_H.XPT')
oral_2016 = pd.read_sas('OHXDEN_I.XPT')
oral_2018 = pd.read_sas('OHXDEN_J.XPT')


# In[ ]:


c_2012 = pd.Series([2012 for i in range(oral_2012.shape[0])])

oral_2012_cohorts = pd.concat(
    (oral_2012, c_2012.rename('cohort')), axis = 1).copy()

c_2014 = pd.Series(
    [2014 for i in range(oral_2014.shape[0])])

oral_2014_cohorts = pd.concat(
    (oral_2014, c_2014.rename('cohort')), axis = 1).copy()

c_2016 = pd.Series(
    [2016 for i in range(oral_2016.shape[0])])

oral_2016_cohorts = pd.concat(
    (oral_2016, c_2016.rename('cohort')), axis = 1).copy()

c_2018 = pd.Series(
    [2018 for i in range(oral_2018.shape[0])])

oral_2018_cohorts = pd.concat(
    (oral_2018, c_2018.rename('cohort')), axis = 1).copy()


# In[ ]:


all_oral_data = pd.concat((oral_2012_cohorts,
                          oral_2014_cohorts,
                          oral_2016_cohorts,
                          oral_2018_cohorts))


# In[ ]:


oral_subsetted_data= all_oral_data.filter(
    regex = r'(SEQN|cohort|OHDDESTS|OHX.*TC)').rename(
    {'SEQN': 'ids',
     'OHDDESTS': 'dentation status code'},
    axis = 1).apply(
    lambda x: x.astype('category')).astype(
    {'ids': int}).copy()

col_names = dict()
tooth_keys = range(1,33)
for i in tooth_keys:
    if i < 10:
        col_names['OHX0' + str(i) +'TC'] = 'Tooth Count ' + str(i)
        col_names['OHX0' + str(i) + 'CTC'] = 'Coronal Count ' + str(i)
        col_names['OHX0' + str(i) + 'RTC'] = 'Coronal Second Restoration ' + str(i)
    else:
        col_names['OHX' + str(i) + 'TC'] = 'Tooth Count ' + str(i)
        col_names['OHX' + str(i) + 'CTC'] = 'Coronal Count ' + str(i)
        col_names['OHX' + str(i) + 'RTC'] = 'Coronal Second Restoration ' + str(i)
        
oral_subsetted_data = oral_subsetted_data.rename(columns = col_names)

oral_subsetted_data


# In[ ]:


oral_subsetted_data.to_pickle('./cleaned_oral_data.pkl')


# *Part C* 

# In[ ]:


merged_df = pd.merge(demographic_data_2,
                   oral_subsetted_data,
                   how='inner',
                   left_on='ids',
                   right_on='ids')
counts = {'Joint': merged_df.shape[0], 
          'Demographic Data': demographic_data_2.shape[0], 
          'Oral Data': oral_subsetted_data.shape[0]}

counts_df = pd.DataFrame(counts, index = ['Counts'])


from IPython.core.display import display, HTML, Markdown
display(HTML(counts_df.to_html(index=True)))


# In[ ]:


merged_df.to_pickle('./merged_df.pkl')


#Adding gender variable

demographic_data = pd.read_pickle('cleaned_demo_data.pkl')

demographic_data['gender'] = pd.Categorical(
    demographic_data['gender'].replace(
        {1.0 : 'female',
         2.0: 'male'}))
