import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
from dash import dash_table
from app import app

# Cargar los datos desde el archivo CSV
df = pd.read_csv('datosCompletos.csv')

def layout():
    return html.Div([
        html.H2('MEDICIONES', className="content-title"),
        html.Div([
            html.P(
        '''
        En esta sección se encuentran los datos de las mediciones realizadas en campo.\n
        Las mediciones recibieron las señales de los radioaltímetros de los aviones al momento de aterrizar
        con el objetivo de validar el rango de frecuencia en el que se encuentran dichas señales.\n
        En esta sección podrá observar los gráficos y datos de las mediciones en campo realizadas.
        '''
            )
        ], className="mediciones-parrafo"),
        html.Div([
            html.Label('Mediciones realizadas', className="mediciones-label"),
            dcc.Dropdown(
                id='mediciones-dropdown', #ID del dropdown
                options=[{'label': m, 'value': m} for m in df['N medición'].unique()],
                value=[df['N medición'].unique()[0]],
                multi=True
            ),
            dcc.Graph(id='line-plot') #ID del gráfico
        ], className="mediciones-line-plot-graph"),
        html.H3("Datos", className="mediciones-titulo-secundario"),
        html.P('''
        A continuación se enceuntran todos los datos en el formato de tabla
        '''),
        dcc.Dropdown(
            id='n-medicion-dropdown',
            options=[{'label': i, 'value': i} for i in df['N medición'].unique()],
            value=[df['N medición'].unique()[0]],
            className="n-medicion-dropdown-table",
            multi=True
        ),
        dash_table.DataTable(
            id='tabla',
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={"overflowX": "auto"}
        )
    ], className="mediciones-container container")



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


