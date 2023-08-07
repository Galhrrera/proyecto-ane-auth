import zipfile
from dash.dependencies import Output, Input
import dash
import os
import base64
from dash import dcc
from dash import html

data_folder = "data"

mediciones_folder = os.path.join(data_folder, "mediciones")
mediciones_files = os.listdir(mediciones_folder)

simulaciones_folder = os.path.join(data_folder, "simulaciones")
simulaciones_files = os.listdir(simulaciones_folder)

def layout():
    return html.Div(
        [
            html.H2('ARCHIVOS', className="content-title"),
            dcc.Tabs(id="tabs", value="mediciones", children=[
                dcc.Tab(label="Mediciones", value="mediciones"),
                dcc.Tab(label="Simulaciones", value="simulaciones")
            ], className="archivos-tabs"),
            html.Div(id="tab-content")
        ],
        className="archivos-container container"
    )


def register_callbacks(app):
    @app.callback(
        Output("tab-content", "children"),
        Input("tabs", "value")
    )
    def update_tab_content(tab):
        if tab == "mediciones":
            dropdown_options = [{'label': 'Todos los archivos', 'value': 'todos'}] + [{'label': f, 'value': f} for f in mediciones_files]
            return html.Div(
                [
                    html.P(children=
                           '''
                           Aquí podrá descargar todos los archivos con los datos obtenidos durante las
                           mediciones realizadas en campo
                           ''', className="archivos_parrafo"),
                    dcc.Dropdown(
                        id="mediciones-dropdown",
                        options=dropdown_options,
                        value='todos'  # Opción por defecto: "Todos los archivos"
                    ),
                    html.A(html.Button("Descargar", id="mediciones-button", className="archivos-descargas-btn"), id="mediciones-link", className="archivo-link")
                ]
            )
        elif tab == "simulaciones":
            dropdown_options = [{'label': 'Todos los archivos', 'value': 'todos'}] + [{'label': f, 'value': f} for f in simulaciones_files]
            return html.Div(
                [
                    html.P(children=
                           '''
                           Aquí podrá descargar todos los archivos con los datos obtenidos durante las
                           simulaciones realizadas en laboratorio
                           ''', className="archivos_parrafo"),
                    dcc.Dropdown(
                        id="simulaciones-dropdown",
                        options=dropdown_options,
                        value='todos'  # Opción por defecto: "Todos los archivos"
                    ),
                    html.A(html.Button("Descargar", id="simulaciones-button", className="archivos-descargas-btn"), id="simulaciones-link", className="archivo-link")
                ]
            )

    # Descargar archivo(s) de mediciones
    @app.callback(
        Output("mediciones-link", "href"),
        Input("mediciones-dropdown", "value")
    )
    def download_mediciones_file(selected_file):
        if selected_file == "todos":
            selected_files = mediciones_files
        else:
            selected_files = [selected_file]

        zip_file_path = os.path.join(data_folder, "mediciones.zip")
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for file in selected_files:
                file_path = os.path.join(mediciones_folder, file)
                zipf.write(file_path, file)

        # Leer el archivo ZIP generado y codificarlo en base64
        with open(zip_file_path, "rb") as file:
            zip_data = file.read()
            zip_base64 = base64.b64encode(zip_data).decode("utf-8")

        # Devolver un enlace que descargará el archivo ZIP codificado en base64
        return "data:application/zip;base64," + zip_base64

    # Descargar archivo(s) de simulaciones
    @app.callback(
        Output("simulaciones-link", "href"),
        Input("simulaciones-dropdown", "value")
    )
    def download_simulaciones_file(selected_file):
        if selected_file == "todos":
            selected_files = simulaciones_files
        else:
            selected_files = [selected_file]

        zip_file_path = os.path.join(data_folder, "simulaciones.zip")
        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            for file in selected_files:
                file_path = os.path.join(simulaciones_folder, file)
                zipf.write(file_path, file)

        # Leer el archivo ZIP generado y codificarlo en base64
        with open(zip_file_path, "rb") as file:
            zip_data = file.read()
            zip_base64 = base64.b64encode(zip_data).decode("utf-8")

        # Devolver un enlace que descargará el archivo ZIP codificado en base64
        return "data:application/zip;base64," + zip_base64

    pass