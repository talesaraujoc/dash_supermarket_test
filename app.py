import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ============ Config Inicial ==============

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ============ DataFrame ===================
df = pd.read_excel('data/testedatasetv2b.xlsx')

lista_rodadas = df['RODADA'].unique()


# ============ Layout ===================
app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div([
            dbc.Row(html.Div([
                html.H4('MR League - Rumo ao Estrelato', style={'text-align':'center'}),
                html.Hr(),
                html.Label('Rodada:'),
                dcc.Dropdown(options=lista_rodadas, value=lista_rodadas[0], id='dpd_01-rg/c1/r1')
                ]), id='rg/c1/r1'),
            
            dbc.Row(html.Div([
                html.Hr(style={'margin-top':'150px','margin-bottom':'0px'}),
                html.H5('Desempenho individual', style={'text-align':'center', 'margin-top':'0px'}),
                html.H6('Player'),
                dcc.Dropdown(options=['Lotta', 'Feitosa'], value='Lotta', id='dpd_02-rg/c1/r2')
                ]),id='rg/c1/r2')
            ]),
        style={'background-color':'yellow'}, md=2, id='rg/c1'),
        
        dbc.Col(html.Div([
            dbc.Row(html.Div([
                dcc.Graph(id='grafico_01_rg/c2/r1')
                ]), 
            id='rg/c2/r1'),
            
            dbc.Row([dbc.Col(html.Div([]),md=4, id='rg/c2/r2/c1'), dbc.Col(html.Div([dcc.Graph(id='grafico_individual')]),md=8, id='rg/c2/r2/c2')],
                    
            id='rg/c2/r2')
            ]),
        style={'background-color':'green'}, md=10, id='rg/c2')
    ], id='rg')
    
])

# ============ Callbacks ===================
@app.callback(
    Output('grafico_01_rg/c2/r1', 'figure'),
    Input('dpd_01-rg/c1/r1', 'value'))
def update_grafico_um(value):
    df_rodada_x = df.loc[df['RODADA']==value]
    
    df_desempenho_times = df_rodada_x.groupby('TIME').agg({'V':'sum', 'E':'sum', 'D':'sum'})/6
    df_desempenho_times = df_desempenho_times.reset_index()
    
    df_pontuacao_player_rodada = df_rodada_x.groupby('PLAYER').agg({'PTS':'sum'}).reset_index()
    df_pontuacao_player_rodada.sort_values(by='PTS', ascending=False, inplace=True)
    
    df_gols_rodada = df_rodada_x.groupby('PLAYER').agg({'GOL':'sum'}).reset_index()
    df_gols_rodada = df_gols_rodada.sort_values(by='GOL', ascending=False)
    
    df_assists_rodada = df_rodada_x.groupby('PLAYER').agg({'ASS':'sum'}).reset_index()
    df_assists_rodada = df_assists_rodada.sort_values(by='ASS', ascending=False)
    
    fig = make_subplots(rows=1, cols=5, subplot_titles=('TIMES: V/E/D', 'Pontuação Individual', 'GOLS', 'ASSISTS'))
    fig.add_trace(go.Bar(x=df_desempenho_times['TIME'], y=df_desempenho_times['V'], marker=dict(color='#3ADE3E'), showlegend=False, name='V'), row=1, col=1)
    fig.add_trace(go.Bar(x=df_desempenho_times['TIME'], y=df_desempenho_times['E'], marker=dict(color='#FAE258'), showlegend=False, name='E'), row=1, col=1)
    fig.add_trace(go.Bar(x=df_desempenho_times['TIME'], y=df_desempenho_times['D'], marker=dict(color='#F52D2A'), showlegend=False, name='D'), row=1, col=1)

    fig.add_trace(go.Bar(x=df_pontuacao_player_rodada['PLAYER'], y=df_pontuacao_player_rodada['PTS'],marker=dict(color='#000000'), showlegend=False, name='PTS'), row=1, col=2)

    fig.add_trace(go.Bar(x=df_gols_rodada['PLAYER'], y=df_gols_rodada['GOL'], showlegend=False, name='GOL', marker=dict(color='#F53189')), row=1, col=3)

    fig.add_trace(go.Bar(x=df_assists_rodada['PLAYER'], y=df_assists_rodada['ASS'], showlegend=False,marker=dict(color='#19D3F5'), name='ASS'), row=1, col=4)


    fig.update_layout(title_text=f"Rodada {value}")
    
    return fig

# ============ Servidor ===================
if __name__=='__main__':
    app.run_server(debug=True)
