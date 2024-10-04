#!/usr/bin/env python
# coding: utf-8

# # <img src="https://selfstudy108.treebymuk.com/wp-content/uploads/2022/05/dashboard-reporting-e1653293915410.jpg">
# 
# # Section 2: Visualized data from customer feedback application
# 
# After get the complete data from survey response, visulized the data as set customer hypothesis

# In[1]:


import pandas as pd
import numpy as np 
from Survey_MLclassification import feature_importance,getROCfigure2,getConfusionMatrix,get_explaination
from RuleBased_Classification import segment_cus

data = pd.read_csv("New Headphone Production Survey Complete.csv")
qlabels = feature_importance()


# In[2]:


# the style arguments for the main content page.

CONTENT_STYLE = {
    'margin-left': '2%',
    'margin-right': '3%',
  #  'margin-left': 'auto',
    'align': 'center',
    'top': 0,
  #  'padding': '20px 10px',
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': 'black',
}



# In[3]:


from collections import defaultdict
from plotly.subplots import make_subplots
from random import setstate
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go

text_input = html.Div(
    [
        #dbc.Card([
             dbc.Row([
                     dbc.Col([
                      html.I("Gender:"),
                        dcc.Dropdown(
                               options=[
                                   {'label': 'Male', 'value': 1},
                                   {'label': 'Female', 'value': 0},
                               ],
                               id = "select_gender",
                               value = 0,
                               searchable=False
                        )
                     ]),
                     dbc.Col([
                        html.I("Age:"),
                        dcc.Dropdown(
                               options=[
                                   {'label': 'Age 20-27', 'value': 1},
                                   {'label': 'Age 28-35', 'value': 2},
                                   {'label': 'Age 36-45', 'value': 3},
                               ],
                               id = "select_age",
                               value = 1,
                               searchable=False
                     )]),
                     dbc.Col([
                        html.I("Status:"),
                        dcc.Dropdown(
                               options=[
                                   {'label': 'Single', 'value': 0},
                                   {'label': 'Married', 'value': 1},
                               ],
                               id = "select_status",
                               value = 0,
                               searchable=False
                     )])
            ]), 
            html.Br(),  
            dbc.Row([        
                    dbc.Col([
                        html.I("Education:"),
                        dcc.Dropdown(
                               options=[
                                   {'label': 'Graduate', 'value': 1},
                                   {'label': 'Undergraduate', 'value': 2},
                                   {'label': 'High School', 'value': 3},
                                   {'label': 'Other', 'value': 4},
                               ],
                               id = "select_edu",
                               value = 1,
                               searchable=False
                     )]),
                    dbc.Col([
                        html.I("Occupation:"),
                        dcc.Dropdown(
                               options=[
                                   {'label': 'Student', 'value': 1},
                                   {'label': 'Employee', 'value': 2},
                                   {'label': 'Business Owner', 'value': 3},
                                   {'label': 'Other', 'value': 4},
                               ],
                               id = "select_occ",
                               value = 1,
                               searchable=False
                     )])
            ]),
     #   ],style={'padding': '20px 50px','height':'680px'}),
         
    ]
   # ,style={'font-size': '15px'} 
)

ruchecklist = html.Div(
    [
  
                #dbc.Label("<b>Characteristic attributes</b>"),
                dbc.Checklist(
                    options=[
                        {"label": "Male", "value": "Male"},
                        {"label": "Female", "value": "Female"},
                        {"label": "Age 20-27", "value": "20-27"},
                        {"label": "Age 28-35", "value": "28-35"},
                        {"label": "Age 36-45", "value": "36-45"},
                        {"label": "Single", "value": "Single"},
                        {"label": "Married", "value": "Married"},
                        {"label": "Graduate", "value": "Graduate"},
                        {"label": "Undergraduate", "value": "Undergraduate"},
                        {"label": "High School", "value": "High School"},
                        {"label": "Other education", "value": "Other education"},
                        {"label": "Student", "value": "Student"},
                        {"label": "Employee", "value": "Employee"},
                        {"label": "Business Owner", "value": "Business Owner"},
                        {"label": "Other occupation", "value": "Other occupation"},

                    ],
                    value=[],
                    inline=True,
                    id="ruchecklist-input",
                ),
    
    ]
       
)


# In[4]:


from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash import Input, Output, State, html

def LabeledSelect(label, **kwargs):
    return dbc.Form([dbc.Label(label), dbc.Select(**kwargs)],style={'width': '80%','margin-left':'5%'}
)
card_gender= dbc.Card([
                dbc.CardHeader("Gender"),
                dbc.CardBody([
                        #html.H5("Gender",className="card-title"),
                        html.H6("TopGender:",className="card-text",id="cs_tgen"),
                        html.H3("TopGenderPercent:",className="card-subtitle",id="cs_tpgen"),
                        html.P("GenderPercent:",className="card-text",id="cs_gen")
                ])
             ],style={"textAlign": "center","height":"205px",'margin':'10px 10px 10px 10px'})
card_age=    dbc.Card([
                    dbc.CardHeader("Age"),
                    dbc.CardBody([
                        #html.H5("Age",className="card-title"),
                        html.H6("TopAge:",className="card-text",id="cs_tage"),
                        html.H3("TopAgePercent:",className="card-subtitle",id="cs_tpage"),
                        html.P("AgePercent:",className="card-text",id="cs_age")
                    ])
             ],style={"textAlign": "center","height":"205px",'margin':'10px 10px 10px 10px'})
card_status=  dbc.Card([
                    dbc.CardHeader("Status"),
                    dbc.CardBody([
                        #html.H5("Status",className="card-title"),
                        html.H6("TopStatus:",className="card-text",id="cs_tsta"),
                        html.H3("TopStatusPercent:",className="card-subtitle",id="cs_tpsta"),
                        html.P("StatusPercent:",className="card-text",id="cs_sta")
                    ])
             ],style={"textAlign": "center","height":"205px",'margin':'10px 10px 10px 10px'})
card_edu=    dbc.Card([
                    dbc.CardHeader("Education"),
                    dbc.CardBody([
                       # html.H5("Education",className="card-title"),
                        html.H6("TopEducation:",className="card-text",id="cs_tedu"),
                        html.H3("TopEducationPercent:",className="card-subtitle",id="cs_tpedu"),
                        html.P("EducationPercent:",className="card-text",id="cs_edu")
                    ])
             ],style={"textAlign": "center","height":"205px",'margin':'10px 10px 10px 10px'})
card_occ=    dbc.Card([
                    dbc.CardHeader("Occupation"),
                    dbc.CardBody([
                       # html.H5("Occupation",className="card-title"),
                        html.H6("TopOccupation:",className="card-text",id="cs_tocc"),
                        html.H3("TopOccupationPercent:",className="card-subtitle",id="cs_tpocc"),
                        html.P("OccupationPercent:",className="card-text",id="cs_occ")
                    ])
             ],style={"textAlign": "center","height":"205px",'margin':'10px 10px 10px 10px'})


maincards =html.Div([dbc.Card([
    dbc.Row(
        [
            dbc.Col(card_gender),
            dbc.Col(card_age),
            dbc.Col(card_status),          
            dbc.Col(card_edu),
            dbc.Col(card_occ)
        ]
    ),
    dbc.Row([
            dbc.Col([dcc.Graph(id='graph_1')], xs=12,sm=12, md=6, lg=6),
            dbc.Col([dcc.Graph(id='graph_9')], xs=12,sm=12, md=6, lg=6)
        ]
    )
    
 ], 
 # color="light",                 
)
],style={'padding': '20px 10px'})
graphcards23 = html.Div([
                  html.Br(),
                  html.H5("Rule-based classification ", style={'align':'center','font-weight': 'bold'}),
                  dbc.Row([         
                            dbc.Col([
                                html.Div(id='rudestext', style={'font-size': '12px', 'font-weight': 'normal'})
                            ], xs=12,sm=12, md=12, lg=12), 
                            dbc.Col([dcc.Graph(id='table_segcustomer')]),


                   ])            
                  
],style={'padding': '10px 10px 10px 10px'} )

resultcards =html.Div([dbc.Card([
    dbc.Row([
        dbc.Col([dcc.Graph(id='table_1')]),

    ])
 ]),
  html.Br(),
  dbc.Card([
    dbc.Row([
        dbc.Col([graphcards23]),
    ])
 ])
])

featurecards =html.Div([dbc.Card([
    dbc.Row(
        dcc.Graph(id='table_feature')
    )
 ],
 # color="light",                 
)
],style={'padding': '10px 2px 10px 2px'})


graphcards2 = html.Div([dbc.Card([
         html.Br(),
         dbc.Row([
                     dbc.Col([
                        LabeledSelect(
                            id="select-dropdown",
                            options=[{
                                'label': 'Ranking score of Headphone features',
                                'value': 'dbScoreV1'
                            },
                                {
                                'label': 'Q1:How many headphones & ear buds do you have?',
                                'value': 'NumberHps'
                            }, {
                                'label': 'Q2:How do you find the headphone’s detail?',
                                'value': 'dbQ2'
                            },
                               {
                                'label': 'Q3:What are the most activity you using your best headphone?',
                                'value': 'ActivityHps'
                            },
                                {
                                'label': 'Q4:When do you buy your latest headphone?',
                                'value': 'TimeHps'
                            }, {
                                'label': 'Q5:Which prices of a headphone did you buy last time?',
                                'value': 'PriceHps'
                            },
                              {
                                'label': 'Q6:Where do you frequently buy a headphone?',
                                'value': 'PlaceHps'
                            },
                              {
                                'label': 'Q7:What is the common problems on your headphone?',
                                'value': 'dbQ7'
                            },
                              {
                                'label': 'Q8:Which factor is the most importance for you to choose a headphone?',
                                'value': 'FactorHps'
                            }
                            ,
                              {
                                'label': 'Q9:Are you concerned using headphones cause harmful your health?',
                                'value': 'HealthHps'
                            },
                              {
                                'label': 'Q10:What is the best innovative headphone technology for the future need to develop?',
                                'value': 'InnovationHps'
                            }

                            ],
                        value="dbScoreV1",
                        label="Questionnaires",
                        )])
        ]),
    dbc.Row(
        [
            dbc.Col([dcc.Graph(id='graph_2')], xs=12,sm=12, md=6, lg=6),
            dbc.Col([dcc.Graph(id='graph_3')], xs=12,sm=12, md=6, lg=6)

        ]
    ),
    dbc.Row(
        [
            dbc.Col([dcc.Graph(id='graph_7')], xs=12,sm=12, md=12, lg=12),
        ]
    ),
 ],style={"align": "center",'margin':'10px 10px 10px 10px'} 
 # color="light",                 
)
])
graphcards3 = html.Div([
              dbc.Card([
                  html.Br(),
                  html.H4("Customer classification from questionaries by machine learning", style={'align':'center','font-weight': 'bold'}),
                  html.Br(),
#                   html.P(id="pp_v1"),
                  dbc.Row([
                    dbc.Col([
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row([
                                        html.H6("Customer charateristic:",style={'font-weight': 'bold'}),
                                        html.Br(),
                                        html.Br(),
                                        dbc.Col([text_input]) 
                                    ]),
                                    html.Br(),
                                    html.Br(),
                                    html.H6("Survey Attributes:",style={'font-weight': 'bold'}),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            html.I("Feature 1:"),
                                            dcc.Dropdown(
                                                       options=np.array(qlabels.index),
                                                       value= np.array(qlabels.index)[0],
                                                       id = "ques_attr1",
                                                       clearable=False
                                                    )
                                        ]),
                                         dbc.Col([
                                                html.I("Options:"),
                                                html.Br(),
                                                dcc.Input(
                                                        id="input_range_1", type="number",min=0, max=6, step=1, value= 0
                                                    )
                                        ]),
                                        html.Div(id='ans_attr1_des')

                                    ]), 
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            html.I("Feature 2:"),
                                            dcc.Dropdown(
                                                       options=np.array(qlabels.index),
                                                       value= np.array(qlabels.index)[1],
                                                       id = "ques_attr2",
                                                       clearable=False
                                                    )
                                        ]),
                                         dbc.Col([
                                                html.I("Options:"),
                                                html.Br(),
                                                dcc.Input(
                                                        id="input_range_2", type="number", min=0, max=6, step=1, value= 0
                                                    )
                                        ]),
                                        html.Div(id='ans_attr2_des')
                                    ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            html.I("Feature 3:"),
                                            dcc.Dropdown(
                                                       options=np.array(qlabels.index),
                                                       value= np.array(qlabels.index)[2],
                                                       id = "ques_attr3",
                                                       clearable=False
                                                    )
                                        ]),
                                         dbc.Col([
                                                html.I("Options:"),
                                                html.Br(),
                                                dcc.Input(
                                                       id="input_range_3", type="number", min=0, max=6, step=1, value= 0
                                                    )
                                        ]),
                                         html.Div(id='ans_attr3_des')
                                        ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            html.I("Feature 4:"),
                                            dcc.Dropdown(
                                                       options=np.array(qlabels.index),
                                                       value= np.array(qlabels.index)[3],
                                                       id = "ques_attr4",
                                                       clearable=False
                                                    )
                                        ]),
                                         dbc.Col([
                                                html.I("Options:"),
                                                html.Br(),
                                                dcc.Input(
                                                       id="input_range_4", type="number", min=0, max=6, step=1, value= 0
                                                    )
                                        ]),
                                         html.Div(id='ans_attr4_des')
                                        ]),
                                    html.Br(),
                                    html.Br(),                                   
                                    dbc.Row([
                                            dbc.Button(
                                                        "SUBMIT",
                                                        id="b_submit",
                                                        n_clicks=0,
                                                    ),
                                        
                                            ],style={'width': '125px','height':'15px','margin-left': '3%',}),
                                     
                                    html.Br(),
                                    html.Br(),

                                ]
                            ),style={'padding': '20px 10px','margin':'10px 10px 10px 20px'}
                        )
                        
                    ], xs=12,sm=12, md=6, lg=6),
                    dbc.Col([
                             html.Br(),
                             dbc.Row([         
                                    dbc.Col([
                                        dcc.Graph(id='graph_15')
                                    ], xs=12,sm=12, md=12, lg=12), 

                             ]),
                            dbc.Row([         
                                    dbc.Col([
                                        html.Div(id='introdestext', style={'font-style': 'italic'}),
                                        html.Div(id='mldestext', style={'font-size': '15px','font-family':"Courier New", 'font-weight': 'normal'})
                                    ]), 

                            ]),
                            html.Br(),
                            dbc.Row([         
                                    dbc.Col([
                                        dcc.Loading(
                                           id="loading-2",
                                            children=[dcc.Graph(id='graph_exp')],
                                            type="circle",

                                        )
                                    ], xs=12,sm=12, md=12, lg=12), 

                             ]),

                    ], xs=12,sm=12, md=6, lg=6), 
                   
                  ]),
                  html.Br(),
                  html.H5("Predictive Analysis of the ML model's results using ROC curves"),
                  html.Br(),
                  dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='graph_18')
                    ], xs=12,sm=12, md=7, lg=7),
                    dbc.Col([
                        dcc.Graph(id='graph_18c')
                    ], xs=12,sm=12, md=3, lg=3)
                  ]),
                  html.Br(),
                  dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='graph_12')
                    ], xs=12,sm=12, md=7, lg=7),
                    dbc.Col([
                        dcc.Graph(id='graph_12c')
                    ], xs=12,sm=12, md=3, lg=3)
                  ]),
                  html.Br(),
                  dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='graph_13')
                    ], xs=12,sm=12, md=7, lg=7),
                    html.Br(),
                    dbc.Col([
                        dcc.Graph(id='graph_13c')
                    ], xs=12,sm=12, md=3, lg=3)
                  ]),
                  html.Br(),
                  dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='graph_14')
                    ], xs=12,sm=12, md=7, lg=7),
                    dbc.Col([
                        dcc.Graph(id='graph_14c')
                    ], xs=12,sm=12, md=3, lg=3),
                  ]),
                  html.Br(),
                  dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='graph_16')
                    ], xs=12,sm=12, md=7, lg=7),
                    dbc.Col([
                        dcc.Graph(id='graph_16c')
                    ], xs=12,sm=12, md=3, lg=3)
                  ]),
                  html.Br(),
                  dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='graph_17')
                    ], xs=12,sm=12, md=7, lg=7),
                    dbc.Col([
                        dcc.Graph(id='graph_17c')
                    ], xs=12,sm=12, md=3, lg=3)
                  ])

                  
 ],style={'margin':'10px 10px 10px 10px','padding': '10px 35px'} 
 # color="light",                 
)
])





# In[5]:


from collections import defaultdict
from plotly.subplots import make_subplots
from random import setstate
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output,State
import plotly.express as px
import plotly.graph_objects as go



controls = html.Div([
#      dbc.Row([         
#                     dbc.Col([
#                         dcc.Graph(id='graph_0')
#                     ], xs=12,sm=12, md=12, lg=12) 
#              ]),
     dbc.Row([         
                    dbc.Col([
                        dcc.Graph(id='graph_8')
                    ], xs=12,sm=12, md=12, lg=12), 
                    
             ]),
      dbc.Card([
       
        html.P('Product version', style={
            'font-weight': 'bold',
        }),
        dbc.RadioItems(
            options=[{
                'label': 'All Headphone Types',
                'value': 'v0'
            },
                {
                'label': 'Headphone-v1 (HP1)',
                'value': 'v1'
            },
                {
                    'label': 'Headphone-v2 (HP2)',
                    'value': 'v2'
                },
                {
                    'label': 'Headphone-v3 (HP3)',
                    'value': 'v3'
                }
            ],
            id='radio_product',
            value='v0',
           # inline=True
        ),
        #html.Br(),
        html.P('Characteristic Groups', style={
            'font-weight': 'bold',
        }),
        dbc.RadioItems(
            options=[{
                'label':  'Not Specific',
                'value': 'none'
            },{
                'label': 'Gender',
                'value': 'gender'
            },
                {
                    'label': 'Age',
                    'value': 'age'
                },
                {
                    'label': 'Status',
                    'value': 'status'
                },
                {
                    'label': 'Education',
                    'value': 'education'
                },            
                {
                    'label': 'Occupation',
                    'value': 'occupation'
                }
            ],
            id='radio_items',
            value='none',
           # inline=True       
        ),
        #html.Br(),
        html.P('Characteristic Fields', style={
            'font-weight': 'bold',
        }),
            dbc.Checklist(
                options=[
                    {"label": "Male", "value": "Male"},
                    {"label": "Female", "value": "Female"},
                    {"label": "Age 20-27", "value": "20-27"},
                    {"label": "Age 28-35", "value": "28-35"},
                    {"label": "Age 36-45", "value": "36-45"},
                    {"label": "Single", "value": "Single"},
                    {"label": "Married", "value": "Married"},
                    {"label": "Graduate", "value": "Graduate"},
                    {"label": "Undergraduate", "value": "Undergraduate"},
                    {"label": "High School", "value": "High School"},
                    {"label": "Other education", "value": "Other education"},
                    {"label": "Student", "value": "Student"},
                    {"label": "Employee", "value": "Employee"},
                    {"label": "Business Owner", "value": "Business Owner"},
                    {"label": "Other occupation", "value": "Other occupation"},

                ],
                value=[],
                inline=True,
                id="checklist-input",
            )
    ],
    style={
    'padding': '30px 20px',
   }

)])


PLOTLY_LOGO = "https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/IS-project-2.jpg"
 
