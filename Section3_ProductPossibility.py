#!/usr/bin/env python
# coding: utf-8

# # <img src="https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/machine-learning-python-intro.jpg">
# 
# # Section 3: Predicted the possibility of bying product
# 
#  Using multiple linear regression in Python by both sklearn and statsmodels.

# In[118]:


import pandas as pd

def create_sumdata():
        data = pd.read_csv("New Headphone Production Survey Complete.csv")
        summale_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Gender'].str.strip()=="Male")].shape[0]
        sumfemale_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Gender'].str.strip()=="Female")].shape[0]
        sumsingle_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Status'].str.strip()=="Single")].shape[0]
        summarried_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Status'].str.strip()=="Married")].shape[0]
        suma1_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Age'].str.strip()=="20-27")].shape[0]
        suma2_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Age'].str.strip()=="28-35")].shape[0]
        suma3_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Age'].str.strip()=="36-45")].shape[0]
        sume1_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Education'].str.strip()=="Graduate")].shape[0]
        sume2_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Education'].str.strip()=="Undergraduate")].shape[0]
        sume3_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Education'].str.strip()=="High School")].shape[0]
        sume4_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Education'].str.strip()=="Other")].shape[0]
        sumo1_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Occupation'].str.strip()=="Student")].shape[0]
        sumo2_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Occupation'].str.strip()=="Employee")].shape[0]
        sumo3_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Occupation'].str.strip()=="Business Owner")].shape[0]
        sumo4_h1 = data.loc[(data['HpAnswer']=="v1") & (data['Occupation'].str.strip()=="Other")].shape[0]
        all_h1 = data.loc[(data['HpAnswer']=="v1")].shape[0]

        summale_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Gender'].str.strip()=="Male")].shape[0]
        sumfemale_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Gender'].str.strip()=="Female")].shape[0]
        sumsingle_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Status'].str.strip()=="Single")].shape[0]
        summarried_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Status'].str.strip()=="Married")].shape[0]
        suma1_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Age'].str.strip()=="20-27")].shape[0]
        suma2_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Age'].str.strip()=="28-35")].shape[0]
        suma3_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Age'].str.strip()=="36-45")].shape[0]
        sume1_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Education'].str.strip()=="Graduate")].shape[0]
        sume2_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Education'].str.strip()=="Undergraduate")].shape[0]
        sume3_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Education'].str.strip()=="High School")].shape[0]
        sume4_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Education'].str.strip()=="Other")].shape[0]
        sumo1_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Occupation'].str.strip()=="Student")].shape[0]
        sumo2_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Occupation'].str.strip()=="Employee")].shape[0]
        sumo3_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Occupation'].str.strip()=="Business Owner")].shape[0]
        sumo4_h2 = data.loc[(data['HpAnswer']=="v2") & (data['Occupation'].str.strip()=="Other")].shape[0]
        all_h2 = data.loc[(data['HpAnswer']=="v2")].shape[0]

        summale_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Gender'].str.strip()=="Male")].shape[0]
        sumfemale_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Gender'].str.strip()=="Female")].shape[0]
        sumsingle_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Status'].str.strip()=="Single")].shape[0]
        summarried_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Status'].str.strip()=="Married")].shape[0]
        suma1_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Age'].str.strip()=="20-27")].shape[0]
        suma2_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Age'].str.strip()=="28-35")].shape[0]
        suma3_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Age'].str.strip()=="36-45")].shape[0]
        sume1_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Education'].str.strip()=="Graduate")].shape[0]
        sume2_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Education'].str.strip()=="Undergraduate")].shape[0]
        sume3_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Education'].str.strip()=="High School")].shape[0]
        sume4_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Education'].str.strip()=="Other")].shape[0]
        sumo1_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Occupation'].str.strip()=="Student")].shape[0]
        sumo2_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Occupation'].str.strip()=="Employee")].shape[0]
        sumo3_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Occupation'].str.strip()=="Business Owner")].shape[0]
        sumo4_h3 = data.loc[(data['HpAnswer']=="v3") & (data['Occupation'].str.strip()=="Other")].shape[0]
        all_h3 = data.loc[(data['HpAnswer']=="v3")].shape[0]
        #print(type(all_h3))
        all_responds = all_h1+all_h2+all_h3
        count_allcharacters =({
                                "Survey_distribution":["R&Dteam","R&Dteam","R&Dteam"],
                                "HP Types":[1,2,3],
                                "C_Male":[summale_h1,summale_h2,summale_h3],
                                "C_Female":[sumfemale_h1,sumfemale_h2,sumfemale_h3],
                                "C_Single":[sumsingle_h1,sumsingle_h2,sumsingle_h3],
                                "C_Married":[summarried_h1,summarried_h2,summarried_h3],
                                "C_A1":[suma1_h1,suma1_h2,suma1_h3],
                                "C_A2":[suma2_h1,suma2_h2,suma2_h3],
                                "C_A3":[suma3_h1,suma3_h2,suma3_h3],
                                "C_E1":[sume1_h1,sume1_h2,sume1_h3],
                                "C_E2":[sume2_h1,sume2_h2,sume2_h3],
                                "C_E3":[sume3_h1,sume3_h2,sume3_h3],
                                "C_E4":[sume4_h1,sume4_h2,sume4_h3],
                                "C_O1":[sumo1_h1,sumo1_h2,sumo1_h3],
                                "C_O2":[sumo2_h1,sumo2_h2,sumo2_h3],
                                "C_O3":[sumo3_h1,sumo3_h2,sumo3_h3],
                                "C_O4":[sumo4_h1,sumo4_h2,sumo4_h3],
                                "Respondents":[all_h1,all_h2,all_h3],
                                "Buying possibility constant":[int((all_h1/all_responds)*100),int((all_h2/all_responds)*100),int((all_h3/all_responds)*100)]                        
                            })
        pdata = pd.read_csv("Total responses categorized characteristic_database.csv")
        ndata = pd.DataFrame(count_allcharacters)
        pdata = pdata.append(ndata, ignore_index=True)
        
        return pdata


