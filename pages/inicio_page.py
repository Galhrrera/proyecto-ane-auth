import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go

def layout():
    return html.Div([
        html.H2(
                '''
                ANÁLISIS TÉCNICOS PARA LA IDENTIFICACIÓN Y MITIGACIÓN DE INTERFERENCIAS 
                ENTRE LOS SISTEMAS DE RADIOCOMUNICACIONES DE 3500 MHZ Y LOS RADIOALTÍMETROS 
                DE LAS AERONAVES EN LAS BANDAS DE 4200 MHZ A 4400 MHZ 
                ''', className="content-title"),
        html.Div([
            html.Div([
                html.P(children=
                       '''
                       Esta aplicación tiene como objetivo proporcionar una herramienta eficiente y 
                       efectiva para analizar técnicamente las interferencias entre las bandas de 3500MHz, 
                       4200MHz y 4400MHz, brindando datos de mediciones en campo, simulaciones e 
                       informes de proyectos.
                       ''', className="inicio-parrafo")
            ],className="inicio-parrafo-container"),
            html.H3("Características principales de nuestra aplicación:"),
    
            html.Ul([
                html.Li("Visualización de la descripción y el funcionamiento: Ofrecemos una visión general de nuestra aplicación y su propósito. Explicamos cómo utilizarla y qué características destacadas tiene."),
                html.Li("Datos y gráficos de mediciones en campo: Presentamos de forma clara y accesible los datos recopilados durante las mediciones en campo. Esto permite a los usuarios visualizar y comprender las mediciones realizadas de manera efectiva."),
                html.Li("Datos y gráficos de simulaciones en laboratorio: Mostramos los resultados de las simulaciones realizadas en nuestro laboratorio. Brindamos información detallada sobre las condiciones de interferencia y los posibles escenarios de mitigación para una comprensión más completa."),
                html.Li("Acceso a informes legales, técnicos y finales del proyecto: Permitimos la visualización de informes relevantes generados durante diferentes etapas del proyecto. Estos informes incluyen aspectos legales, técnicos y conclusiones para ofrecer una perspectiva integral."),
                html.Li("Descarga de datos de mediciones y simulaciones: Facilitamos la descarga de todos los datos recopilados durante las mediciones en campo y las simulaciones realizadas en el laboratorio. Esto brinda la oportunidad de realizar un análisis más detallado y utilizar los datos en otros contextos según sea necesario.")
            ]),
    
            html.H3("Explora las opciones del menú para acceder a las distintas funcionalidades:"),

            html.Ul([
                html.Li("Mediciones: Aquí podrás observar los datos y gráficos de las mediciones realizadas en campo."),
                html.Li("Simulaciones: Accede a los datos obtenidos de las simulaciones realizadas en laboratorio."),
                html.Li("Informe técnico: Encuentra informes técnicos detallados del proyecto."),
                html.Li("Informe legal: Obtén acceso a informes legales relacionados con el proyecto."),
                html.Li("Datos: Descarga todos los datos obtenidos en las mediciones y simulaciones para un análisis más profundo.")
            ])
    ], className="inicio-parrafos-container")
], className="inicio-container container")