content = html.Div(
      [
        html.Div([
            html.Br(),
            html.H2('New Headphones Production Survey Dashboard '),
            ], style={'margin-left': '3%'}),
        html.Div([
            html.Br(),
            dbc.Row([
                dbc.Col([controls],xs=12,sm=12, md=3, lg=3),              
                dbc.Col([maincards], xs=12,sm=12, md=8, lg=8)
            ], justify='center')
        ]),
        html.Div([
              html.Br(),
              dbc.Row([
                    dbc.Col([resultcards], xs=12,sm=12, md=3, lg=3),   
                    dbc.Col([graphcards2], xs=12,sm=12, md=8, lg=8) 
               ], justify='center')
               
         ]),
          
        html.Div([
                  dbc.Row([
                    dbc.Col([featurecards], xs=12,sm=12, md=3, lg=3), 
                    dbc.Col([graphcards3], xs=12,sm=12, md=8, lg=8) 
                  ], justify='center')
        ]),

],style=CONTENT_STYLE)
    

app = JupyterDash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

app.layout = html.Div([content])


    


# 

# In[6]:


@app.callback(
    Output('cs_tgen', 'children'),
    Output('cs_tpgen', 'children'),
    Output('cs_gen', 'children'),
    Output('cs_tage', 'children'),
    Output('cs_tpage', 'children'),
    Output('cs_age', 'children'),
    Output('cs_tsta', 'children'),
    Output('cs_tpsta', 'children'),
    Output('cs_sta', 'children'),
    Output('cs_tedu', 'children'),
    Output('cs_tpedu', 'children'),
    Output('cs_edu', 'children'),
    Output('cs_tocc', 'children'),
    Output('cs_tpocc', 'children'),
    Output('cs_occ', 'children'),
    Input('radio_product', 'value'),
    Input('radio_items', 'value'))
def show_maincards(sp_value,sc_value): 
    if sp_value == "v0":
        g = (data['Gender'].value_counts(normalize=True)).rename_axis('Gender').reset_index(name='Pcount')
        a = (data['Age'].value_counts(normalize=True)).rename_axis('Age').reset_index(name='Pcount')
        s = (data['Status'].value_counts(normalize=True)).rename_axis('Status').reset_index(name='Pcount')
        e = (data['Education'].value_counts(normalize=True)).rename_axis('Education').reset_index(name='Pcount')
        o = (data['Occupation'].value_counts(normalize=True)).rename_axis('Occupation').reset_index(name='Pcount')
    else:
        stadata = data[["HpAnswer","Gender","Age","Status","Education","Occupation"]]\
        .loc[data['HpAnswer']==sp_value].describe(include='all')
        g = (data["Gender"].loc[data['HpAnswer']==sp_value].value_counts(normalize=True)).\
        rename_axis('Gender').reset_index(name='Pcount')
        a = (data["Age"].loc[data['HpAnswer']==sp_value].value_counts(normalize=True)).\
        rename_axis('Age').reset_index(name='Pcount')
        s = (data["Status"].loc[data['HpAnswer']==sp_value].value_counts(normalize=True)).\
        rename_axis('Status').reset_index(name='Pcount')
        e = (data["Education"].loc[data['HpAnswer']==sp_value].value_counts(normalize=True)).\
        rename_axis('Education').reset_index(name='Pcount')
        o = (data["Occupation"].loc[data['HpAnswer']==sp_value].value_counts(normalize=True)).\
        rename_axis('Occupation').reset_index(name='Pcount')
   
    gp = ep = ap = sp = op =" " 
#gender top percentage
    for ind in g.index:
         if(ind == 0):
            gt  = g['Gender'][ind]
            if(sc_value=="gender"):
               gt  = "Top "+g['Gender'][ind]                   
            gtp = "\t"+str("{:.2%}".format(g['Pcount'][ind]))
         else:
            gp += "\t"+str(g['Gender'][ind])+">"+str("{:.2%}".format(g['Pcount'][ind]))           
#age top percentage  
    a.loc[a['Age'].str.strip()=="20-27",'name']="A1"
    a.loc[a['Age'].str.strip()=="28-35",'name']="A2"
    a.loc[a['Age'].str.strip()=="36-45",'name']="A3"
    at  = a['Age'][0]
    if(sc_value=="age"):
        at  = "Top "+a['Age'][0]
    atp = "\t"+str("{:.2%}".format(a['Pcount'][0]))
    for ind in a.index:
        if(ind!=0):
            ap += "\t"+str(a['name'][ind])+">"+str("{:.2%}".format(a['Pcount'][ind]))
#status top percentage
    for ind in s.index:
        if(ind == 0):
            st  = s['Status'][ind] 
            if(sc_value=="status"):
                st  = "Top "+s['Status'][ind]
            stp = "\t"+str("{:.2%}".format(s['Pcount'][ind]))
        else:
            sp += "\t"+str(s['Status'][ind])+">"+str("{:.2%}".format(s['Pcount'][ind]))  
#education top percentage
    e.loc[e['Education'].str.strip()=="Graduate",'name']="GD"
    e.loc[e['Education'].str.strip()=="Undergraduate",'name']="UG"
    e.loc[e['Education'].str.strip()=="High School",'name']="HS"
    e.loc[e['Education'].str.strip()=="Other education",'name']="OT"
    et  = e['Education'][0]
    if(sc_value=="education"):
        et  = "Top "+e['Education'][0]
    etp = "\t"+str("{:.2%}".format(e['Pcount'][0]))
    for ind in e.index:
        if(ind!=0):
            ep += "\t"+str(e['name'][ind])+">"+str("{:.2%}".format(e['Pcount'][ind]))  
#occupation top percentage
    o.loc[o['Occupation'].str.strip()=="Employee",'name']="EP"
    o.loc[o['Occupation'].str.strip()=="Business Owner",'name']="BO"
    o.loc[o['Occupation'].str.strip()=="Student",'name']="SD"
    o.loc[o['Occupation'].str.strip()=="Other occupation",'name']="OT"
    ot  = o['Occupation'][0]
    if(sc_value=="occupation"):
        ot  = "Top "+o['Occupation'][0]
    otp = "\t"+str("{:.2%}".format(o['Pcount'][0]))
    for ind in o.index:
        if(ind!=0):
           op += "\t"+str(o['name'][ind])+">"+str("{:.2%}".format(o['Pcount'][ind]))


            
    return gt,gtp,gp,at,atp,ap,st,stp,sp,et,etp,ep,ot,otp,op


# In[7]:


import plotly.express as px
from skimage import io
@app.callback( 
    #Output('graph_0', 'figure'),
    Output('graph_8', 'figure'),
    Input('radio_product', 'value'))
def show_hps(sp_value):
    fig0 = go.Figure()
    #img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/headphone_allversions.jpg')
    img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/headphone_allversions.jpg')
    if sp_value == 'v1':
        img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/headphone_version1.jpg')
    elif sp_value == 'v2':
        img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/headphone_version2.jpg')
    elif sp_value == 'v3':
        img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/headphone_version3.jpg')    
    fig8 = px.imshow(img)
    fig8.update_layout(title="ABAC-ISproject|ID:6471303",height=200,coloraxis_showscale=False,\
                       font=dict(size=10),paper_bgcolor='rgba(0,0,0,0)',\
                        plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=20, r=20, t=20, b=20))
    fig8.update_xaxes(showticklabels=False)
    fig8.update_yaxes(showticklabels=False) 
    return fig8



# In[8]:


@app.callback( 
    Output('graph_1', 'figure'),
    Input('radio_product', 'value'),
    Input('radio_items', 'value'))
def update_bar_chart_all(sp_value,sc_value):
    a = {'HpAnswer': ["Headphone-v1", "Headphone-v2", "Headphone-v3"]}
    b = {'HpAnswer': ["Headphone-"+sp_value]} 
    htype = hpname(sp_value)
    fig1 = go.Figure()
    if sp_value == "v0":
        stadata = data[["HpAnswer","Gender","Age","Status","Education","Occupation"]].describe(include='all')
        dfs=stadata.iloc[0:4].T
        dfs.rename(index={'HpAnswer': 'TotalResponse'}, inplace=True)
        dfs.iloc[0,2]= dfs.iloc[0,0]    
    else:
        stadata = data[["HpAnswer","Gender","Age","Status","Education","Occupation"]]\
        .loc[data['HpAnswer']==sp_value].describe(include='all')
        dfs = stadata.iloc[0:4].T
        dfs.rename(index={'HpAnswer': 'TotalResponse'}, inplace=True)
        dfs.iloc[0,2]= dfs.iloc[0,0]
#All headphones selected to show
    if sc_value == "none" and sp_value== "v0":
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Total Responses"] =  data.loc[(data['HpAnswer']=="v1")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Total Responses"] =  data.loc[(data['HpAnswer']=="v2")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Total Responses"] =  data.loc[(data['HpAnswer']=="v3")].shape[0]   
     # fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Total Responses"],text=dbar1["Total Responses"]), row=1, col=1)   
      fig1.add_trace(go.Pie(labels=dbar1['HpAnswer'], values=dbar1["Total Responses"], textinfo='label+percent',
                             insidetextorientation='radial'))
      fig1.update_layout(title="<b>All Types Categorized Groups</b>",showlegend=False)
      fig1.update_traces(marker=dict(colors=['darkblue', 'royalblue', '#023047']), textfont_size=15) 
    elif sc_value == "gender" and sp_value== "v0":
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Male"] =  data.loc[(data['HpAnswer']=="v1")&(data['Gender'].str.strip()=="Male")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Female"] =  data.loc[(data['HpAnswer']=="v1")&(data['Gender'].str.strip()=="Female")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Male"] =  data.loc[(data['HpAnswer']=="v2")&(data['Gender'].str.strip()=="Male")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Female"] =  data.loc[(data['HpAnswer']=="v2")&(data['Gender'].str.strip()=="Female")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Male"] =  data.loc[(data['HpAnswer']=="v3")&(data['Gender'].str.strip()=="Male")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Female"] =  data.loc[(data['HpAnswer']=="v3")&(data['Gender'].str.strip()=="Female")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Male"],text=dbar1["Male"],name="Male"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Female"],text=dbar1["Female"],name="Female"))  
      fig1.update_layout(title="<b>All Types Categorized Gender</b>")
    elif sc_value == "age" and sp_value== "v0":
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Age 20-27"] =  data.loc[(data['HpAnswer']=="v1")&(data['Age'].str.strip()=="20-27")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Age 28-35"] =  data.loc[(data['HpAnswer']=="v1")&(data['Age'].str.strip()=="28-35")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Age 36-45"] =  data.loc[(data['HpAnswer']=="v1")&(data['Age'].str.strip()=="36-45")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Age 20-27"] =  data.loc[(data['HpAnswer']=="v2")&(data['Age'].str.strip()=="20-27")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Age 28-35"] =  data.loc[(data['HpAnswer']=="v2")&(data['Age'].str.strip()=="28-35")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Age 36-45"] =  data.loc[(data['HpAnswer']=="v2")&(data['Age'].str.strip()=="36-45")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Age 20-27"] =  data.loc[(data['HpAnswer']=="v3")&(data['Age'].str.strip()=="20-27")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Age 28-35"] =  data.loc[(data['HpAnswer']=="v3")&(data['Age'].str.strip()=="28-35")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Age 36-45"] =  data.loc[(data['HpAnswer']=="v3")&(data['Age'].str.strip()=="36-45")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Age 20-27"],text=dbar1["Age 20-27"],name="Age 20-27"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Age 28-35"],text=dbar1["Age 28-35"],name="Age 28-35")) 
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Age 36-45"],text=dbar1["Age 36-45"],name="Age 36-45"))  
      fig1.update_layout(title="<b>All Types Categorized Age</b>")
    elif sc_value == "education" and sp_value== "v0":
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Graduate"] =  data.loc[(data['HpAnswer']=="v1")&(data['Education'].str.strip()=="Graduate")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Undergraduate"] =  data.loc[(data['HpAnswer']=="v1")&(data['Education'].str.strip()=="Undergraduate")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "High School"] =  data.loc[(data['HpAnswer']=="v1")&(data['Education'].str.strip()=="High School")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Other education"] =  data.loc[(data['HpAnswer']=="v1")&(data['Education'].str.strip()=="Other education")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Graduate"] =  data.loc[(data['HpAnswer']=="v2")&(data['Education'].str.strip()=="Graduate")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Undergraduate"] =  data.loc[(data['HpAnswer']=="v2")&(data['Education'].str.strip()=="Undergraduate")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "High School"] =  data.loc[(data['HpAnswer']=="v2")&(data['Education'].str.strip()=="High School")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Other education"] =  data.loc[(data['HpAnswer']=="v2")&(data['Education'].str.strip()=="Other education")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Graduate"] =  data.loc[(data['HpAnswer']=="v3")&(data['Education'].str.strip()=="Graduate")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Undergraduate"] =  data.loc[(data['HpAnswer']=="v3")&(data['Education'].str.strip()=="Undergraduate")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "High School"] =  data.loc[(data['HpAnswer']=="v3")&(data['Education'].str.strip()=="High School")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Other education"] =  data.loc[(data['HpAnswer']=="v3")&(data['Education'].str.strip()=="Other education")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Graduate"],text=dbar1["Graduate"],name="Graduate"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Undergraduate"],text=dbar1["Undergraduate"],name="Undergraduate")) 
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["High School"],text=dbar1["High School"],name="High School"))  
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Other education"],text=dbar1["Other education"],name="Other education"))  
      fig1.update_layout(title="<b>All Types Categorized Education </b>")
    elif sc_value == "status" and sp_value== "v0":
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Single"] =  data.loc[(data['HpAnswer']=="v1")&(data['Status'].str.strip()=="Single")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Married"] =  data.loc[(data['HpAnswer']=="v1")&(data['Status'].str.strip()=="Married")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Single"] =  data.loc[(data['HpAnswer']=="v2")&(data['Status'].str.strip()=="Single")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Married"] =  data.loc[(data['HpAnswer']=="v2")&(data['Status'].str.strip()=="Married")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Single"] =  data.loc[(data['HpAnswer']=="v3")&(data['Status'].str.strip()=="Single")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Married"] =  data.loc[(data['HpAnswer']=="v3")&(data['Status'].str.strip()=="Married")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Single"],text=dbar1["Single"],name="Single"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Married"],text=dbar1["Married"],name="Married"))  
      fig1.update_layout(title="<b>All Types Categorized Status</b>")
    elif sc_value == "occupation" and sp_value== "v0":
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Student"] =  data.loc[(data['HpAnswer']=="v1")&(data['Occupation'].str.strip()=="Student")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Employee"] =  data.loc[(data['HpAnswer']=="v1")&(data['Occupation'].str.strip()=="Employee")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Business Owner"] =  data.loc[(data['HpAnswer']=="v1")&(data['Occupation'].str.strip()=="Business Owner")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Other occupation"] =  data.loc[(data['HpAnswer']=="v1")&(data['Occupation'].str.strip()=="Other occupation")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Student"] =  data.loc[(data['HpAnswer']=="v2")&(data['Occupation'].str.strip()=="Student")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Employee"] =  data.loc[(data['HpAnswer']=="v2")&(data['Occupation'].str.strip()=="Employee")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Business Owner"] =  data.loc[(data['HpAnswer']=="v2")&(data['Occupation'].str.strip()=="Business Owner")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Other occupation"] =  data.loc[(data['HpAnswer']=="v2")&(data['Occupation'].str.strip()=="Other occupation")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Student"] =  data.loc[(data['HpAnswer']=="v3")&(data['Occupation'].str.strip()=="Student")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Employee"] =  data.loc[(data['HpAnswer']=="v3")&(data['Occupation'].str.strip()=="Employee")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Business Owner"] =  data.loc[(data['HpAnswer']=="v3")&(data['Occupation'].str.strip()=="Business Owner")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Other occupation"] =  data.loc[(data['HpAnswer']=="v3")&(data['Occupation'].str.strip()=="Other occupation")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Student"],text=dbar1["Student"],name="Student"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Employee"],text=dbar1["Employee"],name="Employee"))  
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Business Owner"],text=dbar1["Business Owner"],name="Business Owner"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Other occupation"],text=dbar1["Other occupation"],name="Other occupation"))  
      fig1.update_layout(title="<b>All Types Categorized Occupation</b>")
#One Headphone Type selected to show
    if sc_value == "none" and sp_value!= "v0":
      b = {'HpAnswer': ["Headphone-"+sp_value,"Others"]} 
      dbar1 = pd.DataFrame(data=b) 
      dbar1["Total Responses"] =  data.loc[(data['HpAnswer']==sp_value)].shape[0] 
      dbar1.loc[(dbar1['HpAnswer']=="Others"), "Total Responses"] =  data.loc[(data['HpAnswer']!=sp_value)].shape[0]
      #fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Total Responses"],text=dbar1["Total Responses"],name="Headphone Type"))
      fig1.add_trace(go.Pie(labels=dbar1['HpAnswer'], values=dbar1["Total Responses"], textinfo='label+percent',
                             insidetextorientation='radial'))
      fig1.update_traces(marker=dict(colors=['darkblue', 'royalblue', '#023047']), textfont_size=15)  
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Categorized Groups</b>",showlegend=False)
    elif sc_value == "gender" and sp_value!= "v0":
      dbar1 = pd.DataFrame(data=b) 
      dbar1["Male"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Gender'].str.strip()=="Male")].shape[0]
      dbar1["Female"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Gender'].str.strip()=="Female")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Male"],text=dbar1["Male"],name="Male"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Female"],text=dbar1["Female"],name="Female"))  
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Categorized Gender</b>")
    elif sc_value == "age" and sp_value != "v0":
      dbar1 = pd.DataFrame(data=b) 
      dbar1["Age 20-27"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="20-27")].shape[0]
      dbar1["Age 28-35"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="28-35")].shape[0]
      dbar1["Age 36-45"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="36-45")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Age 20-27"],text=dbar1["Age 20-27"],name="Age 20-27"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Age 28-35"],text=dbar1["Age 28-35"],name="Age 28-35")) 
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Age 36-45"],text=dbar1["Age 36-45"],name="Age 36-45"))  
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Categorized Age</b>")
    elif sc_value == "education" and sp_value!= "v0":
      dbar1 = pd.DataFrame(data=b) 
      dbar1["Graduate"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Graduate")].shape[0]
      dbar1["Undergraduate"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Undergraduate")].shape[0]
      dbar1["High School"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="High School")].shape[0]
      dbar1["Other education"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Other education")].shape[0]  
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Graduate"],text=dbar1["Graduate"],name="Graduate"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Undergraduate"],text=dbar1["Undergraduate"],name="Undergraduate")) 
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["High School"],text=dbar1["High School"],name="High School"))  
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Other education"],text=dbar1["Other education"],name="Other education")) 
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Categorized Education</b>")
    elif sc_value == "status" and sp_value!= "v0":
      dbar1 = pd.DataFrame(data=b) 
      dbar1["Single"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Status'].str.strip()=="Single")].shape[0]
      dbar1["Married"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Status'].str.strip()=="Married")].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Single"],text=dbar1["Single"],name="Single"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Married"],text=dbar1["Married"],name="Married"))  
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Categorized Status</b>")
    elif sc_value == "occupation" and sp_value!= "v0":
      dbar1 = pd.DataFrame(data=b) 
      dbar1["Student"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Student")].shape[0]
      dbar1["Employee"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Employee")].shape[0]
      dbar1["Business Owner"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Business Owner")].shape[0]
      dbar1["Other occupation"] =  data.loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Other occupation")].shape[0]    
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Student"],text=dbar1["Student"],name="Student"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Employee"],text=dbar1["Employee"],name="Employee"))  
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Business Owner"],text=dbar1["Business Owner"],name="Business Owner"))   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Other occupation"],text=dbar1["Other occupation"],name="Other occupation"))  
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Categorized Occupation</b>")
    fig1.update_layout(
         yaxis=dict(title= "Total Responses"),
         #xaxis=dict(title= "Product Types"),
         font=dict(size=12),
         height=550,
         margin=dict(l=30, r=30, t=100, b=100),
         #yaxis_range=[0,50],
#          legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1,
#             xanchor="right",
#             x=1
#         )
    )
    return fig1


