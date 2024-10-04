#!/usr/bin/env python
# coding: utf-8

# # Test Survey with ML

# In[34]:


import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

pd.set_option('display.max_colwidth', None)  # or 199
np.set_printoptions(threshold=np.inf)
pd.set_option('display.max_columns', None)

df = pd.read_csv("New Headphone Production Survey for ML.csv")


# In[35]:


from dash import dcc

def feature_importance():
    df3 = pd.concat([df]*20, ignore_index=True)

    train_df,test_df = train_test_split(df3, test_size=0.3, random_state=42, shuffle=True)

    X_train = train_df.drop(labels=['Gender','Age','Status','Education','Occupation','HpAnswer'],axis=1)
    Y_train = train_df["HpAnswer"]
    X_test  = test_df.drop(labels=['Gender','Age','Status','Education','Occupation','HpAnswer'],axis=1)
    Y_test  = test_df["HpAnswer"]

    # X_train = train_df.drop("HpAnswer", axis=1)
    # Y_train = train_df["HpAnswer"]
    # X_test  = test_df.drop("HpAnswer", axis=1)
    # Y_test  = test_df["HpAnswer"]

    random_forest = RandomForestClassifier(n_estimators=100)
    random_forest.fit(X_train, Y_train)
    Y_prediction = random_forest.predict(X_test)
    Y3           = random_forest.predict_proba(X_test)

    random_forest.score(X_train, Y_train)
    acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
    #print(classification_report(Y_test, Y_prediction))
    #print(acc_random_forest)
    #print(Y_prediction,Y3)

    importances = pd.DataFrame({'feature':X_train.columns,'importance':np.round(random_forest.feature_importances_,3)})
    importances = importances.sort_values('importance',ascending=False).set_index('feature')
    #importances_cut = importances.loc[importances['feature']!=['Gender','Age','Status','Education','Occupation']]
    #importances_qicks = importances.drop(labels=['Gender','Age','Status','Education','Occupation'],axis=0)
    #importances_qicks = importances_qicks.sort_values(by=['importance'])
    importances

    return importances


# In[36]:


feature_importance()


# In[37]:


def predict_input(que1,que2,que3,que4,ans1,ans2,ans3,ans4):  
    X1=({que1: [ans1],
        que2: [ans2],
        que3: [ans3],
        que4: [ans4]})

    #X1 = ({'Gender':[0], 'Age': [2], 'Status':[0], 'Education':[1],'Occupation': [2]})
    
    dfs = pd.DataFrame(X1)
    
    return dfs


# In[38]:


def MLdecision_tree(xtest):
    X_train = train_df[xtest.columns.values]
    Y_train = train_df["HpAnswer"]
    random_forest = RandomForestClassifier(n_estimators=100)
    
    X_test  = test_df[xtest.columns.values]
    Y_test  = test_df["HpAnswer"]
    random_forest.fit(X_train, Y_train)
    Y_pred = random_forest.predict(X_test)
    Y3           = random_forest.predict_proba(X_test)
    
    Y_train = train_df["HpAnswer"]
    random_forest.fit(X_train, Y_train)  
    Y_pred_hp = random_forest.predict(xtest)  
    Y3           = random_forest.predict_proba(xtest)
    acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
    print("acc_random_forest_hp:",acc_random_forest)
    
    Y_train = train_df["Gender"]
    random_forest.fit(X_train, Y_train)  
    Y_pred_gender = random_forest.predict(xtest)  
    acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
    print("acc_random_forest_gender:",acc_random_forest)
    
    Y_train = train_df["Age"]
    random_forest.fit(X_train, Y_train)  
    Y_pred_age = random_forest.predict(xtest)  
    acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
    print("acc_random_forest_age:",acc_random_forest)
    
    Y_train = train_df["Status"]
    random_forest.fit(X_train, Y_train)  
    Y_pred_status = random_forest.predict(xtest)
    acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
    print("acc_random_forest_status:",acc_random_forest)
    
    Y_train = train_df["Education"]
    random_forest.fit(X_train, Y_train)  
    Y_pred_edu = random_forest.predict(xtest)  
    acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
    print("acc_random_forest_edu:",acc_random_forest)
    
    Y_train = train_df["Occupation"]
    random_forest.fit(X_train, Y_train)  
    Y_pred_occ = random_forest.predict(xtest)
    acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
    print("acc_random_forest_occ:",acc_random_forest)

    if Y_pred_hp[0] == 1 : charac_hp = "HP1"
    if Y_pred_hp[0] == 2 : charac_hp = "HP2"
    if Y_pred_hp[0] == 3 : charac_hp = "HP3"

    if Y_pred_gender[0] == 0 : charac_gender = "female"
    if Y_pred_gender[0] == 1 : charac_gender = "male"

    if Y_pred_age[0] == 1 : charac_age = "20-27"
    if Y_pred_age[0] == 2 : charac_age = "28-35"
    if Y_pred_age[0] == 3 : charac_age = "36-45"

    if Y_pred_status[0] == 0 : charac_status = "single"
    if Y_pred_status[0] == 1 : charac_status = "married"

    if Y_pred_edu[0] == 1 : charac_edu = "graduate"
    if Y_pred_edu[0] == 2 : charac_edu = "undergraduate"
    if Y_pred_edu[0] == 3 : charac_edu = "high school"
    if Y_pred_edu[0] == 4 : charac_edu = "unspecified education"

    if Y_pred_occ[0] == 1 : charac_occ = "student"
    if Y_pred_occ[0] == 2 : charac_occ = "employee"
    if Y_pred_occ[0] == 3 : charac_occ = "business owner"
    if Y_pred_occ[0] == 4 : charac_occ = "unspecified occupation"

    #acc_decision_tree = round(decision_tree.score(X_train, Y_train) * 100, 2)
    print(classification_report(Y_test, Y_pred))
    #print("acc_decision_tree:",label,acc_decision_tree)
    #print(Y_pred,Y3)
    return charac_hp,charac_gender,charac_age,charac_status,charac_edu,charac_occ,Y_pred_hp[0],Y_pred_gender[0],\
          Y_pred_age[0],Y_pred_status[0],Y_pred_occ[0],Y_pred_edu[0],Y3


# In[39]:


import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.metrics import confusion_matrix,precision_score,recall_score,accuracy_score
from sklearn.metrics import classification_report

#     X_train = train_df.drop(labels=[label],axis=1)
#     Y_train = train_df[label]
df3 = pd.concat([df]*20, ignore_index=True)
train_df,test_df = train_test_split(df3, test_size=0.3, random_state=42, shuffle=True)

