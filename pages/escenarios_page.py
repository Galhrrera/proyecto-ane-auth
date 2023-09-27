import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go
import os

# Obtener la lista de archivos CSV en la carpeta "data/escenarios/escenarios"
folder_path = 'data/escenarios/escenarios'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Obtener la lista de archivos CSV en la carpeta "data/escenarios/radioaltímetros"
folder_path_radioaltimetros = 'data/escenarios/radioaltímetros'
csv_files_radioaltimetros = [f for f in os.listdir(
    folder_path_radioaltimetros) if f.startswith('radioaltimetro_') and f.endswith('.csv')]


def layout():
    # Obtener los valores predeterminados para los dropdowns y sliders
    default_csv_scenario = csv_files[0]
    default_csv_radioaltimetros = csv_files_radioaltimetros[0]
    default_distancia_value = 100
    default_frecuencia_value = 3000

    # Generar los gráficos iniciales
    initial_line_plot_scenario = update_line_plot(default_csv_scenario)
    initial_line_plot_radioaltimetros = update_radioaltimetros_with_slider_values(
        default_distancia_value, default_frecuencia_value, default_csv_radioaltimetros, default_csv_scenario)

    return html.Div([
        html.H2('ESCENARIOS', className="content-title"),
        html.Div([
            html.P(
                '''
                En esta sección se encuentra una herramienta de interacción que sirve para verificar
                y validar en qué punto específicamente comienza a haber interferencia entre las 
                frecuencias y potencias de los radioaltímetros y las estaciones base.
                '''
            )
        ], className="escenarios-parrafo"),

        # Dropdown para seleccionar el archivo CSV de escenarios
        dcc.Dropdown(
            id='csv-dropdown',
            options=[{'label': file, 'value': file} for file in csv_files],
            value=default_csv_scenario  # Establecer el primer archivo como valor predeterminado
        ),

        # Gráfico de líneas para escenarios
        dcc.Graph(id='line-plot-escenario', figure=initial_line_plot_scenario),

        # Elemento para mostrar el valor de distancia seleccionada
        html.Div(id='slider_distancia_value', className='slider-value'),

        # Slider para la distancia
        dcc.Slider(
            id='slide_distancia',
            min=100,
            max=1500,
            step=100,
            value=default_distancia_value
        ),

        # Elemento para mostrar el valor de frecuencia seleccionada
        html.Div(id='slider_frecuencia_value', className='slider-value'),

        # Slider para la frecuencia
        dcc.Slider(
            id='slide_frecuencia',
            min=3000,
            max=4500,
            step=100,
            value=default_frecuencia_value,
            # Mostrar etiquetas completas en el slider de frecuencia
            marks={i: str(i) for i in range(3000, 4600, 100)}
        ),

        # Dropdown para seleccionar el archivo CSV de radioaltímetros
        dcc.Dropdown(
            id='csv-dropdown-radioaltimetros',
            options=[{'label': file, 'value': file}
                     for file in csv_files_radioaltimetros],
            # Establecer el primer archivo como valor predeterminado
            value=default_csv_radioaltimetros
        ),

        # Gráfico de líneas para radioaltímetros
        dcc.Graph(id='line-plot-radioaltimetros',
                  figure=initial_line_plot_radioaltimetros)
    ], className="escenarios-container container")


def register_callbacks(app):
    # Método para actualizar el gráfico de radioaltímetros y obtener la potencia
    def update_radioaltimetros_with_slider_values(slider_distancia_value, slider_frecuencia_value, selected_csv_radioaltimetros, selected_csv_scenario):
        # Leer los datos desde el archivo CSV de radioaltímetros seleccionado
        csv_path_radioaltimetros = os.path.join(
            folder_path_radioaltimetros, selected_csv_radioaltimetros)
        df_radioaltimetros = pd.read_csv(
            csv_path_radioaltimetros, delimiter=';')
        # print("Radialtímetros:")
        # print(df_radioaltimetros.head())

        csv_path_scenarios = os.path.join(folder_path, selected_csv_scenario)
        df_scenario = pd.read_csv(csv_path_scenarios, delimiter=';')
        # print("Escenario:")
        # print(df_scenario.head())

        # Obtener el valor de potencia correspondiente a la distancia seleccionada
        filtered_df = df_scenario[df_scenario['distancia']
                                  == slider_distancia_value]
        # print("filtered")
        # print(filtered_df.head())

        filtered_radioaltimetro_df = df_radioaltimetros[df_radioaltimetros['frecuencia']
                                                        == slider_frecuencia_value]
        # print("filtered frecuencia")
        # print(filtered_radioaltimetro_df)

        if not filtered_df.empty and not filtered_radioaltimetro_df.empty:
            potencia = filtered_df.iloc[0]['potencia']
            poencia_radioaltimetro = filtered_radioaltimetro_df.iloc[0]['potencia']

            # Obtener el nombre del archivo sin la extensión
            filename_without_extension_radioaltimetros = os.path.splitext(
                selected_csv_radioaltimetros)[0]

            # Crear el gráfico de líneas para radioaltímetros
            fig_radioaltimetros = go.Figure(data=[go.Scatter(
                x=df_radioaltimetros['frecuencia'], y=df_radioaltimetros['potencia'], mode='lines', name=f'{filename_without_extension_radioaltimetros}')])

            if poencia_radioaltimetro < potencia:
                fig_radioaltimetros.add_trace(go.Scatter(x=[slider_frecuencia_value], y=[
                                              potencia], mode='markers', marker=dict(size=15, color='red')))
            else:
                fig_radioaltimetros.add_trace(go.Scatter(x=[slider_frecuencia_value], name='Potencia estación', y=[
                                              potencia], mode='markers', marker=dict(size=15, color='green')))

            fig_radioaltimetros.update_layout(
                title=f'{filename_without_extension_radioaltimetros}', xaxis_title='Frecuencia (MHz)', yaxis_title='Potencia (dBm)')

            return fig_radioaltimetros

        else:
            return go.Figure()

    # Callback para actualizar el gráfico de radioaltímetros y obtener la potencia
    @app.callback(
        dash.dependencies.Output('line-plot-radioaltimetros', 'figure'),
        [dash.dependencies.Input('slide_distancia', 'value'),
         dash.dependencies.Input('slide_frecuencia', 'value'),
         dash.dependencies.Input('csv-dropdown-radioaltimetros', 'value'),
         dash.dependencies.Input('csv-dropdown', 'value')
         ]
    )
    def update_radioaltimetros(slider_distancia_value, slider_frecuencia_value, selected_csv_radioaltimetros, selected_csv_scenario):
        return update_radioaltimetros_with_slider_values(slider_distancia_value, slider_frecuencia_value, selected_csv_radioaltimetros, selected_csv_scenario)

    # Callback para almacenar valores de los sliders en variables
    @app.callback(
        [dash.dependencies.Output('slider_distancia_value', 'children'),
         dash.dependencies.Output('slider_frecuencia_value', 'children')],
        [dash.dependencies.Input('slide_distancia', 'value'),
         dash.dependencies.Input('slide_frecuencia', 'value')]
    )
    def update_slider_values(slider_distancia_value, slider_frecuencia_value):
        return f'Distancia seleccionada: {slider_distancia_value}', f'Frecuencia seleccionada: {slider_frecuencia_value}'

    # Callback para cargar el gráfico de líneas inicial
    @app.callback(
        dash.dependencies.Output('line-plot-escenario', 'figure'),
        [dash.dependencies.Input('csv-dropdown', 'value')]
    )
    def update_line_plot(selected_csv):
        if selected_csv:
            # Leer los datos desde el archivo CSV seleccionado
            csv_path = os.path.join(folder_path, selected_csv)
            df = pd.read_csv(csv_path, delimiter=';')

            # Obtener el nombre del archivo sin la extensión
            filename_without_extension = os.path.splitext(selected_csv)[0]

            # Crear el gráfico de líneas
            fig = go.Figure(
                data=[go.Scatter(x=df['distancia'], y=df['potencia'], mode='lines')])
            fig.update_layout(title=f'{filename_without_extension}',
                              xaxis_title='Distancia (m)', yaxis_title='Potencia (dBm)')

            return fig
        else:
            return go.Figure()


def update_line_plot(selected_csv):
    if selected_csv:
        # Leer los datos desde el archivo CSV seleccionado
        csv_path = os.path.join(folder_path, selected_csv)
        df = pd.read_csv(csv_path, delimiter=';')

        # Obtener el nombre del archivo sin la extensión
        filename_without_extension = os.path.splitext(selected_csv)[0]

        # Crear el gráfico de líneas
        fig = go.Figure(
            data=[go.Scatter(x=df['distancia'], y=df['potencia'], mode='lines')])
        fig.update_layout(title=f'{filename_without_extension}',
                          xaxis_title='Distancia (m)', yaxis_title='Potencia (dBm)')

        return fig
    else:
        return go.Figure()

    # Método para actualizar el gráfico de radioaltímetros y obtener la potencia


def update_radioaltimetros_with_slider_values(slider_distancia_value, slider_frecuencia_value, selected_csv_radioaltimetros, selected_csv_scenario):
    # Leer los datos desde el archivo CSV de radioaltímetros seleccionado
    csv_path_radioaltimetros = os.path.join(
        folder_path_radioaltimetros, selected_csv_radioaltimetros)
    df_radioaltimetros = pd.read_csv(csv_path_radioaltimetros, delimiter=';')
    # print("Radialtímetros:")
    # print(df_radioaltimetros.head())

    csv_path_scenarios = os.path.join(folder_path, selected_csv_scenario)
    df_scenario = pd.read_csv(csv_path_scenarios, delimiter=';')
    # print("Escenario:")
    # print(df_scenario.head())

    # Obtener el valor de potencia correspondiente a la distancia seleccionada
    filtered_df = df_scenario[df_scenario['distancia']
                              == slider_distancia_value]
    # print("filtered")
    # print(filtered_df.head())

    filtered_radioaltimetro_df = df_radioaltimetros[df_radioaltimetros['frecuencia']
                                                    == slider_frecuencia_value]
    # print("filtered frecuencia")
    # print(filtered_radioaltimetro_df)

    if not filtered_df.empty and not filtered_radioaltimetro_df.empty:
        potencia = filtered_df.iloc[0]['potencia']
        poencia_radioaltimetro = filtered_radioaltimetro_df.iloc[0]['potencia']

        # Obtener el nombre del archivo sin la extensión
        filename_without_extension_radioaltimetros = os.path.splitext(
            selected_csv_radioaltimetros)[0]

        # Crear el gráfico de líneas para radioaltímetros
        fig_radioaltimetros = go.Figure(data=[go.Scatter(
            x=df_radioaltimetros['frecuencia'], y=df_radioaltimetros['potencia'], mode='lines')])

        if poencia_radioaltimetro < potencia:
            fig_radioaltimetros.add_trace(go.Scatter(x=[slider_frecuencia_value], y=[
                                          potencia], mode='markers', marker=dict(size=15, color='red')))
        else:
            fig_radioaltimetros.add_trace(go.Scatter(x=[slider_frecuencia_value], y=[
                                          potencia], mode='markers', marker=dict(size=15, color='green')))

        fig_radioaltimetros.update_layout(
            title=f'{filename_without_extension_radioaltimetros}', xaxis_title='Frecuencia (MHz)', yaxis_title='Potencia (dBm)')

        return fig_radioaltimetros

    else:
        return go.Figure()