# In[9]:


#ranking score of 5 features for all headphone type 
def create_ranking_all():
    s_range_ha = pd.DataFrame({'score':[1,2,3,4,5]})
    s_range_ha['response_options']=['S1-Strongly disagree','S2-Somewhat disagree','S3-Neither agree nor disagree','S4-Somewhat agree','S5-Strongly agree']    
    HpTS1_score= data['HpTS1'].value_counts().rename_axis('score').reset_index(name='Feature1')
    HpTS2_score= data['HpTS2'].value_counts().rename_axis('score').reset_index(name='Feature2')
    HpTS3_score= data['HpTS3'].value_counts().rename_axis('score').reset_index(name='Feature3')
    HpTS4_score= data['HpTS4'].value_counts().rename_axis('score').reset_index(name='Feature4')
    HpTS5_score= data['HpTS5'].value_counts().rename_axis('score').reset_index(name='Feature5')       
    s_range_ha= s_range_ha.merge(HpTS1_score,on='score',how='outer')
    s_range_ha= s_range_ha.merge(HpTS2_score,on='score',how='outer')
    s_range_ha= s_range_ha.merge(HpTS3_score,on='score',how='outer')
    s_range_ha= s_range_ha.merge(HpTS4_score,on='score',how='outer')
    s_range_ha= s_range_ha.merge(HpTS5_score,on='score',how='outer')
    s_range_ha.fillna(0, inplace=True)
    return s_range_ha


# In[10]:


#ranking score of 5 features for all headphone type 
def create_ranking_one(sp_value):
    s_range_one = pd.DataFrame({'score':[1,2,3,4,5]})
    s_range_one['response_options']=['S1-Strongly disagree','S2-Somewhat disagree','S3-Neither agree nor disagree','S4-Somewhat agree','S5-Strongly agree']    
    HpTS1_score= data.loc[(data['HpAnswer']==sp_value), ['HpTS1']].value_counts().rename_axis('score').reset_index(name='Feature1')
    HpTS2_score= data.loc[(data['HpAnswer']==sp_value), ['HpTS2']].value_counts().rename_axis('score').reset_index(name='Feature2')
    HpTS3_score= data.loc[(data['HpAnswer']==sp_value), ['HpTS3']].value_counts().rename_axis('score').reset_index(name='Feature3')
    HpTS4_score= data.loc[(data['HpAnswer']==sp_value), ['HpTS4']].value_counts().rename_axis('score').reset_index(name='Feature4')
    HpTS5_score= data.loc[(data['HpAnswer']==sp_value), ['HpTS5']].value_counts().rename_axis('score').reset_index(name='Feature5')        
    s_range_one= s_range_one.merge(HpTS1_score,on='score',how='outer')
    s_range_one= s_range_one.merge(HpTS2_score,on='score',how='outer')
    s_range_one= s_range_one.merge(HpTS3_score,on='score',how='outer')
    s_range_one= s_range_one.merge(HpTS4_score,on='score',how='outer')
    s_range_one= s_range_one.merge(HpTS5_score,on='score',how='outer')
    s_range_one.fillna(0, inplace=True)
    return s_range_one


# In[11]:


def qname(sq_value):
    if(sq_value=="NumberHps"):
        title_text="<b>Q1-</b>"
    elif(sq_value=="ActivityHps"):
        title_text="<b>Q3-</b>"
    elif(sq_value=="TimeHps"):
        title_text="<b>Q4-</b>"
    elif(sq_value=="PriceHps"):
        title_text="<b>Q5-</b>"
    elif(sq_value=="PlaceHps"):
        title_text="<b>Q6-</b>"
    elif(sq_value=="FactorHps"):
        title_text="<b>Q8-</b>"
    elif(sq_value=="HealthHps"):
        title_text="<b>Q9-</b>"
    elif(sq_value=="InnovationHps"):
        title_text="<b>Q10-</b>"
    return title_text


# In[12]:


def hpname(sp_value):
    if(sp_value=="v1"): 
        name="<b>HP1</b>"
    elif(sp_value=="v2"):
        name="<b>HP2</b>"
    elif(sp_value=="v3"):
        name="<b>HP3</b>"
    elif(sp_value=="v0"):
        name="<b>All types</b>"
    return name


# In[13]:


def HNC_all():    
    s_range_ha = create_ranking_all()
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha["Feature1"],name = "Feature 1",marker_color='#0e77bb'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature2'],name = "Feature 2",marker_color='#bc7c50'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature3'],name = "Feature 3",marker_color='#ac292f'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature4'],name = "Feature 4",marker_color='#6c6c6c'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature5'],name = "Feature 5",marker_color='#000000'))
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text="<b>All types features preference scores</b>",
        xaxis=dict(
            title= "Response Option",          
        ),
        yaxis=dict(
            title= "Total Responses",          
        ),
        barmode='stack',
        font=dict(size=12)
    )
    return fig2


# In[14]:


def HNC_one(sp_value):    
    s_range_ha = create_ranking_one(sp_value)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha["Feature1"],name = "Feature 1",marker_color='#0e77bb'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature2'],name = "Feature 2",marker_color='#bc7c50'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature3'],name = "Feature 3",marker_color='#ac292f'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature4'],name = "Feature 4",marker_color='#6c6c6c'))
    fig2.add_trace(go.Bar(x= s_range_ha["response_options"], y= s_range_ha['Feature5'],name = "Feature 5",marker_color='#000000'))
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text= hpname(sp_value)+"<b> features preference scores</b>",
        xaxis=dict(
            title= "Response Option",          
        ),
        yaxis=dict(
            title= "Total Responses",          
        ),
        barmode='stack',
        font=dict(size=12)
    )
    return fig2


# In[15]:


