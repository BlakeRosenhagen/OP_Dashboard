#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install missingno


# In[ ]:


import pandas as pd
import numpy as np


# In[ ]:


df = pd.read_csv("data/input.csv", header=0)


# In[ ]:


import missingno as msno 
msno.matrix(df)


# In[ ]:


msno.bar(df)


# In[ ]:


df["New"] = df['New'].astype('str')
df["Stage"] = df['Stage'].astype('str')


# In[ ]:


true_phrases = ["new","New","ew","Ne","ne"]
false_phrases = ["exist","Exist","ex","Ex","ist","ng","st"]
stage_phrases = ["confirming","con","nfirm","application","app","investigating","invest","gating"]
for index, row in df.iterrows():
    for t_p in true_phrases:
        if type(row["New"]) == bool: break
        if t_p in row["New"]:
            df.at[index,"New"] = True
            
    for f_p in false_phrases:
        if type(row["New"]) == bool: break
        if f_p in row["New"]:
            df.at[index,"New"] = False
    if type(row["New"]) != bool:
        print(index)
        print(type(row["New"]))
        print(row["New"])
        #df.at[index,"New"] = np.nan
        
    
    for s_p in stage_phrases:
        if s_p in row["Stage"]:
            df.at[index,"Stage"] = "Discovery (S.P.I.N.)"
            print(df.at[index,"Stage"])


# ### removing artifacts from PV and PP

# In[ ]:


df["PotentialValue"] = df['PotentialValue'].astype('str')
df["ProbPercent"] = df['ProbPercent'].astype('str')


# In[ ]:


numlist = ["0","1","2","3","4","5","6","7","8","9"]
PVindex = []
PPindex = []
nonnumindex = []
for index, row in df.iterrows():
    stringa = row['PotentialValue']
    row['PotentialValue'] = stringa.strip("$").replace(',',"")
    stringb = row['ProbPercent']
    row['ProbPercent'] = stringb.strip("%")
    counta = 0
    countb = 0
    for num in numlist:
        if num in stringa: counta += 1
        if num in stringb: countb += 1
    if counta == 0: 
        df.at[index,"PotentialValue"] = np.NaN
        PVindex.append(index)
        if index not in nonnumindex:
            nonnumindex.append(index)
        print("PV"+str(index))
    if countb == 0:
        df.at[index,"ProbPercent"] = np.NaN
        PPindex.append(index)
        if index not in nonnumindex:
            nonnumindex.append(index)
        print("PP"+str(index))


# In[ ]:


df_num = df.dropna(subset=["PotentialValue","ProbPercent"])
print(len(df_num))


# In[ ]:


df_num["PotentialValue"] = df_num['PotentialValue'].astype('int')
df_num["ProbPercent"] = df_num['ProbPercent'].astype('float')


# In[ ]:


df_num["ProbPercent"] = df_num["ProbPercent"] / 100


# In[ ]:


df_num["ExpectedValue"] = df_num["PotentialValue"] * df_num["ProbPercent"]
df_num["ExpectedValue"] = df_num["ExpectedValue"].astype("int")


# In[ ]:


column_names = ['Div', 'Branch', 'OAM', 'UpdateDate', 'LeadType', 'LeadSpecifics',
       'Customer', 'Type', 'New', 'City, St', 'ProjectOpportunity',
       'KeyVendor', 'TechnologiesServices Proposed', 'PotentialValue',
       'ProbPercent','ExpectedValue','CustomerCompelingEvent', 'Stage', 'YourNextBIGStep',
       'ExpectedOrderDate', 'Notes']
df_num = df_num.reindex(columns=column_names)


# # Opportunity Funnel

# ### creating junk DataFrame

# In[ ]:


list(str(int(i*100)) for i in df_num["ProbPercent"].unique())


# In[ ]:


df_num["ProbPercent"].unique()


# In[ ]:


PV_list = list(str(i) for i in df_num["PotentialValue"].unique())
PP_list = list(str(int(i*100)) for i in df_num["ProbPercent"].unique())
df_junka = df[~df.PotentialValue.isin(PV_list)]
df_junkb = df_junka.append(df[~df.ProbPercent.isin(PP_list)])


# In[ ]:


stages = ["Discovery (S.P.I.N.)","Solution Development","Quoting","Working","On Hold","Won","Lost (why?)"]
#stages_other = ["Lost (why?)"]
df_junkc = df_junkb.append(df_num[~df_num.Stage.isin(stages)])
df_num =df_num[df_num.Stage.isin(stages)]
df_num[~df_num.Stage.isin(stages)]


# ### numbers management

# In[ ]:


df_num["Stage"].unique()


# In[ ]:


#code examples not used
df_num[(df_num["Branch"]=="Austin") & (df_num["Stage"]=="Won")]
df_num[df_num["Stage"]=="Lost (why?)"]


# In[ ]:


df_noncumun = {}
for branch in df_num["Branch"].unique():
    df_sum = df_num[df_num["Branch"]==branch].groupby("Stage")["PotentialValue","ExpectedValue"].sum()
    df_mean = df_num[df_num["Branch"]==branch].groupby("Stage")[["ProbPercent"]].mean()
    df_count = df_num[df_num["Branch"]==branch].groupby("Stage")[["Div"]].count()
    #df_sum[["PotentialValue","ExpectedValue"]]

    columns = ["PV_sum","EV_sum","PP_mean","Count"]
    df_branch = pd.DataFrame(columns=columns)
    df_branch[["PV_sum","EV_sum"]] = df_sum[["PotentialValue","ExpectedValue"]]
    df_branch[["PP_mean"]] = df_mean[["ProbPercent"]]
    df_branch[["Count"]] = df_count[["Div"]]
    df_branchh = pd.DataFrame(df_branch,index=["Discovery (S.P.I.N.)",
                                               "Solution Development",
                                               "Quoting ",
                                               "Working",
                                               "On Hold"
                                               "Won",
                                               "Lost (why?)"
                                              ])
    #df_branch = df_branch.sort(['A', 'B'], ascending=[1, 0])
    
    df_noncumun[branch] = df_branch


# In[ ]:


df_noncumun


# In[ ]:


#df_num.groupby(["Branch","Stage"]).agg("count")


# In[ ]:


#df_num.groupby(["Branch","Stage"]).agg("count")["Customer"]


# Cummunalative: cummun_sum of PV, cummun_sum of EV, cummun_len of rows
# 
# 
# 
# Snapshot: sum of PV, sum of EV, avg of PP, len of rows

# ### Opportunity Funnel Plot

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html


# In[ ]:


app = dash.Dash()


# In[ ]:


app.layout = html.Div([
    html.label("Select View")
    dcc.Dropdown(
        id = "first-dropdown",
        options = [
            {"label":"PotentialValue Sum", "value":"PV_sum"},
            {"label":"ExpectedValue Sum", "value":"EV_sum"},
            {"label":"ProbPercent Mean", "value":"PP_mean"},
            {"label":"Lead Count", "value":"count"}
        ],
        value = "PV_sum"
    )
    
])


# In[ ]:


if __name__ == '__main__':
    app.run_server()


# In[ ]:


from plotly import graph_objects as go

fig = go.Figure()

fig.add_trace(go.Funnel(
    name = 'Montreal',
    y = ["Website visit", "Downloads", "Potential customers", "Requested price"],
    x = [120, 60, 30, 20],
    textinfo = "value+percent initial"))

fig.add_trace(go.Funnel(
    name = 'Toronto',
    orientation = "h",
    y = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"],
    x = [100, 60, 40, 30, 20],
    textposition = "inside",
    textinfo = "value+percent previous"))

fig.add_trace(go.Funnel(
    name = 'Vancouver',
    orientation = "h",
    y = ["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent", "Finalized"],
    x = [90, 70, 50, 30, 10, 5],
    textposition = "outside",
    textinfo = "value+percent total"))

fig.show()


# In[ ]:





# # Anvil

# # OAM Visualization

# In[ ]:


df_OAM = df.groupby("OAM").mean()
df_OAM


# In[ ]:





# In[ ]:





# In[ ]:





# # Dash

# In[ ]:


#pip install dash_bootstrap_components


# In[2]:


import homepage
import index


# In[ ]:


run index


# In[ ]:


import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/bcdunbar/datasets/master/parcoords_data.csv")

fig = go.Figure(data=
    go.Parcoords(
        line = dict(color = df['colorVal'],
                   colorscale = 'Electric',
                   showscale = True,
                   cmin = -4000,
                   cmax = -100),
        dimensions = list([
            dict(range = [32000,227900],
                 constraintrange = [100000,150000],
                 label = "Block Height", values = df['blockHeight']),
            dict(range = [0,700000],
                 label = 'Block Width', values = df['blockWidth']),
            dict(tickvals = [0,0.5,1,2,3],
                 ticktext = ['A','AB','B','Y','Z'],
                 label = 'Cyclinder Material', values = df['cycMaterial']),
            dict(range = [-1,4],
                 tickvals = [0,1,2,3],
                 label = 'Block Material', values = df['blockMaterial']),
            dict(range = [134,3154],
                 visible = True,
                 label = 'Total Weight', values = df['totalWeight']),
            dict(range = [9,19984],
                 label = 'Assembly Penalty Wt', values = df['assemblyPW']),
            dict(range = [49000,568000],
                 label = 'Height st Width', values = df['HstW'])])
    )
)
fig.show()


# In[ ]:





# In[ ]:


import plotly.graph_objects as go
import ipywidgets as widgets
import pandas as pd
import numpy as np

cars_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/imports-85.csv')

# Build parcats dimensions
categorical_dimensions = ['body-style', 'drive-wheels', 'fuel-type']

dimensions = [dict(values=cars_df[label], label=label) for label in categorical_dimensions]

# Build colorscale
color = np.zeros(len(cars_df), dtype='uint8')
colorscale = [[0, 'gray'], [0.33, 'gray'],
              [0.33, 'firebrick'], [0.66, 'firebrick'],
              [0.66, 'blue'], [1.0, 'blue']]
cmin = -0.5
cmax = 2.5

