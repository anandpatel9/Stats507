#!/usr/bin/env python
# coding: utf-8

# ### STATS 507 - Homework 1 
# 
# ##### Name: Anandkumar Patel
# ##### Date: 09 - 17 - 2021
# ##### UMID: 6417 7534

# In[85]:

#### Submission Comments

#Q0: -3 for not provide both raw and formatted versions.# 

#I have added the raw version to this script# 



import math
import pandas as pd
import timeit
import time
import tabulate
import IPython
import statistics as stat
import scipy.stats as st 
import numpy as np


# This is *question 0* for
# <a href="https://jbhender.github.io/Stats507/F21/ps/ps1.html">*problem set 1*</a> of 
# <a href="https://jbhender.github.io/Stats507/F21/">Stats 507</a>. 
# 
# # | Question 0 is about markdown
# 
# The next question is about the **Fibonacci sequence**, $F_n = F_{n - 2} + F_{n-1}$. In part **a** we will define a python function ```fib_rec()```. 
# 
# Below is a...
# 
# ### Level 3 Header
# 
# Next, we can make a bulleted list:
# - Item 1 <br>
#     -  detail 1
#     -  detail 2 <br>
# - Item 2
# 
# <br> Finally, we can make an enumerated list:
# 
# 1. Item 1 
# 2. Item 2 
# 3. Item 3
# 
# # *Raw Version*

## ```
# This is *question 0* for
# <a href="https://jbhender.github.io/Stats507/F21/ps/ps1.html">*problem set 1*</a> of 
# <a href="https://jbhender.github.io/Stats507/F21/">Stats 507</a>. 
# 
# # | Question 0 is about markdown
# 
# The next question is about the **Fibonacci sequence**, $F_n = F_{n - 2} + F_{n-1}$. In part **a** we will define a python function ```fib_rec()```. 
# 
# Below is a...
# 
# ### Level 3 Header
# 
# Next, we can make a bulleted list:
# - Item 1 <br>
#     -  detail 1
#     -  detail 2 <br>
# - Item 2
# 
# <br> Finally, we can make an enumerated list:
# 
# 1. Item 1 
# 2. Item 2 
# 3. Item 3
# 
# 
# ```
# 

# **Question 1 - Fibonacci Sequence**
# <br>
# 
# **Part A - Recursive Fibonacci Sequence**

# In[86]:


def fib_rec(n):
    """
    Recursively find values of Fibonacci Sequence. 

    Parameters
    ----------
    n : integer
        Index of Fibonacci Sequence.
        Returns TypeError if not an int

     Returns
     -------
     Specific Fibonacci value based on 
     user input index. 
    
    """
    
    if not isinstance(n,int):
        raise TypeError
    else:
        if n < 0:
            print('Please enter a positive integer')
        elif n in [0, 1]:
            return n
        else: 
            fib_value = fib_rec(n-1) + fib_rec(n-2)
            return fib_value
    
print(fib_rec(7))
print(fib_rec(11))
print(fib_rec(13))


# **Part B - Fibbonaci For Loop**

# In[87]:


def fib_for(n):
    """
    Find specific values of Fibonacci Sequence
    using a for loop. 

    Parameters
    ----------
    n : integer
        Index of Fibbonaci Sequence.
        Returns TypeError if not an int

     Returns
     -------
     Specific Fibonacci value based on 
     user input index. 
    
    """
    if not isinstance(n, int):
        raise TypeError
    (fib_0,fib_1) = (0,1)
    for i in range(0, n+1):
        if i <= 1:
            next_term = 1
        else:
            next_term = fib_0 + fib_1
            (fib_0,fib_1) = (fib_1, next_term)      
    return next_term

            
print(fib_for(7))
print(fib_for(11))
print(fib_for(13))


# **Part C - Fibonnaci Using a While Loop** 

# In[88]:


def fib_whl(n):
    """
    Find specific values of Fibonacci Sequence
    using a while loop. 

    Parameters
    ----------
    n : integer
        Index of Fibonacci Sequence.
        Returns TypeError if not an int

     Returns
     -------
     Specific Fibonacci value based on 
     user input index. 
    
    """
    (first_term, second_term) = (0,1)
    if not isinstance(n, int):
        raise TypeError
    else: 
        count = 0
        if n < 0:
            print('Enter a positive integer: ')
        elif n in [0,1]:
            return 1
        else:
            while count <= n - 2:
                new_term = first_term + second_term
                (first_term, second_term) = (second_term, new_term)
                count += 1
            return new_term
            

print(fib_whl(7))
print(fib_whl(11))
print(fib_whl(13))
            


# **Part D - Rounding Method**

