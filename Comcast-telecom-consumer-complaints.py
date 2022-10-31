#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


df_complaints=pd.read_csv('/home/labsuser/Assessment/Comcast_telecom_complaints_data.csv')


# In[3]:


df_complaints.head()


# In[4]:


df_complaints["date_index"] = df_complaints["Date_month_year"] + " " + df_complaints["Time"]
df_complaints["date_index"] = pd.to_datetime(df_complaints["date_index"])
df_complaints["Date_month_year"] = pd.to_datetime(df_complaints["Date_month_year"])
df_complaints = df_complaints.set_index(df_complaints["date_index"])


# ### Trend Chart - Number of complaints at monthly granularity levels ###

# In[5]:


df_complaints.groupby(pd.Grouper(freq="M")).size().plot()


# ### Trend Chart - Number of complaints at daily granularity levels ###

# In[6]:


df_complaints['Day of Month'] = pd.to_datetime(df_complaints["Date"])
df_complaints = df_complaints.set_index(df_complaints["Day of Month"])
df_complaints.groupby(pd.Grouper(freq="D")).size().plot()


# ### Table of complaint types and frequency ###

# In[7]:


df_type = df_complaints['Customer Complaint'].str.upper().value_counts()
df_type


# ##### Complaints are maximum around Comcast, Comcast Data Cap, Comcast Internet, Comcast billing #####

# ### Create a new categorical variables with values "Open" and "Closed" ###

# Open & Pending is to be categorized as Open and Closed & Solved is to be categorized as Closed. 

# In[8]:


def new_status(value):
    if value=="Open" or value=="Pending":
        return "Open"
    else:
        return "Closed"
df_complaints['New_Status']=df_complaints['Status'].apply(new_status)


# In[28]:


df_status = df_complaints.groupby('State')['New_Status'].value_counts().unstack()


# #### State-wise complaint data ####

# In[26]:


df_status


# In[11]:


df_status['Open'].fillna(value=0,inplace=True)


# ##### State-wise status of complaints in a stacked bar chart #####

# In[12]:


plt.figure(figsize=(200,100))
plt.rcParams['figure.dpi']=200
df_status.plot(kind='bar', stacked=True)


# Georgia has maximum number of complaints

# #### Unresolved complaints distribution across states ####

# In[13]:


df_unresolved = df_complaints[df_complaints['New_Status']=='Open']
df_unresolved=df_unresolved['State'].value_counts()
df_unresolved


# In[14]:


df_unresolved.head().plot(kind='pie', autopct='%1.1f%%', explode=(0.05,0,0,0,0))
plt.axis('equal')
plt.title('Unresolved Complaints across States')
plt.show()


# Georgia has the maximum number of unresolved complaints

# #### Percentage of complaints resolved till date, which were received through the Internet and customer care calls ####

# In[15]:


df_received=df_complaints[df_complaints['Received Via'].isin(['Internet','Customer Care Call'])]


# In[16]:


df_received.head()


# In[17]:


df_received['New_Status'].value_counts()


# In[18]:


df_received['New_Status'].value_counts().plot(kind='pie', autopct='%1.1f%%', explode=(0.05,0))
plt.title('Percentage of resolved complaints received via Internet and Customer Care Call')
plt.axis('equal')
plt.show()


# In[19]:


df_received[df_received['New_Status']=='Closed']['New_Status'].value_counts()


# In[ ]:




