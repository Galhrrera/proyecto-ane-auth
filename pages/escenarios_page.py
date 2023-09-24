import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table

# Cargar los datos desde el archivo CSV
df = pd.read_csv('datosCompletos.csv')

def layout():
    return html.Div([
        html.H2('ESCENARIOS', className="content-title"),
        html.Div([
            html.P(
        '''
        En esta sección se encuentra la una herramienta de interacción que sirve para verificar
        y válidad en qué punto específicamente comienza a haber interferencia entre las 
        frecuencias y potencias de los radioaltímetros y las estaciones base.
        '''
            )
        ], className="escenarios-parrafo")

    ], className="escenarios-container container")





