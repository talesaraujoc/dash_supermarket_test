import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc

import pandas as pd
import numpy as np

import plotly
import plotly.graph_objects as go
import plotly.express as px


# ============ Config Inicial ==============

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# ============ DataFrame ===================



# ============ Layout ===================



# ============ Callbacks ===================



# ============ Servidor ===================
if __name__=='__main__':
    app.run_server(debug=True)