def getROCfigure2(features,label):
    X_train = train_df[features]
    Y_train = train_df[label]
    X_test  = test_df[features]
    Y_test  = test_df[label]  
    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(X_train, Y_train)
    y_scores = decision_tree.predict_proba(X_test)
    # One hot encode the labels in order to plot them
    y_onehot = pd.get_dummies(Y_test, columns=decision_tree.classes_)
    # Create an empty figure, and iteratively add new lines
    # every time we compute a new class
    fig = go.Figure()
    fig.add_shape(
        type='line', line=dict(dash='dash'),
        x0=0, x1=1, y0=0, y1=1
    )

    for i in range(y_scores.shape[1]):
        y_true = y_onehot.iloc[:, i]
        y_score = y_scores[:, i]
        fpr, tpr, _ = roc_curve(y_true, y_score)
        auc_score = roc_auc_score(y_true, y_score)
        
        if(label == "HpAnswer"):
            if y_onehot.columns[i] == 1 : attrcol = "HP1"
            if y_onehot.columns[i] == 2 : attrcol = "HP2"
            if y_onehot.columns[i] == 3 : attrcol = "HP3"
        elif(label == "Gender"):
            if y_onehot.columns[i] == 0 : attrcol = "F"
            if y_onehot.columns[i] == 1 : attrcol = "M"
        elif(label == "Age"):
            if y_onehot.columns[i] == 1 : attrcol = "20-27"
            if y_onehot.columns[i] == 2 : attrcol = "28-35"
            if y_onehot.columns[i] == 3 : attrcol = "36-45"
        elif(label == "Status"):
            if y_onehot.columns[i] == 0 : attrcol = "S"
            if y_onehot.columns[i] == 1 : attrcol = "M"
        elif(label == "Education"):
            if y_onehot.columns[i] == 1 : attrcol = "G"
            if y_onehot.columns[i] == 2 : attrcol = "U"
            if y_onehot.columns[i] == 3 : attrcol = "H"
            if y_onehot.columns[i] == 4 : attrcol = "O"
        elif(label == "Occupation"):
            if y_onehot.columns[i] == 1 : attrcol = "S"
            if y_onehot.columns[i] == 2 : attrcol = "E"
            if y_onehot.columns[i] == 3 : attrcol = "B"
            if y_onehot.columns[i] == 4 : attrcol = "O"
        
        name = f"{attrcol}(AUC={auc_score:.2f})"
        fig.add_trace(go.Scatter(x=fpr, y=tpr, name=name, mode='lines'))
    if(label == "HpAnswer"):
        labels="Headphone Type"
    else:
        labels= label
    fig.update_layout(
        xaxis_title='False Positive Rate',
        yaxis_title='True Positive Rate',
        title=f'ROC Curve of {labels}',
        yaxis=dict(scaleanchor="x", scaleratio=1),
        xaxis=dict(constrain='domain'),
        height=450,
        font=dict(size=12),margin=dict(l=50, r=50, t=100, b=100))
    
    return fig

 
def getConfusionMatrix(features,label):
    X_train = train_df[features]
    Y_train = train_df[label]
    X_test  = test_df[features]
    Y_test  = test_df[label]  
    decision_tree = DecisionTreeClassifier()
    decision_tree.fit(X_train, Y_train)
    Y_pred = decision_tree.predict(X_test)  
    cm = confusion_matrix(Y_test,Y_pred,normalize='true')
    cm1 = np.round(cm,2)
    #print(Y_train.value_counts().index.shape[0])
    #list(map(str,Y_train.value_counts().index.sort_values()))
    ames = str(classification_report(Y_test , Y_pred))
    if(label == "HpAnswer"):
        ac = ['HP1','HP2','HP3']
    elif(label == "Gender"):
        ac = ['F','M']
    elif(label == "Age"):
        ac = ['20-27','28-35', '36-45']
    elif(label == "Status"):
        ac = ['S','M']
    elif(label == "Education"):
        ac = ['G','U','H','O']
    elif(label == "Occupation"):
        if(Y_train.value_counts().index.shape[0]==3):
           ac = ['E','B','O']
        else:
           ac = ['S','E','B','O']

    fig2 = px.imshow(cm1,
                    labels=dict(x="Predicted label", y="True label"),
                    color_continuous_scale='blues',
                    aspect="auto",
                    x = ac,
                    y = ac,
                    #title=a,
                    text_auto=True)
    score =accuracy_score(Y_test , Y_pred)
    sensitivity_recall = recall_score(Y_test , Y_pred, average='weighted')
    specificity = recall_score(Y_test , Y_pred, average='weighted', pos_label=0)
    precision = precision_score(Y_test , Y_pred, average='weighted')
    acc=f"Accuracy: {round(score*100,2)}%"
    pres=f"Precision: {round(precision,3)}|"
    tpr = f"TPR: {round(sensitivity_recall,3)}|"
    fpr = f"FPR: {round(1-specificity,3)}|"
    spe = f"Specificity: {round(specificity,3)}"
    ames= ames.replace('\n',"<br>")
    text23=f"avg_ {tpr}{fpr}{spe}"
    fig2.add_annotation(text=ames+text23, 
                    align='left',
                    showarrow=False,
                    xref='paper',
                    yref='paper',
                    x=1.5,
                    y=2.3,
                    bordercolor='black',
                    borderwidth=1)   
    fig2.update_xaxes(side="bottom")
    fig2.update_layout(width=300,height=380, font=dict(size=10),margin=dict(l=80, r=80, t=180, b=80))
    fig2.update_coloraxes(showscale=False)
    
    return fig2


# In[40]:


import dalex as dx


from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import warnings
warnings.filterwarnings('ignore')


# In[41]:


# choose a data point to explain
# observation = X.iloc[[0]]
# observation
observation = pd.DataFrame({'Gender': [1],
                   'Age': [2],
                   'Status': [0],
                   'Education':[2],
                   'Occupation':[2],
                   'FactorHps':[3],
                   'ActivityHps':[2],
                   'InnovationHps':[2],
                   'PriceHps':[2]},
                    index = ['Me'])
#p_parts_list = [e.predict_parts(observation) for e in exp_list]
#p_parts_list[0].plot(p_parts_list[1:], min_max=[-0.1, 1.1])


# In[42]:


import plotly.express as px

def get_explaination(observation):
    X = train_df[observation.columns.values]
    y = train_df["HpAnswer"]
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y) 
    exp_list = []

    for i in range(len(np.unique(y))):
        # add i parameter to `predict_function` just to do it in a loop
        pf = lambda m, d, i=i: m.predict_proba(d)[:, i]
        e = dx.Explainer(
            model, X, 
            y == i, 
            predict_function=pf,
            label=f'{i+1}',
            verbose=False
        )
        exp_list += [e]
    
    p_parts_list = [e.predict_parts(observation) for e in exp_list]
    adata = pd.concat((p_parts_list[0].result,p_parts_list[1].result,p_parts_list[2].result))    
    adata['contribution'] = round(adata['contribution'],3)
    pt = adata.loc[adata['variable']=="prediction"]
    pmax = pt['contribution'].max()
    pt = pt.loc[pt['contribution']==pmax]
    htype = pt['label'].iloc[0]

    adata = adata.loc[adata['label']==htype]
    #print(adata)
    fig = go.Figure()
    dpos = []
    dneg = []
    adata['bcolors'] = 'green'
    adata['variable_name'].replace("",'prediction', inplace=True)
    for i in range(len(adata['contribution'])):
        if (adata['contribution'].iloc[i] < 0):
               adata['bcolors'].iloc[i]="red"
               dneg.append(adata['variable_name'].iloc[i])
        if(adata['variable_name'].iloc[i]=="prediction"):
               adata['bcolors'].iloc[i]="blue"
        if(adata['variable_name'].iloc[i]=="intercept"):
               adata['bcolors'].iloc[i]="white"
        if(adata['bcolors'].iloc[i]=='green'):
               dpos.append(adata['variable_name'].iloc[i])

    fig.add_trace(go.Bar(
        y= adata['variable_name'],
        x=adata['contribution'],
        orientation='h',
        text = adata['contribution'],
        marker=dict(
            color=adata['bcolors'],
            #line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
        )
    ))
    fig.update_layout(
        title= f'Explaination: product selection HP{htype}',
        margin=dict(l=0, r=0, t=35, b=0),
        height=300
    )

    return fig,htype,dpos,dneg,pmax,adata


# In[43]:


observation2 = pd.DataFrame({'Gender': [1],
                   'Age': [2],
                   'Status': [0],
                   'Education':[2],
                   'Occupation':[2],
                   'FactorHps':[5],
                   'ActivityHps':[2],
                   'InnovationHps':[2],
                   'PriceHps':[2]})


# In[ ]:


get_explaination(observation)


# In[ ]:





# In[ ]:




