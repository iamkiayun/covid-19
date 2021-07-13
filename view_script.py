#visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#scraping
import requests
from bs4 import BeautifulSoup
import json
from scraper_covid import scrape_kini_labs

#time
import schedule
import time


""" 
Cummulative Confirmed Cases
"""
def cumul_confirm_cases(chartdata_df2):
    graph = px.bar(chartdata_df2, x='date', y='totalCase',
                   labels={
                       'date': '',
                       'totalCase':''
                   },
                   title='Cumulative confirmed cases')
    return graph


"""
#daily confirmed cases
"""
def daily_confirm_cases(chartdata_df2):
    graph_daily = px.bar(chartdata_df2, x='date', y='newCase',
               labels={
                   'date': '',
                   'newCase':''
               },
               title='Daily new cases')
    return graph_daily

"""
# positive rate
"""
def daily_positive_rate(chartdata_df2):
    positive_rate_daily = px.bar(chartdata_df2, x='date', y='Positivity rate',
                       labels= {
                           "date": "",
                           "total_daily": "Positivity Rate (%)"
                       },
                       title='Daily Positivity Rate')

    positive_rate_daily.update_yaxes(ticksuffix= '%')
    positive_rate_daily.update_layout(yaxis_title="")
    return positive_rate_daily

"""
# vaccine daily
"""
def vaccine_daily(vax_malaysia_citf_df):
    vaccine_daily = px.bar(vax_malaysia_citf_df, x='date', y=['dose1_daily','dose2_daily'],
                           template='simple_white',
                           labels= {
                               "date": "",
                               "dose1_daily": "1st dose",
                               "dose2_daily": "2nd dose"
                           },
                           title='Daily vaccine doses administered',
                           #color_discrete_sequence=px.colors.sequential.Plasma_r
                           color_discrete_map={'dose1_daily':'#009dc4',    #rgba(255,0,0,0.4)      #FFA15A    #46039F      #3EB489
                                                'dose2_daily':'#a88905'}   #E1AD01

                           )
    vaccine_daily.update_yaxes( # the y-axis is in dollars
        tickprefix="", showgrid=True, showticklabels=True
    )
    vaccine_daily.update_xaxes( # the y-axis is in dollars
        tickprefix="", showgrid=False
    )
    vaccine_daily.update_traces( #marker_line_color='#009dc4',       ##009dc4 #a88905
                      marker_line_width=0, opacity=1)
    # vaccine_daily.update_traces(marker_color=['green', 'blue'])
    vaccine_daily.update_layout(yaxis_title=None, legend_title_text='')

    def custom_legend_name(fig, new_names):
        for i, new_name in enumerate(new_names):
            fig.data[i].name = new_name
    custom_legend_name(fig=vaccine_daily,new_names=['1st dose', '2nd dose'])

    return vaccine_daily

"""
#resitration, target population to be vaccinated
"""

def vaccination_target(vax_malaysia_citf_df, vax_reg_malaysia,population_df):
    data= {'type':['individual with 2nd_dose','individual with 1st_dose', 'registered individuals'],
           'total':[round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1],2),
                    round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1],2),
                    round(vax_reg_malaysia['total'].iloc[-1],2)
                    ]}
    compare_df = pd.DataFrame(data=data)
    target = px.bar(compare_df, x='total', y='type', orientation='h')

    target.update_layout(yaxis_title='', xaxis_title='', showlegend=False, legend_title_text= '')
    target.update_layout(title='Vaccination Target')
    target.update_xaxes(range=[0,30000000], showgrid=False)
    target.update_yaxes(showticklabels=False)
    colors = ['#0c3953']*3    #f67e7d #843b62 #0c3953
    colors[1] = '#009dc4'  #1st dose
    colors[0] = '#a88905'  #2nd dose
    target.update_traces(marker_color=colors, #marker_line_color='#009dc4',       ##009dc4 #a88905
                      marker_line_width=0, opacity=1, width=0.4)
    # Source
    target.add_annotation(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Source: Covid-19 Immunisation Task Force (CITF)',
                                  font=dict(#family='Arial',
                                  #           size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))
    target.add_vline(x=26130000, line_width=3, line_dash="dash", line_color="red", #population_df['pop'].iloc[0]
                     annotation_text="target: 26.13 million <br>(80% population<br> to be vaccinated)",
                     annotation_position='left')

    target.add_annotation(dict(xref='paper', yref='paper', x=0.07, y=0.61,
                                  xanchor='left', yanchor='auto',
                                  text=f"population with at least 1 dose: {round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/1000000,2)} mil " #population with at least 1 dose
                                       f"({round(vax_malaysia_citf_df['dose1_cumul'].iloc[-1]/population_df['pop'].iloc[0]*100,2)}%)",
                                  showarrow=False,
                                  #font=dict(family='Arial',
                                            #size=12,
                                            # color='rgb(150,150,150)'
                               ))
    target.add_annotation(dict(xref='paper', yref='paper', x=0.07, y=0.24,
                                  xanchor='left', yanchor='auto',
                                  text= f"fully inoculated: {round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1]/1000000,2)} mil "
                                        f"({round(vax_malaysia_citf_df['dose2_cumul'].iloc[-1]/population_df['pop'].iloc[0]*100,2)}%)",
                                  showarrow=False
                                  #font=dict(family='Arial',
                                            #size=12,
                                            # color='rgb(150,150,150)'
                                ))

    target.add_annotation(dict(xref='paper', yref='paper', x=0.07, y=0.97,
                                  xanchor='left', yanchor='auto',
                                  text=f"registration: {round(vax_reg_malaysia['total'].iloc[-1]/1000000,2)} mil "
                                       f"({round(vax_reg_malaysia['total'].iloc[-1]/population_df['pop'].iloc[0]*100,2)}%)",
                                  showarrow=False
                                  #font=dict(family='Arial',
                                            #size=12,
                                            # color='rgb(150,150,150)'
                               ))

    target.add_annotation(dict(xref='paper', yref='paper', x=-0.081, y=1.08,
                               xanchor='left', yanchor='auto',
                               text=f"* total population estimated at {round(population_df['pop'].iloc[0]/1000000,2)} mil",
                               font=dict(color='rgb(150,150,150)'),
                               showarrow=False
                               ))

    return target

"""
#vaccination progress
"""
def vaccination_progress_line(vax_malaysia_citf_df, population_df):
    #total population is estimated at 32.66 million
    total_pop = population_df.iloc[0]['pop']
    # vaccine_df['total_cum/total_pop'] = vaccine_df['dose2_cumul']/ total_pop*100                      #vaccine_df['total_cum/total_pop']     #vaccine_df['dose2_cumul']
    # vaccine_df['first/total_pop'] = vaccine_df['dose1_cumul']/ total_pop**100                         #vaccine_df['first/total_pop']         #vaccine_df['dose1_cumul']
    second_cumul_percent = vax_malaysia_citf_df['dose2_cumul']/total_pop*100
    first_cumul_percent = vax_malaysia_citf_df['dose1_cumul']/total_pop*100
    vaccine_population = px.line(vax_malaysia_citf_df, x='date', y=[first_cumul_percent,second_cumul_percent],
                           title='Population vaccination progress',
                           template='simple_white',
                           color_discrete_sequence=['#009dc4','#a88905']
                           # color_discrete_map={'first_cumul_percent': '#009dc4',
                           #                      'second_cumul_percent': '#a88905'}
                             )

    def custom_legend_name(fig, new_names):
        for i, new_name in enumerate(new_names):
            fig.data[i].name = new_name

    custom_legend_name(fig=vaccine_population, new_names=['received 1st dose only', 'fully inoculated with 2nd dose'])

    vaccine_population.update_yaxes( # the y-axis is in dollars
         ticksuffix='%',showgrid=True, showticklabels=True            #tickprefix=""
    )

    vaccine_population.update_layout(yaxis_title='', xaxis_title='', showlegend=True, legend_title_text= ''
                                     )

    vaccine_population.add_scatter(x=[vax_malaysia_citf_df.iloc[-1]['date']],
                                   y=[second_cumul_percent.iloc[-1]],
                                   text=[f"{round(second_cumul_percent.iloc[-1],2)}%"],
                                   mode='markers+text',
                                   marker=dict(color='#a88905', size=1),
                                   # textfont=dict(color='', size=20),
                                   textposition='middle left',
                                   showlegend=False)

    vaccine_population.add_scatter(x=[vax_malaysia_citf_df.iloc[-1]['date']],
                                   y=[first_cumul_percent.iloc[-1]],
                                   text=[f"{round(first_cumul_percent.iloc[-1],2)}%"],
                                   mode='markers+text',
                                   marker=dict(color='#009dc4', size=1),
                                   # textfont=dict(color='', size=20),
                                   textposition='middle left',
                                   showlegend=False)
    return vaccine_population


if __name__ == '__main__':
    cumul_confirm_cases(chartdata_df2)
    daily_confirm_cases(chartdata_df2)
    daily_positive_rate(chartdata_df2)
    vaccine_daily(vax_malaysia_citf_df)
    vaccination_target(vax_malaysia_citf_df, vax_reg_malaysia, population_df)
    vaccination_progress_line(vax_malaysia_citf_df, population_df)