# In[89]:


def fib_rnd(n):
    """
    Find specific values of Fibonacci Sequence
    using a rounding method. 

    Parameters
    ----------
    n : integer
        Index of Fibbonaci Sequence.
        Returns TypeError if not an int

     Returns
     -------
     Specific Fibonacci value based on 
     user input index. 
    
    """
    golden_ratio = (1 + math.sqrt(5)) / 2 
    fib = ((golden_ratio)**n) / math.sqrt(5)
    return int(round(fib,0))
    
print(fib_rnd(7))
print(fib_rnd(11))
print(fib_rnd(13))


# **Part E - Truncation Method**

# In[90]:


def fib_flr(n):
    """
    Find specific values of Fibonacci Sequence
    using a floor method. 

    Parameters
    ----------
    n : integer
        Index of Fibbonaci Sequence.
        Returns TypeError if not an int

    Returns
     -------
     Specific Fibonacci value based on 
     user input index. 
    
    """
    golden_ratio = (1 + math.sqrt(5)) / 2 
    fib_flr = math.floor(((golden_ratio**n)/math.sqrt(5)) + 0.5)
    return fib_flr

print(fib_flr(7))
print(fib_flr(11))
print(fib_flr(13))


# **Part F - Computational Time**

# In[91]:


def timing(n, func):
    """
    Times how long a function takes
    to run 50 times/trials. 

    Parameters
    ----------
    n : integer
        Value to put in to function.
    Returns TypeError if not an int
    
    func: function
        Function you want to time. 

    Returns
     -------
     The median time for 50 runs of 
     one function with a specified n. 
    
    """
    if not isinstance(n, int):
        raise TypeError
    else:
        temp = list()
        for i in range(50):
            start = time.time()
            func(n)
            end = time.time()
            total_time = end - start
            temp.append(total_time)
        median_time = stat.median(temp)
        return median_time


# In[92]:


def totalmed(function):
    """
    Runs through multiple values of 
    n as inputs for functions. 
    
    Then each function is timed. 

    Parameters
    ----------
    
    func: function
        Function you want to time. 

    Returns
     -------
     The median time for 50 runs of 
     one function for each specified value
     of n. 
    
    """
    temp_list = list()
    for i in range(0,30,5):
        results = timing(i, function)
        temp_list.append(results)
    return temp_list

        
fib_flr_med = totalmed(fib_flr)   
fib_rnd_med = totalmed(fib_rnd)
fib_for_med = totalmed(fib_for)
fib_whl_med = totalmed(fib_whl)
fib_rec_med = totalmed(fib_rec)


timing_data = {'n': range(0,30,5),
                'Fibbonaci Floor Method': fib_flr_med,
                'Fibbonaci Rounding Method': fib_rnd_med,
                'Fibbonacci For Loop': fib_for_med,
                'Fibonacci While Loop': fib_whl_med,
                'Fibonacci Recursive Method': fib_rec_med}

timing_df = pd.DataFrame(timing_data)


# In[93]:


print(timing_df.to_markdown())


# In[94]:


from IPython.core.display import display, HTML, Markdown
display(HTML(timing_df.to_html(index=False)))


# *Table 1 - Shows the median computational time for 50 trials using different values of n*
# 
# From the above table, one can deduce that the slowest method is the recursive Fibonacci. 
# The fastest methods were the floor and rounding methods, each having similar times. 
# 
# One should note that the while loop is faster than the for loop. 
# 
# 

# **Question 2 - Pascals Triangle**
# <br>
# 
# **Part a - Pascal Function**

# In[95]:


def pascal_triangle(n):
    """
    Finds a specific row of Pascal's Triangle
    

    Parameters
    ----------
    
    n: integer
        The row of Pascal the user wants. 
    Returns TypeError if not an int

    Returns
     -------
     A string of the specific row of Pascal's Triangle
    
    """    
    if not isinstance(n, int):
        raise TypeError
    else:
        results = ''
        for i in range(0, n+1):
            combination = int(
                math.factorial(n)/(math.factorial(i)*math.factorial(n-i))
            )
            results += (str(combination) + ' ')
        return results
        
pascal_triangle(6)        


# **Part b - Pretty Pascal**

# In[96]:


def pretty_pascal(n):
    """
    Produces a nicely printed Pascal Triangle
    for a specified number of rows. 
    

    Parameters
    ----------
    
    n: integer
        The number of rows in Pascal's Triangle
        the user wants. 

    Returns
     -------
     n rows of Pascal's Triangle (centered).
    
    """        
    empty = list()
    for i in range(n+1):
        temp = pascal_triangle(i)
        empty.append(temp)
    width = len(empty[-1])
    for i in empty:
        width_2 = len(i)
        diff = width - width_2
        placement = int(diff/2)
        print(' ' * placement + i)
        
pretty_pascal(10)


# ##### Question 3 - Statistical 101

# *Part A*

# In[97]:


def zint(data, confidence):
    """
    Finds confidence interval for a 
    specified data set and confidence level. 
    

    Parameters
    ----------
    
    data: vector/list/array
        Raw data that the user wants to find
        the interval for
    confidence: float 
        Percentage confidence level the user wants.
        Float must be number between 0 and 1. 
    Output: String
        User must specify how they would like 
        the output to look. 
        Default: None

    Returns
     -------
     Dictionary of z interval.
    
    """       
    data = np.asarray(data)
    percent = confidence * 100
    z_crit = abs(st.norm.ppf((1-confidence)/2))   
    se = np.std(data) / math.sqrt(len(data))
    mean = np.mean(data)
    lwr, upr = round(mean - (z_crit * se),2), round(mean + (z_crit * se),2)
    d = {'est': round(mean, 2), 'lower': lwr, 'upper': upr, 'level': percent}
    return d
   


# In[98]:


def user_format(data, 
                confidence, 
                output = "{est: .4f}[{level}% ({lower}, {upper})]"
               ):
    """
    Gives a user specified format of 
    a confidence interval. 
    

    Parameters
    ----------
    
    data: vector/list/array
        Raw data that the user wants to find
        the interval for. 
        Needs to be coercible to a 1D Array. 
    confidence: float 
        Percentage confidence level the user wants.
        Float must be number between 0 and 1. 
    Output: String
        Default: None
        User must specify how they would like 
        the output to look. 
        User can input: 'dict' or 'string'
        otherwise, error will be thrown. 

    Returns
     -------
     User specified format of Z interval.
    
    """
    temp = zint(data, confidence)
    if output == None:
        return temp
    else:
        return output.format_map(temp)
        


# *Part B*

# *Part i*

# In[99]:


def binom_normal(data, confidence):
    """
    Returns normal binomial interval 
    

    Parameters
    ----------
    
    data: vector/list/array
        Raw data that the user wants to find
        the interval for. 
        Needs to be coercible to a 1D Array.
    confidence: float 
        Percentage confidence level the user wants.
        Float must be number between 0 and 1. 
    Method: String
        Default: normal
        A normal approximation is used 
        for calculation

    Returns
     -------
     Dictionary of interval from normal approximation.
    
    """     
    z_crit = abs(st.norm.ppf((1-confidence)/2))
    percent = confidence * 100
    mean_norm = np.mean(data)
    q_norm = 1-mean_norm
    n = len(data)
    temp_1 = n*mean_norm
    temp_2 = n*(1-mean_norm)
    temp_3 = min(temp_1, temp_2)
    if temp_3 <= 12:
        print('Conditions not met for normal approximation for binomial')
    else:
        lower = (mean_norm - (z_crit * math.sqrt((mean_norm*q_norm)/n)))
        lower = round(lower, 3)
        upper = (mean_norm + (z_crit * math.sqrt((mean_norm*q_norm)/n)))
        upper = round(upper, 3)
        d = {'est': round(mean_norm, 2), 'lower': lower, 
             'upper': upper, 'level': percent}
        return d


# *Part ii*

# In[100]:


def binom_clooper(data, confidence):
    """
    Returns clooper binomial interval 
    

    Parameters
    ----------
    
    data: vector/list/array
        Raw data that the user wants to find
        the interval for. 
        Needs to be coercible to a 1D Array.
    confidence: float 
        Percentage confidence level the user wants.
        Float must be number between 0 and 1. 
    Method: String
        Default: clooper
        A clooper approximation is used 
        for calculation

    Returns
     -------
     Dictionary of interval from clooper approximation.
    
    """     
    n = len(data)
    x = sum(data)
    percent = confidence * 100
    avg = np.mean(data)
    lower = round(
        st.beta.ppf(
            (1-confidence)/ 2 ,
            x,
            n - x + 1),
        3)
    upper = round(
        st.beta.ppf(
            1-((1-confidence)/ 2) , 
            x + 1,
            n - x), 3)
    temp = {'est': avg, 'level': percent,
            'lower' : lower,
            'upper': upper 
           }
    return temp


# *Part iii*

# In[101]:


def binom_jeff(data, confidence):
    """
    Returns jeffrey binomial interval 
    

    Parameters
    ----------
    
    data: vector/list/array
        Raw data that the user wants to find
        the interval for. 
        Needs to be coercible to a 1D Array.
    confidence: float 
        Percentage confidence level the user wants.
        Float must be number between 0 and 1. 
    Method: String
        Default: jeffrey
        A normal approximation is used 
        for calculation

    Returns
     -------
     Dictionary of interval from jeffrey approximation.
    
    """     

    n = len(data)
    x = sum(data)
    percent = confidence * 100
    avg = np.mean(data)
    lower = round(st.beta.ppf(
    (1-confidence)/2, 
        x + 0.5, 
        n - x + 0.5),3)
    upper = round(st.beta.ppf(
    1-((1-confidence)/2), 
        x + 0.5, 
        n - x + 0.5),3)
    final_lower = max(lower, 0)
    final_upper = min(upper, 1)
    temp_2 = {'est': avg, 'level': percent,
            'lower' : final_lower,
            'upper': final_upper 
           }
    return temp_2


# *Part iv*

# In[102]:


def binom_agresti(data, confidence):
    """
    Creates agresti binomial interval 
    

    Parameters
    ----------
    
    data: vector/list/array
        Raw data that the user wants to find
        the interval for. 
        Needs to be coercible to a 1D Array.
    confidence: float 
        Percentage confidence level the user wants.
        Float must be number between 0 and 1. 
    Method: String
        Default: agresti
        A agresti approximation is used 
        for calculation

    Returns
     -------
     Dictionary of interval from agresti approximation.
    
    """     
    z_crit = abs(st.norm.ppf((1-confidence)/2))
    percent = confidence * 100
    n_tilda = len(data) + z_crit**2
    p_tilda = (sum(data) + (z_crit **2/2)) / n_tilda
    q_tilda = 1 - p_tilda
    lower = p_tilda - math.sqrt(p_tilda * q_tilda / n_tilda)
    lower = round(lower, 3)
    upper = p_tilda + math.sqrt(p_tilda * q_tilda / n_tilda)
    upper = round(upper, 3)
    temp_3 = {
        'est': round(p_tilda, 3), 
        'level': percent,
        'lower' : lower,
        'upper': upper 
    }
    return temp_3


# In[103]:


def binom_confint(data, confidence, method = None, output = "{est: .4f}[{level}% ({lower}, {upper})]"):
    """
    Gives a confidence interval for binomial data
    given a user inputed method. 
    

    Parameters
    ----------
    
    data: vector/list/array
        Raw data that the user wants to find
        the interval for. 
    confidence: float 
        Percentage confidence level the user wants.
        Float must be number between 0 and 1. 
    Method: String
        Default: Nonr
        Users can input one of the following: 
        normal
        clooper
        jeffrey
        agresti

    Returns
     -------
     Dictionary of interval approximation from the user specified
     method using binomial data.
    
    """        
    data = np.asarray(data)
    if np.ndim(data) != 1:
        raise ValueError
    else:
        temp = method(data, confidence)
        if output == None: 
            return temp
        else: 
            return output.format_map(temp)


# *Part C*

# In[104]:


f = [0] * 48
s= [1] * 42

test_data = f + s 
test_data = np.asarray(test_data)

end = dict()
for i in [0.9, 0.95,0.99]:
    temp_list = list()
    a = binom_normal(test_data, i)
    a_lwr = str(a['lower'])
    a_upr = str(a['upper'])
    normal_int = '(' + a_lwr + ' , ' + a_upr + ')'
    b = binom_clooper(test_data, i)
    b_lwr = str(b['lower'])
    b_upr = str(b['upper'])
    clooper_int = '(' + b_lwr + ' , ' + b_upr + ')'
    c = binom_jeff(test_data, i)
    c_lwr = str(c['lower'])
    c_upr = str(c['upper'])
    jeff_int = '(' + c_lwr + ' , ' + c_upr + ')'
    d = binom_agresti(test_data, i)
    d_lwr = str(d['lower'])
    d_upr = str(d['upper'])
    agresti_int = '(' + d_lwr + ' , ' + d_upr + ')'
    temp_list.append(normal_int)
    temp_list.append(clooper_int)
    temp_list.append(jeff_int)
    temp_list.append(agresti_int)
    end[str(i)] = temp_list
    

method = ['Normal', 'Clooper', 'Jeffrey', 'Agresti-Coull']
results = pd.DataFrame(data = end, index = method)
display(HTML(results.to_html(index=True)))


# *Table 2 - Confidence Interval's for Different Methods and Confidence Levels on the same data*
# 
# The above table shows the confidence intervals for different methods using binomial data. One should note how the intervals grow in size as confidence level grows. Additionally, the Agresti model is the most liberal, as the range of calues is the smallest. Finally, the Normal approximation is the most conservative. 
