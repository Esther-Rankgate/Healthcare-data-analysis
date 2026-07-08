#import python modules
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

#import, sort and create new data frame
Data = pd.read_csv("worldometer_coronavirus_summary_data.csv")                                            #read that data using pandas
view = Data[['country', 'total_deaths', 'population']]                                                    # pick out specific columns
view = view.rename(columns={'country': 'Country', 'total_deaths': 'Deaths', 'population': 'Population' }) # rename those columns

fig3 = go.Figure(data=[go.Table(                                                                          # display the table using plotly
    header=dict(values=list(view.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[view.Country, view.Deaths, view.Population],
               fill_color='lavender',
               align='left'))
])
fig3.update_layout(
    title=dict(
        text="<b>COVID-19 Statistics by Country</b>", # HTML tags like <b> work for bolding
        font=dict(size=24, color="black"),            # Change font size and color
        x=0.5,                                        # Centers the title (0 = left, 1 = right)
        xanchor='center'
    ),
    margin=dict(t=60) # Adds top margin space so the title doesn't overlap the table
)

pio.renderers.default = "browser"
fig3.show()

#calculate total deaths per 100,000 in each country and display as colored map 
per = []
for i in range(0,226,1):
    result = (newData.iloc[i,1] / newData.iloc[i,2]) * 100000
    per.append(result)
perarray = np.array(per)

newData1 = pd.DataFrame({'Country': countryname,'Total deaths': deaths, 'Population': population, 'Death per 100,000': perarray})

fig = px.choropleth(
    newData1,
    locations="Country",
    locationmode="country names",         
    color="Death per 100,000",              
    hover_name="Country",           
    color_continuous_scale="Reds", 
    title="Covid 19 deaths per 100,000 by country 2020",
    scope="world",                
    projection="natural earth"
)

fig.update_layout(
    geo=dict(showframe=False, showcoastlines=True),
    margin=dict(l=0, r=0, t=50, b=0)
)

pio.renderers.default = "browser"
fig.show()


#bar graph of COVID-19 fatality data in South America 
Data1 = Data[Data["continent"] == 'South America']

countries1 = Data1["country"].unique()
countryname1 = []
death = []
popu = []

for country in countries1:
    currentcountry = Data1[(Data1['country'] == country)]
    countryname1.append(country)
    death.append(currentcountry['total_deaths'].sum())
    popu.append(currentcountry['population'].sum())

newData2 = pd.DataFrame({'Country': countryname1, 'Total Deaths': death, 'Population': popu})

perr = []
for i in range(0,14,1):
    result = (newData2.iloc[i,1] / newData2.iloc[i,2]) * 100000
    perr.append(result)
perrarray = np.array(perr)

newData3 = pd.DataFrame({'Country': countryname1,'Death per 100,000': perrarray})

fig1 = px.bar(newData3, y='Death per 100,000', x='Country', text_auto='.2s',
            title="Total Deaths per 100,000 due to COVID 19 in South America")
fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
pio.renderers.default = "browser"
fig1.show()
