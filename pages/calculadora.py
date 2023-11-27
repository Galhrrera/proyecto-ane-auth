from dash.dependencies import Output, Input
import dash
from dash import dcc
from dash import html

def layout():
    return html.Div([
        html.H2("CALCULADORA"),
        # Campos de entrada
        html.Div([
            html.Label("Límite de Potencia Rx Radio Altímetro (dBm)"),
            dcc.Input(id="limite-potencia", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Ancho de banda contemplado (MHz)"),
            dcc.Input(id="ancho-banda-comtemplado", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        # Campos de salida
        html.Div([
            html.Label("Resultado Densidad Rx Radio Altímetro/100MHz (dBm/MHz)"),
            html.Div(id="resultado-densidad", className="output-field"),
            # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
        ], className="output-container container"),
        html.Div([
            html.Label("Frecuencia (GHz)"),
            dcc.Input(id="frecuancia", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Resultado Aten. FDR del filtro del Rx 24 dB/octava (dB)"),
            html.Div(id="resultado-densidad", className="output-field"),
            # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
        ], className="output-container container"),
        html.Div([
            html.Label("Pérdida Cable Coaxial Antena RA: -6 dB y/o -3 dB (dB)"),
            dcc.Input(id="perdida-cable-coaxial-antena-ra", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Margen Seguridad ICAO 6 dB (dB)"),
            dcc.Input(id="margen-seguridad-icao", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Altura AGL de la aeronave"),
            dcc.Input(id="altura-agl-aeronave", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Altura centro Radiante sobre el Aérodromo ARLL (mts)"),
            dcc.Input(id="altura-centro-radiante-aeronave", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Resultado Diferencia altura Centro Radiante y AGL (mts)"),
            html.Div(id="resultado-densidad", className="output-field"),
            # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
        ], className="output-container container"),
        html.Div([
            html.Label("Diferencia Estación a Centro (mts)"),
            dcc.Input(id="diferencia-estacion-centro-pista", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Derivada de la Aeronave (mts)"),
            dcc.Input(id="derivada-aeronave", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
        html.Div([
            html.Label("Resultado Distancia Centro Centro radiante y Aeronave"),
            html.Div(id="resultado-distancia-centro-radiante-aeronave", className="output-field"),
            # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
        ], className="output-container container"),
        html.Div([
            html.Label("Cabeceo máximo de la aeronave ± 30º (grados)"),
            dcc.Input(id="cabeceo-maximo-aeronave", type="number", value=0, className="input-field"),
            # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
        ], className="input-container container"),
    ], className="calculadora-container container")