import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import time

import datetime
import json
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output, State

from utils import *


app = dash.Dash(__name__, url_base_pathname='/vbc-payer-demo/contract-generator/')

server = app.server

file = open('configure/input_ds.json', encoding = 'utf-8')
custom_input = json.load(file)
df_quality = pd.read_csv("data/quality_setup.csv")

def create_layout(app):
	return html.Div(
                [ 
                    html.Div([Header_contract(app, False, False, True, False)], style={"height":"6rem"}, className = "sticky-top navbar-expand-lg"),
                    
                    html.Div(
                        [
                        dbc.Row(contract_gen_basic(app)),
                        dbc.Row(contract_gen_parameter(app)),
                        dbc.Row(contract_gen_measure(app)),
						dbc.Row([
							dbc.Col(
								dcc.Upload(
								id = 'upload-data',
								children = html.Div([
									'Select Contract Template to Upload'
									],style={"font-family":"NotoSans-Regular","font-size":"1rem","text-decoration":"underline","color":"#1357DD"}),
								style={
									'height': '60px',
									'lineHeight': '60px',
									'borderWidth': '1px',
									'borderStyle': 'dashed',
									'borderRadius': '5px',
									'textAlign': 'center',
									'margin': '10px'
									}
								),style={"padding-top":"1rem"}, width=12),
							]),
						dbc.Row(dbc.Button('Generate Contract'))

                                
                        ],
                        className="mb-3",
                        style={"padding-left":"3rem", "padding-right":"3rem","padding-top":"1rem","padding-bottom":"0rem"},
                    ),
                ])

def contract_gen_basic(app):
	return html.Div([
		dbc.Row([
			dbc.Col('Plan Year'),
			dbc.Col([
				dbc.InputGroup([
					dbc.Input(value = '1/1/2020'),
					dbc.InputGroupAddon('-', addon_type = 'append'),
					dbc.Input(value = '12/31/2020'),
					])
				])
			]),
		dbc.Row([
			dbc.Col("ACO's name"),
			dbc.Col([
				dbc.Input(value = 'ACO1')
				]),
			]),
		])

def contract_gen_parameter(app):
	return html.Div([
		dbc.Row([
			dbc.Col('Medical Cost Target PMPM'),
			dbc.Col([
				dbc.InputGroup([
					dbc.InputGroupAddon('$', addon_type = 'prepend'),
					dbc.Input(value = custom_input['medical cost target']['user target']), 
					]),
				])
			]),
		html.Hr(),
		dbc.Row([
			dbc.Col('Shared Savings'),
			]),
		dbc.Row([
			dbc.Col('MSR (Minimum Savings Rate)'),
			dbc.Col([
				dbc.InputGroup([
					dbc.Input(value = custom_input['savings/losses sharing arrangement']['msr']),
					dbc.InputGroupAddon('%', addon_type = 'append'),
					]),
				])
			]),
		dbc.Row([
			dbc.Col('Max Sharing % (When quality targets are met)'),
			dbc.Col([
				dbc.InputGroup([
					dbc.Input(value = custom_input['savings/losses sharing arrangement']['savings sharing']),
					dbc.InputGroupAddon('%', addon_type = 'append'),
					]),
				])
			]),
		dbc.Row([
			dbc.Col('Min Sharing %'),
			dbc.Col([
				dbc.InputGroup([
					dbc.Input(value = custom_input['savings/losses sharing arrangement']['savings sharing min']),
					dbc.InputGroupAddon('%', addon_type = 'append'),
					]),
				])
			]),
		dbc.Row([
			dbc.Col('Sharing Method'),
			dbc.Col([
				dcc.Dropdown(options = [{'label':'First Dollar Sharing', 'value':'First Dollar Sharing'},
					{'label':'Second Dollar Sharing (Below MLR)', 'value':'Second Dollar Sharing (Below MLR)'}],
					value = custom_input['savings/losses sharing arrangement']['saving sharing method'],clearable = False),

				])
			]),
		dbc.Row([
			dbc.Col('Shared Savings Cap'),
			dbc.Col([
				dbc.InputGroup([
					dbc.Input(value = custom_input['savings/losses sharing arrangement']['savings share cap']),
					dbc.InputGroupAddon('%', addon_type = 'append'),
					]),
				])
			]),
		html.Div([
			html.Hr(),
			dbc.Row([
				dbc.Col('Shared Losses'),
				]),
			dbc.Row([
				dbc.Col('MLR (Minimum Losses Rate)'),
				dbc.Col([
					dbc.InputGroup([
						dbc.Input(value = custom_input['savings/losses sharing arrangement']['mlr']),
						dbc.InputGroupAddon('%', addon_type = 'append'),
						]),
					])
				]),
			dbc.Row([
				dbc.Col('Min Sharing % (When quality targets are met)'),
				dbc.Col([
					dbc.InputGroup([
						dbc.Input(value = custom_input['savings/losses sharing arrangement']['losses sharing min']),
						dbc.InputGroupAddon('%', addon_type = 'append'),
						]),
					])
				]),
			dbc.Row([
				dbc.Col('Max Sharing %'),
				dbc.Col([
					dbc.InputGroup([
						dbc.Input(value = custom_input['savings/losses sharing arrangement']['losses sharing']),
						dbc.InputGroupAddon('%', addon_type = 'append'),
						]),
					])
				]),
			dbc.Row([
				dbc.Col('Sharing Method'),
				dbc.Col([
					dcc.Dropdown(options = [{'label':'First Dollar Sharing', 'value':'First Dollar Sharing'},
					{'label':'Second Dollar Sharing (Below MLR)', 'value':'Second Dollar Sharing (Below MLR)'}],
						value = custom_input['savings/losses sharing arrangement']['loss sharing method'],clearable = False),
					])
				]),
			dbc.Row([
				dbc.Col('Shared Losses Cap'),
				dbc.Col([
					dbc.InputGroup([
						dbc.Input(value = custom_input['savings/losses sharing arrangement']['losses share cap']),
						dbc.InputGroupAddon('%', addon_type = 'append'),
						]),
					])
				]),
			], hidden = not custom_input['savings/losses sharing arrangement']['two side']),
		])

def contract_gen_measure(app):

	df = df_quality.iloc[custom_input['quality adjustment']['selected measures']]
	df=pd.DataFrame(df['measure'].tolist(),columns=['Measure'])
	df=df.reindex(columns=['Measure','Target Type','Target Value','Domain','Weight'])
	df['Target Type'] = custom_input['quality adjustment']['user_tar_type']
	df['Target Value']  = custom_input['quality adjustment']['user_tar_value']
	domain_list = []
	weight_list = []

	selected_row=custom_input['quality adjustment']['selected measures']
	domain1=list(range(0,10))
	domain2=list(range(10,14))
	domain3=list(range(14,20))
	domain4=list(range(20,23))
	pos=0
	table_len=0

	style1=[]
	style2=[]

	domain_name=['Patient/Caregiver Experience','Care Coordination/Patient Safety','Preventive Health','At-Risk Population']

	for i in range(0,4):
		exec('selected_intersect_' + str(i) + '=set(selected_row).intersection( set(eval("domain"+str(i+1)) ))')
		n = eval('len(selected_intersect_' + str(i)+')')
		if n>0:	
			style1.append(table_len)		
			pos=int(round(n/2,0))
			domain_list = domain_list + (['']*n)
			domain_list[pos+table_len-1]=domain_name[i]
			weight_list = weight_list + (['']*n)
			weight_list[pos+table_len-1]=custom_input['quality adjustment'][eval('"usr_dom_'+str(i+1)+'"')]

			table_len=table_len+n

			style2.append(table_len-1)


	df['Domain'] = domain_list
	df['Weight'] = weight_list

	return html.Div([
		dash_table.DataTable(
			data = df.to_dict('records'),
			columns = [{'name': i, 'id':i} for i in df.columns],
			style_data = {'textAlign' : 'center','font-family': 'NotoSans-CondensedLight',},
			style_header = {'backgroundColor': '#f1f6ff',
			'fontWeight': 'bold',
			'font-family':'NotoSans-CondensedLight',
			'fontSize':14,
			'color': '#1357DD',
			'text-align':'center',
			'border':'1px solid grey'},
			style_data_conditional=[
				{ 'if': {'column_id':'Measure'}, 
				 'font-weight':'bold', 
				 'textAlign': 'start',
				 'width':'14rem',
				 'height':'3rem',
				 'whiteSpace':'normal'
				 #'minWidth': '25rem',
				 #'maxWidth':'25rem',
				  },
		]+
		[
			{ 'if': {'row_index':c}, 
					'border':'1px solid grey',
					'border-bottom':'0px',
			 
					  } if c in style1 else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-top':'0px',
			 
					  } if c in style2 else
			{'if': {'row_index':c},
					'border':'1px solid grey',
					'border-bottom':'0px',
					'border-top':'0px',   
					}  for c in range(0,len(df))


		]
			)
		])

app.layout = create_layout(app)

if __name__ == "__main__":
    app.run_server(host="127.0.0.1",debug=True,port=8052)