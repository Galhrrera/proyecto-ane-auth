from dash.dependencies import Output, Input
import dash
from dash import dcc
from dash import html

def layout():
    return html.Div([
        html.H2("CALCULADORA"),
        html.Div([
            html.H3("Entradas"),
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
            html.Div([
                html.Label("Frecuencia (GHz)"),
                dcc.Input(id="frecuancia", type="number", value=0, className="input-field"),
                # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
            ], className="input-container container"),
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
                html.Label("Cabeceo máximo de la aeronave ± 30º (grados)"),
                dcc.Input(id="cabeceo-maximo-aeronave", type="number", value=0, className="input-field"),
                # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
            ], className="input-container container"),
            html.Div([
                html.Label("Corrección para un tiempo del 1% IUT-R P525 6dB (dB)"),
                dcc.Input(id="correcion-para-tiempo", type="number", value=0, className="input-field"),
                # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
            ], className="input-container container"),
            html.Div([
                html.Label("Margen Seguridad Femtocelda u Otro (dB)"),
                dcc.Input(id="margen-seguridad-femtocelda", type="number", value=0, className="input-field"),
                # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
            ], className="input-container container"),
            html.Div([
                html.Label("Ganancia Antena Base Típico 15dBi - 5dBi de till = 10 dB (dB) (dB)"),
                dcc.Input(id="ganancia-antena-base", type="number", value=0, className="input-field"),
                # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
            ], className="input-container container"),
            html.Div([
                html.Label("Pérdida de cable coaxial antena base -3 dB (dB)"),
                dcc.Input(id="ganancia-antena-base", type="number", value=0, className="input-field"),
                # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
            ], className="input-container container"),
        ], className='inputs'),

        # Campos de entrada
        html.Div([
            html.H3("Salidas"),
            html.Div([
                html.Label("Resultado Densidad Rx Radio Altímetro/100MHz (dBm/MHz)"),
                html.Div(id="resultado-densidad", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),

            html.Div([
                html.Label("Resultado Aten. FDR del filtro del Rx 24 dB/octava (dB)"),
                html.Div(id="resultado-densidad", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),

            html.Div([
                html.Label("Resultado Diferencia altura Centro Radiante y AGL (mts)"),
                html.Div(id="resultado-densidad", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),

            html.Div([
                html.Label("Resultado Distancia Centro Centro radiante y Aeronave"),
                html.Div(id="resultado-distancia-centro-radiante-aeronave", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),

            html.Div([
                html.Label("Resultado Ángulo de recepción con respecto a la vertical de la Antena RA (Grados)"),
                html.Div(id="resultado-angulo-recepcion-respecto-vertical-de-antena-RA", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),
            html.Div([
                html.Label("Resultado Ganancia Antena Aeronave (dB)"),
                html.Div(id="resultado-ganancia-antena-aeronave", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),
            html.Div([
                html.Label("Resultado Insidencia de señal en la superficie Avión"),
                html.Div(id="resultado-insidencia-señal-superficie-aeronave", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),
            html.Div([
                html.Label("Resultado Distancia Línea de vista"),
                html.Div(id="resultado-distancia-linea-vista", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),
            html.Div([
                html.Label("Resultado Pérdida por propagación en espacio libre UIT-R P525 (dB)"),
                html.Div(id="resultado-distancia-linea-vista", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),

            html.Div([
                html.Label("Resultado PIRE (dB)"),
                html.Div(id="resultado-pire-db", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),
            html.Div([
                html.Label("Resultado PIRE (W)"),
                html.Div(id="resultado-pire-w", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),

            html.Div([
                html.Label("Resultado Tx Base (dBm)"),
                html.Div(id="resultado-tx-base-dbm", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container"),
            html.Div([
                html.Label("Resultado Tx Base (W)"),
                html.Div(id="resultado-tx-base-w", className="output-field"),
                # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
            ], className="output-container container")
        ], className="outputs")
    ], className="calculadora-container container")