#All headphone categorized gender
def HC_gender(sp_value):
    
    s_range_gender = pd.DataFrame({'score':[1,2,3,4,5]})
    if sp_value == "v0":
        HpTS1_male= data.loc[(data['Gender'].str.strip()=="Male"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature1')
        HpTS1_female= data.loc[(data['Gender'].str.strip()=="Female"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature1')
        HpTS2_male= data.loc[(data['Gender'].str.strip()=="Male"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature2')
        HpTS2_female= data.loc[(data['Gender'].str.strip()=="Female"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature2')
        HpTS3_male= data.loc[(data['Gender'].str.strip()=="Male"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature3')
        HpTS3_female= data.loc[(data['Gender'].str.strip()=="Female"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature3')
        HpTS4_male= data.loc[(data['Gender'].str.strip()=="Male"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature4')
        HpTS4_female= data.loc[(data['Gender'].str.strip()=="Female"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature4')
        HpTS5_male= data.loc[(data['Gender'].str.strip()=="Male"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature5')
        HpTS5_female= data.loc[(data['Gender'].str.strip()=="Female"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature5')
    else:
        HpTS1_male= data.loc[(data['Gender'].str.strip()=="Male")&(data['HpAnswer']==sp_value), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature1')
        HpTS1_female= data.loc[(data['Gender'].str.strip()=="Female")&(data['HpAnswer']==sp_value), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature1')
        HpTS2_male= data.loc[(data['Gender'].str.strip()=="Male")&(data['HpAnswer']==sp_value), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature2')
        HpTS2_female= data.loc[(data['Gender'].str.strip()=="Female")&(data['HpAnswer']==sp_value), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature2')
        HpTS3_male= data.loc[(data['Gender'].str.strip()=="Male")&(data['HpAnswer']==sp_value), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature3')
        HpTS3_female= data.loc[(data['Gender'].str.strip()=="Female")&(data['HpAnswer']==sp_value), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature3')
        HpTS4_male= data.loc[(data['Gender'].str.strip()=="Male")&(data['HpAnswer']==sp_value), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature4')
        HpTS4_female= data.loc[(data['Gender'].str.strip()=="Female")&(data['HpAnswer']==sp_value), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature4')
        HpTS5_male= data.loc[(data['Gender'].str.strip()=="Male")&(data['HpAnswer']==sp_value), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='MaleFeature5')
        HpTS5_female= data.loc[(data['Gender'].str.strip()=="Female")&(data['HpAnswer']==sp_value), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='FemaleFeature5')

    s_range_gender['response_options']=['S1','S2','S3','S4','S5']      
    s_range_gender=s_range_gender.merge(HpTS1_male,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS1_female,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS2_male,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS2_female,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS3_male,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS3_female,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS4_male,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS4_female,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS5_male,on='score',how='outer')
    s_range_gender=s_range_gender.merge(HpTS5_female,on='score',how='outer')
    s_range_gender.fillna(0, inplace=True)
    fig2 = make_subplots(
        rows=5, cols=1,
        specs=[[{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}]],
        vertical_spacing=0.05)
     #subplot_titles=("F1", "F2", "F3", "F4","F5"))
    
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender["MaleFeature1"],\
                              name = "Male",showlegend=False,marker_color='#636EFA',text=s_range_gender["MaleFeature1"]),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender['FemaleFeature1'],\
                              name = "Female",showlegend=False,marker_color='#EF553B',text=s_range_gender['FemaleFeature1']),row=1, col=1)    
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender["MaleFeature2"],\
                              name = "Male",showlegend=False,marker_color ='#636EFA',text= s_range_gender["MaleFeature2"]),row=2, col=1)
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender['FemaleFeature2'],\
                              name = "Female",marker_color='#EF553B',showlegend=False,text=s_range_gender['FemaleFeature2']),row=2, col=1)   
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender["MaleFeature3"],\
                              name = "Male",marker_color='#636EFA',showlegend=False,text=s_range_gender["MaleFeature3"]),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender['FemaleFeature3'],\
                              name = "Female",marker_color='#EF553B',showlegend=False,text=s_range_gender['FemaleFeature3']),row=3, col=1)   
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender["MaleFeature4"],\
                              name = "Male",marker_color='#636EFA',showlegend=False,text=s_range_gender["MaleFeature4"]),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender['FemaleFeature4'],\
                              name = "Female",marker_color='#EF553B',showlegend=False,text=s_range_gender['FemaleFeature4']),row=4, col=1)   
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender["MaleFeature5"],\
                              name = "Male",marker_color='#636EFA',showlegend=False,text=s_range_gender["MaleFeature5"]),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_gender["response_options"],y= s_range_gender['FemaleFeature5'],\
                              name = "Female",marker_color='#EF553B',showlegend=False,text=s_range_gender['FemaleFeature5']),row=5, col=1)
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text= hpname(sp_value)+"<b> ranking score categorized gender</b>",
        barmode='group',
         font=dict(size=10),
         margin=dict(l=20, r=20, t=100, b=0),
    )
    fig2.update_yaxes(title_text="Feature 1", row=1, col=1)
    fig2.update_yaxes(title_text="Feature 2", row=2, col=1)
    fig2.update_yaxes(title_text="Feature 3", row=3, col=1)
    fig2.update_yaxes(title_text="Feature 4", row=4, col=1)
    fig2.update_yaxes(title_text="Feature 5", row=5, col=1)    
    return fig2


# In[16]:


#All headphone categorized status
def HC_status(sp_value):    
    s_range_status = pd.DataFrame({'score':[1,2,3,4,5]})
    if sp_value== "v0":
        HpTS1_single= data.loc[(data['Status'].str.strip()=="Single"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='SingleFeature1')
        HpTS1_married= data.loc[(data['Status'].str.strip()=="Married"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='MarriedFeature1')
        HpTS2_single= data.loc[(data['Status'].str.strip()=="Single"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='SingleFeature2')
        HpTS2_married= data.loc[(data['Status'].str.strip()=="Married"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='MarriedFeature2')
        HpTS3_single= data.loc[(data['Status'].str.strip()=="Single"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='SingleFeature3')
        HpTS3_married= data.loc[(data['Status'].str.strip()=="Married"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='MarriedFeature3')
        HpTS4_single= data.loc[(data['Status'].str.strip()=="Single"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='SingleFeature4')
        HpTS4_married= data.loc[(data['Status'].str.strip()=="Married"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='MarriedFeature4')
        HpTS5_single= data.loc[(data['Status'].str.strip()=="Single"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='SingleFeature5')
        HpTS5_married= data.loc[(data['Status'].str.strip()=="Married"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='MarriedFeature5')
    else:
    
         HpTS1_single= data.loc[(data['Status'].str.strip()=="Single")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='SingleFeature1')
         HpTS1_married= data.loc[(data['Status'].str.strip()=="Married")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='MarriedFeature1')
         HpTS2_single= data.loc[(data['Status'].str.strip()=="Single")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='SingleFeature2')
         HpTS2_married= data.loc[(data['Status'].str.strip()=="Married")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='MarriedFeature2')
         HpTS3_single= data.loc[(data['Status'].str.strip()=="Single")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='SingleFeature3')
         HpTS3_married= data.loc[(data['Status'].str.strip()=="Married")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='MarriedFeature3')
         HpTS4_single= data.loc[(data['Status'].str.strip()=="Single")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='SingleFeature4')
         HpTS4_married= data.loc[(data['Status'].str.strip()=="Married")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='MarriedFeature4')
         HpTS5_single= data.loc[(data['Status'].str.strip()=="Single")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='SingleFeature5')
         HpTS5_married= data.loc[(data['Status'].str.strip()=="Married")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='MarriedFeature5')

    s_range_status['response_options']=['S1','S2','S3','S4','S5']      
    s_range_status=s_range_status.merge(HpTS1_single,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS1_married,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS2_single,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS2_married,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS3_single,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS3_married,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS4_single,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS4_married,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS5_single,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS5_married,on='score',how='outer')
    s_range_status.fillna(0, inplace=True)

    fig2 = make_subplots(
        rows=5, cols=1,
        specs=[[{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}]],
        vertical_spacing=0.05)
    
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["SingleFeature1"],\
                         name = "Single",marker_color='#636EFA',showlegend=False,text=s_range_status["SingleFeature1"]),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status['MarriedFeature1'],\
                         name = "Married",marker_color='#EF553B',showlegend=False,text=s_range_status['MarriedFeature1']),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["SingleFeature2"],\
                         name = "Single",marker_color='#636EFA' ,showlegend=False,text=s_range_status["SingleFeature2"]),row=2, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status['MarriedFeature2'],\
                         name = "Married",marker_color='#EF553B',showlegend=False,text=s_range_status['MarriedFeature2']),row=2, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["SingleFeature3"],\
                         name = "Single",marker_color='#636EFA' ,showlegend=False,text= s_range_status["SingleFeature3"]),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status['MarriedFeature3'],\
                         name = "Married",marker_color='#EF553B',showlegend=False,text=s_range_status['MarriedFeature3']),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["SingleFeature4"],\
                         name = "Single",marker_color='#636EFA' ,showlegend=False,text=s_range_status["SingleFeature4"]),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status['MarriedFeature4'],\
                         name = "Married",marker_color='#EF553B',showlegend=False,text=s_range_status['MarriedFeature4']),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["SingleFeature5"],\
                         name = "Single",marker_color='#636EFA' ,showlegend=False,text=s_range_status["SingleFeature5"]),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status['MarriedFeature5'],\
                         name = "Married",marker_color='#EF553B',showlegend=False,text=s_range_status['MarriedFeature5']),row=5, col=1)
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text=hpname(sp_value)+"<b> ranking score categorized status</b>",
        barmode='group',
        font=dict(size=10),
         margin=dict(l=20, r=20, t=100, b=0),
    )
    fig2.update_yaxes(title_text="Feature 1", row=1, col=1)
    fig2.update_yaxes(title_text="Feature 2", row=2, col=1)
    fig2.update_yaxes(title_text="Feature 3", row=3, col=1)
    fig2.update_yaxes(title_text="Feature 4", row=4, col=1)
    fig2.update_yaxes(title_text="Feature 5", row=5, col=1)  
    #fig2.show()
    return fig2


# In[17]:


#All headphone categorized status
def FHC_question1(sp_value,cs_value):    
    s_range_status = pd.DataFrame({'score':[1,2,3,4,5]})
    dt = data.copy()
    for i in range(len(cs_value)):
      #  print(cs_value[i])
        dt = dt[dt[["Gender","Age","Status","Education","Occupation"]].\
                            apply(lambda row: row.astype(str).str.contains(cs_value[i], case=True).any(), axis=1)]
    if sp_value== "v0":
         HpTS1 = dt['HpTS1'].value_counts().rename_axis('score').reset_index(name='Feature1')
         HpTS2 = dt['HpTS2'].value_counts().rename_axis('score').reset_index(name='Feature2')
         HpTS3 = dt['HpTS3'].value_counts().rename_axis('score').reset_index(name='Feature3')
         HpTS4 = dt['HpTS4'].value_counts().rename_axis('score').reset_index(name='Feature4')
         HpTS5 = dt['HpTS5'].value_counts().rename_axis('score').reset_index(name='Feature5')
    else:
    
         HpTS1 = dt.loc[dt['HpAnswer']==sp_value, ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='Feature1')
         HpTS2 = dt.loc[dt['HpAnswer']==sp_value, ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='Feature2')
         HpTS3 = dt.loc[dt['HpAnswer']==sp_value, ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='Feature3')
         HpTS4 = dt.loc[dt['HpAnswer']==sp_value, ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='Feature4')
         HpTS5 = dt.loc[dt['HpAnswer']==sp_value, ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='Feature5')
         

    s_range_status['response_options']=['S1','S2','S3','S4','S5']      
    s_range_status=s_range_status.merge(HpTS1,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS2,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS3,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS4,on='score',how='outer')
    s_range_status=s_range_status.merge(HpTS5,on='score',how='outer')
    s_range_status.fillna(0, inplace=True)

    fig2 = make_subplots(
        rows=5, cols=1,
        specs=[[{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}]],
        vertical_spacing=0.05)
    
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["Feature1"],\
                         marker_color='crimson',showlegend=False,text=s_range_status["Feature1"]),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status['Feature2'],\
                         marker_color='crimson',showlegend=False,text=s_range_status['Feature2']),row=2, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["Feature3"],\
                         marker_color='crimson' ,showlegend=False,text=s_range_status["Feature3"]),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status['Feature4'],\
                         marker_color='crimson',showlegend=False,text=s_range_status['Feature4']),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_status["response_options"],y= s_range_status["Feature5"],\
                         marker_color='crimson' ,showlegend=False,text= s_range_status["Feature5"]),row=5, col=1)
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text=hpname(sp_value)+"<b> Ranking score categorized fields</b>",
        barmode='group',
        font=dict(size=10),
        margin=dict(l=80, r=80, t=50, b=50),
    )
    fig2.update_yaxes(title_text="Feature 1", row=1, col=1)
    fig2.update_yaxes(title_text="Feature 2", row=2, col=1)
    fig2.update_yaxes(title_text="Feature 3", row=3, col=1)
    fig2.update_yaxes(title_text="Feature 4", row=4, col=1)
    fig2.update_yaxes(title_text="Feature 5", row=5, col=1)  
    #fig2.show()
    return fig2


# In[18]:


#All headphone categorized age
def HC_age(sp_value):
    s_range_age = pd.DataFrame({'score':[1,2,3,4,5]})
    if sp_value == "v0":
        HpTS1_A1= data.loc[(data['Age'].str.strip()=="20-27"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature1')
        HpTS1_A2= data.loc[(data['Age'].str.strip()=="28-35"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature1')
        HpTS1_A3= data.loc[(data['Age'].str.strip()=="36-45"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature1')
        HpTS2_A1= data.loc[(data['Age'].str.strip()=="20-27"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature2')
        HpTS2_A2= data.loc[(data['Age'].str.strip()=="28-35"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature2')
        HpTS2_A3= data.loc[(data['Age'].str.strip()=="36-45"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature2') 
        HpTS3_A1= data.loc[(data['Age'].str.strip()=="20-27"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature3')
        HpTS3_A2= data.loc[(data['Age'].str.strip()=="28-35"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature3')
        HpTS3_A3= data.loc[(data['Age'].str.strip()=="36-45"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature3')
        HpTS4_A1= data.loc[(data['Age'].str.strip()=="20-27"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature4')
        HpTS4_A2= data.loc[(data['Age'].str.strip()=="28-35"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature4')
        HpTS4_A3= data.loc[(data['Age'].str.strip()=="36-45"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature4')
        HpTS5_A1= data.loc[(data['Age'].str.strip()=="20-27"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature5')
        HpTS5_A2= data.loc[(data['Age'].str.strip()=="28-35"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature5')
        HpTS5_A3= data.loc[(data['Age'].str.strip()=="36-45"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature5')
    else:
 
        HpTS1_A1= data.loc[(data['Age'].str.strip()=="20-27")&(data['HpAnswer']==sp_value), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature1')
        HpTS1_A2= data.loc[(data['Age'].str.strip()=="28-35")&(data['HpAnswer']==sp_value), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature1')
        HpTS1_A3= data.loc[(data['Age'].str.strip()=="36-45")&(data['HpAnswer']==sp_value), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature1')
        HpTS2_A1= data.loc[(data['Age'].str.strip()=="20-27")&(data['HpAnswer']==sp_value), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature2')
        HpTS2_A2= data.loc[(data['Age'].str.strip()=="28-35")&(data['HpAnswer']==sp_value), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature2')
        HpTS2_A3= data.loc[(data['Age'].str.strip()=="36-45")&(data['HpAnswer']==sp_value), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature2') 
        HpTS3_A1= data.loc[(data['Age'].str.strip()=="20-27")&(data['HpAnswer']==sp_value), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature3')
        HpTS3_A2= data.loc[(data['Age'].str.strip()=="28-35")&(data['HpAnswer']==sp_value), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature3')
        HpTS3_A3= data.loc[(data['Age'].str.strip()=="36-45")&(data['HpAnswer']==sp_value), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature3')
        HpTS4_A1= data.loc[(data['Age'].str.strip()=="20-27")&(data['HpAnswer']==sp_value), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature4')
        HpTS4_A2= data.loc[(data['Age'].str.strip()=="28-35")&(data['HpAnswer']==sp_value), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature4')
        HpTS4_A3= data.loc[(data['Age'].str.strip()=="36-45")&(data['HpAnswer']==sp_value), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature4')
        HpTS5_A1= data.loc[(data['Age'].str.strip()=="20-27")&(data['HpAnswer']==sp_value), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='A1Feature5')
        HpTS5_A2= data.loc[(data['Age'].str.strip()=="28-35")&(data['HpAnswer']==sp_value), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='A2Feature5')
        HpTS5_A3= data.loc[(data['Age'].str.strip()=="36-45")&(data['HpAnswer']==sp_value), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='A3Feature5')

    s_range_age['response_options']=['S1','S2','S3','S4','S5']      
    s_range_age=s_range_age.merge(HpTS1_A1,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS1_A2,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS1_A3,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS2_A1,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS2_A2,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS2_A3,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS3_A1,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS3_A2,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS3_A3,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS4_A1,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS4_A2,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS4_A3,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS5_A1,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS5_A2,on='score',how='outer')
    s_range_age=s_range_age.merge(HpTS5_A3,on='score',how='outer')
    s_range_age.fillna(0, inplace=True)

    fig2 = make_subplots(
        rows=5, cols=1,
        specs=[[{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}]],
        vertical_spacing=0.05)
    
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age["A1Feature1"],name = "Age 20-27",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_age["A1Feature1"]),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A2Feature1'],name = "Age 28-35",\
                              marker_color='#EF553B',showlegend=False,text=s_range_age['A2Feature1']),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age["A3Feature1"],name = "Age 36-45",\
                              marker_color='#00CC96' ,showlegend=False,text=s_range_age["A3Feature1"]),row=1, col=1) 
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A1Feature2'],name = "Age 20-27",\
                              marker_color='#636EFA',showlegend=False,text=s_range_age['A1Feature2']),row=2, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A2Feature2'],name = "Age 28-35",\
                              marker_color='#EF553B',showlegend=False,text=s_range_age['A2Feature2']),row=2, col=1) 
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A3Feature2'],name = "Age 36-45",\
                              marker_color='#00CC96',showlegend=False,text=s_range_age['A3Feature2']),row=2, col=1)  
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age["A1Feature3"],name = "Age 20-27",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_age["A1Feature3"]),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A2Feature3'],name = "Age 28-35",\
                              marker_color='#EF553B',showlegend=False,text=s_range_age['A2Feature3']),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A3Feature3'],name = "Age 36-45",\
                              marker_color='#00CC96',showlegend=False,text=s_range_age['A3Feature3']),row=3, col=1)  
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age["A1Feature4"],name = "Age 20-27",\
                              marker_color='#636EFA',showlegend=False,text=s_range_age["A1Feature4"]),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A2Feature4'],name = "Age 28-35",\
                              marker_color='#EF553B',showlegend=False,text=s_range_age['A2Feature4']),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A3Feature4'],name = "Age 36-45",\
                              marker_color='#00CC96',showlegend=False,text=s_range_age['A3Feature4']),row=4, col=1)   
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age["A1Feature5"],name = "Age 20-27",\
                              marker_color='#636EFA',showlegend=False,text=s_range_age["A1Feature5"]),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A2Feature5'],name = "Age 28-35",\
                              marker_color='#EF553B',showlegend=False,text=s_range_age['A2Feature5']),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_age["response_options"],y= s_range_age['A3Feature5'],name = "Age 36-45",\
                              marker_color='#00CC96',showlegend=False,text=s_range_age['A3Feature5']),row=5, col=1)
    
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text=hpname(sp_value)+"<b> ranking score categorized age</b>",
        barmode='group',
        font=dict(size=10),
         margin=dict(l=20, r=20, t=100, b=0),
    )
    fig2.update_yaxes(title_text="Feature 1", row=1, col=1)
    fig2.update_yaxes(title_text="Feature 2", row=2, col=1)
    fig2.update_yaxes(title_text="Feature 3", row=3, col=1)
    fig2.update_yaxes(title_text="Feature 4", row=4, col=1)
    fig2.update_yaxes(title_text="Feature 5", row=5, col=1)  
    return fig2


# In[19]:


#All headphone categorized age
def HC_education(sp_value):
    s_range_edu = pd.DataFrame({'score':[1,2,3,4,5]})
    if sp_value =="v0":
        HpTS1_E1= data.loc[(data['Education'].str.strip()=="Graduate"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='E1Feature1')
        HpTS1_E2= data.loc[(data['Education'].str.strip()=="Undergraduate"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='E2Feature1')
        HpTS1_E3= data.loc[(data['Education'].str.strip()=="High School"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='E3Feature1')
        HpTS1_E4= data.loc[(data['Education'].str.strip()=="Other education"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='E4Feature1')   
        HpTS2_E1= data.loc[(data['Education'].str.strip()=="Graduate"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='E1Feature2')
        HpTS2_E2= data.loc[(data['Education'].str.strip()=="Undergraduate"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='E2Feature2')
        HpTS2_E3= data.loc[(data['Education'].str.strip()=="High School"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='E3Feature2')
        HpTS2_E4= data.loc[(data['Education'].str.strip()=="Other education"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='E4Feature2')   
        HpTS3_E1= data.loc[(data['Education'].str.strip()=="Graduate"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='E1Feature3')
        HpTS3_E2= data.loc[(data['Education'].str.strip()=="Undergraduate"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='E2Feature3')
        HpTS3_E3= data.loc[(data['Education'].str.strip()=="High School"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='E3Feature3')
        HpTS3_E4= data.loc[(data['Education'].str.strip()=="Other education"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='E4Feature3')  
        HpTS4_E1= data.loc[(data['Education'].str.strip()=="Graduate"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='E1Feature4')
        HpTS4_E2= data.loc[(data['Education'].str.strip()=="Undergraduate"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='E2Feature4')
        HpTS4_E3= data.loc[(data['Education'].str.strip()=="High School"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='E3Feature4')
        HpTS4_E4= data.loc[(data['Education'].str.strip()=="Other education"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='E4Feature4')
        HpTS5_E1= data.loc[(data['Education'].str.strip()=="Graduate"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='E1Feature5')
        HpTS5_E2= data.loc[(data['Education'].str.strip()=="Undergraduate"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='E2Feature5')
        HpTS5_E3= data.loc[(data['Education'].str.strip()=="High School"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='E3Feature5')
        HpTS5_E4= data.loc[(data['Education'].str.strip()=="Other education"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='E4Feature5')
    else:   
        HpTS1_E1= data.loc[(data['Education'].str.strip()=="Graduate")&(data['HpAnswer']==sp_value), ['HpTS1']].\
        value_counts().rename_axis('score').reset_index(name='E1Feature1')
        HpTS1_E2= data.loc[(data['Education'].str.strip()=="Undergraduate")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='E2Feature1')
        HpTS1_E3= data.loc[(data['Education'].str.strip()=="High School")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='E3Feature1')
        HpTS1_E4= data.loc[(data['Education'].str.strip()=="Other education")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='E4Feature1')   
        HpTS2_E1= data.loc[(data['Education'].str.strip()=="Graduate")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='E1Feature2')
        HpTS2_E2= data.loc[(data['Education'].str.strip()=="Undergraduate")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='E2Feature2')
        HpTS2_E3= data.loc[(data['Education'].str.strip()=="High School")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='E3Feature2')
        HpTS2_E4= data.loc[(data['Education'].str.strip()=="Other education")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='E4Feature2')   
        HpTS3_E1= data.loc[(data['Education'].str.strip()=="Graduate")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='E1Feature3')
        HpTS3_E2= data.loc[(data['Education'].str.strip()=="Undergraduate")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='E2Feature3')
        HpTS3_E3= data.loc[(data['Education'].str.strip()=="High School")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='E3Feature3')
        HpTS3_E4= data.loc[(data['Education'].str.strip()=="Other education")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='E4Feature3')  
        HpTS4_E1= data.loc[(data['Education'].str.strip()=="Graduate")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='E1Feature4')
        HpTS4_E2= data.loc[(data['Education'].str.strip()=="Undergraduate")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='E2Feature4')
        HpTS4_E3= data.loc[(data['Education'].str.strip()=="High School")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='E3Feature4')
        HpTS4_E4= data.loc[(data['Education'].str.strip()=="Other education")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='E4Feature4')
        HpTS5_E1= data.loc[(data['Education'].str.strip()=="Graduate")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='E1Feature5')
        HpTS5_E2= data.loc[(data['Education'].str.strip()=="Undergraduate")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='E2Feature5')
        HpTS5_E3= data.loc[(data['Education'].str.strip()=="High School")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='E3Feature5')
        HpTS5_E4= data.loc[(data['Education'].str.strip()=="Other education")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='E4Feature5')
    
    s_range_edu['response_options']=['S1','S2','S3','S4','S5']      
    s_range_edu=s_range_edu.merge(HpTS1_E1,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS1_E2,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS1_E3,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS1_E4,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS2_E1,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS2_E2,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS2_E3,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS2_E4,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS3_E1,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS3_E2,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS3_E3,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS3_E4,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS4_E1,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS4_E2,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS4_E3,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS4_E4,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS5_E1,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS5_E2,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS5_E3,on='score',how='outer')
    s_range_edu=s_range_edu.merge(HpTS5_E4,on='score',how='outer')
    s_range_edu.fillna(0, inplace=True)

    fig2 = make_subplots(
        rows=5, cols=1,
        specs=[[{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}]],
        vertical_spacing=0.05)
    
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu["E1Feature1"],name = "Graduate",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_edu["E1Feature1"]),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E2Feature1'],name = "Undergraduate",\
                              marker_color='#EF553B',showlegend=False,text=s_range_edu['E2Feature1']),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu["E3Feature1"],name = "High School",\
                              marker_color='#00CC96' ,showlegend=False,text=s_range_edu["E3Feature1"]),row=1, col=1) 
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu["E4Feature1"],name = "Other education",\
                              marker_color='#AB63FA' ,showlegend=False,text=s_range_edu["E4Feature1"]),row=1, col=1) 
    
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E1Feature2'],name = "Graduate",\
                              marker_color='#636EFA',showlegend=False,text=s_range_edu['E1Feature2']),row=2, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E2Feature2'],name = "Undergraduate",\
                              marker_color='#EF553B',showlegend=False,text=s_range_edu['E2Feature2']),row=2, col=1) 
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E3Feature2'],name = "High School",\
                              marker_color='#00CC96',showlegend=False,text=s_range_edu['E3Feature2']),row=2, col=1) 
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E4Feature2'],name = "Other education",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_edu['E4Feature2']),row=2, col=1)  
    
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu["E1Feature3"],name = "Graduate",\
                              marker_color='#636EFA',showlegend=False,text=s_range_edu["E1Feature3"]),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E2Feature3'],name = "Undergraduate",\
                              marker_color='#EF553B',showlegend=False,text=s_range_edu['E2Feature3']),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E3Feature3'],name = "High School",\
                              marker_color='#00CC96',showlegend=False,text=s_range_edu['E3Feature3']),row=3, col=1) 
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E4Feature3'],name = "Other education",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_edu['E4Feature3']),row=3, col=1)
    
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu["E1Feature4"],name = "Graduate",\
                              marker_color='#636EFA',showlegend=False,text=s_range_edu["E1Feature4"]),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E2Feature4'],name = "Undergraduate",\
                              marker_color='#EF553B',showlegend=False,text=s_range_edu['E2Feature4']),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E3Feature4'],name = "High School",\
                              marker_color='#00CC96',showlegend=False,text=s_range_edu['E3Feature4']),row=4, col=1)  
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E4Feature4'],name = "Other education",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_edu['E4Feature4']),row=4, col=1) 
    
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu["E1Feature5"],name = "Graduate",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_edu["E1Feature5"]),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E2Feature5'],name = "Undergraduate",\
                              marker_color='#EF553B',showlegend=False,text=s_range_edu['E2Feature5']),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E3Feature5'],name = "High School",\
                              marker_color='#00CC96',showlegend=False,text=s_range_edu['E3Feature5']),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_edu["response_options"],y= s_range_edu['E4Feature5'],name = "Other education",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_edu['E4Feature5']),row=5, col=1)
    
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text=hpname(sp_value)+"<b> ranking score categoried education</b>",
        barmode='group',
        font=dict(size=10),
        margin=dict(l=20, r=20, t=100, b=0),
    )
    fig2.update_yaxes(title_text="Feature 1", row=1, col=1)
    fig2.update_yaxes(title_text="Feature 2", row=2, col=1)
    fig2.update_yaxes(title_text="Feature 3", row=3, col=1)
    fig2.update_yaxes(title_text="Feature 4", row=4, col=1)
    fig2.update_yaxes(title_text="Feature 5", row=5, col=1)  
    return fig2


# In[20]:


#All headphone categorized age
def HC_occupation(sp_value):
    s_range_occ = pd.DataFrame({'score':[1,2,3,4,5]})
    if sp_value == "v0":
        HpTS1_O1= data.loc[(data['Occupation'].str.strip()=="Student"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='O1Feature1')
        HpTS1_O2= data.loc[(data['Occupation'].str.strip()=="Employee"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='O2Feature1')
        HpTS1_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='O3Feature1')
        HpTS1_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation"), ['HpTS1']].value_counts()\
        .rename_axis('score').reset_index(name='O4Feature1')   
        HpTS2_O1= data.loc[(data['Occupation'].str.strip()=="Student"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='O1Feature2')
        HpTS2_O2= data.loc[(data['Occupation'].str.strip()=="Employee"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='O2Feature2')
        HpTS2_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='O3Feature2')
        HpTS2_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation"), ['HpTS2']].value_counts()\
        .rename_axis('score').reset_index(name='O4Feature2')   
        HpTS3_O1= data.loc[(data['Occupation'].str.strip()=="Student"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='O1Feature3')
        HpTS3_O2= data.loc[(data['Occupation'].str.strip()=="Employee"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='O2Feature3')
        HpTS3_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='O3Feature3')
        HpTS3_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation"), ['HpTS3']].value_counts()\
        .rename_axis('score').reset_index(name='O4Feature3')  
        HpTS4_O1= data.loc[(data['Occupation'].str.strip()=="Student"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='O1Feature4')
        HpTS4_O2= data.loc[(data['Occupation'].str.strip()=="Employee"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='O2Feature4')
        HpTS4_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='O3Feature4')
        HpTS4_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation"), ['HpTS4']].value_counts()\
        .rename_axis('score').reset_index(name='O4Feature4')
        HpTS5_O1= data.loc[(data['Occupation'].str.strip()=="Student"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='O1Feature5')
        HpTS5_O2= data.loc[(data['Occupation'].str.strip()=="Employee"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='O2Feature5')
        HpTS5_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='O3Feature5')
        HpTS5_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation"), ['HpTS5']].value_counts()\
        .rename_axis('score').reset_index(name='O4Feature5')
    else:
        HpTS1_O1= data.loc[(data['Occupation'].str.strip()=="Student")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='O1Feature1')
        HpTS1_O2= data.loc[(data['Occupation'].str.strip()=="Employee")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='O2Feature1')
        HpTS1_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='O3Feature1')
        HpTS1_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation")&(data['HpAnswer']==sp_value), ['HpTS1']]\
        .value_counts().rename_axis('score').reset_index(name='O4Feature1')   
        HpTS2_O1= data.loc[(data['Occupation'].str.strip()=="Student")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='O1Feature2')
        HpTS2_O2= data.loc[(data['Occupation'].str.strip()=="Employee")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='O2Feature2')
        HpTS2_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='O3Feature2')
        HpTS2_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation")&(data['HpAnswer']==sp_value), ['HpTS2']]\
        .value_counts().rename_axis('score').reset_index(name='O4Feature2')   
        HpTS3_O1= data.loc[(data['Occupation'].str.strip()=="Student")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='O1Feature3')
        HpTS3_O2= data.loc[(data['Occupation'].str.strip()=="Employee")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='O2Feature3')
        HpTS3_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='O3Feature3')
        HpTS3_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation")&(data['HpAnswer']==sp_value), ['HpTS3']]\
        .value_counts().rename_axis('score').reset_index(name='O4Feature3')  
        HpTS4_O1= data.loc[(data['Occupation'].str.strip()=="Student")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='O1Feature4')
        HpTS4_O2= data.loc[(data['Occupation'].str.strip()=="Employee")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='O2Feature4')
        HpTS4_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='O3Feature4')
        HpTS4_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation")&(data['HpAnswer']==sp_value), ['HpTS4']]\
        .value_counts().rename_axis('score').reset_index(name='O4Feature4')
        HpTS5_O1= data.loc[(data['Occupation'].str.strip()=="Student")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='O1Feature5')
        HpTS5_O2= data.loc[(data['Occupation'].str.strip()=="Employee")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='O2Feature5')
        HpTS5_O3= data.loc[(data['Occupation'].str.strip()=="Business Owner")&(data['HpAnswer']==sp_value), ['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='O3Feature5')
        HpTS5_O4= data.loc[(data['Occupation'].str.strip()=="Other occupation")&(data['HpAnswer']==sp_value),['HpTS5']]\
        .value_counts().rename_axis('score').reset_index(name='O4Feature5')
    
    s_range_occ['response_options']=['S1','S2','S3','S4','S5']      
    s_range_occ=s_range_occ.merge(HpTS1_O1,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS1_O2,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS1_O3,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS1_O4,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS2_O1,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS2_O2,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS2_O3,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS2_O4,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS3_O1,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS3_O2,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS3_O3,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS3_O4,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS4_O1,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS4_O2,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS4_O3,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS4_O4,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS5_O1,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS5_O2,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS5_O3,on='score',how='outer')
    s_range_occ=s_range_occ.merge(HpTS5_O4,on='score',how='outer')
    s_range_occ.fillna(0, inplace=True)
 
    fig2 = make_subplots(
        rows=5, cols=1,
        specs=[[{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}],
               [{"rowspan": 1,"colspan": 1}]],
        vertical_spacing=0.05)
    
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ["O1Feature1"],name = "Student",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_occ["O1Feature1"]),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O2Feature1'],name = "Employee",\
                              marker_color='#EF553B',showlegend=False,text=s_range_occ['O2Feature1']),row=1, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ["O3Feature1"],name = "Business Owner",\
                              marker_color='#00CC96' ,showlegend=False,text=s_range_occ["O3Feature1"]),row=1, col=1) 
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ["O4Feature1"],name = "Other occupation",\
                              marker_color='#AB63FA' ,showlegend=False,text=s_range_occ["O4Feature1"]),row=1, col=1) 
    
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O1Feature2'],name = "Student",\
                              marker_color='#636EFA',showlegend=False,text=s_range_occ['O1Feature2']),row=2, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O2Feature2'],name = "Employee",\
                              marker_color='#EF553B',showlegend=False,text=s_range_occ['O2Feature2']),row=2, col=1) 
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O3Feature2'],name = "Business Owner",\
                              marker_color='#00CC96',showlegend=False,text=s_range_occ['O3Feature2']),row=2, col=1) 
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O4Feature2'],name = "Other occupation",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_occ['O4Feature2']),row=2, col=1)  
    
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ["O1Feature3"],name = "Student",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_occ["O1Feature3"]),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O2Feature3'],name = "Employee",\
                              marker_color='#EF553B',showlegend=False,text=s_range_occ['O2Feature3']),row=3, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O3Feature3'],name = "Business Owner",\
                              marker_color='#00CC96',showlegend=False,text=s_range_occ['O3Feature3']),row=3, col=1) 
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O4Feature3'],name = "Other occupation",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_occ['O4Feature3']),row=3, col=1)
    
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ["O1Feature4"],name = "Student",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_occ["O1Feature4"]),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O2Feature4'],name = "Employee",\
                              marker_color='#EF553B',showlegend=False,text=s_range_occ['O2Feature4']),row=4, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O3Feature4'],name = "Business Owner",\
                              marker_color='#00CC96',showlegend=False,text=s_range_occ['O3Feature4']),row=4, col=1)  
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O4Feature4'],name = "Other occupation",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_occ['O4Feature4']),row=4, col=1) 
    
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ["O1Feature5"],name = "Student",\
                              marker_color='#636EFA' ,showlegend=False,text=s_range_occ["O1Feature5"]),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O2Feature5'],name = "Employee",\
                              marker_color='#EF553B',showlegend=False,text=s_range_occ['O2Feature5']),row=5, col=1)
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O3Feature5'],name = "Business Owner",\
                              marker_color='#00CC96',showlegend=False,text=s_range_occ['O3Feature5']),row=5, col=1)  
    fig2.add_trace(go.Bar(x= s_range_occ["response_options"],y= s_range_occ['O4Feature5'],name = "Other occupation",\
                              marker_color='#AB63FA',showlegend=False,text=s_range_occ['O4Feature5']),row=5, col=1) 
    fig2.update_layout(height=500,showlegend=True)
    fig2.update_layout(
        title_text=hpname(sp_value)+"<b> ranking score categoried occupation</b>",
        barmode='group',
        font=dict(size=10),
        margin=dict(l=20, r=20, t=100, b=0),
    )
    fig2.update_yaxes(title_text="Feature 1", row=1, col=1)
    fig2.update_yaxes(title_text="Feature 2", row=2, col=1)
    fig2.update_yaxes(title_text="Feature 3", row=3, col=1)
    fig2.update_yaxes(title_text="Feature 4", row=4, col=1)
    fig2.update_yaxes(title_text="Feature 5", row=5, col=1)  
    return fig2


# In[21]:


def feature_selection_defined(a):
    for i in range(len(a)):
        if(a[i]=="C_Male"):
            a[i] = "Male"
        if(a[i]=="C_Female"):
            a[i] = "Female"
        if(a[i]=="C_Single"):
            a[i]= "Single"
        if(a[i]=="C_Married"):
            a[i]= "Married"
        if(a[i]=="C_A1"):
            a[i]= "Age 20-27"
        if(a[i]=="C_A2"):
            a[i]= "Age 28-35"
        if(a[i]=="C_A3"):
            a[i]= "Age 36-45"
        if(a[i]=="C_E1"):
            a[i]= "Graduate"
        if(a[i]=="C_E2"):
            a[i]= "Undergraduate"
        if(a[i]=="C_E3"):
            a[i]= "High School"
        if(a[i]=="C_E4"):
            a[i]= "Other education"
        if(a[i]=="C_O1"):
            a[i]= "Student"
        if(a[i]=="C_O2"):
            a[i]= "Employee"
        if(a[i]=="C_O3"):
            a[i]= "Business Owner"
        if(a[i]=="C_O4"):
            a[i]= "Other occupation"
    return a


# In[22]:


def rtable_answer(sp_value):
    if(sp_value=="v0"):
        stadata=data[["HpTS1","HpTS2","HpTS3","HpTS4","HpTS5"]].\
        describe(include='all').applymap('{:.2f}'.format)
        hname= "All HPs"
    elif(sp_value!="v0"):
        stadata = data[["HpTS1","HpTS2","HpTS3","HpTS4","HpTS5"]]\
            .loc[data['HpAnswer']==sp_value].describe(include='all').applymap('{:.2f}'.format)
        hname= "HP-"+sp_value
        
    table_header=["<b>Stat.</b>",'<b>F1</b>','<b>F2</b>','<b>F3</b>',\
                  '<b>F4</b>','<b>F5</b>']    
    rtable = go.Figure(data=[go.Table( columnorder = [1,2,3,4,5,6,7,8,9],      
                header=dict(values=table_header,                                   
                line_color='#E5ECF6',
                fill=dict(color=['#6BAED6', 'white']),
                align='center',
                font = dict(color = 'black', size = 12)),\
                cells=dict(values=[stadata.index,stadata["HpTS1"],stadata["HpTS2"],stadata["HpTS3"],
                                    stadata["HpTS4"],stadata["HpTS5"]],
                line_color='#E5ECF6',
                fill=dict(color=['#6BAED6', 'white']),
                align='left',
                font = dict(color = 'black', size = 12),
                height=30
                  ))
                ])
    rtable.update_layout(title=hpname(sp_value)+"<b> ranking statistics data</b>",\
                         margin=dict(l=35, r=20, t=105, b=0))
    return  rtable   
    
def q2_table(sp_value):
    if(sp_value=="v0"):
        stadata=data[["InfoHps_online","InfoHps_Social","InfoHps_Google","InfoHps_PR","InfoHps_Ads"]].\
        describe(include='all').applymap('{:.2f}'.format)
        hname= "All HPs"
    elif(sp_value!="v0"):
        stadata = data[["InfoHps_online","InfoHps_Social","InfoHps_Google","InfoHps_PR","InfoHps_Ads"]]\
            .loc[data['HpAnswer']==sp_value].describe(include='all').applymap('{:.2f}'.format)
        hname= "HP-"+sp_value
    
    table_header=["<b>Stat.</b>",'<b>Online</b>','<b>Social</b>','<b>Google</b>',\
                  '<b>Friend</b>','<b>Ads.</b>']    
    q2table = go.Figure(data=[go.Table( columnorder = [1,2,3,4,5,6,7,8,9],      
                header=dict(values=table_header,                                   
                line_color='#E5ECF6',
                fill=dict(color=['#6BAED6', 'white']),
                align='center',
                font = dict(color = 'black', size = 12)),\
                cells=dict(values=[stadata.index,stadata["InfoHps_online"],stadata["InfoHps_Social"],stadata["InfoHps_Google"],
                                    stadata["InfoHps_PR"],stadata["InfoHps_Ads"]],
                line_color='#E5ECF6',
                fill=dict(color=['#6BAED6', 'white']),
                align='left',
                font = dict(color = 'black', size = 12),
                height=30
                  ))
                ])
    q2table.update_layout(title=hpname(sp_value)+"<b> Info statistics data</b>",\
                         margin=dict(l=35, r=20, t=105, b=0))


    return  q2table

def q7_table(sp_value):
    if(sp_value=="v0"):
        stadata=data[["PB_nosound","PB_disconnect","PB_badsound","PB_unfit","PB_oneear","PB_battery","PB_toosd",\
               "PB_audiocut","PB_unplug"]].describe(include='all').applymap('{:.2f}'.format)
        hname= "All HPs"
    elif(sp_value!="v0"):
        stadata = data[["PB_nosound","PB_disconnect","PB_badsound","PB_unfit","PB_oneear","PB_battery","PB_toosd",\
               "PB_audiocut","PB_unplug"]].loc[data['HpAnswer']==sp_value].describe(include='all').applymap('{:.2f}'.format)
        hname= "HP-"+sp_value
    
 
    table_header=["<b>Stat.</b>",'<b>NoSO.</b>','<b>Disc.</b>','<b>SOqL</b>',\
                  '<b>Unfit</b>','<b>OneEar</b>','<b>Batt.</b>','<b>SOLe.</b>','<b>SOCut</b>',\
                  '<b>Unplug</b>']    
    q7table = go.Figure(data=[go.Table( columnorder = [1,2,3,4,5,6,7,8,9,10],      
                header=dict(values=table_header,                                   
                line_color='#E5ECF6',
                fill=dict(color=['#6BAED6', 'white']),
                align='center',
                font = dict(color = 'black', size = 10)),\
                cells=dict(values=[stadata.index,stadata["PB_nosound"],stadata["PB_disconnect"],\
                                   stadata["PB_badsound"],stadata["PB_unfit"],stadata["PB_oneear"],\
                                   stadata["PB_battery"],stadata["PB_toosd"],stadata["PB_audiocut"],\
                                   stadata["PB_unplug"]],
                line_color='#E5ECF6',
                fill=dict(color=['#6BAED6', 'white']),
                align='left',
                font = dict(color = 'black', size = 10),
                #height=30
                  ))
                ])
    q7table.update_layout(title=hpname(sp_value)+"<b> Problem statistics data</b>",\
                         margin=dict(l=35, r=20, t=105, b=0))


    return  q7table
        


# In[23]:


def show_cc_questions(sp_value,sq_value):
    if(sp_value=="v0"):
       stadata = data[sq_value].value_counts()
    else:
       stadata = data[sq_value].loc[data['HpAnswer']==sp_value].value_counts()
    hname = hpname(sp_value)     
    fig2 = go.Figure(data=[go.Pie(labels=stadata.index, values=stadata.values, textinfo='percent',
                             insidetextorientation='radial')]) 
    if(sq_value=="NumberHps"):
        fig2.update_layout(title_text="<b>Q1-</b>"+hname+"<b> Headphones number</b>")
    elif(sq_value=="ActivityHps"):
        fig2.update_layout(title_text="<b>Q3-</b>"+hname+"<b> Best activity </b>")
    elif(sq_value=="TimeHps"):
        fig2.update_layout(title_text="<b>Q4-</b>"+hname+"<b> Latest time to buy </b>")
    elif(sq_value=="PriceHps"):
        fig2.update_layout(title_text="<b>Q5-</b>"+hname+"<b> Price affordable</b>")
    elif(sq_value=="PlaceHps"):
        fig2.update_layout(title_text="<b>Q6-</b>"+hname+"<b> Place to buy</b>")
    elif(sq_value=="FactorHps"):
        fig2.update_layout(title_text="<b>Q8-</b>"+hname+"<b> Factor to buy</b>")
    elif(sq_value=="HealthHps"):
        fig2.update_layout(title_text="<b>Q9-</b>"+hname+"<b> Health Concern</b>")
    elif(sq_value=="InnovationHps"):
        fig2.update_layout(title_text="<b>Q10-</b>"+hname+"<b> Innovation</b>")
    fig2.update_layout(
         font=dict(size=12),
         margin=dict(l=30, r=20, t=120, b=20),      
    )
        
    return fig2


# In[24]:


def sum_answers(sp_value,sq_value):
    if(sp_value=="v0"):
        asum = int(data[sq_value].sum())
        femalesum = int(data[sq_value].loc[(data['Gender'].str.strip()=="Female")].sum())
        malesum = int(data[sq_value].loc[(data['Gender'].str.strip()=="Male")].sum())
        singlesum = int(data[sq_value].loc[(data['Status'].str.strip()=="Single")].sum())
        marriedsum = int(data[sq_value].loc[(data['Status'].str.strip()=="Married")].sum())
        a1sum = int(data[sq_value].loc[(data['Age'].str.strip()=="20-27")].sum())
        a2sum = int(data[sq_value].loc[(data['Age'].str.strip()=="28-35")].sum())
        a3sum = int(data[sq_value].loc[(data['Age'].str.strip()=="36-45")].sum())
        e1sum = int(data[sq_value].loc[(data['Education'].str.strip()=="Graduate")].sum())
        e2sum = int(data[sq_value].loc[(data['Education'].str.strip()=="Undergraduate")].sum())
        e3sum = int(data[sq_value].loc[(data['Education'].str.strip()=="High School")].sum())
        e4sum = int(data[sq_value].loc[(data['Education'].str.strip()=="Other education")].sum())
        o1sum = int(data[sq_value].loc[(data['Occupation'].str.strip()=="Employee")].sum())
        o2sum = int(data[sq_value].loc[(data['Occupation'].str.strip()=="Business Owner")].sum())
        o3sum = int(data[sq_value].loc[(data['Occupation'].str.strip()=="Student")].sum())
        o4sum = int(data[sq_value].loc[(data['Occupation'].str.strip()=="Other occupation")].sum())
    
    elif(sp_value!="v0"):
        asum = int(data[sq_value].loc[data['HpAnswer']==sp_value].sum())
        femalesum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Gender'].str.strip()=="Female")].sum())
        malesum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Gender'].str.strip()=="Male")].sum())
        singlesum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Status'].str.strip()=="Single")].sum())
        marriedsum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Status'].str.strip()=="Married")].sum())
        a1sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="20-27")].sum())
        a2sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="28-35")].sum())
        a3sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="36-45")].sum())
        e1sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Graduate")].sum())
        e2sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Undergraduate")].sum())
        e3sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="High School")].sum())
        e4sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Other education")].sum())
        o1sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Employee")].sum())
        o2sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Business Owner")].sum())
        o3sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Student")].sum())
        o4sum = int(data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Other occupation")].sum())
        
    return asum,femalesum,malesum,singlesum,marriedsum,a1sum,a2sum,a3sum,e1sum,e2sum,\
          e3sum,e4sum,o1sum,o2sum,o3sum,o4sum


# In[25]:


def sum_answers_field(sp_value,sq_value,cs_value):
    dt = data.copy()
    for i in range(len(cs_value)):
      #  print(cs_value[i])
        dt = dt[dt[["Gender","Age","Status","Education","Occupation"]].\
                            apply(lambda row: row.astype(str).str.contains(cs_value[i], case=True).any(), axis=1)]
    if(sp_value=="v0"):
        asum = int(dt[sq_value].sum())
    elif(sp_value!="v0"):
        asum = int(dt[sq_value].loc[dt['HpAnswer']==sp_value].sum())
        
    return asum


# In[26]:


def show_hc_questions(sp_value,sc_value,sq_value):
    #"NumberHps","ActivityHps","TimeHps","PriceHps","FactorHps","HealthHps","InnovationHps","PlaceHps"
    if(sp_value=="v0"):
        stadata = data[sq_value].value_counts()
        stadata_female = data[sq_value].loc[(data['Gender'].str.strip()=="Female")].value_counts()
        stadata_male = data[sq_value].loc[(data['Gender'].str.strip()=="Male")].value_counts()
        stadata_single = data[sq_value].loc[(data['Status'].str.strip()=="Single")].value_counts()
        stadata_married = data[sq_value].loc[(data['Status'].str.strip()=="Married")].value_counts()
        stadata_a1 = data[sq_value].loc[(data['Age'].str.strip()=="20-27")].value_counts()
        stadata_a2 = data[sq_value].loc[(data['Age'].str.strip()=="28-35")].value_counts()
        stadata_a3 = data[sq_value].loc[(data['Age'].str.strip()=="36-45")].value_counts()
        stadata_e1 = data[sq_value].loc[(data['Education'].str.strip()=="Graduate")].value_counts()
        stadata_e2 = data[sq_value].loc[(data['Education'].str.strip()=="Undergraduate")].value_counts()
        stadata_e3 = data[sq_value].loc[(data['Education'].str.strip()=="High School")].value_counts()
        stadata_e4 = data[sq_value].loc[(data['Education'].str.strip()=="Other education")].value_counts()
        stadata_o1 = data[sq_value].loc[(data['Occupation'].str.strip()=="Employee")].value_counts()
        stadata_o2 = data[sq_value].loc[(data['Occupation'].str.strip()=="Business Owner")].value_counts()
        stadata_o3 = data[sq_value].loc[(data['Occupation'].str.strip()=="Student")].value_counts()
        stadata_o4 = data[sq_value].loc[(data['Occupation'].str.strip()=="Other occupation")].value_counts()
    
    elif(sp_value!="v0"):
        stadata = data[sq_value].loc[data['HpAnswer']==sp_value].value_counts()
        stadata_female = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Gender'].str.strip()=="Female")].value_counts()
        stadata_male = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Gender'].str.strip()=="Male")].value_counts()
        stadata_single = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Status'].str.strip()=="Single")].value_counts()
        stadata_married = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Status'].str.strip()=="Married")].value_counts()
        stadata_a1 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="20-27")].value_counts()
        stadata_a2 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="28-35")].value_counts()
        stadata_a3 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Age'].str.strip()=="36-45")].value_counts()
        stadata_e1 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Graduate")].value_counts()
        stadata_e2 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Undergraduate")].value_counts()
        stadata_e3 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="High School")].value_counts()
        stadata_e4 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Education'].str.strip()=="Other education")].value_counts()
        stadata_o1 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Employee")].value_counts()
        stadata_o2 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Business Owner")].value_counts()
        stadata_o3 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Student")].value_counts()
        stadata_o4 = data[sq_value].loc[(data['HpAnswer']==sp_value)&(data['Occupation'].str.strip()=="Other occupation")].value_counts()
        
    
    fig3 = go.Figure()    
    if(sc_value=='none'):
        fig3.add_trace(go.Bar(x= stadata.index, y= stadata.values,text=stadata.values))
        stitle="<b> responses</b>"
    elif(sc_value=='gender'):  
        fig3.add_trace(go.Bar(x= stadata_male.index, y= stadata_male.values,name="Male",text= stadata_male.values))
        fig3.add_trace(go.Bar(x= stadata_female.index, y= stadata_female.values,name="Female",text= stadata_female.values))
        stitle="<b> Categorized gender</b>"
    elif(sc_value=='status'):  
        fig3.add_trace(go.Bar(x= stadata_single.index, y= stadata_single.values,name="Single", text= stadata_single.values))
        fig3.add_trace(go.Bar(x= stadata_married.index, y= stadata_married.values,name="Married",text= stadata_married.values))
        stitle="<b> Categorized status</b>"
    elif(sc_value=='age'):  
        fig3.add_trace(go.Bar(x= stadata_a1.index, y= stadata_a1.values,name="Age 20-27",text= stadata_a1.values))
        fig3.add_trace(go.Bar(x= stadata_a2.index, y= stadata_a2.values,name="Age 28-35",text= stadata_a2.values))
        fig3.add_trace(go.Bar(x= stadata_a3.index, y= stadata_a3.values,name="Age 36-45",text= stadata_a3.values))
        stitle="<b> Categorized age</b>"
    elif(sc_value=='education'): 
        fig3.add_trace(go.Bar(x= stadata_e1.index, y= stadata_e1.values,name="Graduate", text=stadata_e1.values))
        fig3.add_trace(go.Bar(x= stadata_e2.index, y= stadata_e2.values,name="Undergraduate", text=stadata_e2.values))
        fig3.add_trace(go.Bar(x= stadata_e3.index, y= stadata_e3.values,name="High School", text=stadata_e3.values))
        fig3.add_trace(go.Bar(x= stadata_e4.index, y= stadata_e4.values,name="Other education", text=stadata_e4.values))
        stitle="<b> Categorized education</b>"
    elif(sc_value=='occupation'):  
        fig3.add_trace(go.Bar(x= stadata_o1.index, y= stadata_o1.values,name="Employee", text= stadata_o1.values))
        fig3.add_trace(go.Bar(x= stadata_o2.index, y= stadata_o2.values,name="Business Owner", text= stadata_o2.values))
        fig3.add_trace(go.Bar(x= stadata_o3.index, y= stadata_o3.values,name="Student", text= stadata_o3.values))
        fig3.add_trace(go.Bar(x= stadata_o4.index, y= stadata_o4.values,name="Other occupation", text= stadata_o4.values))
        stitle="<b> Categorized occupation</b>"
    fig3.update_layout(title_text=qname(sq_value)+hpname(sp_value)+stitle)
    fig3.update_layout(
#        title_text="<b>Categorized Gender</b>",
        xaxis=dict(
            title= "Answers",          
        ),
        yaxis=dict(
            title= "Total Responses",          
        ),
        #yaxis_range=[0,50],
        font=dict(size=12),
        height=420,
        margin=dict(l=0, r=20, t=125, b=0),
    )
    return fig3


# In[27]:


def show_fhc_questions(sp_value,sq_value,cs_value):
    #"NumberHps","ActivityHps","TimeHps","PriceHps","FactorHps","HealthHps","InnovationHps","PlaceHps"
    if(sp_value=="v0"):       
        dt = data.copy()
        for i in range(len(cs_value)):
          #  print(cs_value[i])
            dt = dt[dt[["Gender","Age","Status","Education","Occupation"]].\
                                apply(lambda row: row.astype(str).str.contains(cs_value[i], case=True).any(), axis=1)]
        stadata = dt[sq_value].value_counts()
    elif(sp_value!="v0"):
        dt = data.copy()
        for i in range(len(cs_value)):
          #  print(cs_value[i])
            dt = dt[dt[["Gender","Age","Status","Education","Occupation"]].\
                                apply(lambda row: row.astype(str).str.contains(cs_value[i], case=True).any(), axis=1)]
        stadata = dt[sq_value].loc[dt['HpAnswer']==sp_value].value_counts()
 
    fig3 = go.Figure()     
    fig3.add_trace(go.Bar(x= stadata.index, y= stadata.values,text=stadata.values,marker_color='crimson'))
    stitle="<b> Categorized Fields</b>"
    fig3.update_layout(title_text=qname(sq_value)+hpname(sp_value)+stitle)
    fig3.update_layout(
#        title_text="<b>Categorized Gender</b>",
        xaxis=dict(
            title= "Answers",          
        ),
        yaxis=dict(
            title= "Total Responses",          
        ),
        #yaxis_range=[0,50],
        font=dict(size=12),
        height=420,
        margin=dict(l=80, r=80, t=50, b=50),
    )
    return fig3


# In[28]:


def show_graph2_q2(sp_value):
    xname=["Online Site","Social Media","Google","Friend","Advertising"]
    g1= sum_answers(sp_value,"InfoHps_online")
    g2= sum_answers(sp_value,"InfoHps_Social")
    g3= sum_answers(sp_value,"InfoHps_Google")
    g4= sum_answers(sp_value,"InfoHps_PR")
    g5= sum_answers(sp_value,"InfoHps_Ads")
    pg1 = "{:.0%}".format((g1[0]/(g1[0]+g2[0]+g3[0]+g4[0]+g5[0])))
    pg2 = "{:.0%}".format((g2[0]/(g1[0]+g2[0]+g3[0]+g4[0]+g5[0])))
    pg3 = "{:.0%}".format((g3[0]/(g1[0]+g2[0]+g3[0]+g4[0]+g5[0])))
    pg4 = "{:.0%}".format((g4[0]/(g1[0]+g2[0]+g3[0]+g4[0]+g5[0])))
    pg5 = "{:.0%}".format((g5[0]/(g1[0]+g2[0]+g3[0]+g4[0]+g5[0])))
    fig2 = go.Figure()    
    fig2.add_trace(go.Bar(y= xname, x= [g1[0],g2[0],g3[0],g4[0],g5[0]],text=[pg1,pg2,pg3,pg4,pg5], orientation='h'))
    stitle="<b> Information source</b>"
    
    fig2.update_layout(title_text="<b>Q2-</b>"+hpname(sp_value)+stitle,margin=dict(l=0, r=0, t=120, b=0))
    fig2.update_traces(textfont_size=12,textposition="inside")
    return fig2

def show_graph3_q2(sp_value,sc_value):
    xname=["Online Site","Social Media","Google","Friend","Advertising"]
    g1= sum_answers(sp_value,"InfoHps_online")
    g2= sum_answers(sp_value,"InfoHps_Social")
    g3= sum_answers(sp_value,"InfoHps_Google")
    g4= sum_answers(sp_value,"InfoHps_PR")
    g5= sum_answers(sp_value,"InfoHps_Ads")

    fig3 = go.Figure()    
    if(sc_value=='gender'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[2],g2[2],g3[2],g4[2],g5[2]],\
                              text=[g1[2],g2[2],g3[2],g4[2],g5[2]],name="Male"))
        fig3.add_trace(go.Bar(x= xname, y= [g1[1],g2[1],g3[1],g4[1],g5[1]],\
                              text=[g1[1],g2[1],g3[1],g4[1],g5[1]],name="Female"))
        stitle="<b> Categorized gender</b>"
    elif(sc_value=='status'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[3],g2[3],g3[3],g4[3],g5[3]],\
                              text=[g1[3],g2[3],g3[3],g4[3],g5[3]],name="Single"))
        fig3.add_trace(go.Bar(x= xname, y= [g1[4],g2[4],g3[4],g4[4],g5[4]],\
                              text=[g1[4],g2[4],g3[4],g4[4],g5[4]],name="Married"))
        stitle="<b> Categorized status</b>"    
    elif(sc_value=='age'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[5],g2[5],g3[5],g4[5],g5[5]],name="Age 20-27",\
                              text= [g1[5],g2[5],g3[5],g4[5],g5[5]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[6],g2[6],g3[6],g4[6],g5[6]],name="Age 28-35",\
                              text= [g1[6],g2[6],g3[6],g4[6],g5[6]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[7],g2[7],g3[7],g4[7],g5[7]],name="Age 36-45",\
                              text= [g1[7],g2[7],g3[7],g4[7],g5[7]]))
        stitle="<b> Categorized age</b>"
    elif(sc_value=='education'): 
        fig3.add_trace(go.Bar(x= xname, y= [g1[8],g2[8],g3[8],g4[8],g5[8]],name="Graduate",\
                              text=[g1[8],g2[8],g3[8],g4[8],g5[8]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[9],g2[9],g3[9],g4[9],g5[9]],name="Undergraduate",\
                              text=[g1[9],g2[9],g3[9],g4[9],g5[9]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[10],g2[10],g3[10],g4[10],g5[10]],name="High School",\
                              text=[g1[10],g2[10],g3[10],g4[10],g5[10]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[11],g2[11],g3[11],g4[11],g5[11]],name="Other education",\
                              text=[g1[11],g2[11],g3[11],g4[11],g5[11]]))
        stitle="<b> Categorized education</b>" 
    elif(sc_value=='occupation'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[12],g2[12],g3[12],g4[12],g5[12]],name="Employee",\
                              text= [g1[12],g2[12],g3[12],g4[12],g5[12]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[13],g2[13],g3[13],g4[13],g5[13]],name="Business Owner",\
                              text= [g1[13],g2[13],g3[13],g4[13],g5[13]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[14],g2[14],g3[14],g4[14],g5[14]],name="Student",\
                              text= [g1[14],g2[14],g3[14],g4[14],g5[14]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[15],g2[15],g3[15],g4[15],g5[15]],name="Other occupation",\
                              text= [g1[15],g2[15],g3[15],g4[15],g5[15]]))
        stitle="<b> Categorized occupation</b>"
    
    fig3.update_layout(title_text="<b>Q2-</b>"+hpname(sp_value)+stitle,margin=dict(l=0, r=0, t=70, b=0))
    fig3.update_traces(textfont_size=12)
    
    return fig3

def show_graph3_fq2(sp_value,cs_value):
    xname=["Online Site","Social Media","Google","Friend","Advertising"]
    g1= sum_answers_field(sp_value,"InfoHps_online",cs_value)
    g2= sum_answers_field(sp_value,"InfoHps_Social",cs_value)
    g3= sum_answers_field(sp_value,"InfoHps_Google",cs_value)
    g4= sum_answers_field(sp_value,"InfoHps_PR",cs_value)
    g5= sum_answers_field(sp_value,"InfoHps_Ads",cs_value)

    fig3 = go.Figure()    

    fig3.add_trace(go.Bar(x= xname, y= [g1,g2,g3,g4,g5],\
                          text= [g1,g2,g3,g4,g5],marker_color='crimson'))
    stitle="<b> Categorized Fields</b>"
    
    fig3.update_layout(title_text="<b>Q2-</b>"+hpname(sp_value)+stitle,margin=dict(l=80, r=80, t=50, b=50))
    fig3.update_traces(textfont_size=12)
    
    return fig3


# In[29]:


def show_graph2_q7(sp_value):
    xname=["Slient","Disconnect","Sound Quality","Unfit Design","Sound Level","Sound Cut",\
           "Battery","Jack Unplug","OneEar Usable"]
    g1= sum_answers(sp_value,"PB_nosound")
    g2= sum_answers(sp_value,"PB_disconnect")
    g3= sum_answers(sp_value,"PB_badsound")
    g4= sum_answers(sp_value,"PB_unfit")
    g5= sum_answers(sp_value,"PB_toosd")
    g6= sum_answers(sp_value,"PB_audiocut")
    g7= sum_answers(sp_value,"PB_battery")
    g8= sum_answers(sp_value,"PB_unplug")
    g9= sum_answers(sp_value,"PB_oneear")
    asum_q7 = g1[0]+g2[0]+g3[0]+g4[0]+g5[0]+g6[0]+g7[0]+g8[0]+g9[0]
    pg1 = "{:.0%}".format(g1[0]/asum_q7)
    pg2 = "{:.0%}".format(g2[0]/asum_q7)
    pg3 = "{:.0%}".format(g3[0]/asum_q7)
    pg4 = "{:.0%}".format(g4[0]/asum_q7)
    pg5 = "{:.0%}".format(g5[0]/asum_q7)
    pg6 = "{:.0%}".format(g6[0]/asum_q7)
    pg7 = "{:.0%}".format(g7[0]/asum_q7)
    pg8 = "{:.0%}".format(g8[0]/asum_q7)
    pg9 = "{:.0%}".format(g9[0]/asum_q7)
    fig2 = go.Figure()    
    fig2.add_trace(go.Bar(y= xname, x= [g1[0],g2[0],g3[0],g4[0],g5[0],g6[0],g7[0],g8[0],g9[0]],\
                                text=[pg1,pg2,pg3,pg4,pg5,pg6,pg7,pg8,pg9], orientation='h'))
    stitle="<b> Headphone problems</b>"
    
    fig2.update_layout(title_text="<b>Q7-</b>"+hpname(sp_value)+stitle,margin=dict(l=0, r=0, t=120, b=0))
    fig2.update_traces(textfont_size=12,textposition="inside")

    return fig2

