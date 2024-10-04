#!/usr/bin/env python
# coding: utf-8

# # Test Rule Based Classification Problem

# In[28]:


import pandas as pd
import numpy as np 

pd.set_option('display.max_colwidth', None)  # or 199
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_columns', None)

df = pd.read_csv("New Headphone Production Survey Complete.csv")


# In[29]:


df["Htype"] = df["HpAnswer"].copy()
df.shape


# In[30]:


agg_df = df.groupby(["Gender","Status","Age","Education","Occupation","Htype"])[["HpAnswer"]].count()
agg_df.shape


# In[31]:


agg_df = agg_df.reset_index()
agg_df = agg_df.sort_values(by=["Htype"])
agg_df.head(10)


# In[32]:


agg_df["customers_level_based"] = [f"{i[0]}|{i[1]}|{i[2]}|{i[3]}|{i[4]}" for i in agg_df.values]
#agg_df= agg_df.loc[:,["customers_level_based","HpAnswer"]].groupby("customers_level_based").agg({"HpAnswer": "sum"}).sort_values(by="HpAnswer", ascending=False).reset_index()
agg_df.shape # Just checking data again


# In[33]:


#agg_df[(agg_df.HpAnswer == agg_df.HpAnswer.max()) and (agg_df.Htype.equal("v1"))]
a = agg_df.loc[(agg_df["Htype"]=="v1")]
a = a[["customers_level_based","Htype","HpAnswer"]][(a.HpAnswer == a.HpAnswer.max())]
b = agg_df.loc[(agg_df["Htype"]=="v2")]
b = b[["customers_level_based","Htype","HpAnswer"]][(b.HpAnswer == b.HpAnswer.max())]
c = agg_df.loc[(agg_df["Htype"]=="v3")]
c = c[["customers_level_based","Htype","HpAnswer"]][(c.HpAnswer == c.HpAnswer.max())]

lst_max = a.append(b, ignore_index = True)
lst_max = lst_max.append(c, ignore_index = True)
lst_max


# In[34]:


#a = (lst_max['HpAnswer'].sum()*
maxv1= round((lst_max['HpAnswer'].loc[lst_max['Htype']=="v1"])/lst_max['HpAnswer'].sum()*100,2)
maxv2= round((lst_max['HpAnswer'].loc[lst_max['Htype']=="v2"])/lst_max['HpAnswer'].sum()*100,2)
maxv3= round((lst_max['HpAnswer'].loc[lst_max['Htype']=="v3"])/lst_max['HpAnswer'].sum()*100,2)
#print("Hp1:",lst_max['customers_level_based'].loc[lst_max['Htype']=="v1"].values,float(maxv1))
#print("Hp2:",lst_max['customers_level_based'].loc[lst_max['Htype']=="v2"].values,float(maxv2))
#print("Hp3:",lst_max['customers_level_based'].loc[lst_max['Htype']=="v3"].values,float(maxv3))
maxv1[0]


# In[35]:


bt = agg_df.groupby(["customers_level_based","Htype"])[["HpAnswer"]].sum()
bt


# In[36]:


bt.shape


# In[37]:


b = agg_df.groupby(["customers_level_based"])[["Htype"]].nunique().reset_index()
b


# In[38]:


b = b.loc[b['Htype']==1]
b.reset_index(drop =True)


# In[39]:


b["customers_level_based"].shape[0]


# In[40]:


segment =agg_df[["customers_level_based","Htype","HpAnswer"]].loc[agg_df['customers_level_based'].isin(b["customers_level_based"])]
segment = segment.sort_values(by=["Htype"])
segment = segment.reset_index(drop=True)
segment


# In[41]:


segment.shape[0]


# In[42]:


def segment_cus():
    a1 = str(lst_max['customers_level_based'].loc[lst_max['Htype']=="v1"].values).replace('|', '')
    a2 =str(lst_max['customers_level_based'].loc[lst_max['Htype']=="v2"].values).replace('|', '')
    a3 =str(lst_max['customers_level_based'].loc[lst_max['Htype']=="v3"].values).replace('|', '')
    a = f'Highest segmentations: Hp1 {maxv1[0]}%-{a1} Hp2 {maxv1[0]}%-{a2} Hp3-{maxv1[0]}%-{a3}'
     
    return a,segment

c = segment_cus()
c[0]


# In[43]:


new_user = "Male _Single _36-45 _Undergraduate _Employee"
d =segment["Htype"].loc[segment['customers_level_based'].str.strip()==new_user]

print(d.values)


# In[44]:


c1 = segment.loc[segment['customers_level_based'].str.contains("Undergraduate _Employee")] 
c1


# In[45]:


#c = round(c['Htype'].value_counts(normalize=True)*100,2)
p1 =  round(c1['Htype'].value_counts(normalize=True)*100,2).rename_axis('Htype').reset_index(name='Pros')
p1


# In[46]:


p1.Pros.max()


# In[47]:


g = segment.loc[segment['customers_level_based'].str.contains("_36-45 _Other education_Business Owner")] 
g


# In[48]:


c2 = c1.append(g, ignore_index=True)
c2


# In[49]:


p2 =  round(c2['Htype'].value_counts(normalize=True)*100,2).rename_axis('Htype').reset_index(name='Pros')
p2

