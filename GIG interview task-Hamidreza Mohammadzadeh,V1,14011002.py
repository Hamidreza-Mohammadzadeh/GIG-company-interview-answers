#!/usr/bin/env python
# coding: utf-8

# ## Answer question1:

# In[60]:


import pandas as pd
data = pd.read_csv(r"G:\Job interviews\Iran\GIG\Digital transformation\sample_data.csv")
data = data.fillna(0)
date = pd.read_excel(r"G:\Job interviews\Iran\GIG\Digital transformation\Full_DimDate_PB.xlsx", sheet_name='DATES')
My_date= date[['Miladi4','JWeekDay']]
data2 = data.groupby('date')['order_id'].count().reset_index()
data3= data2.copy()
data3 = data3.merge(My_date, how='left', left_on='date', right_on = 'Miladi4')
Answer1 = data3.groupby('JWeekDay')['order_id'].agg({'mean','std'}).reset_index()
Answer1['Row_num'] = [7,3,4,1,6,5,2]
Ans = pd.DataFrame(Answer1.sort_values(by='Row_num'))
#Ans.columns = ['روزهفته','انحراف معیار تقاضای روزانه','میانگین تقاضای روزانه','ترتیب']
Ans = Ans.iloc[:,0:3]
Ans.columns = ['WeekDay','Average demand', 'Std demand']
Ans


# ## Answer question2:

# In[ ]:


db=data3.copy()
maping={
    'شنبه':'WorkingDays',
    'یکشنبه':'WorkingDays',
    'دوشنبه':'WorkingDays',
    'سه شنبه':'WorkingDays',
    'چهارشنبه':'WorkingDays',
    'پنج شنبه':'Weekend',
    'جمعه':'Weekend',
}
db['DayType'] = db['JWeekDay'].map(maping)

import seaborn as sns
My_hist = sns.histplot(data=db, x=db['order_id'], hue='DayType')


# ## Answer question3:

# In[61]:


df = data.copy()
# convert date column to Data type in order to calculate the last date of purchase:
df['date'] = pd.to_datetime(df['date']).dt.date
last_date = df.date.max()
rfm = df.groupby('user_id').agg({'date': lambda date: (last_date - date.max()).days,
                                     'order_id': lambda order_id: order_id.nunique(),
                                     'total_purchase': lambda total_purchase: total_purchase.sum()})
# rename columns:
rfm.columns = ['recency', 'frequency', 'monetary']

# RFM part:
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

sc = MinMaxScaler((0, 1))
df = sc.fit_transform(rfm[['recency','frequency','monetary']])
a = input("Insert your number of clusters:")
kmeans = KMeans(n_clusters= int(a), init= 'k-means++', max_iter= 1000)
# 'max_iter':It is given in order to avoid an endless loop.
# 'k-means++' parameter selects initial cluster centers for k-mean clustering in a smart way to speed up convergence
kmeans.fit(df)
clusters = pd.DataFrame(kmeans.labels_)
Final = rfm.groupby(kmeans.labels_)['recency','frequency','monetary'].mean()
Final.columns = ['Ave.R','Ave.F','Ave.M']
print(pd.DataFrame(Final))

x=rfm['frequency']
y=rfm['recency']
plt.scatter(x, y, c=kmeans.labels_)


# # Thanks for your attention,
# #### Sincerely, Hamidreza Mohammadzadeh