def show_graph3_q7(sp_value,sc_value):
    xname=["Slient","Disconnect","Sound Quality","Unfit Design","Sound Level","Sound Cut",\
           "Battery","Jack Unplug","OneEar Usable"]
    g1= sum_answers(sp_value,"PB_nosound")
    g2= sum_answers(sp_value,"PB_disconnect")
    g3= sum_answers(sp_value,"PB_badsound")
    g4= sum_answers(sp_value,"PB_unfit")
    g5= sum_answers(sp_value,"PB_toosd")
    g6= sum_answers(sp_value,"PB_audiocut")
    g7= sum_answers(sp_value,"PB_battery")
    g8= sum_answers(sp_value,"PB_unplug")
    g9= sum_answers(sp_value,"PB_oneear")
    asum_q7 = g1[0]+g2[0]+g3[0]+g4[0]+g5[0]+g6[0]+g7[0]+g8[0]+g9[0]
    pg1 = "{:.0%}".format(g1[0]/asum_q7)
    pg2 = "{:.0%}".format(g2[0]/asum_q7)
    pg3 = "{:.0%}".format(g3[0]/asum_q7)
    pg4 = "{:.0%}".format(g4[0]/asum_q7)
    pg5 = "{:.0%}".format(g5[0]/asum_q7)
    pg6 = "{:.0%}".format(g6[0]/asum_q7)
    pg7 = "{:.0%}".format(g7[0]/asum_q7)
    pg8 = "{:.0%}".format(g8[0]/asum_q7)
    pg9 = "{:.0%}".format(g9[0]/asum_q7)

    fig3 = go.Figure()    
    if(sc_value=='gender'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[2],g2[2],g3[2],g4[2],g5[2],g6[2],g7[2],g8[2],g9[2]],\
                              text=[g1[2],g2[2],g3[2],g4[2],g5[2],g6[2],g7[2],g8[2],g9[2]],name="Male"))
        fig3.add_trace(go.Bar(x= xname, y= [g1[1],g2[1],g3[1],g4[1],g5[1],g6[1],g7[1],g8[1],g9[1]],\
                              text=[g1[1],g2[1],g3[1],g4[1],g5[1],g6[1],g7[1],g8[1],g9[1]],name="Female"))
        stitle="<b> Categorized gender</b>"
    elif(sc_value=='status'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[3],g2[3],g3[3],g4[3],g5[3],g6[3],g7[3],g8[3],g9[3]],\
                              text=[g1[3],g2[3],g3[3],g4[3],g5[3],g6[3],g7[3],g8[3],g9[3]],name="Single"))
        fig3.add_trace(go.Bar(x= xname, y= [g1[4],g2[4],g3[4],g4[4],g5[4],g6[4],g7[4],g8[4],g9[4]],\
                              text=[g1[4],g2[4],g3[4],g4[4],g5[4],g6[4],g7[4],g8[4],g9[4]],name="Married"))
        stitle="<b> Categorized status</b>"    
    elif(sc_value=='age'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[5],g2[5],g3[5],g4[5],g5[5],g6[5],g7[5],g8[5],g9[5]],name="Age 20-27",\
                              text= [g1[5],g2[5],g3[5],g4[5],g5[5],g6[5],g7[5],g8[5],g9[5]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[6],g2[6],g3[6],g4[6],g5[6],g6[6],g7[6],g8[6],g9[6]],name="Age 28-35",\
                              text= [g1[6],g2[6],g3[6],g4[6],g5[6],g6[6],g7[6],g8[6],g9[6]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[7],g2[7],g3[7],g4[7],g5[7],g6[7],g7[7],g8[7],g9[7]],name="Age 36-45",\
                              text= [g1[7],g2[7],g3[7],g4[7],g5[7],g6[7],g7[7],g8[7],g9[7]]))
        stitle="<b> Categorized age</b>"
    elif(sc_value=='education'): 
        fig3.add_trace(go.Bar(x= xname, y= [g1[8],g2[8],g3[8],g4[8],g5[8],g6[8],g7[8],g8[8],g9[8]],name="Graduate",\
                              text=[g1[8],g2[8],g3[8],g4[8],g5[8],g6[8],g7[8],g8[8],g9[8]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[9],g2[9],g3[9],g4[9],g5[9],g6[9],g7[9],g8[9],g9[9]],name="Undergraduate",\
                              text=[g1[9],g2[9],g3[9],g4[9],g5[9],g6[9],g7[9],g8[9],g9[9]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[10],g2[10],g3[10],g4[10],g5[10],g6[10],g7[10],g8[10],g9[10]],name="High School",\
                              text=[g1[10],g2[10],g3[10],g4[10],g5[10],g6[10],g7[10],g8[10],g9[10]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[11],g2[11],g3[11],g4[11],g5[11],g6[11],g7[11],g8[11],g9[11]],name="Other education",\
                              text=[g1[11],g2[11],g3[11],g4[11],g5[11],g6[11],g7[11],g8[11],g9[11]]))
        stitle="<b> Categorized education</b>" 
    elif(sc_value=='occupation'):  
        fig3.add_trace(go.Bar(x= xname, y= [g1[12],g2[12],g3[12],g4[12],g5[12],g6[12],g7[12],g8[12],g9[12]],name="Employee",\
                              text= [g1[12],g2[12],g3[12],g4[12],g5[12],g6[12],g7[12],g8[12],g9[12]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[13],g2[13],g3[13],g4[13],g5[13],g6[13],g7[13],g8[13],g9[13]],name="Business Owner",\
                              text= [g1[13],g2[13],g3[13],g4[13],g5[13],g6[13],g7[13],g8[13],g9[13]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[14],g2[14],g3[14],g4[14],g5[14],g6[14],g7[14],g8[14],g9[14]],name="Student",\
                              text= [g1[14],g2[14],g3[14],g4[14],g5[14],g6[14],g7[14],g8[14],g9[14]]))
        fig3.add_trace(go.Bar(x= xname, y= [g1[15],g2[15],g3[15],g4[15],g5[15],g6[15],g7[15],g8[15],g9[15]],name="Other occupation",\
                              text= [g1[15],g2[15],g3[15],g4[15],g5[15],g6[15],g7[15],g8[15],g9[15]]))
        stitle="<b> Categorized occupation</b>"
    
    fig3.update_layout(title_text="<b>Q7-</b>"+hpname(sp_value)+stitle,margin=dict(l=0, r=0, t=120, b=0))
    fig3.update_traces(textfont_size=12)

    return fig3