# In[119]:


from sklearn import linear_model

def predict_ppdemand(XC,field1,field2,field3,field4,field5):
    sdata = create_sumdata()
    X0 = sdata[[field1,field2,field3,field4,field5]]
    Y0 = sdata['Respondents']
    X1 = sdata[[field1,field2,field3,field4,field5]].loc[sdata['HP Types']==1]
    Y1 = sdata['Respondents'].loc[sdata['HP Types']==1]
    X2 = sdata[[field1,field2,field3,field4,field5]].loc[sdata['HP Types']==2]
    Y2 = sdata['Respondents'].loc[sdata['HP Types']==2]
    X3 = sdata[[field1,field2,field3,field4,field5]].loc[sdata['HP Types']==3]
    Y3 = sdata['Respondents'].loc[sdata['HP Types']==3]
    regr0 = linear_model.LinearRegression()
    regr0.fit(X0, Y0)
    sp0 = regr0.predict([XC])
    
    regr1 = linear_model.LinearRegression()
    regr1.fit(X1, Y1)
    sp1 = regr1.predict([XC])
    
    regr2 = linear_model.LinearRegression()
    regr2.fit(X2, Y2)
    sp2 = regr2.predict([XC])
    
    regr3 = linear_model.LinearRegression()
    regr3.fit(X3, Y3)
    sp3 = regr3.predict([XC])
    
    #print('Intercept: \n', regr.intercept_)
    #print('Coefficients: \n', regr.coef_)
    print ('Predicted all: \n', sp0)
    print ('Predicted Type 1: \n', sp1)
    print ('Predicted Type 2: \n', sp2)
    print ('Predicted Type 3: \n', sp3)
    return sp0[0],sp1[0],sp2[0],sp3[0]


# In[120]:


#h1test = [50,60,50,10,10]
#predict_ppdemand(h1test,"C_Female","C_Single","C_A3","C_E3","C_O3")


# In[121]:


# XC = [10,19,20,9,10,\
#        15,4,9,8,10,2,5,6,7,11]
# XC = [2,2,3,1,1,\
#         3,0,2,2,0,0,0,4,0,0]
# XC = [4,15,11,8,1,\
#         14,4,7,8,3,1,0,15,1,3]
# XC = [3,3,4,2,0,\
#         5,1,2,3,1,0,0,3,1,2]
create_sumdata().to_csv(r'Total responses categorized characteristic survey.csv', index=False)
sdata = create_sumdata()


# In[122]:


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sdata = create_sumdata()
#a = sdata.loc[sdata['HP Types'].str.strip()=="v1"]
# sns.lmplot(x="C_Female", y="Respondents", data=sdata, scatter_kws={"s": 80});
# sns.lmplot(x="C_Male", y="Respondents", data=sdata, scatter_kws={"s": 80});

#plt.title('v1')

# b = sdata.loc[sdata['HP Types'].str.strip()=="v2"]
# sns.lmplot(x="C_Married", y="Respondents", data=b, scatter_kws={"s": 80});
# plt.title('v2')

# b = sdata.loc[sdata['HP Types'].str.strip()=="v2"]
# sns.lmplot(x="C_Single", y="Respondents", data=b, scatter_kws={"s": 80});
# plt.title('v2')

# c = sdata.loc[sdata['HP Types'].str.strip()=="v3"]
# sns.lmplot(x="C_Female", y="Buying possibility constant", data=c,ci=None, scatter_kws={"s": 80});
# plt.title('v3')
#sdata = create_sumdata()
#x1= sdata['C_Male']
#x2= sdata['C_Female']
#y = sdata['Respondents']
#plt.scatter(x1,y, color='blue')
#plt.scatter(x2,y, color='red')

# Generating the parameters of the best fit line
#m, c1 = np.polyfit(x1, y, 1)

# Plotting the straight line by using the generated parameters
#plt.plot(x1, m*x1+c1, label='Male')

# Generating the parameters of the best fit line
#m, c2 = np.polyfit(x2, y, 1)

# Plotting the straight line by using the generated parameters
#plt.plot(x2, m*x2+c2, label='Female')


#plt.title('Categorized by Gender', fontsize=14)
#plt.xlabel('Respondents', fontsize=14)
#plt.ylabel('Total', fontsize=14)
# plt.legend()
# plt.grid(True)
# plt.show()


# In[123]:



#sdata.describe().round(2).T


# In[124]:


#corrMatrix = sdata.corr()
#display(corrMatrix)


# In[ ]:




