from dash import dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import pandas as pd
import numpy as np

import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# Servidor
load_figure_template("minty")

app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
server = app.server



# DataFrame =================
df = pd.read_csv('data/supermarket_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Time'] = pd.to_datetime(df['Time'])

lista_cidades = df['City'].value_counts().index



# Pré-layout ================

card = dbc.Card(
    [
        html.Img(id="logo_b", src=app.get_asset_url("supermarketlogo.png")),
        dbc.CardBody(
            [
                html.H6("| Dashboard |", className="card-text", style={'text-align':'center', 'margin-top':'30px'}),
                html.H6("| Análise de vendas: Trimestral |", className="card-text", style={'text-align':'center'}),
                html.H4('Cidades:', id='html-1', style={'margin-top':'30px', 'font-size':'20px'}),
                dcc.Checklist(options=lista_cidades, value=lista_cidades, id='checklist-1-cidades', inputStyle={'margin-right':'5px', 'margin-left':'20px'}),
                html.H4('Variável de análise:', style={'font-size':'20px', 'margin-top':'35px'}),
                dcc.RadioItems(options=['gross income','Rating'], value='Rating', id='rdi-1-categoria',inputStyle={'margin-right':'5px', 'margin-left':'20px'} ,inline=True),
            ]
        ),
    ],
    style={'margin':'10px', 'height':'90vh'}, 
    id='card_01-rg/c1'
)


# Layout    =================
app.layout = html.Div([
    dbc.Row(
        [
        dbc.Col([html.Div([
            card
            ])], sm=2, id='rg/c1'),
        
        dbc.Col(
            [
            dbc.Row(
                    [dbc.Col(dcc.Graph(id='grafico-1'),sm=4, id='rg/c2/r1/c1'), 
                     dbc.Col(dcc.Graph(id='grafico-1/2'), sm=4, id='rg/c2/r1/c2'), 
                     dbc.Col(dcc.Graph(id='grafico-1/3') ,sm=4, id='rg/c2/r1/c3')
                     ], 
                    ),
            dbc.Row(dcc.Graph(id='grafico_2-c1')),
            dbc.Row(dcc.Graph(id='grafico_last'))
            ], sm=10, id='rg/c2'),
        ])
], style={'margin-top':'20px'})


# Callbacks =================
@app.callback(
    Output('grafico-1', 'figure'),
    Input('checklist-1-cidades', 'value'),
    Input('rdi-1-categoria', 'value')
)
def update_layout(cidades, categoria):
    df_selected = df[df['City'].isin(cidades)]
    
    if categoria == 'gross income':
        df_selected = df_selected.groupby('City').agg({categoria:'sum'})
        
    elif categoria == 'Rating':
        df_selected = df_selected.groupby('City').agg({categoria:'mean'})
    
    fig = go.Figure(data=go.Bar(x=df_selected.index, y=df_selected[categoria]))
    
    fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    fig.update_yaxes(title_text=f"{categoria}")
    
    return fig

@app.callback(
    Output('grafico-1/2', 'figure'),
    Input('checklist-1-cidades', 'value'),
    Input('rdi-1-categoria', 'value')
)
def update_layout(cidades, categoria):
    df_selected = df[df['City'].isin(cidades)]
    
    if categoria == 'gross income':
        df_selected = df_selected.groupby(['City','Gender']).agg({categoria:'sum'})
        df_selected = df_selected.reset_index()
        
    elif categoria == 'Rating':
        df_selected = df_selected.groupby(['City','Gender']).agg({categoria:'mean'})
        df_selected = df_selected.reset_index()
    
    fig = px.bar(df_selected, x='Gender', y=categoria, color='City', barmode='group')
    
    fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    
    return fig

@app.callback(
    Output('grafico-1/3', 'figure'),
    Input('checklist-1-cidades', 'value'),
    Input('rdi-1-categoria', 'value')
)
def update_layout(cidades, categoria):
    df_selected_p = df[df['City'].isin(cidades)]
    
    if categoria == 'gross income':
        df_selected_p = df_selected_p.groupby('Payment').agg({categoria:'sum'})
        
    elif categoria == 'Rating':
        df_selected_p = df_selected_p.groupby('Payment').agg({categoria:'mean'})
    
    fig = go.Figure(data=go.Bar(y=df_selected_p.index, x=df_selected_p[categoria], orientation="h"))
    
    fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200)
    fig.update_xaxes(title_text=f"{categoria}")
    
    return fig

@app.callback(
    Output('grafico_2-c1', 'figure'),
    Input('checklist-1-cidades', 'value'),
    Input('rdi-1-categoria', 'value')
)
def update_layout(cidades, categoria):
    df_selected_p = df[df['City'].isin(cidades)]

    if categoria == 'gross income':
        df_selected_p = df_selected_p.groupby('Date').agg({categoria:'sum'})
        df_selected_p = df_selected_p.reset_index()
        
    elif categoria == 'Rating':
        df_selected_p = df_selected_p.groupby('Date').agg({categoria:'mean'})
        df_selected_p = df_selected_p.reset_index()
        
    fig = px.bar(df_selected_p, x=df_selected_p['Date'], y=df_selected_p[categoria])
    
    fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=300)
    
    return fig

    

@app.callback(
    Output('grafico_last', 'figure'),
    Input('checklist-1-cidades', 'value'),
    Input('rdi-1-categoria', 'value')
)
def update_layout(cidades, categoria):
    df_selected_p_l = df[df['City'].isin(cidades)]
    
    if categoria == 'gross income':
        df_selected_p_l = df_selected_p_l.groupby(['Product line','City']).agg({categoria:'sum'})
        df_selected_p_l = df_selected_p_l.reset_index()
        
    elif categoria == 'Rating':
        df_selected_p_l = df_selected_p_l.groupby(['Product line','City']).agg({categoria:'mean'})
        df_selected_p_l = df_selected_p_l.reset_index()
        
    fig = px.bar(df_selected_p_l, x=df_selected_p_l['Product line'], y=df_selected_p_l[categoria], color='City', barmode="group")
    
    fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500)
    
    return fig



# Servidor  =================
if __name__=='__main__':
    app.run_server(debug=True)