def show_graph3_fq7(sp_value,cs_value):
    xname=["Slient","Disconnect","Sound Quality","Unfit Design","Sound Level","Sound Cut",\
           "Battery","Jack Unplug","OneEar Usable"]
    g1= sum_answers_field(sp_value,"PB_nosound",cs_value)
    g2= sum_answers_field(sp_value,"PB_disconnect",cs_value)
    g3= sum_answers_field(sp_value,"PB_badsound",cs_value)
    g4= sum_answers_field(sp_value,"PB_unfit",cs_value)
    g5= sum_answers_field(sp_value,"PB_toosd",cs_value)
    g6= sum_answers_field(sp_value,"PB_audiocut",cs_value)
    g7= sum_answers_field(sp_value,"PB_battery",cs_value)
    g8= sum_answers_field(sp_value,"PB_unplug",cs_value)
    g9= sum_answers_field(sp_value,"PB_oneear",cs_value)
    asum_q7 = g1+g2+g3+g4+g5+g6+g7+g8+g9

    fig3 = go.Figure()    
    fig3.add_trace(go.Bar(x= xname, y= [g1,g2,g3,g4,g5,g6,g7,g8,g9],name="Other",\
                          text= [g1,g2,g3,g4,g5,g6,g7,g8,g9],marker_color='crimson'))
    stitle="<b> Categorized Fields</b>"
    fig3.update_layout(title_text="<b>Q7-</b>"+hpname(sp_value)+stitle,margin=dict(l=80, r=80, t=50, b=50))
    fig3.update_traces(textfont_size=12)

    return fig3


# In[30]:


def max_mean_qr27(sp_value):
    if(sp_value=="v0"):
        qrank=data[["HpTS1","HpTS2","HpTS3","HpTS4","HpTS5"]].mean()
    elif(sp_value!="v0"):
        qrank=data[["HpTS1","HpTS2","HpTS3","HpTS4","HpTS5"]].loc[data['HpAnswer']==sp_value].mean()
    qrank=qrank.reset_index(name='mean')
    im_qrank = qrank['mean'].idxmax()
    featuremax = qrank['index'][im_qrank]

    if(featuremax== "HpTS1"):
        featuremax = "Feature 1"
    elif(featuremax=="HpTS2"):
        featuremax = "Feature 2"
    elif(featuremax=="HpTS3"):
        featuremax = "Feature 3"
    elif(featuremax=="HpTS4"):
        featuremax = "Feature 4"
    elif(featuremax=="HpTS5"):
        featuremax = "Feature 5"
    #print(type(qrank))       
    #xname=["Online Site","Social Media","Google","Friend","Advertising"]
    g1= sum_answers(sp_value,"InfoHps_online")
    g2= sum_answers(sp_value,"InfoHps_Social")
    g3= sum_answers(sp_value,"InfoHps_Google")
    g4= sum_answers(sp_value,"InfoHps_PR")
    g5= sum_answers(sp_value,"InfoHps_Ads")
    gdata = {'info':['Online Site','Social Media','Google','Friend','Advertising'],\
             'asum':[g1[0],g2[0],g3[0],g4[0],g5[0]]}
    q2 = pd.DataFrame(data=gdata)
    im_q2 = q2['asum'].idxmax()
    q2max = q2['info'][im_q2]
    #print(q2max)
    
    p1= sum_answers(sp_value,"PB_nosound")
    p2= sum_answers(sp_value,"PB_disconnect")
    p3= sum_answers(sp_value,"PB_badsound")
    p4= sum_answers(sp_value,"PB_unfit")
    p5= sum_answers(sp_value,"PB_oneear")
    p6= sum_answers(sp_value,"PB_battery")
    p7= sum_answers(sp_value,"PB_toosd")
    p8= sum_answers(sp_value,"PB_audiocut")
    p9= sum_answers(sp_value,"PB_unplug")
    pdata = {'pb':["Slient","Disconnect","Sound Quality","Unfit Design","OneEar Usable","Battery","Sound Level"\
                       ,"Sound Cut","Jack Unplug"],\
             'asum':[p1[0],p2[0],p3[0],p4[0],p5[0],p6[0],p7[0],p8[0],p9[0]]}
    q7 = pd.DataFrame(data=pdata)
    im_q7 = q7['asum'].idxmax()
    q7max = q7['pb'][im_q7]
    #print(q7)
    
    return featuremax,q2max,q7max


# In[31]:


#Not finish Question 2,7
@app.callback(
    Output('table_1', 'figure'),
    Input('radio_product', 'value'),
    Input('select-dropdown', 'value'))
def table_answer(sp_value,sq_value):
    if(sp_value=="v0"):
        stadata=data[["HpAnswer","NumberHps","InfoHps","ActivityHps","TimeHps","PriceHps","PlaceHps","ProblemHps",\
                        "FactorHps","HealthHps","InnovationHps"]].\
        describe(include='all')
        hname= "all types "
    else:
        stadata = data[["HpAnswer","NumberHps","InfoHps","ActivityHps","TimeHps","PriceHps","PlaceHps","ProblemHps",\
                        "FactorHps","HealthHps","InnovationHps"]]\
            .loc[data['HpAnswer']==sp_value].describe(include='all')
        hname= "Headphone-"+sp_value
    
    table_index=['Top Feature','Q1:HPnumber','Q2:Information','Q3:Activity','Q4:TimeTobuy',\
                  'Q5:Price','Q6:PlaceToBuy','Q7:Problem','Q8:FactorToBuy','Q9:HealthCare',\
                  'Q10:Innovation']    
    threemax = max_mean_qr27(sp_value)
    stadata["HpAnswer"][2]= threemax[0]
    stadata["InfoHps"][2]= threemax[1]
    stadata["ProblemHps"][2]= threemax[2]
    table_header=["Stat.","<b>Top </b>"+"<b>"+hname+"</b>"]
    if(sq_value=="dbScoreV1"):
        hcolors = ["lightcyan","white","white","white","white","white","white","white","white","white","white"]
    elif(sq_value=="NumberHps"):
        hcolors = ["white","lightcyan","white","white","white","white","white","white","white","white","white"]
    elif(sq_value=="dbQ2"):
        hcolors = ["white","white","lightcyan","white","white","white","white","white","white","white","white"]
    elif(sq_value=="ActivityHps"):
        hcolors = ["white","white","white","lightcyan","white","white","white","white","white","white","white"]
    elif(sq_value=="TimeHps"):
        hcolors = ["white","white","white","white","lightcyan","white","white","white","white","white","white"]
    elif(sq_value=="PriceHps"):
        hcolors = ["white","white","white","white","white","lightcyan","white","white","white","white","white"]
    elif(sq_value=="PlaceHps"):
        hcolors = ["white","white","white","white","white","white","lightcyan","white","white","white","white"]
    elif(sq_value=="dbQ7"):
        hcolors = ["white","white","white","white","white","white","white","lightcyan","white","white","white"]
    elif(sq_value=="FactorHps"):
        hcolors = ["white","white","white","white","white","white","white","white","lightcyan","white","white"]
    elif(sq_value=="HealthHps"):    
        hcolors = ["white","white","white","white","white","white","white","white","white","lightcyan","white"]
    elif(sq_value=="InnovationHps"): 
        hcolors = ["white","white","white","white","white","white","white","white","white","white","lightcyan"]
    else:
        hcolors = ["white","white","white","white","white","white","white","white","white","white","white"]
    
    #line_color=[df.Color], fill_color=[df.Color],
    fig_table = go.Figure(data=[go.Table( columnorder = [1,2,3,4,5,6,7,8,9,10,11],      
                header=dict(values=table_header,                                   
                line_color='white',
                fill=dict(color=['#E5ECF6','#E5ECF6']),
                align='left',
                font = dict(color = 'black', size = 14)),
                cells=dict(values=[table_index,stadata.iloc[2]],
                line_color='white',
                fill_color=[hcolors],
                align='left',
                font = dict(color = 'black', size = 14),
                height=30
                  ))
                ])
    fig_table.update_layout(margin=dict(l=10, r=10, t=20, b=20))


    return  fig_table

@app.callback(
    Output('table_feature', 'figure'),
    Input('radio_product', 'value'))
def table_featureims(sinput):
    dtable  = feature_importance()
    table_header=["Feature Selection.","<b>Importance Score</b>"]
    hcolors = ["white","white","white","white","white","white","white","white","white","white","white"]

    fig_table = go.Figure(data=[go.Table( columnorder = [1,2,3,4,5,6,7,8,9,10,11],       
                header=dict(values=table_header,                                   
                line_color='white',
                fill=dict(color=['#E5ECF6','#E5ECF6']),
                align='left',
                font = dict(color = 'black', size = 14)),
                cells=dict(values=[dtable.index.values,dtable['importance'].values],
                line_color='white',
                fill_color=[hcolors],
                align='left',
                font = dict(color = 'black', size = 12),
                height=30
                  ))
                ])
    fig_table.update_layout(height=800,margin=dict(l=10, r=10, t=20, b=20))


    return  fig_table

@app.callback(
    Output('rudestext', 'children'),
    Output('table_segcustomer', 'figure'),
    Input('radio_product', 'value'))
def table_segcustomer(sinput):
    dtable  = segment_cus()[1]
    table_header=["Customer Group.","<b>HP type</b>"]
    hcolors = ["white","white","white","white","white","white","white","white","white","white","white"]

    fig_table = go.Figure(data=[go.Table( columnorder = [1,2],       
                header=dict(values=table_header,                                   
                line_color='white',
                fill=dict(color=['#E5ECF6','#E5ECF6']),
                align='center',
                font = dict(color = 'black', size = 14)),
                cells=dict(values=[dtable['customers_level_based'].values,dtable['Htype'].values],
                line_color='white',
                fill_color=[hcolors],
                align='center',
                font = dict(color = 'black', size = 12),
                height=30
                  ))
                ])
    fig_table.update_layout(margin=dict(l=10, r=10, t=10, b=10))


    return  segment_cus()[0],fig_table


# In[32]:


@app.callback(
    Output('graph_2', 'figure'),
    Input('radio_product', 'value'),
    Input('select-dropdown', 'value'))
def update_graph2(sp_value,sq_value):
    fig2 = go.Figure()
    if sp_value== "v0" and sq_value == 'dbScoreV1': 
        fig2 = HNC_all()
    elif sp_value!= "v0" and sq_value == 'dbScoreV1':
        fig2 = HNC_one(sp_value)
    elif sq_value != 'dbQ2'and sq_value !='dbQ7':
        fig2=show_cc_questions(sp_value,sq_value)
    elif sq_value == 'dbQ2':
        fig2 = show_graph2_q2(sp_value)
    elif sq_value == 'dbQ7':
        fig2 =show_graph2_q7(sp_value)
        
    return fig2


# In[33]:


@app.callback(
    Output('graph_9', 'figure'),
    Input('radio_product', 'value'),
    Input("checklist-input", "value"))
def update_graph9(sp_value, cs_value):
    #print(cs_value)
    a = {'HpAnswer': ["Headphone-v1", "Headphone-v2", "Headphone-v3"]}
    b = {'HpAnswer': ["Headphone-"+sp_value,"Others"]} 
    htype = hpname(sp_value)
    fig1 = go.Figure()
        #All headphones selected to show
    if (cs_value != [] and sp_value=="v0"):
      dt = data.copy()
      for i in range(len(cs_value)):
      #  print(cs_value[i])
        dt = dt[dt[["Gender","Age","Status","Education","Occupation"]].\
                            apply(lambda row: row.astype(str).str.contains(cs_value[i], case=True).any(), axis=1)]
      #display(dt)
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "clist"] =  dt.loc[dt['HpAnswer']=="v1"].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "clist"] =  dt.loc[dt['HpAnswer']=="v2"].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "clist"] =  dt.loc[dt['HpAnswer']=="v3"].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["clist"],text=dbar1["clist"]))  
      fig1.update_layout(title="<b>All Type Categorized Fields</b>")
    elif (cs_value == [] and sp_value=="v0"):
      dbar1 = pd.DataFrame(data=a) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v1"), "Total Responses"] =  data.loc[(data['HpAnswer']=="v1")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v2"), "Total Responses"] =  data.loc[(data['HpAnswer']=="v2")].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-v3"), "Total Responses"] =  data.loc[(data['HpAnswer']=="v3")].shape[0]   
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["Total Responses"],\
                            text=dbar1["Total Responses"]))   

#       fig1.add_trace(go.Pie(labels=dbar1['HpAnswer'], values=dbar1["Total Responses"], textinfo='label+percent',
#                               insidetextorientation='radial'))
#       fig1.update_traces(hole=.5,marker=dict(colors=['#e5383b', '#ba181b', '#8d99ae']), textfont_size=15)    
      fig1.update_layout(title="<b>All Types Categorized Fields</b>")    

    elif (cs_value != [] and sp_value!="v0"):
      dt = data.copy()
      for i in range(len(cs_value)):
        #print(cs_value[i])
        dt = dt[dt[["Gender","Age","Status","Education","Occupation"]].\
                            apply(lambda row: row.astype(str).str.contains(cs_value[i], case=True).any(), axis=1)]
      #display(dt)
      dbar1 = pd.DataFrame(data=b) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-"+sp_value), "clist"] =  dt.loc[dt['HpAnswer']==sp_value].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["clist"],text=dbar1["clist"]))  
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Categorized Fields</b>") 
    elif (cs_value == [] and sp_value!="v0"):
      dbar1 = pd.DataFrame(data=b) 
      dbar1.loc[(dbar1['HpAnswer']=="Headphone-"+sp_value), "clist"] =  data.loc[data['HpAnswer']==sp_value].shape[0]
      dbar1.loc[(dbar1['HpAnswer']=="Others"), "clist"] =  data.loc[(data['HpAnswer']!=sp_value)].shape[0]
      fig1.add_trace(go.Bar(x=dbar1["HpAnswer"], y=dbar1["clist"],text=dbar1["clist"]))  
      fig1.update_layout(title="<b>"+htype+"</b>"+"<b> Uncategorized</b>"+(' '.join(cs_value)))
    fig1.update_layout(
         yaxis=dict(title= "Total Responses"),
         #xaxis=dict(title= "Product Types"),
         font=dict(size=12),
         height=550,
         margin=dict(l=30, r=30, t=100, b=100),
         #yaxis_range=[0,50],
#          legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1,
#             xanchor="right",
#             x=1
#         )
    )
    fig1.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)
    return fig1
    


# In[34]:


@app.callback(
    Output('graph_7', 'figure'),
    Input('radio_product', 'value'),
    Input("checklist-input", "value"),
    Input('select-dropdown', 'value'))
def update_graph(sp_value,cs_value,sq_value):
    #dbScoreV1 dbQ2 dbQ7
    if sq_value == 'dbScoreV1':
        fig3 = FHC_question1(sp_value,cs_value) 
    elif(sq_value=="dbQ2"):
        fig3 = show_graph3_fq2(sp_value,cs_value)
    elif(sq_value=="dbQ7"):
        fig3 = show_graph3_fq7(sp_value,cs_value)
    else:
        fig3 = show_fhc_questions(sp_value,sq_value,cs_value)
  
    return fig3
   
    


# In[35]:


@app.callback(
    Output('graph_3', 'figure'),
    Input('radio_product', 'value'),
    Input('radio_items', 'value'),
    Input('select-dropdown', 'value'))
def update_graph3(sp_value,sc_value,sq_value):
    #dbScoreV1 dbQ2 dbQ7
    if sc_value == "gender" and sq_value == 'dbScoreV1':
        fig3 = HC_gender(sp_value) 
    elif sc_value == "age" and sq_value == 'dbScoreV1':
        fig3 = HC_age(sp_value) 
    elif sc_value == "education" and sq_value == 'dbScoreV1':
        fig3 = HC_education(sp_value) 
    elif sc_value == "occupation" and sq_value == 'dbScoreV1':
        fig3 = HC_occupation(sp_value) 
    elif sc_value == "status" and sq_value == 'dbScoreV1':
        fig3 = HC_status(sp_value) 
    elif sc_value == "none" and sq_value == 'dbScoreV1':
        fig3 = rtable_answer(sp_value)        
    elif(sq_value=="dbQ2" and sc_value !="none"):
        fig3 = show_graph3_q2(sp_value,sc_value)
    elif(sq_value=="dbQ2" and sc_value =="none"):
        fig3 = q2_table(sp_value)
    elif(sq_value=="dbQ7"and sc_value !="none"):
        fig3 = show_graph3_q7(sp_value,sc_value)
    elif(sq_value=="dbQ7"and sc_value =="none"):
        fig3 = q7_table(sp_value)
    else:
        fig3 = show_hc_questions(sp_value,sc_value,sq_value)
  
    return fig3
   
    


# In[36]:


def predict_att(field):
        if(field=="C_Male"):
            field = "Male"
        if(field=="C_Female"):
            field = "Female"
        if(field=="C_Single"):
            field= "Single"
        if(field=="C_Married"):
            field= "Married"
        if(field=="C_A1"):
            field= "Age 20-27"
        if(field=="C_A2"):
            field= "Age 28-35"
        if(field=="C_A3"):
            field= "Age 36-45"
        if(field=="C_E1"):
            field= "Graduate"
        if(field=="C_E2"):
            field= "Undergraduate"
        if(field=="C_E3"):
            field= "High School"
        if(field=="C_E4"):
            field= "Other education"
        if(field=="C_O1"):
            field= "Student"
        if(field=="C_O2"):
            field= "Employee"
        if(field=="C_O3"):
            field= "Business Owner"
        if(field=="C_O4"):
            field= "Other occupation"
        return field



# In[37]:


def show_mldes(sp_value):
    fig0 = go.Figure()
    img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/machine-learning-python-intro.jpg')
    ats = "Survey analysis with ML"
    if sp_value == 1:
        img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2023/03/htype1.jpg')
        ats = f"Customer tends to select product type HP{sp_value}"
    elif sp_value == 2:
        img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2023/03/htype2.jpg')
        ats = f"Customer tends to select product type HP{sp_value}"
    elif sp_value == 3:
        img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2023/03/htype3.jpg')  
        ats = f"Customer tends to select product type HP{sp_value}"
    elif sp_value == "all":
        img = io.imread('https://selfstudy108.treebymuk.com/wp-content/uploads/2022/06/headphone_allversions.jpg')  
        ats = f"Explaination model"
    fig8 = px.imshow(img)
    fig8.update_layout(title=ats,height=200,coloraxis_showscale=False,\
                       font=dict(size=10),paper_bgcolor='rgba(0,0,0,0)',\
                        plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=20, r=20, t=20, b=20))
    fig8.update_xaxes(showticklabels=False)
    fig8.update_yaxes(showticklabels=False) 
    return fig8

