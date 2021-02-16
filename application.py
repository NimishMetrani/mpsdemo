import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input,Output
import pandas as pd
from numpy import random

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha512-8bHTC73gkZ7rZ7vpqUQThUDhqcNFyYi2xgDgPDHc+GXVGHXq+xPjynxIopALmOPqzo9JZj0k6OqqewdGO3EsrQ==',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash()
df = pd.read_excel('samplecrime.xls')
df2 = df.loc[df['Lad11nm'] == 'Westminster']
df3 = df2.sort_values(by=['Crime Month','totalOffence'])
df4 = df2.loc[df2['monthYear'] == 'Jan-19']
bcu_name = df['BCU_Name'].unique()
monthYear = df['monthYear'].unique()

app.layout = html.Div([
            html.Div([
                html.H1([
                            'UK Police Service'
                        ], style={'text-align':'center', 'color':'#401d06'}),
                       html.Div([
            dcc.Graph(id='London_pd',
                                figure={
                                    'data':[go.Bar(
                                        x=df['Lad11nm'],
                                        y=df['totalOffence'],
                                        text = df['BCU_Name'],
                                        
                                    )],
                                    'layout': go.Layout(title='Crimes of London Borough',
                                    xaxis={'title':'Names'},
                                    yaxis={'title': 'Total offences in last 24 months'},
                                    plot_bgcolor='rgb(250, 230, 217)',
                                    paper_bgcolor='rgb(250, 230, 217)'
                                    ),
                                    

            }),
            ], style={'width':'70%','padding-left':'200px', 'padding-bottom':'100px'}),
            html.Div([
        
            dcc.Dropdown(
                id='unit_name',
                options=[{'label': i, 'value': i} for i in bcu_name],
                value='BCU_Name'
            ),
            html.H2([
                'Select the Crime Unit'
            ])],
        style={'width': '30%', 'display': 'inline-block', 'padding-bottom':'50px'}),
        html.Div([
            dcc.Dropdown(
                id='borough_name',
                options=[{'label': i, 'value': i} for i in df['Lad11nm'].unique()],
                value='name'
            ),
            html.H2([
                'Select the borough'
            ])],
        style={'width': '30%', 'display': 'inline-block', 'padding-bottom':'50px', 'float':'right'}),
            html.Div([ 
                html.Div([
            dcc.Graph(id='London_Boroughs',
                                figure={
                                    'data':[go.Bar(
                                        x=df['Lad11nm'],
                                        y=df['totalOffence'],
                                        text = df['BCU_Name'],
                                        
                                    )],
                                    'layout': go.Layout(title='Crimes of London Borough',
                                    xaxis={'title':'Names'},
                                    yaxis={'title': 'Total offences in last 24 months'},
                                    plot_bgcolor='rgb(250, 230, 217)',
                                    paper_bgcolor='rgb(250, 230, 217)'
                                    ),
                                    

            }),
            ], style={'width':'50%','display':'inline-block'}),
            html.Div([
                dcc.Graph(id='major_crime',
                        figure={})
                        ],style={'width':'40%','height':'50%','display':'inline-block','float':'right', 'margin-bottom':'500px'}),]),
            html.Div([
                html.Div([
            
    ])])]),

            html.Div([ dcc.Graph(id='Crime in Scatter',
                                figure={
                                    'data':[go.Scatter(
                                        x=df2['monthYear'],
                                        y=df2['totalOffence'],
                                        mode='markers',
                                    )],
                                    'layout': go.Layout(title='Total Offence in Westminster',
                                                        xaxis={'title':'crime'},
                                                        yaxis={'title': 'Months'},
                                                        plot_bgcolor='rgb(250, 230, 217)',
                                                        paper_bgcolor='rgb(250, 230, 217)')
                                })
            ], style={'width':'70%','padding-left':'200px', 'padding-bottom':'100px', 'padding-top':'100px'}),

            html.Div([
                dcc.Graph(id='pie_chart',
                hoverData={'points': [{'customdata': 'Japan'}]},
                        figure={
                            'data':[go.Pie(
                                labels=df2['Major Class Description'],
                                values=df2['totalOffence']
                            )],
                            'layout': go.Layout(title='Crime Pie',
                                                plot_bgcolor='rgb(250, 230, 217)',
                                                paper_bgcolor='rgb(250, 230, 217)')
                        })
            ],style={'width':'70%', 'padding-left':'200px'}),
            html.Div([dcc.Slider(
                                id='year--slider',
                                min=df['monthYear'].min(),
                                max=monthYear.max(),
                                value=monthYear.max(),
                                step=1
    )])

],style={'padding':'5%', 'background-color':'#faeee6'})

@app.callback(Output('pie_chart','figure'),
                [Input('London_Boroughs','hoverData')])
def hover_graph(hoverData):
    v_index = hoverData['points'][0]['customdata']
    v_index2 = hoverData['points'][0]['y']
    #####
    filtered_df = df[df['BCU_Name'] == hoverData]
    traces = []
    for borough_name in filtered_df['Lad11nm'].unique():
        df_by_borough = filtered_df[filtered_df['Lad11nm'] == borough_name]
        df_sorted = df_by_borough.sort_values(by=['Crime Month','totalOffence'])
        traces.append(go.Pie(
                                labels=df_sorted[v_index]['Major Class Description'],
                                values=df_sorted[v_index2]['totalOffence']
                            )),
                            
    
    return {
        'data': traces,
        'layout': go.Layout(
            title='Crime Pie',
            plot_bgcolor='rgb(250, 230, 217)',
            paper_bgcolor='rgb(250, 230, 217)'
            
        )
    }
##################

@app.callback(Output('major_crime','figure'),
                [Input('borough_name','value')])
def callback_graph(selected_borough):
    filtered_df2 = df[df['Lad11nm'] == selected_borough]
    traces = []
    for borough_crime in filtered_df2['Major Class Description'].unique():
        df_by_borough2 = filtered_df2[filtered_df2['Major Class Description'] == borough_crime]
        df_sorted = df_by_borough2.sort_values(by=['Crime Month','totalOffence'])
        traces.append(go.Bar(
            x=df_sorted['Major Class Description'],
            y=df_sorted['totalOffence'],
            text=df_sorted['Borough/Business Unit / BCU Code'],
            name=borough_crime
        ))
 
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Major Crime'},
            yaxis={'title': 'Total offence'},
            plot_bgcolor='rgb(250, 230, 217)',
            paper_bgcolor='rgb(250, 230, 217)'
            
        )
    }

################
## this is just a test

@app.callback(Output('London_Boroughs', 'figure'),
              [Input('unit_name', 'value')])
def update_figure(selected_unit):
    filtered_df = df[df['BCU_Name'] == selected_unit]
    traces = []
    for borough_name in filtered_df['Lad11nm'].unique():
        df_by_borough = filtered_df[filtered_df['Lad11nm'] == borough_name]
        traces.append(go.Bar(
            x=df_by_borough['Lad11nm'],
            y=df_by_borough['totalOffence'],
            text=df_by_borough['BCU_Name'],
            name=borough_name
        ))
 
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Borough'},
            yaxis={'title': 'Total offence'},
            plot_bgcolor='rgb(250, 230, 217)',
            paper_bgcolor='rgb(250, 230, 217)'
            
        )
    }
    
 


if __name__ =='__main__' :
    app.run_server(debug=True,dev_tools_ui=False,dev_tools_props_check=False)
