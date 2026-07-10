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
def func(group):
    td = group['Deaths']
    tp = group['Population']

    rate = (td/tp) * 100000
    return rate
country_rate = (view.groupby('Country').apply(func, include_groups=False))
country_rate = country_rate.reset_index(name='Deaths per 100,000')
fig = px.choropleth(
    country_rate,
    locations="Country",
    locationmode="country names",         
    color="Deaths per 100,000",              
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
view1 = Data1[['country', 'total_deaths', 'population']]
view1 = view1.rename(columns={'country': 'Country', 'total_deaths': 'Deaths', 'population': 'Population' })

sa_rate = (view1.groupby('Country').apply(func, include_groups=False))
sa_rate = sa_rate.reset_index(name='Deaths per 100,000')

fig1 = px.bar(sa_rate, y='Deaths per 100,000', x='Country', text_auto='.2s',
            title="Total Deaths per 100,000 due to COVID 19 in South America")
fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
pio.renderers.default = "browser"
fig1.show()

#daily data in peru 
df = pd.read_csv("worldometer_coronavirus_daily_data.csv")
df["date"] = pd.to_datetime(df["date"])

peru_df = df[
    (df["country"] == "Peru") &
    (df["date"] >= "2020-02-15") &
    (df["date"] <= "2022-05-14")
]

fig = px.scatter(
    peru_df,
    x="date",
    y="daily_new_deaths",
    trendline="lowess",
    trendline_options={"frac": 0.03},
    title="Daily New Deaths in Peru (2020–2022)"
)

fig.show()