def senten_input(colnum,inputword):
#      colname=['NumberHps', 'ActivityHps', 'TimeHps','PriceHps','PlaceHps','FactorHps','HealthHps','InnovationHps',\
#              "PB_nosound","PB_disconnect","PB_badsound","PB_unfit","PB_oneear","PB_toosd","PB_audiocut","PB_battery",\
#              "PB_unplug","InfoHps_online","InfoHps_Social","InfoHps_Google","InfoHps_Store","InfoHps_PR","InfoHps_Ads"]
    senten_man = ' '
    senten_woman = ' '
    if(colnum == "NumberHps"):
        if(inputword != 'invalid value'):
            senten_man = f"He has {inputword} headphones pieces in used."
            senten_woman = f"She has {inputword} headphones pieces in used."
    elif(colnum == "ActivityHps"):
        if(inputword == 'music'):
           senten_man = f"He normally uses headphones to listen to music."
           senten_woman = f"She normally uses headphones to listen to music."
        if(inputword == 'sport'):
           senten_man = f"He normally uses headphones to play sports."
           senten_woman = f"She normally uses headphones to play sports."
        if(inputword == 'conference'):
           senten_man = f"He normally uses headphones in a conference."
           senten_woman = f"She normally uses headphones in a conference."
        if(inputword == 'movie'):
           senten_man = f"He normally uses headphones to watch a movie."
           senten_woman = f"She normally uses headphones to watch a movie."
        if(inputword == 'study'):
           senten_man = f"He normally uses headphones to study."
           senten_woman = f"She normally uses headphones to study."
        if(inputword == 'driving'):
           senten_man = f"He normally uses headphones to driving."
           senten_woman = f"She normally uses headphones to driving."
    elif(colnum == 'TimeHps'):
        #'last year', 'this year', 'later than last year'
        if(inputword != 'invalid value'):
           senten_man = f"He buys latest headphones {inputword}."
           senten_woman = f"She buys latest headphones {inputword}."
    elif(colnum == 'PriceHps'):
        #'less than 100', '100-299', '300-1199','1200-3500','3500 Up'
           if(inputword == 'less than 100'):
               senten_man = f"His headphones price are {inputword} Baht."
               senten_woman = f"Her headphones price are {inputword} Baht."
           if(inputword != 'invalid value'):
               senten_man = f"His headphones price are around {inputword} Baht."
               senten_woman = f"Her headphones price are around {inputword} Baht."
    elif(colnum == 'PlaceHps'):
        #'online', 'store', 'direct selling','tv direct','mini mart'
         if(inputword != 'invalid value'):
               senten_man = f"He often buys headphones from {inputword}."
               senten_woman = f"She often buys headphones from {inputword}."
    elif(colnum == 'FactorHps'):
       # 'feature', 'function', 'price','sound','brand','design','health'
         if(inputword == 'feature'):
           senten_man = f"He decided to buy headphones if its features are attrative."
           senten_woman = f"She decided to buy headphones if its features are attractive."
         if(inputword == 'function'):
           senten_man = f"He decided to buy headphones if its functions support his work."
           senten_woman = f"She decided to buy headphones if its functions support her work."
         if(inputword == 'price'):
           senten_man = f"He decided to buy headphones if the price is reasonable."
           senten_woman = f"She decided to buy headphones if the price is reasonable."
         if(inputword == 'brand'):
           senten_man = f"He decided to buy headphones if the brand is reliable."
           senten_woman = f"She decided to buy headphones if the brand is reliable."
         if(inputword == 'design'):
           senten_man = f"He decided to buy headphones if the design is most useful for him."
           senten_woman = f"She decided to buy headphones if the design is most useful for her."
         if(inputword == 'health'):
           senten_man = f"He decided to buy headphones if it is best for ear health."
           senten_woman = f"She decided to buy headphones if it is best for ear health."
         if(inputword == 'sound'):
           senten_man = f"He decided to buy headphones if it has the best sound quality."
           senten_woman = f"She decided to buy headphones if it has the best sound quality."
    elif(colnum == 'HealthHps'):
      #  'no', 'yes'
           if(inputword == "yes"):
               senten_man = f"He thinks that listening through headphones is harmful to hearing."
               senten_woman = f"She thinks that listening through headphones is harmful to hearing."  
           if(inputword == "no"):
               senten_man = f"He thinks that listening through headphones is not harmful to hearing."
               senten_woman = f"She thinks that listening through headphones is not harmful to hearing."  
    elif(colnum == 'InnovationHps'):
    #'software and application', 'sound for health',\
    #                        'creative design','eco-friendly material','artificial Intelligence'
           if(inputword != 'invalid value'):
               senten_man = f"His headphones would be much more fabulous with a new {inputword}."
               senten_woman = f"Her headphones would be much more fabulous with a new {inputword}."  
    elif(colnum == 'PB_nosound'):
           if(inputword == "yes"):
               senten_man = f"His headphones are always broken or been silent too early."
               senten_woman = f"Her headphones are always broken or been silent too early."  
           if(inputword == "no"):
               senten_man = f"His headphones has never broken or silent too early."
               senten_woman = f"Her headphones has never broken or silent too early."  
    elif(colnum == 'PB_disconnect'):
           if(inputword == "yes"):
               senten_man = f"He always faces disconnecting to a device when he used headphones."
               senten_woman = f"She always faces disconnecting to a device when she used headphones."  
           if(inputword == "no"):
               senten_man = f"He has never faced disconnecting to a device when he used headphones."
               senten_woman = f"She has never faced disconnecting to a device when she used headphones."  
    elif(colnum == 'PB_badsound'):
           if(inputword == "yes"):
               senten_man = f"He always faces bad sound quality when he used headphones."
               senten_woman = f"She always faces bad sound quality when she used headphones."  
           if(inputword == "no"):
               senten_man = f"He has never faced bad sound quality when he used headphones."
               senten_woman = f"She has never faced bad sound quality when she used headphones."  
    elif(colnum == 'PB_unfit'):
           if(inputword == "yes"):
               senten_man = f"He always faces uncomfortable waring when he used headphones."
               senten_woman = f"She always faces uncomfortable waring when she used headphones."  
           if(inputword == "no"):
               senten_man = f"He has never faced uncomfortable waring when he used headphones."
               senten_woman = f"She has never faced uncomfortable waring when she used headphones."  
    elif(colnum == 'PB_oneear'):
           if(inputword == "yes"):
               senten_man = f"His headphones are always broken on one side."
               senten_woman = f"Her headphones are always broken on one side."  
           if(inputword == "no"):
               senten_man = f"His headphones has never broken on one side."
               senten_woman = f"Her headphones has never broken on one side."  
    elif(colnum == 'PB_toosd'):
           if(inputword == "yes"):
               senten_man = f"His headphones mostly cannot adjust the sound in balance volume."
               senten_woman = f"Her headphones mostly cannot adjust the sound in balance volume."  
           if(inputword == "no"):
               senten_man = f"His headphones never has the problem with adjusting the sound."
               senten_woman = f"Her headphones never has the problem with adjusting the sound."  
    elif(colnum == 'PB_audiocut'):
           if(inputword == "yes"):
               senten_man = f"He always faces sound cut when he used headphones."
               senten_woman = f"She always faces  sound cut when she used headphones."  
           if(inputword == "no"):
               senten_man = f"He has never faced sound cut when he used headphones."
               senten_woman = f"She has never faced sound cut when she used headphones."  
    elif(colnum == 'PB_battery'):
           if(inputword == "yes"):
               senten_man = f"He always faces headphones's battery lifetime unsustainable."
               senten_woman = f"She always faces headphones's battery lifetime unsustainable."  
           if(inputword == "no"):
               senten_man = f"He has never faced headphones's battery lifetime unsustainable."
               senten_woman = f"She has never faced headphones's battery lifetime unsustainable."  
    elif(colnum == 'PB_unplug'):
           if(inputword == "yes"):
               senten_man = f"His headphones always cannot plug-in to the device."
               senten_woman = f"Her headphones always cannot plug-in to the device."  
           if(inputword == "no"):
               senten_man = f"His headphones never has the problem with plug-in to the device."
               senten_woman = f"Her headphones never has the problem with plug-in to the device."                  
    elif(colnum == 'InfoHps_online'):
           if(inputword == "yes"):
               senten_man = f"He usually searches the information about headphones through the official website."
               senten_woman = f"She usually searches the information about headphones through the official website." 
           if(inputword == "no"):
               senten_man = f"He has never searched the information about headphones through the official website."
               senten_woman = f"She has never searched the information about headphones through the official website." 
    elif(colnum == 'InfoHps_Social'):
           if(inputword == "yes"):
               senten_man = f"He usually searches the information about headphones through social media."
               senten_woman = f"She usually searches the information about headphones through social media." 
           if(inputword == "no"):
               senten_man = f"He has never searched the information about headphones through social media."
               senten_woman = f"She has never searched the information about headphones through social media." 
    elif(colnum == 'InfoHps_Google'):
           if(inputword == "yes"):
               senten_man = f"He usually searches the information about headphones via Google search engine."
               senten_woman = f"She usually searches the information about headphones via Google search engine." 
           if(inputword == "no"):
               senten_man = f"He has never searched the information about headphones via Google search engine."
               senten_woman = f"She has never searched the information about headphones via Google search engine." 
    elif(colnum == 'InfoHps_Store'):
           if(inputword == "yes"):
               senten_man = f"He usually asks for the information about headphones from the physical store."
               senten_woman = f"She usually asks for the information about headphones from physical store." 
           if(inputword == "no"):
               senten_man = f"He has never asked for the information about headphones from the physical store."
               senten_woman = f"She has never asked for the information about headphones from the physical store." 
    elif(colnum == 'InfoHps_PR'):
           if(inputword == "yes"):
               senten_man = f"He usually asks for the information about headphones from well-known people."
               senten_woman = f"She usually asks for the information about headphones from well-known people." 
           if(inputword == "no"):
               senten_man = f"He has never asked for the information about headphones from well-known people."
               senten_woman = f"She has never asked for the information about headphones from well-known people." 
    elif(colnum == 'InfoHps_Ads'):
           if(inputword == "yes"):
               senten_man = f"He has been attracted to information about headphones from advertising."
               senten_woman = f"She has been attracted to information about headphones from advertising.." 
           if(inputword == "no"):
               senten_man = f"He has never been attracted to information about headphones from advertising."
               senten_woman = f"She has never been attracted to information about headphones from advertising." 

    return senten_man,senten_woman

    


# In[38]:


@app.callback(
     Output('b_submit', 'n_clicks'),
     Output("ans_attr1_des", "children"),
     Output("ans_attr2_des", "children"),
     Output("ans_attr3_des", "children"),
     Output("ans_attr4_des", "children"),
     Output("mldestext", "children"),
     Output("introdestext", "children"),
     Output('graph_15', 'figure'),
     Output('graph_exp', 'figure'),
     Input('select_gender', 'value'),
     Input('select_age', 'value'),
     Input('select_status', 'value'),
     Input('select_edu', 'value'),
     Input('select_occ', 'value'),
     Input('ques_attr1', 'value'),
     Input('ques_attr2', 'value'),
     Input('ques_attr3', 'value'),
     Input('ques_attr4', 'value'),
     Input('input_range_1', 'value'),
     Input('input_range_2', 'value'),
     Input('input_range_3', 'value'),
     Input('input_range_4', 'value'),
     Input('b_submit', 'n_clicks'))
def dlist_output1(select_gender,select_age,select_status,select_edu,select_occ,ques_attr1,ques_attr2,ques_attr3,ques_attr4,input_range_1,input_range_2,input_range_3,input_range_4,b_submit):
   # print(ques_attr1,ques_attr2,ques_attr3,input_range_1,input_range_2,input_range_3,b_submit)
    textintro = f"This section will analyze the data from survey response by using machine learning.\
              On the left hand side, you see the importanced features that identify in the survey form\
              The first three attributes are precise to create a train model for predictions. There are various\
              algorithms to apply with the machine learning. Currently this survey data can give the most accurate result\
              with the decision tree. Let's see the ROC curve below to estimate the outcome!"

    qto  = feature_importance()
    colname=['Gender','Age','Status','Education','Occupation','NumberHps', 'ActivityHps', 'TimeHps','PriceHps',\
             'PlaceHps','FactorHps','HealthHps','InnovationHps',"PB_nosound","PB_disconnect","PB_badsound",\
             "PB_unfit","PB_oneear","PB_toosd","PB_audiocut","PB_battery","PB_unplug","InfoHps_online",\
             "InfoHps_Social","InfoHps_Google","InfoHps_Store","InfoHps_PR","InfoHps_Ads"]
    xts = pd.DataFrame(np.array([[select_gender,select_age,select_status,select_edu,select_occ,\
                                  0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]),columns=colname)
  
    xts[ques_attr1].iloc[0]=input_range_1
    xts[ques_attr2].iloc[0]=input_range_2
    xts[ques_attr3].iloc[0]=input_range_3
    xts[ques_attr4].iloc[0]=input_range_4
    xts1 = xts[np.unique([ques_attr1, ques_attr2, ques_attr3, ques_attr4])]
    xts3 = xts[np.unique(['Gender','Age','Status','Education','Occupation',ques_attr1, ques_attr2, ques_attr3, ques_attr4])]

    invtext = f'invalid value'
    xts["Gender"].replace([0, 1],['female', 'male'], inplace=True, regex=True)
    xts["Age"].replace([1, 2, 3],['20-27','28-35', '36-45'], inplace=True, regex=True)
    xts["Status"].replace([0,1],['single','married'], inplace=True, regex=True)
    xts["Education"].replace([1, 2, 3, 4],['graduate','undergraduate', 'high School','other unspecified education'],\
                             inplace=True, regex=True)
    xts["Occupation"].replace([1, 2, 3, 4],['student','employee', 'business Owner','other unspecified occupation'],
                                     inplace=True, regex=True)
    xts['NumberHps'].replace([0, 1, 2,3,4,5,6,7],['1-2', '2-5', 'more than 5',invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True,regex=True)
    xts['ActivityHps'].replace([0,1,2, 3, 4, 5,6,7],['music', 'sport', 'conference','movie','study','driving',\
                                                     invtext,invtext], inplace=True, regex=True)
    xts['TimeHps'].replace([0,1, 2,3,4,5,6,7],['last year', 'this year', 'later than last year',invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts['PriceHps'].replace([0,1, 2,3,4,5,6,7],['less than 100', '100-299', '300-1199','1200-3500','3500 Up',\
                                            invtext,invtext,invtext], inplace=True, regex=True)
    xts['PlaceHps'].replace([0,1, 2,3,4,5,6,7],['online shop', 'store', 'direct selling','TV direct','mini mart',\
                                               invtext,invtext,invtext], inplace=True, regex=True)
    xts['FactorHps'].replace([0,1, 2, 3, 4, 5, 6,7],['feature', 'function', 'price','sound','brand','design','health',\
                                            invtext], inplace=True, regex=True)
    xts['HealthHps'].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts['InnovationHps'].replace([0,1, 2, 3, 4, 5, 6,7],['software and application', 'sound for health',\
                            'creative design','eco-friendly material','artificial Intelligence',invtext,invtext,invtext],\
                                                 inplace=True, regex=True)
    
    xts["PB_nosound"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_disconnect"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_badsound"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_unfit"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_oneear"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_toosd"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_audiocut"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_battery"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["PB_unplug"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["InfoHps_online"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["InfoHps_Social"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["InfoHps_Google"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["InfoHps_Store"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["InfoHps_PR"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
    xts["InfoHps_Ads"].replace([0,1, 2, 3, 4, 5, 6,7],['no', 'yes',invtext,invtext,invtext,\
                                                  invtext,invtext,invtext], inplace=True, regex=True)
   
    xts2 = xts[np.unique(['Gender','Age','Status','Education','Occupation',ques_attr1, ques_attr2, ques_attr3, ques_attr4])]
    text1 =  xts2[ques_attr1].iloc[0],": ",input_range_1
    text2 =  xts2[ques_attr2].iloc[0],": ",input_range_2
    text3 =  xts2[ques_attr3].iloc[0],": ",input_range_3
    text4 =  xts2[ques_attr4].iloc[0],": ",input_range_4
    textdes =' '
    fig7 = show_mldes(0)
    fig8 = show_mldes('all')
    if(b_submit):
        mlresult = get_explaination(xts3)
        fig7 = show_mldes(int(mlresult[1]))
        fig8 = mlresult[0]
        cgender = xts2['Gender'].iloc[0]
        cage= xts2['Age'].iloc[0]
        cstatus= xts2['Status'].iloc[0]
        cedu = xts2['Education'].iloc[0]
        cocc = xts2['Occupation'].iloc[0]
        pscore = int(mlresult[4]*100)
        if(cgender == 'male'):
            textdes = f'A customer who has responed this feature option from questionaire would be a {cgender}. His age\
                        is between {cage}. He is a {cstatus} man. He has education in {cedu} and doing \
                        full time {cocc}. {senten_input(ques_attr1,xts2[ques_attr1][0])[0]}\
                        {senten_input(ques_attr2,xts2[ques_attr2][0])[0]}\
                        {senten_input(ques_attr3,xts2[ques_attr3][0])[0]}\
                        Analysis his responses from this survey, he would\
                        be interested to buy product type HP{mlresult[1]} with predictive score {pscore}%.\
                        Positive inputs are {mlresult[2]}.\
                         Negative inputs are {mlresult[3]}'
            
        elif(cgender == 'female'):
            textdes = f'A customer who has responed this feature option from questionaire would be a {cgender}. Her age\
                        is between {cage}. She is a {cstatus} man. She has education in {cedu} and doing \
                        full time {cocc}. {senten_input(ques_attr1,xts2[ques_attr1][0])[1]}\
                        {senten_input(ques_attr2,xts2[ques_attr2][0])[1]}\
                        {senten_input(ques_attr3,xts2[ques_attr3][0])[1]}\
                        Analysis her responses from this survey, she would\
                        be interested to buy product type HP{mlresult[1]} with predictive score {pscore}%.\
                        Positive inputs are {mlresult[2]}.\
                         Negative inputs are {mlresult[3]}'
        textintro = ''


    #rint(xts2)
    return False,text1,text2,text3,text4,textdes,textintro,fig7,fig8
    
@app.callback(
     Output('graph_12', 'figure'),
     Output('graph_13', 'figure'),
     Output('graph_14', 'figure'),
     Output('graph_16', 'figure'),
     Output('graph_17', 'figure'),
     Output('graph_18', 'figure'),
     Output('graph_12c', 'figure'),
     Output('graph_13c', 'figure'),
     Output('graph_14c', 'figure'),
     Output('graph_16c', 'figure'),
     Output('graph_17c', 'figure'),
     Output('graph_18c', 'figure'),
     Input('ques_attr1', 'value'),
     Input('ques_attr2', 'value'),
     Input('ques_attr3', 'value'),
     Input('ques_attr4', 'value'))
def dlist_output2(ques_attr1,ques_attr2,ques_attr3,ques_attr4):
    
    fig1 = getROCfigure2([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Gender')
    fig2 = getROCfigure2([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Status')
    fig3 = getROCfigure2([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Age')
    fig4 = getROCfigure2([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Education')
    fig5 = getROCfigure2([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Occupation')
    fig6 = getROCfigure2([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'HpAnswer')
    fc1 = getConfusionMatrix([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Gender')
    fc2 = getConfusionMatrix([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Status')
    fc3 = getConfusionMatrix([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Age')
    fc4 = getConfusionMatrix([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Education')
    fc5 = getConfusionMatrix([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'Occupation')
    fc6 = getConfusionMatrix([ques_attr1,ques_attr2,ques_attr3,ques_attr4],'HpAnswer')

    return fig1,fig2,fig3,fig4,fig5,fig6,fc1,fc2,fc3,fc4,fc5,fc6



# In[39]:


def show_graph_pall1(npredict):

    npall = pd.DataFrame(npredict)
    figp = go.Figure()
    figp.add_trace(go.Bar(y= npall.iloc[0], x= npall.columns,\
                          text=npall.iloc[1]))
   
    # Set y-axes titles
    figp.update_layout(
                    xaxis=dict(
                        title="Prediction Characteristics",
#                         anchor="free",
                        overlaying="y",
                       # side="left",
                       # position=0.15
                    ),
                   margin=dict(l=0, r=0, t=0, b=0),
                  
                )
    figp.update_traces(textfont_size=12,textposition="outside")

    return figp


# In[40]:


if __name__ == "__main__":
   app.run_server(mode='external',host='127.0.0.1',port='8050', debug=True)   
#     #app.run_server(mode='external', debug=True)  


# In[ ]:




