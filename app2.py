import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from plotly import tools


app=dash.Dash()
server = app.server

#Do some additional cleaning on the data
data=pd.read_csv('https://rawgit.com/obxkid413/Dash-App-Fantasy-Football-Player-Comparison-Tool/master/fantasy_17_1_9_17_ver3.csv', encoding = 'unicode_escape')
data['player_name']=data['player'].str.split(',').str[0]
data['player_name']=data['player_name'].str.strip('*')
data['player']=data['player'].astype(str)
data.loc[data['player'].str.contains('Alex Smith, KC'), 'player_name'] = 'Alex Smith, QB'
player_selection=data['player_name'].sort_values().unique()

#Create a summary table across all weeks that contains the players mean, median, and standard deviation for the season.
#We will display these in a separate bar chart.


data_summary=pd.pivot_table(data, index='player_name', values='points', aggfunc=[np.sum, np.mean, np.median, np.std])
data_summary=data_summary.reset_index()
data_summary['player_name']=data_summary.index
data_summary=data_summary.reset_index(drop=True)


app.layout=html.Div([
    html.H1("Fantasy Football Player Scoring Trends/Comparisons for the 2017/18 season"),
    html.Div(
        [
    dcc.Dropdown(id="Player_Choice",
                 options=[{
                     'label':i,
                     'value':i
                     } for i in player_selection],
                     value="All players"
                 ),
    
    dcc.Dropdown(id="Player_Choice2",
                 options=[{
                     'label':i,
                     'value':i
                     } for i in player_selection],
                 value=" ")
    ],

    
    style={'width': '25%'}),

    
    
dcc.Graph(id='line_graph'),

    html.Div([
            dcc.Graph(id='bar_graph')
                   
            ]),
])



#Update graph objects
@app.callback(
    dash.dependencies.Output('line_graph', 'figure'),
    [dash.dependencies.Input('Player_Choice', 'value'),
     dash.dependencies.Input('Player_Choice2', 'value')])


def update_graph(Player_Choice, Player_Choice2):
    
    

    plot_data1=data.loc[(data['player_name'] == Player_Choice)]
    plot_data2=data.loc[(data['player_name'] == Player_Choice2)]
    
    
    trace1=go.Scatter(x=plot_data1.week, y=plot_data1.points,  name=Player_Choice)
    trace2=go.Scatter(x=plot_data2.week, y=plot_data2.points, name=Player_Choice2)
    
    
    
    return {
        'data': [trace1, trace2],
        'layout':
        go.Layout(
            title='Points by week for {} and {}'.format(Player_Choice, Player_Choice2),
            yaxis=dict(range=[0, 60])
            )
        }


@app.callback(dash.dependencies.Output('bar_graph', 'figure'),
[dash.dependencies.Input('Player_Choice', 'value'),
 dash.dependencies.Input('Player_Choice2', 'value')])

def update_chart2(Player_Choice,Player_Choice2):
    
    plot_data1=data.loc[(data['player_name'] == Player_Choice)]
    plot_data2=data.loc[(data['player_name'] == Player_Choice2)]

    mean_p1=plot_data1['points'].mean()
    mean_p2=plot_data2['points'].mean()
    median_p1=plot_data1['points'].median()
    median_p2=plot_data2['points'].median()
    std_p1=plot_data1['points'].std()
    std_p2=plot_data2['points'].std()
    CR_1=std_p1/mean_p1
    CR_2=std_p2/mean_p2
    
    trace3 = go.Bar(
        x=['Mean', 'Median', 'Std.Dev', 'ConsistencyIndex'],
        y=[mean_p1, median_p1, std_p1, CR_1],
        name=Player_Choice
        )

    trace4=go.Bar(
        x=['Mean', 'Median', 'Std.Dev', 'ConsistencyIndex'],
        y=[mean_p2, median_p2, std_p2, CR_2],
        name=Player_Choice2
        )

    return {
        'data': [trace3, trace4],
        'layout':
        go.Layout(
             annotations=[
        dict(
            text='Note: A lower Consistency Index is better.',
            x='ConsistencyIndex',
            y=2,
            )
        ],
            title='Summary Statistics for {} and {}.'.format(Player_Choice, Player_Choice2),
            width=1000,
            barmode='group')
        
        }
    
    

if __name__=='__main__':
    app.run_server()

    
        
            

                
