import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
# from app import app

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



# Definir la función de actualización del gráfico
def register_callbacks(app):
    @app.callback(
        dash.dependencies.Output('line-plot', 'figure'),
        [dash.dependencies.Input('mediciones-dropdown', 'value')]
    )
    def update_graph(selected_mediciones):
        filtered_df = df[df['N medición'].isin(selected_mediciones)]
        traces = []
        for medicion in filtered_df['N medición'].unique():
            data = filtered_df[filtered_df['N medición'] == medicion]
            trace = go.Scatter(
                x=data['Freq'],
                y=data['SA Max Hold'],
                mode='lines',
                name=medicion
            )
            traces.append(trace)
        layout = go.Layout(
            title='Potencia de la señal',
            xaxis={'title': 'Frequencia'},
            yaxis={'title': 'Potencia'},
            hovermode='closest',
            shapes=[
                # Línea vertical en x=4200
                {
                    'type': 'line',
                    'x0': 4200000000,
                    'y0': filtered_df['SA Max Hold'].min(),
                    'x1': 4200000000,
                    'y1': filtered_df['SA Max Hold'].max(),
                    'line': {
                        'color': 'red',
                        'width': 1,
                        'dash': 'solid'
                    }
                },
                # Línea vertical en x=4400
                {
                    'type': 'line',
                    'x0': 4400000000,
                    'y0': filtered_df['SA Max Hold'].min(),
                    'x1': 4400000000,
                    'y1': filtered_df['SA Max Hold'].max(),
                    'line': {
                        'color': 'red',
                        'width': 1,
                        'dash': 'solid'
                    }
                }
            ]
        )
        return {'data': traces, 'layout': layout}

    @app.callback(
        dash.dependencies.Output('tabla', 'data'),
        [dash.dependencies.Input('n-medicion-dropdown', 'value')]
    )
    def update_table(selected_options):
        if selected_options is None or len(selected_options) == 0:
            # Si no se selecciona ninguna opción, mostrar todos los datos del dataframe
            return df.to_dict("records")
        else:
            # Filtrar el dataframe según las opciones seleccionadas en el dropdown
            filtered_df = df[df['N medición'].isin(selected_options)]
            return filtered_df.to_dict("records")
    
    pass