# Build figure as FigureWidget
fig = go.FigureWidget(
    data=[go.Scatter(x=cars_df.horsepower, y=cars_df['highway-mpg'],
                marker={'color': color, 'cmin': cmin, 'cmax': cmax,
                        'colorscale': colorscale, 'showscale': True,
                        'colorbar': {'tickvals': [0, 1, 2], 'ticktext': ['None', 'Red', 'Blue']}},
                     mode='markers'),

      go.Parcats(domain={'y': [0, 0.4]}, dimensions=dimensions,
                   line={'colorscale': colorscale, 'cmin': cmin,
                   'cmax': cmax, 'color': color, 'shape': 'hspline'})]
)

fig.update_layout(height=800, xaxis={'title': 'Horsepower'},
                  yaxis={'title': 'MPG', 'domain': [0.6, 1]},
                  dragmode='lasso', hovermode='closest')

# Build color selection widget
color_toggle = widgets.ToggleButtons(
    options=['None', 'Red', 'Blue'],
    index=1, description='Brush Color:', disabled=False)

# Update color callback
def update_color(trace, points, state):
    # Compute new color array
    new_color = np.array(fig.data[0].marker.color)
    new_color[points.point_inds] = color_toggle.index

    with fig.batch_update():
        # Update scatter color
        fig.data[0].marker.color = new_color

        # Update parcats colors
        fig.data[1].line.color = new_color

# Register callback on scatter selection...
fig.data[0].on_selection(update_color)
# and parcats click
fig.data[1].on_click(update_color)

# Display figure
widgets.VBox([color_toggle, fig])


# In[ ]:


import plotly.graph_objects as go
import ipywidgets as widgets
import pandas as pd
import numpy as np

cars_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/imports-85.csv')

# Build parcats dimensions
categorical_dimensions = ['body-style', 'drive-wheels', 'fuel-type']

dimensions = [dict(values=cars_df[label], label=label) for label in categorical_dimensions]

# Build colorscale
color = np.zeros(len(cars_df), dtype='uint8')
colorscale = [[0, 'gray'], [0.33, 'gray'],
              [0.33, 'firebrick'], [0.66, 'firebrick'],
              [0.66, 'blue'], [1.0, 'blue']]
cmin = -0.5
cmax = 2.5

# Build figure as FigureWidget
fig = go.FigureWidget(
    data=[go.Scatter(x=cars_df.horsepower, y=cars_df['highway-mpg'],
                marker={'color': color, 'cmin': cmin, 'cmax': cmax,
                        'colorscale': colorscale, 'showscale': True,
                        'colorbar': {'tickvals': [0, 1, 2], 'ticktext': ['None', 'Red', 'Blue']}},
                     mode='markers'),

      go.Parcats(domain={'y': [0, 0.4]}, dimensions=dimensions,
                   line={'colorscale': colorscale, 'cmin': cmin,
                   'cmax': cmax, 'color': color, 'shape': 'hspline'})]
)

fig.update_layout(height=800, xaxis={'title': 'Horsepower'},
                  yaxis={'title': 'MPG', 'domain': [0.6, 1]},
                  dragmode='lasso', hovermode='closest')

# Build color selection widget
color_toggle = widgets.ToggleButtons(
    options=['None', 'Red', 'Blue'],
    index=1, description='Brush Color:', disabled=False)

# Update color callback
def update_color(trace, points, state):
    # Compute new color array
    new_color = np.array(fig.data[0].marker.color)
    new_color[points.point_inds] = color_toggle.index

    with fig.batch_update():
        # Update scatter color
        fig.data[0].marker.color = new_color

        # Update parcats colors
        fig.data[1].line.color = new_color

# Register callback on scatter selection...
fig.data[0].on_selection(update_color)
# and parcats click
fig.data[1].on_click(update_color)

# Display figure
widgets.VBox([color_toggle, fig])


# In[ ]:





# In[ ]:





# In[ ]:


import plotly.graph_objects as go

import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/bcdunbar/datasets/master/parcoords_data.csv")

fig = go.Figure(data=
    go.Parcoords(
        line = dict(color = df['colorVal'],
                   colorscale = 'Electric',
                   showscale = True,
                   cmin = -4000,
                   cmax = -100),
        dimensions = list([
            dict(range = [32000,227900],
                 constraintrange = [100000,150000],
                 label = "Block Height", values = df['blockHeight']),
            dict(range = [0,700000],
                 label = 'Block Width', values = df['blockWidth']),
            dict(tickvals = [0,0.5,1,2,3],
                 ticktext = ['A','AB','B','Y','Z'],
                 label = 'Cyclinder Material', values = df['cycMaterial']),
            dict(range = [-1,4],
                 tickvals = [0,1,2,3],
                 label = 'Block Material', values = df['blockMaterial']),
            dict(range = [134,3154],
                 visible = True,
                 label = 'Total Weight', values = df['totalWeight']),
            dict(range = [9,19984],
                 label = 'Assembly Penalty Wt', values = df['assemblyPW']),
            dict(range = [49000,568000],
                 label = 'Height st Width', values = df['HstW'])])
    )
)
fig.show()


# In[ ]:




