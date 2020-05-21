# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:01:53 2020

@author: rongxu
"""

import pandas as pd
import numpy as np
from numpy import arange
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme
import dash_table.FormatTemplate as FormatTemplate
import dash_daq as daq

df_dim_order=pd.read_csv("data/dimvalue_ordering.csv")

colors={'blue':'rgba(18,85,222,100)','yellow':'rgba(246,177,17,100)','transparent':'rgba(255,255,255,0)','grey':'rgba(191,191,191,100)',
       'lightblue':'rgba(143,170,220,100)'}

domain_set = ["Cost & Utilization  Reduction", "Improving Disease Outcome",
                 "Decreasing Health Disparities", "Increasing Patient Safety",
                 "Enhancing Care Quality", "Better Patient Experience"]

domain_colordict={'Cost & Utilization  Reduction':'rgba(246,177,17,0.7)','Improving Disease Outcome':'rgba(31,64,229,0.7)','Decreasing Health Disparities':'grey'
                  ,'Increasing Patient Safety':'yellow' ,'Enhancing Care Quality':'blue' ,'Better Patient Experience':'white'} #'rgba(223,136,133,0.7)' pink   'rgba(31,64,229,0.7)' blue rgba(246,177,17,0.7) yellow
    
  
table_header_bg_color = "#f1f6ff"

def bargraph_overall(df):  #df_overall['month'] df_overall['base'] df_overall['adjusted']
    
    x_overall=df['month']
    y1_overall=df['base']
    y2_overall=df['adjusted']
    y3_trend=df['trend']
    n=len(x_overall)
    
    fig_overall = make_subplots(specs=[[{"secondary_y": True}]])

    fig_overall.add_trace(
        go.Bar(
            name='Cumulative Revenue', 
            x=x_overall, 
            y=y1_overall,
            text=y1_overall,
            textposition='auto',
            texttemplate='%{y:.2s}',
            marker=dict(
                color=colors['blue'],
                opacity=arange(0.34,0.34+0.06*n,0.06) 
                       ),
            hovertemplate='%{y:,.0f}',
        ),
        row=1,col=1,secondary_y=False,
    )
        
    fig_overall.add_trace(    
        go.Bar(
            name='Monthly Revenue', 
            x=x_overall, 
            y=y2_overall,
            text=y2_overall,
            textposition='inside',
            texttemplate='%{y:.2s}',
            marker=dict(
                color=colors['yellow'],
                opacity=arange(0.34,0.34+0.06*n,0.06) 
                       ),
            hovertemplate='%{y:,.0f}',
        ),
        row=1,col=1,secondary_y=False,
    )
    
    
    fig_overall.add_trace(
        go.Scatter(
            x=x_overall[1:], 
            y=y3_trend[1:],
            name="Monthly Increasing",
            marker=dict(color=colors['grey']),
            mode='lines+markers+text',
            line=dict(color=colors['grey']),
            textfont=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="black"
            ),
            text=y3_trend[1:],
            textposition='top center',
            texttemplate='%{y:.0%}',
            hovertemplate='%{y:.2%}',
        ),
        row=1,col=1,secondary_y=True,
    )
    # Change the bar mode
    fig_overall.update_layout(
        barmode='stack',
        title='Monthly and Cumulative Revenue',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        legend=dict(
            orientation='h',
            x=0.0,y=-0.1
        ),
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1,
        ),
        yaxis2 = dict(
        showticklabels=False,
       # tickformat='%',
        rangemode="tozero",
       # nticks=3,
       # showgrid = True,
       # gridcolor =colors['grey'],
        ),
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        
        margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
    )
    return fig_overall

def waterfall_overall(x,y1,y2): #df_waterfall['label']  df_waterfall['base'] df_waterfall['adjusted']

    x_waterfall=x
    y1_waterfall=y1
    y2_waterfall=y2
    fig_waterfall = go.Figure(data=[
        go.Bar(
            name='',
            x=x_waterfall, 
            y=y1_waterfall,
            text=y1_waterfall,
            textposition='auto',
            textfont=dict(color=['white','white',colors['transparent'],'white','white']),
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=[colors['blue'],colors['blue'],colors['transparent'],colors['blue'],colors['grey']],
                    opacity=[1,0.7,0,0.5,0.7]
                    ),
            marker_line=dict( color = colors['transparent'] ),
            hovertemplate='%{y:,.0f}',
            hoverinfo='y',
            
        ),
        go.Bar(  
            name='',
            x=x_waterfall, 
            y=y2_waterfall,
            text=y2_waterfall,
            textposition='outside',
            textfont=dict(color=[colors['transparent'],colors['transparent'],'black',colors['transparent'],'black']),
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=colors['yellow'],
                    opacity=0.7
                    ),
            hovertemplate='%{y:,.0f}',
            hoverinfo='y',
        )
    ])
    # Change the bar mode
    fig_waterfall.update_layout(
        barmode='stack',
        title='Revenue Projection',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1,
        ),
        showlegend=False,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
    )
    return fig_waterfall  



def tbl_utilizer(df_utilizer):
    utilizer_tbl=dash_table.DataTable(
        data=df_utilizer.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df_utilizer.columns],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Condensed',
            'fontSize':16,
            'backgroundColor':"#f7f7f7"
        },
        style_cell_conditional=[
            {'if': {'column_id': df_utilizer.columns[0]},
             'width': '6rem',
             'font-family':'NotoSans-Condensed',
            },     
        ],
        style_table={
            'back':  colors['blue']
        },
        style_header={
            'height': '4rem',
            'backgroundColor': table_header_bg_color,
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#1357DD'
        },
    )
    
       
    return utilizer_tbl

def piechart_utilizer(label,value): #df_util_split['Class']  df_util_split['%']
    label_pie=label
    value_pie=value
    fig_util_split = go.Figure(data=[
        go.Pie(        
            labels=label_pie, 
            values=value_pie,
            pull=[0,0,0.1,0],
            marker=dict(
                    colors=["#1357DD","F5B111","#df8885"]            
                    ),
            textinfo='label+percent',
            textposition='auto',
            hoverinfo='skip',
        )
    ])
    fig_util_split.update_layout(
       showlegend=False,
       margin=dict(l=0,r=0,b=0,t=0,pad=0),
       paper_bgcolor=colors["transparent"],
       font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )   
    return fig_util_split

def bargraph_h(x,y):#df_script_per_util['avg script']  df_script_per_util['label']
    x_script_per_util=x
    y_script_per_util=y
    fig_script_per_util = go.Figure(data=[
        go.Bar(
            name='',
            x=x_script_per_util, 
            y=y_script_per_util,
            text="",
            textposition='inside', 
            texttemplate='%{x:.2s}',
            width=0.5,
            textangle=0,
            marker=dict(
                    color=[colors['grey'],'#1357DD','#1357DD'],
                    opacity=[0.7,0.7,1]
                    ),
            orientation='h',
            hoverinfo='y',
            hovertemplate='%{x:,.2f}',
        )
    ])
    # Change the bar mode
    fig_script_per_util.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        margin=dict(l=0,r=0,b=30,t=30,pad=10),
       font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )
    return fig_script_per_util

def bargraph_stack3(x,y1,y2,y3) : #   df_tot_script_split['dosage'] df_tot_script_split['YTD'] df_tot_script_split['Annualized'] df_tot_script_split['Plan Target']
    x_tot_script_split=x
    y1_tot_script_split=y1
    y2_tot_script_split=y2
    y3_tot_script_split=y3
    fig_tot_script_split = go.Figure(data=[
        go.Bar(
            name='YTD', 
            x=x_tot_script_split, 
            y=y1_tot_script_split,
            text=y1_tot_script_split,
            textposition='auto',
            textangle=0,
            texttemplate='%{y:.2s}',
            marker=dict(
                    color='#1357DD',
                    opacity=1
                    ),
            hovertemplate='%{y:,.0f}',
        ),
        go.Bar(
            name='Annualized', 
            x=x_tot_script_split, 
            y=y2_tot_script_split,
            text=y2_tot_script_split,
            textposition='inside',
            textangle=0,
            texttemplate='%{y:.2s}',
            marker=dict(
                    color='#1357DD',
                    opacity=0.7
                    ),
            hovertemplate='%{y:,.0f}',
        ),
        go.Bar(
            name='Plan Target', 
            x=x_tot_script_split, 
            y=y3_tot_script_split,
            text=y3_tot_script_split,
            textposition='inside',
            textangle=0,
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=colors['grey'],
                    opacity=0.7
                    ),
            hovertemplate='%{y:,.0f}',
        )
    ])
    # Change the bar mode
    fig_tot_script_split.update_layout(
        barmode='group',
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        legend=dict(
            orientation='h',
            x=0.2,y=-0.2
        ),
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1
        ),
        #hovermode=True,
        margin=dict(l=0,r=0,b=30,t=50,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )    
    return fig_tot_script_split


def bubblegraph(df_domain_perform,traces,obj): # 数据，[0,1] ,'Domain' or 'Measure'
    
    x = [0+1*i/100 for i in range(100)]
    y = [-0.15+0.3*i/100 for i in range(100)]
    z = []

    for xi in x:
        zt = []
        for yi in y:
            zt.append(0.8-0.6*(1-xi)-yi)
        z.append(zt)

    fig_domain_perform = go.Figure()

    fig_domain_perform.add_trace( go.Heatmap(x=x,y=y,z=z,
                                             colorscale=[[0, 'rgba(241,0,28,0.6)'], [0.3, 'rgba(241,0,28,0.2)'], 
                                                         [0.5, 'rgba(241,0,28,0)'],[1, 'rgba(241,0,28,0)']],
                                             colorbar=dict(len=1,
                                                           tickmode='array',
                                                           tickvals=[0.08,0.6],
                                                           ticktext=['High risk','Low risk'],
                                                           x=1,y=0.7
                                                           ),
                                            hoverinfo='skip',))

    for k in traces:
        fig_domain_perform.add_trace(
                go.Scatter(        
                x=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Weight'] , 
                y=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Performance Diff from Target'] ,
                x0=0,y0=0,
                #text=df_domain_perform[df_domain_perform['Domain']==domain_set[k]][obj],
                mode='markers+text',             
                name=domain_set[k],
                #dx=0.1,dy=0.1,
                marker=dict(
                    size=df_domain_perform[df_domain_perform['Domain']==domain_set[k]]['Weight']*4000,
                    color=domain_colordict[domain_set[k]],
                    opacity=0.8,
                    sizemode='area',
                )

            )
        )

    annotations = []
    annotations.append(dict(xref='paper', yref='paper',
                            x=0, y=1,
                            text='Performance<br>(% diff from target)',
                            font=dict(family='NotoSans-CondensedLight', size=8, color='#38160f'),
                            showarrow=False))
    annotations.append(dict(xref='paper', yref='paper',
                            x=0.98, y=0.47,
                            text='Weight',
                            font=dict(family='NotoSans-CondensedLight', size=8, color='#38160f'),
                            showarrow=False))

    fig_domain_perform.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        annotations=annotations,
        showlegend=True,
        xaxis = dict(
            tickmode='linear',
            range=[0,0.9],
            tick0=0,
            dtick=0.1,
            showticklabels=True,
            tickformat='%',
            position=0.48,

            showgrid=True,
            gridcolor =colors['grey'],

            zeroline=False,
            zerolinecolor='grey',
            rangemode="tozero"
        ),
        margin=dict(l=0,r=0,b=50,t=10,pad=0),
       font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#38160f"
        ),
        yaxis = dict(
            #showgrid = True, 
            #gridcolor =colors[3],
            showline=True,
            linecolor='grey',
            tickmode='linear',
            dtick=0.05,
            range=[-0.15,0.15],
            tickformat='%',
            showticklabels=True,
            zeroline=True,
            zerolinecolor='grey',
            ticks='inside'
        ),
        legend=dict(
            orientation='h',
            x=0,y=-0.05
        ),
        #hovermode=True,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
    )
    return fig_domain_perform
    '''
def bubblegraph(x,y,t):#df_domain_perform['weight'] df_domain_perform['performance'] df_domain_perform['domain']
    x_domain_perform=x
    y_domain_perform=y
    t_domain_perform=t
    color_set=['rgb(93, 164, 214)', 'rgb(255, 144, 14)', 'rgb(44, 160, 101)', 'rgb(255, 65, 54)']
    opacity_set=[1, 0.8, 0.6, 0.4]
    bubble_traces = []
    for i in range(len(x)):
        bubble_traces.append(go.Scatter(dict(x = [x_domain_perform[i]], y = [y_domain_perform[i]],
                                      x0=0,y0=0,
            text=t_domain_perform[i],
            mode='markers+text',
            #dx=0.1,dy=0.1,
            marker=dict(
                size=60,
                color=color_set[i],
                opacity=opacity_set[i]),
            name = i+1)))
    return bubble_traces



def bubblegraph_layout():
    bubble_layout = dict(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        #showlegend=True,
       # shapes=dict(x0=0,y0=0),
        xaxis = dict(
            tickmode='linear',
            tick0=0,
            dtick=0.1,
            showticklabels=True,
            tickformat='%',
            position=0.37,
            
            showgrid=True,
            gridcolor =colors['grey'],
            
            zeroline=False,
            zerolinecolor='grey',
            rangemode="tozero"
        ),
        margin=dict(l=0,r=10,b=50,t=10,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
        yaxis = dict(
            #showgrid = True, 
            #gridcolor =colors[3],
            showline=True,
            linecolor='grey',
            tickmode='linear',
            dtick=0.1,
            tickformat='%',
            showticklabels=True,
            zeroline=True,
            zerolinecolor='grey',
            ticks='inside'
        ),
        hovermode=False
    )
    return bubble_layout
'''
def waterfall_domain(x,y1,y2): #df_waterfall['label']  df_waterfall['base'] df_waterfall['adjusted']

    x_waterfall=x
    y1_waterfall=y1
    y2_waterfall=y2
    fig_waterfall = go.Figure(data=[
        go.Bar(
            
            x=x_waterfall, 
            y=y1_waterfall,
            text=y1_waterfall,
            textposition='auto',
            textfont=dict(color=['white','white','white',colors['transparent'],'white']),
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=[colors['blue'],colors['blue'],colors['grey'],colors['transparent'],colors['grey']],
                    opacity=[1,0.7,0.7,0,0.7]
                    ),
            marker_line=dict( color = colors['transparent'] )
            
        ),
        go.Bar(     
            x=x_waterfall, 
            y=y2_waterfall,
            text=y2_waterfall,
            textposition='inside',
            texttemplate='%{y:.2s}',
            marker=dict(
                    color=colors['yellow'],
                    opacity=0.7
                    )
        )
    ])
    # Change the bar mode
    fig_waterfall.update_layout(
        barmode='stack',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        yaxis = dict(
            showgrid = True, 
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1,
        ),
        showlegend=False,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=14,
            color="#38160f"
        ),
    )
    return fig_waterfall  

def bargraph_perform(df_measure_perform,d): #df_measure_perform, 0 or 1 or 2.... domain number

    x=df_measure_perform[df_measure_perform['Domain']==domain_set[d]]['Performance Diff from Target'].tolist()
    y=df_measure_perform[df_measure_perform['Domain']==domain_set[d]]['Measure'].tolist()
    x.reverse()
    y.reverse()
    fig_measure_perform = go.Figure(data=[
        go.Bar(
            name='',
            x=x, 
            y=y,
            text=x,
            textposition='inside',
            texttemplate='%{x}',
            marker=dict(
                    color=['green' if i>0 else 'red' for i in x ],
                    opacity=0.7
                    ),
            orientation='h',
            width=0.5,
            hovertemplate='%{x:.2%}',
            hoverinfo='x',
        )
    ])
    # Change the bar mode
    fig_measure_perform.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        xaxis=dict(
            tickformat='%',
            zeroline=True,
            zerolinecolor='black'
        ),
        modebar=dict(
                bgcolor=colors['transparent']
                ),
        margin=dict(l=0,r=0,b=30,t=50,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
    )
    return fig_measure_perform

'''def tbl_measure(df_measure_perform,d): 

    df=df_measure_perform[df_measure_perform['Domain']==domain_set[d]].iloc[:,1:6]
    tbl = go.Figure(data=[
        go.Table(
            header=dict(
                values=df.columns,
                line_color='white' ,       
                fill_color=colors['yellow'],
                align=['left','center'],
                font=dict(color='white',size=10)
            ),
            cells=dict(
                values=df.T,
                line_color='white' ,       
                fill_color='lightgrey',
                font=dict(size=10)
            ),
            columnwidth=[0.4,0.15,0.15,0.15,0.15],
        )
    ])
    
    tbl.update_layout(
       autosize=True,
       margin=dict(l=0,r=0,b=30,t=50,pad=0),
       paper_bgcolor=colors["transparent"],
       font=dict(
            family="NotoSans-CondensedLight",
            size=12,
            color="#38160f"
        ),
    )     
    return tbl'''

def tbl_measure(df_measure_perform,d):
    df=df_measure_perform[df_measure_perform['Domain']==domain_set[d]].iloc[:,1:]
    if len(df)>0 :
        df['highlight']=df.apply(lambda x : 1 if (x['Performance Diff from Target']<0.05)& (x['Weight']>0.3)  else 0, axis=1)
    else: df['highlight']=1
    
    percent_list=['Performance Diff from Target','Weight']
    
    measure_tbl=dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[ {'id': c, 'name': c,'type': 'numeric',"format":FormatTemplate.percentage(1)} if c in percent_list else {'id': c, 'name': c} for c in df.columns ],
        sort_action="native",
        sort_mode='multi',
        style_data={
            'height': 'auto',
            'whiteSpace': 'normal',
        },
        style_data_conditional=[
            {
                'if': {'column_id':c,
                    'filter_query': '{highlight} eq 1' },
                'backgroundColor': '#ffe3e5',
                'color': 'black',
            }  for c in df.columns
        ],
        style_cell={
            'width':'auto',
            'textAlign': 'center',
            'font-family':'NotoSans-Condensed',
            'fontSize':14
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             'minWidth': '2.5rem',
             'font-family':'NotoSans-CondensedLight',
            }, 
            {'if': {'column_id': 'highlight'},
            'display': 'none'}
        ],
        style_table={
            'back':  colors['blue']
        },
        style_header={
            'height': 'auto',
            'whiteSpace': 'normal',
            'maxWidth':'3rem',
            'backgroundColor': table_header_bg_color,
            'fontWeight': 'bold',
            'font-family':'NotoSans-Condensed',
            'fontSize':11,
            'color': '#1357DD'
        },
    )
    
       
    return html.Div(measure_tbl, style={"padding":"1rem"})

def tbl_non_contract(df,measures):
    df=df[df['Measure'].isin(measures)]
    
    percent_list=['Performance Diff from Target']
    
    measure_tbl=dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[ {'id': c, 'name': c,'type': 'numeric',"format":FormatTemplate.percentage(1)} if c in percent_list else {'id': c, 'name': c} for c in df.columns ],
        sort_action="native",
        sort_mode='single',
        sort_by=[{"column_id":"Performance Diff from Target","direction":"desc"},],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Condensed',
            'fontSize':14
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             'maxWidth': '4rem',
             'font-family':'NotoSans-CondensedLight',
            },            
        ],
        style_table={
            'back':  colors['blue']
        },
        style_header={
            'height': 'auto',
            'whiteSpace': 'normal',
            'maxWidth': '2rem',
            'backgroundColor': table_header_bg_color,
            'fontWeight': 'bold',
            'font-family':'NotoSans-Condensed',
            'fontSize':12,
            'color': '#1357DD'
        },
    )
    
       
    return measure_tbl

####################################################################################################################################################################################
######################################################################       Drilldown         ##################################################################################### 
#################################################################################################################################################################################### 
def drill_bubble(df):
    df['Weight']=df['Pt_Count']/df.values[0,7]
    n=len(df)
    valmax=((df['% Cost Diff from Target']/0.01).apply(np.ceil)*0.01).max()+0.05
    divide=valmax/2
    
    colorbar1=dict(
        len=0.5,
       tickmode='array',
       tickvals=[-valmax+0.05,valmax-0.05],
       ticktext=['Better','Worse'],
       thickness=5,
       x=1,y=0.78
    )
    colorbar2=dict(
        len=0.5,
       tickmode='array',
       tickvals=[-valmax+0.05,valmax-0.05],
       ticktext=['Better','Worse'],
       thickness=5,
       x=1,y=0.22
    )
    colorscale=[[0, 'rgba(0,255,0,1)'],[0.5, 'rgba(0,255,0,0.2)'],[0.5, 'rgba(255,0,0,0.2)'], [1, 'rgba(255,0,0,1)']]
    #color_axis=dict(cmin=-valmax,cmax=valmax,colorscale=colorscale,colorbar=colorbar,)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.1,
        row_heights = [0.5,0.5],
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    fig.add_trace(
        go.Scatter(
            x=[0.5+i for i in range(n)],
            y=df['% Cost Diff from Target'],
            text=df['% Cost Diff from Target'],
            textposition='middle center',
            texttemplate='%{y:.1%}',
            mode="markers+text",
            marker=dict(
                size=df['Weight']*1500,
                sizemode='area',
                color=df['% Cost Diff from Target'],#df['performance'].apply(lambda x: 'red' if x>0 else 'green'),
                cmin=-valmax+0.05,
                cmax=valmax-0.05,
                #opacity=0.8,
                colorbar=colorbar1,
                colorscale=colorscale,
                showscale=True,

                #coloraxis=coloraxis1
            )

        ),
        row=1, col=1
    )


    fig.add_trace(
        go.Scatter(
            x=[0.5+i for i in range(n)],
            y=df['Contribution to Overall Performance Difference'],
            text=df['Contribution to Overall Performance Difference'],
            textposition='middle center',
            texttemplate='%{y:.1%}',
            mode="markers+text",
            marker=dict(
                size=df['Weight']*1500,
                sizemode='area',
                color=df['Contribution to Overall Performance Difference'],#df['Contribution'].apply(lambda x: 'red' if x>0 else 'green'),
                cmin=-valmax+0.05,
                cmax=valmax-0.05,
                #opacity=0.8,
                colorbar=colorbar2,
                colorscale=colorscale,
                showscale=True,
                #coloraxis=coloraxis2
            )

        ),
        row=2, col=1
    )
    
    annotations = []
    annotations.append(dict(xref='paper', yref='paper',
                            x=0, y=-0.01,yanchor='top',
                            text='*Bubble size proportional to patient count',
                            font=dict(family='NotoSans-CondensedLight', size=12, color='#38160f'),
                            showarrow=False))
    
    fig.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,#tickmode='array',tickvals=[0,1,2,3,4,5,6],
        modebar=dict( bgcolor=colors['transparent']),
        xaxis=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=False,range=[0,n],dtick=1,autorange=False,gridcolor=colors['grey'],zeroline=True ,zerolinecolor=colors['grey']),
        xaxis2=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=False,range=[0,n],dtick=1,autorange=False,gridcolor=colors['grey'],zeroline=True ,zerolinecolor=colors['grey']),
        yaxis=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=True,tickformat='%',range=[-valmax,valmax],dtick=divide,autorange=False,zeroline=True ,zerolinecolor=colors['grey']),
        yaxis2=dict(showline=True,mirror=True,linecolor=colors['grey'],showticklabels=True,tickformat='%',range=[-valmax,valmax],dtick=divide,autorange=False
                    ,zeroline=True ,zerolinecolor=colors['grey'] ),
        #coloraxis=dict(cmin=-0.5,cmax=0.5,colorscale=colorscale,colorbar=colorbar,),
        #coloraxis2=dict(cmin=-0.5,cmax=0.5,colorscale=colorscale,colorbar=colorbar,),
        #margin=dict(l=115)
        annotations=annotations,
        hovermode=False,
        margin=dict(l=2,r=2,b=20,t=2,pad=0),
        height=300,

    )
    return fig


def drillgraph_table(df_table,tableid,dim):
    tbl=dash_table.DataTable(
        id=tableid,
        data=df_table.to_dict('records'),
        columns=[ {'id': c, 'name': dim+':'+c,"selectable": True,'type': 'numeric',"format":FormatTemplate.money(0)} for c in df_table.columns ],
        column_selectable="single",
        selected_columns=[],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
       
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Condensed',
            'fontSize':14
        },
        style_cell_conditional=[
            
            {'if': {'column_id': 'highlight'},
            'display': 'none'}
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '4rem',
            'minWidth': '3rem',
            'maxWidth':'3rem',
            'whiteSpace': 'normal',
            'backgroundColor': "#f1f6ff",
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':16,
            'color': '#1357DD',
            'text-align':'center',
        },
    )
    return tbl

def drillgraph_lv1(df,tableid,dim):

    df=df.merge(df_dim_order[df_dim_order['dimension']==df.columns[0]],how='left',left_on=df.columns[0],right_on='value').sort_values(by='ordering')
    df_table=df[['YTD Avg Episode Cost']].T
    df_table.columns=df[df.columns[0]]
    
    drillgraph= [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(html.H2(""), style={"height":"2rem","display":"table"}),
                            html.Hr(className="ml-1"),
                            html.Div(html.H2("YTD CHF Related Average Cost per Patient",style={"font-size":"0.8rem","display":"table-cell", "vertical-align":"bottom"}), style={"height":"1rem","display":"table"}),
                            html.Hr(className="ml-1"),
                            html.Div(html.H2("% Diff from Target", style={"font-size":"1rem","display":"table-cell", "vertical-align":"middle"}), style={"height":"7.5rem","display":"table"}),
                            html.Hr(className="ml-1"),
                            html.Div(html.H2("Contribution to Overall Difference", style={"font-size":"1rem","display":"table-cell", "vertical-align":"middle"}), style={"height":"10rem","display":"table"}),
                        ],
                        width=3,
                        style={"padding-left":"2rem"}
                    ),

                    dbc.Col(
                        [
                            html.Div(
                                [
                                    drillgraph_table(df_table,tableid,dim)
                                ],
                                style={"padding-left":"3rem","padding-right":"5rem"}
                            ),
                            html.Div(
                                [
                                    dcc.Graph(figure=drill_bubble(df),config={'displayModeBar': False})
                                ],
                                style={"padding-top":"1rem","padding-bottom":"2rem"}
                            ),
                        ],
                        width=9,
                    ),
                ]
            )
        ]
        #style={"padding-top":"2rem","padding-bottom":"2rem"}
    
    
    return drillgraph
       
   
def dashtable_lv3(df,dimension,tableid,row_select):#row_select: numeric 0 or 1
    
    #df1=df[0:len(df)-1].sort_values(by='Contribution to Overall Performance Difference',ascending=False)
    #df1.append(df[len(df)-1:len(df)])
    #df1['id']=df1[df1.columns[0]]
    #df1.set_index('id', inplace=True, drop=False)
    df['id']=df[df.columns[0]]
    df.set_index('id', inplace=True, drop=False)

    if row_select==0:
        row_sel=False
    else:
        row_sel='single'
        
    table_lv3=dash_table.DataTable(
        data=df.to_dict('records'),
        id=tableid,
        columns=[
        {"name": ["", dimension], "id": dimension},
        {"name": ["Average CHF Related Cost Per Patient", "YTD Avg Cost"], "id": "YTD Avg Episode Cost",'type': 'numeric',"format":FormatTemplate.money(0)},
        {"name": ["Average CHF Related Cost Per Patient", "% Diff from Benchmark"], "id": "% Cost Diff from Target",'type': 'numeric',"format":FormatTemplate.percentage(1)},
        {"name": ["Average CHF Related Cost Per Patient", "Contribution to Overall Performance Difference"], "id": "Contribution to Overall Performance Difference",'type': 'numeric',"format":FormatTemplate.percentage(1)},
        {"name": ["Average Utilization Rate Per Patient", "YTD Avg Utilization Rate"], "id": "YTD Avg Utilization Rate",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": ["Average Utilization Rate Per Patient", "% Diff from Benchmark"], "id": "% Util Diff from Target",'type': 'numeric',"format":FormatTemplate.percentage(1)},
        {"name": ["Average Unit Cost", "YTD Avg Unit Cost"], "id": "YTD Avg Cost per Unit",'type': 'numeric',"format":FormatTemplate.money(0)},
        {"name": ["Average Unit Cost", "% Diff from Benchmark"], "id": "% Unit Cost Diff from Target",'type': 'numeric',"format":FormatTemplate.percentage(1)},
    ],
        merge_duplicate_headers=True,
        sort_action="custom",
        sort_mode='single',
        sort_by=[{"column_id":"Contribution to Overall Performance Difference","direction":"desc"},],
        row_selectable=row_sel,
        selected_rows=[],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
       
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             
             'fontWeight': 'bold',
            }, 
            
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '4rem',
            'minWidth': '3rem',
            'maxWidth':'3rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#1357DD',
            'text-align':'center',
        },
    )
    return table_lv3

def drilldata_process(df_drilldown,dimension,dim1='All',f1='All',dim2='All',f2='All',dim3='All',f3='All'):#dimension='Sub Category'    
    
    df_pre=df_drilldown
    
    if f1!='All':
        df_pre=df_pre[df_pre[dim1]==f1]
        
    if f2!='All':
        df_pre=df_pre[df_pre[dim2]==f2]
        
    if  f3!='All':
        df_pre=df_pre[df_pre[dim3]==f3]

    df_pre2=df_pre.groupby(list(np.unique([dimension,'Service Category', 'Sub Category'])))[df_pre.columns[14:]].agg(np.sum).reset_index()
    
    df=df_pre2.groupby([dimension]).agg(YTD_Total_cost=pd.NamedAgg(column='YTD Total Cost',aggfunc=sum)
                                             ,Annualized_Total_cost=pd.NamedAgg(column='Annualized Total Cost',aggfunc=sum)
                                             ,Target_Total_cost=pd.NamedAgg(column='Benchmark Total Cost',aggfunc=sum)
                                             ,YTD_Utilization=pd.NamedAgg(column='YTD Utilization',aggfunc=sum)
                                             ,Annualized_Utilization=pd.NamedAgg(column='Annualized Utilization',aggfunc=sum)
                                             ,Target_Utilization=pd.NamedAgg(column='Benchmark Utilization',aggfunc=sum)
                                             ,Pt_Count=pd.NamedAgg(column='Pt Count',aggfunc=np.mean)
                                             ).reset_index()
    allvalue=df.sum().values 
    allvalue[0]='All'
    if dimension in ['Service Category', 'Sub Category']:
        allvalue[-1]=df['Pt_Count'].mean()

    if len(df[df[dimension]=='Others'])>0:
        otherpos=df[df[dimension]=='Others'].index[0]
        otherlist=df.loc[otherpos]
        df.loc[otherpos]=df.loc[len(df)-1]
        df.loc[len(df)-1]=otherlist
  
    df.loc[len(df)] = allvalue
    
    df['YTD Avg Episode Cost']=df['YTD_Total_cost']/df['Pt_Count']
    df['Target Avg Episode Cost']=df['Target_Total_cost']/df['Pt_Count']
    df['Annualized Avg Episode Cost']=df['Annualized_Total_cost']/df['Pt_Count']

    df['% Cost Diff from Target']=(df['Annualized Avg Episode Cost']-df['Target Avg Episode Cost'])/df['Target Avg Episode Cost']
    df['Contribution to Overall Performance Difference']=(df['Annualized_Total_cost']-df['Target_Total_cost'])/allvalue[3]

    df['YTD Avg Utilization Rate']=df['YTD_Utilization']/df['Pt_Count']
    df['Target Avg Utilization Rate']=df['Target_Utilization']/df['Pt_Count']
    df['Annualized Avg Utilization Rate']=df['Annualized_Utilization']/df['Pt_Count']

    df['% Util Diff from Target']=(df['Annualized Avg Utilization Rate']-df['Target Avg Utilization Rate'])/df['Target Avg Utilization Rate']

    df['YTD Avg Cost per Unit']=df['YTD_Total_cost']/df['YTD_Utilization']
    df['Target Avg Cost per Unit']=df['Target_Total_cost']/df['Target_Utilization']
    df['Annualized Avg Cost per Unit']=df['Annualized_Total_cost']/df['Annualized_Utilization']

    df['% Unit Cost Diff from Target']=(df['Annualized Avg Cost per Unit']-df['Target Avg Cost per Unit'])/df['Target Avg Cost per Unit']
    
    return df

def drill_waterfall(df):

    x_waterfall=['Target','Adj','Target Adj']
    y_base=df[['base']][3:4].values[0,0]
    y_adjust=df[['adjusted']][4:5].values[0,0]

    fig_waterfall = go.Figure(data=[
        go.Bar(
            
            x=x_waterfall, 
            y=[y_base,y_base,y_base+y_adjust],
            text=[y_base,y_base,y_base+y_adjust],
            textposition='inside',
            textangle=0,
            constraintext='none',
            width=0.5,
            textfont=dict(color=['black',colors['transparent'],'black'],
                          family="NotoSans-Condensed",
                          size=14,
                          ),
            texttemplate='%{y:$,.0f}',
            marker=dict(
                    color=[colors['grey'],colors['transparent'],colors['grey']],
                    opacity=[0.5,0,0.7]
                    ),
            marker_line=dict( color = colors['transparent'] )
            
        ),
        go.Bar(     
            x=x_waterfall, 
            y=[0,y_adjust,0],
            width=0.5,
            text=[0,y_adjust,0],
            textposition='outside',
            textfont=dict(color=[colors['transparent'],'black',colors['transparent']],
                          family="NotoSans-Condensed",
                          size=14,
                          ),
            texttemplate='%{y:$,.0f}',
            marker=dict(
                    color=colors['yellow'],
                    opacity=0.7
                    )
        )
    ])
    # Change the bar mode
    fig_waterfall.update_layout(
        barmode='stack',
        plot_bgcolor=colors['transparent'],
        paper_bgcolor=colors['transparent'],
        xaxis=dict(
                tickfont=dict(family="NotoSans-Condensed",
                          size=14,)
                ),
        yaxis = dict(
            showgrid = True, 
            range=[0,y_base+y_base/5],
            gridcolor =colors['grey'],
            nticks=5,
            showticklabels=True,
            zeroline=True,
            zerolinecolor=colors['grey'],
            zerolinewidth=1,
        ),
        showlegend=False,
        hovermode=False,
        modebar=dict(
            bgcolor=colors['transparent']
        ),
        #margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
        margin=dict(l=30,r=30,b=0,t=40,pad=0,),
        
        
    )
    return fig_waterfall 

def drill_bar(df):
    bar1_y=df['base'][0:3].values.tolist()

    fig_bar = go.Figure(data=[
        go.Bar(        
            x=['YTD','Annualized','Target Adj'], 
            y=bar1_y,
            text=bar1_y,
            textposition='inside',
            texttemplate='%{y:$,.0f}',
            textfont=dict(family="NotoSans-Condensed",
                          size=14,),
            textangle=0,
            width=0.5,
            marker=dict(
                color=[colors['blue'],colors['blue'],colors['grey']],
                opacity=[1,0.7,0.7]
                       )

        ),
    ])
    fig_bar.update_layout(
        paper_bgcolor=colors['transparent'],
        plot_bgcolor=colors['transparent'],
        showlegend=False,
        modebar=dict( bgcolor=colors['transparent'] ),
        xaxis=dict(showline=True,linecolor=colors['grey'],zeroline=True ,zerolinecolor=colors['grey'], tickfont=dict(family="NotoSans-Condensed", size=14,) ), 
        yaxis=dict(showline=True,linecolor=colors['grey'],gridcolor=colors['grey'],zeroline=True ,zerolinecolor=colors['grey']),  
        hovermode=False,
        #margin=dict(l=10,r=10,b=100,t=40,pad=0),
        font=dict(
            family="NotoSans-Condensed",
            size=12,
            color="#38160f"
        ),
        margin=dict(l=30,r=30,b=80,t=40,pad=0),
    )
    return fig_bar


def gaugegraph(df,row):
    fig=daq.Gauge(
            #showCurrentValue=True,
            scale={'start': -5, 'interval': 1, 'labelInterval': 2},
            #units="%",
            color={"gradient":True,"ranges":{"#18cc75":[-5,-1],"#39db44":[-1,0],"#aeff78":[0,2],"#ffeb78":[2,3.5],"#ff4d17":[3.5,5]}}, #
            value=df['%'][row]*100,
            label=df['Name'][row],
            labelPosition='top',    
            max=5,
            min=-5,
            size=110,
            style={"font-family":"NotoSans-CondensedLight","font-size":"0.4rem"}
        )  
    return fig

def table_driver_all(df):        
    table=dash_table.DataTable(
        data=df.to_dict('records'),
        #id=tableid,
        columns=[{"name": c, "id": c,} for c in df.columns ],  
        sort_action="native",
        sort_mode='single',
        sort_by=[{"column_id":"Impact to Overall Difference","direction":"desc"},],
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
       
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             
             'fontWeight': 'bold',
            }, 
            
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '4rem',
            'minWidth': '3rem',
            'maxWidth':'3rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#1357DD',
            'text-align':'center',
        },
    )
    return table

####################################################################################################################################################################################
######################################################################       Simulation         ####################################################################################
####################################################################################################################################################################################
   

def sim_result_box(df_sim_result):
    ### k used for pick color
    k=1 
    
    if len(df_sim_result)==10:
        df=df_sim_result.iloc[[0,3,6,9]]
        k=k-1
        bartext='Baseline:<br><br>'
        x=['Contract w/o<br>VBC Payout','Contract with VBC Payout<br>(Recommended)','Contract with VBC Payout<br>(User Defined)']
        m=0.4
    else:
        df=df_sim_result.iloc[[2,5,8]]
        bartext='Contract w/o<br>VBC Payout:<br><br>'
        x=['Contract with VBC Payout<br>(Recommended)','Contract with VBC Payout<br>(User Defined)']
        m=0.3
    n=len(df)
    
    
    #x=df['Contract Type'].to_list()[1:n]
    median=df['Best Estimate'].to_list()[1:n]
    base=df.values[0,2]
    
    #color for bar and box
    fillcolor=['rgba(226,225,253,0)','rgba(18,85,222,0)','rgba(246,177,17,0)']
    markercolor=['rgba(226,225,253,0.7)','rgba(191,191,191,0.7)','rgba(18,85,222,0.7)','rgba(246,177,17,0.7)']
        
    annotations = []
    
    if df.values[1,3]<df.values[1,4]:
        lowerfence=df['Worst'].to_list()[1:n]
        q1=df['Lower End'].to_list()[1:n]
        q3=df['Higher End'].to_list()[1:n]
        upperfence=df['Best'].to_list()[1:n]
    else:
        lowerfence=df['Best'].to_list()[1:n]
        q1=df['Higher End'].to_list()[1:n]
        q3=df['Lower End'].to_list()[1:n]
        upperfence=df['Worst'].to_list()[1:n]
        
    
    fig_sim =go.Figure()

    fig_sim.add_trace( 
            go.Bar(
            #name='Revenue before adj', 
            x=x,
            y=[base]*(n-1),
            #text=base,
            textposition='none',
            marker=dict(
                color=markercolor[0+k],
                #opacity=0.7,
                line=dict(
                    color=fillcolor[0+k],

                )
                       ), 
            ),

    )
    
    for i in range(n-1):
        fig_sim.add_trace(
            go.Box(
                x=[x[i]],       
                lowerfence=[lowerfence[i]],
                q1=[q1[i]],
                median=[median[i]],
                q3=[q3[i]],
                upperfence=[upperfence[i]],
                fillcolor=fillcolor[i],
                width=0.2,
                line_width=3,
                marker=dict(
                    color=markercolor[i+1+k],
                    #opacity=0.7,

                )

            ),  
        )
        annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
                        x=0+i, y=df['Best'].to_list()[1:n][i],ax=m+i, ay=df['Best'].to_list()[1:n][i],
                        startstandoff=10,
                        text='Best: '+str(round(df['Best'].to_list()[1:n][i],1))+'Mn',
                        font=dict(family='NotoSans-CondensedLight', size=12, color='green'),
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=2,
                        arrowside='start',
                        arrowcolor='green',
                       )
                  )
        annotations.append(dict(xref='x', yref='y',axref='x', ayref='y',
                        x=0+i, y=df['Worst'].to_list()[1:n][i],ax=m+i, ay=df['Worst'].to_list()[1:n][i],
                        startstandoff=10,
                        text='Worst: '+str(round(df['Worst'].to_list()[1:n][i],1))+'Mn',
                        font=dict(family='NotoSans-CondensedLight', size=12, color='red'),
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=2,
                        arrowside='start',
                        arrowcolor='red',
                       )
                  )
    
    
    annotations.append(dict(xref='paper', yref='y',axref='pixel', ayref='y',
                            x=1.05, y=base,ax=1.05,ay=base/3*2,
                            standoff=0,
                            showarrow=True,
                            arrowcolor=colors['grey'],
                            arrowwidth=2,
                            arrowhead=2,
                           )
                      )
    annotations.append(dict(xref='paper', yref='y',axref='pixel', ayref='y',
                            x=1.05, y=0,ax=1.05,ay=base/3,
                            standoff=0,
                            showarrow=True,
                            arrowcolor=colors['grey'],
                            arrowwidth=2,
                            arrowhead=2,
                           )
                      )
    annotations.append(dict(xref='paper', yref='y',
                            x=1.12, y=base/2,
                            text=bartext+str(round(base,1))+'Mn',
                            font=dict(family='NotoSans-CondensedLight', size=12, color='#38160f'),
                            showarrow=False,
                           )
                      )
    

    
    shapes=[]
    shapes.append( dict(type='line',
                        xref='paper',yref='y',x0=1,x1=1.1,y0=base,y1=base,
                        line=dict(color=colors['grey'],width=1),
                       )
    
    )
    
    shapes.append( dict(type='line',
                        xref='paper',yref='y',x0=1,x1=1.1,y0=0,y1=0,
                        line=dict(color=colors['grey'],width=1),
                       )
    
    )
    
    
    fig_sim.update_layout(
            plot_bgcolor=colors['transparent'],
            paper_bgcolor=colors['transparent'],
            bargap=0, 
            yaxis = dict(
                side='left',
                
                showgrid = True, 
                showline=True,
                linecolor=colors['grey'],
                gridcolor =colors['grey'],
                tickcolor =colors['grey'],
                ticks='inside',
                ticksuffix='Mn',
                nticks=5,
                showticklabels=True,
                tickfont=dict(
                    color=colors['grey']
                ),
                zeroline=True,
                zerolinecolor=colors['grey'],
                zerolinewidth=1,
            ),
            xaxis = dict(   
                showgrid = True,
                zeroline=True,
                zerolinecolor=colors['grey'],
                zerolinewidth=1,
            ),
            showlegend=False,
            modebar=dict(
                bgcolor=colors['transparent']
            ),
            margin=dict(l=10,r=100,b=10,t=40,pad=0),
            font=dict(
                family="NotoSans-Condensed",
                size=14,
                color="#38160f"
            ),
        hovermode=False,
        annotations=annotations,
        shapes=shapes,
        )
    return fig_sim

def table_sim_result(df):
    column1=[]
    n=len(df)
    style1=[0,3,6]
    style2=[1,4,7]
    style3=[2,5,8]
    
    if len(df)==10:
        column1.append('Baseline')
        style1=[0,1,4,7]
        style2=[2,5,8]
        style3=[3,6,9]
    column1=column1+['Contract','w/o','VBC Payout','Contract with','VBC Payout','(Recommended)','Contract with','VBC Payout','(User Defined)']
 
    df['scenario']=column1
    
   
    table=dash_table.DataTable(
        data=df.to_dict('records'),
        #id=tableid,
        columns=[
        {"name": ["Contract Type","Contract Type"], "id": "scenario"},
        {"name": ["Item","Item"], "id": "Item"},
        {"name": ["","Best Estimate(Mn)"], "id": "Best Estimate",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Full Range","Low(Mn)"], "id": "Worst",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Full Range","High(Mn)"], "id": "Best",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Most Likely Range","Low(Mn)"], "id": "Lower End",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        {"name": [ "Most Likely Range","High(Mn)"], "id": "Higher End",'type': 'numeric',"format":Format( precision=1, scheme=Scheme.fixed,),},
        ],  
        merge_duplicate_headers=True,
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
       
        style_cell={
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            'border':'0px',
            'height': '1.5rem',
        },
        style_data_conditional=[
            { 'if': {'row_index':c }, 
             'color': 'black', 
             'font-family': 'NotoSans-CondensedLight',
             'border-top': '1px solid grey',
             'border-left': '1px solid grey',
             'border-right': '1px solid grey',
              } if c in style1 else 
            
            { 'if': {'row_index':c }, 
             'color': 'black', 
             'font-family': 'NotoSans-CondensedBlackItalic',
             'border-left': '1px solid grey',
             'border-right': '1px solid grey',
             'text-decoration':'underline'
              } if c in style2 else 
            { "if": {"row_index":c },
             'font-family': 'NotoSans-CondensedLight',
             'backgroundColor':'rgba(191,191,191,0.7)',
             'color': '#1357DD',
             'fontWeight': 'bold',
             'border-bottom': '1px solid grey',
             'border-left': '1px solid grey',
             'border-right': '1px solid grey',
              } if c in style3  else 
            { "if": {"column_id":"scenario" }, 
             'font-family': 'NotoSans-CondensedLight',
             'backgroundColor':'white',
             'color': 'black',
             'fontWeight': 'bold', 
             'text-decoration':'none'
              } for c in range(0,n+1)
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '2.5rem',
            'minWidth': '3rem',
            'maxWidth':'3rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#1357DD',
            'text-align':'center',
            'border':'1px solid grey',
            'text-decoration':'none'
        },
        style_header_conditional=[
            { 'if': {'column_id':'scenario'},
            'backgroundColor': colors['transparent'],
            'color': colors['transparent'],
            'border':'0px'          
            },
            { 'if': {'column_id':'Item'},
            'backgroundColor': colors['transparent'],
            'color': colors['transparent'],
            'border':'0px' , 
            'border-right':'1px solid grey' ,
            },
        ],
        
        
    )
    return table

def table_factor_doc(df,tableid='factor_doc'):        
    table=dash_table.DataTable(
        data=df.to_dict('records'),
        id=tableid,
        columns=[{"name": c, "id": c} for c in df.columns  ],       
       
        style_data={
            'height':'auto',
            'width':'3rem',
            'whiteSpace':'normal',
            'textAlign': 'center',
            'font-family':'NotoSans-Regular',
            'fontSize':12,
            
        },
        style_cell_conditional=[
            {'if': {'column_id': df.columns[0]},
             
             'fontWeight': 'bold',
            }, 
            
        ],
        style_table={
            'back':  colors['blue'],
        },
        style_header={
            'height': '4rem',
            'whiteSpace': 'normal',
            'backgroundColor': '#f1f6ff',
            'fontWeight': 'bold',
            'font-family':'NotoSans-CondensedLight',
            'fontSize':14,
            'color': '#1357DD',
            'text-align':'center',
        },
    )
    return table

