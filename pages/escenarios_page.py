import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
import os

# Obtener la lista de archivos CSV en la carpeta "data/escenarios/escenarios"
folder_path = 'data/escenarios/escenarios'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Definir el diseño de la aplicación
def layout():
    return html.Div([
        html.H2('ESCENARIOS', className="content-title"),
        html.Div([
            html.P(
                '''
                En esta sección se encuentra la una herramienta de interacción que sirve para verificar
                y validar en qué punto específicamente comienza a haber interferencia entre las 
                frecuencias y potencias de los radioaltímetros y las estaciones base.
                '''
            )
        ], className="escenarios-parrafo"),
        
        # Dropdown para seleccionar el archivo CSV
        dcc.Dropdown(
            id='csv-dropdown',
            options=[{'label': file, 'value': file} for file in csv_files],
            value=csv_files[0]  # Establecer el primer archivo como valor predeterminado
        ),
        
        # Gráfico de líneas
        dcc.Graph(id='line-plot-escenario')
    ], className="escenarios-container container")

def register_callbacks(app):
    # print("holi")
    # Callback para actualizar el gráfico de líneas cuando se seleccione un archivo CSV
    @app.callback(
        dash.dependencies.Output('line-plot-escenario', 'figure'),
        [dash.dependencies.Input('csv-dropdown', 'value')]
    )
    def update_line_plot(selected_csv):
        # Leer los datos desde el archivo CSV seleccionado
        csv_path = os.path.join(folder_path, selected_csv)
        df = pd.read_csv(csv_path, delimiter=';')

        # Obtener el nombre del archivo sin la extensión
        filename_without_extension = os.path.splitext(selected_csv)[0]

        # Crear el gráfico de líneas
        fig = go.Figure(data=[go.Scatter(x=df['distancia'], y=df['potencia'], mode='lines')])
        fig.update_layout(title=f'{filename_without_extension}', xaxis_title='Distancia (m)', yaxis_title='Potencia (dBm)')

        return fig





