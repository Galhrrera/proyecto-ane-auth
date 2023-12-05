from math import atan, log, log10, pi, sqrt, ceil
from dash.dependencies import Output, Input, State
import dash
from dash import dcc
from dash import html


def layout():
    return html.Div([
        html.H2("CALCULADORA"),
        dcc.Tabs(id="calculadora-tabs", value="Calculadora libre", children=[
            dcc.Tab(label="UPB  UIT-R M.2059", value="UPB  UIT-R M.2059"),
            dcc.Tab(label="UPB  AVSI Vol", value="UPB  AVSI Vol"),
            dcc.Tab(label="UPB  AVSI Vol. III", value="UPB  AVSI Vol. III"),
            dcc.Tab(label="Calculadora libre", value="Calculadora libre")
        ], className="calculadora-tabs"),
        html.Div(id="calculadora-tab-content")
    ], className="container calculadora-container")


def calcular(limite_potencia, ancho_banda_contemplado, frecuencia, perdida_cable_coaxial_antena_ra,
             margen_seguridad_icao, altura_agl_aeronave, altura_centro_radiante_aeronave,
             diferencia_estacion_centro_pista, derivada_aeronave, cabeceo_maximo_aeronave,
             correcion_para_tiempo, margen_seguridad_femtocelda, ganancia_antena_base,
             perdida_cable_coaxial_antena_base):

    densidad_rx = limite_potencia - 10 * log10(ancho_banda_contemplado)

    atenuacion_fdr = (4.2 - frecuencia) * 24 / 2.2
    diferencia_altura = max(0, altura_agl_aeronave -
                            altura_centro_radiante_aeronave)
    distancia_centro_aeronave = diferencia_estacion_centro_pista - derivada_aeronave

    # Check for valid input values for arctangent
    if diferencia_altura == 0 or distancia_centro_aeronave == 0:
        angulo_recepcion = 0
    else:
        angulo_recepcion = 90 - \
            atan(diferencia_altura / distancia_centro_aeronave) * \
            180 / pi - cabeceo_maximo_aeronave

    # Check for valid input values for ganancia_antena_aeronave
    if -(12 / 45**2) * angulo_recepcion**2 + 13 < 0:
        ganancia_antena_aeronave = 0
    else:
        ganancia_antena_aeronave = -(12 / 45**2) * angulo_recepcion**2 + 13

    intensidad_senal = (limite_potencia + perdida_cable_coaxial_antena_ra -
                        margen_seguridad_icao - ganancia_antena_aeronave)

    distancia_linea_vista = sqrt(
        diferencia_altura**2 + distancia_centro_aeronave**2)

    perdidas_espacio_libre = 32.4 + 20 * \
        log10(distancia_linea_vista * 1000) + 20 * log10(frecuencia / 1000)

    pire_dbm = intensidad_senal + perdidas_espacio_libre + \
        correcion_para_tiempo - margen_seguridad_femtocelda

    pire_w = 10**((pire_dbm - 30) / 10)

    tx_base_dbm = pire_dbm - ganancia_antena_base - perdida_cable_coaxial_antena_base

    tx_base_w = 10**((tx_base_dbm - 30) / 10)

    return round(densidad_rx), round(atenuacion_fdr), round(diferencia_altura), round(distancia_centro_aeronave), ceil(angulo_recepcion), \
        ceil(ganancia_antena_aeronave), ceil(intensidad_senal), round(distancia_linea_vista), round(perdidas_espacio_libre), \
        round(pire_dbm), round(pire_w), round(tx_base_dbm), round(tx_base_w)


def register_callbacks(app):
    @app.callback(
        Output("calculadora-tab-content", "children"),
        Input("calculadora-tabs", "value")
    )
    def update_tab_content(tab):
        if tab == "UPB  UIT-R M.2059":
            dropdown_options = [
                "< 3.35",
                "3.35/3.45",
                "3.45/3.55",
                "3.55/3.65",
                "3.65/3.75",
                "3.75/3.85",
                "3.85/3.95"
            ]
            return html.Div([
                dcc.Dropdown(
                    id="calculadora-dropdown",
                    options=[{'label': option, 'value': option}
                             for option in dropdown_options],
                    value="< 3.35"
                ),
                html.Div(id="selected-calculadora-content")
            ])
        elif tab == "UPB  AVSI Vol":
            dropdown_options = [
                "Cat. 1",
                "Cat. 2",
                "Cat. 3"
            ]
            return html.Div([
                dcc.Dropdown(
                    id="calculadora-dropdown",
                    options=[{'label': option, 'value': option}
                             for option in dropdown_options],
                    value="Cat. 1"
                ),
                html.Div(id="selected-calculadora-content")
            ])
        elif tab == "UPB  AVSI Vol. III":
            dropdown_options = [
                "< 3.35",
                "3.35/3.45",
                "3.45/3.55",
                "3.55/3.65"
            ]
            return html.Div([
                dcc.Dropdown(
                    id="calculadora-dropdown",
                    options=[{'label': option, 'value': option}
                             for option in dropdown_options],
                    value="< 3.35"
                ),
                html.Div(id="selected-calculadora-content")
            ])
        elif tab == "Calculadora libre":
            return html.Div([
                html.H2("CALCULADORA"),
                html.H3("Entradas", className="calculadora-subtitle"),
                html.Div([

                    html.Div([
                        html.Label("Límite de Potencia Rx Radio Altímetro"),
                        dcc.Input(id="limite-potencia", type="number",
                                  value=-19, className="input-field"),
                        html.Label("dBm", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Ancho de banda contemplado"),
                        dcc.Input(id="ancho-banda-comtemplado", type="number",
                                  value=100, className="input-field"),
                        html.Label("MHz", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Frecuencia"),
                        dcc.Input(id="frecuancia", type="number",
                                  value=4.2, className="input-field"),
                        html.Label("GHz", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Pérdida Cable Coaxial Antena RA: -6 dB y/o -3 dB"),
                        dcc.Input(id="perdida-cable-coaxial-antena-ra",
                                  type="number", value=-3, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Margen Seguridad ICAO 6 dB"),
                        dcc.Input(id="margen-seguridad-icao", type="number",
                                  value=6, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Altura AGL de la aeronave"),
                        dcc.Input(id="altura-agl-aeronave", type="number",
                                  value=819, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Altura centro Radiante sobre el Aérodromo ARLL"),
                        dcc.Input(id="altura-centro-radiante-aeronave",
                                  type="number", value=15, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Diferencia Estación a Centro de pista"),
                        dcc.Input(id="diferencia-estacion-centro-pista",
                                  type="number", value=910, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Deriva de la Aeronave"),
                        dcc.Input(id="derivada-aeronave", type="number",
                                  value=91, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Cabeceo máximo de la aeronave ± 30º"),
                        dcc.Input(id="cabeceo-maximo-aeronave", type="number",
                                  value=0, className="input-field"),
                        html.Label("Grados", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Corrección para un tiempo del 1% IUT-R P525 6dB"),
                        dcc.Input(id="correcion-para-tiempo", type="number",
                                  value=6, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Margen Seguridad Femtocelda u Otro"),
                        dcc.Input(id="margen-seguridad-femtocelda",
                                  type="number", value=6, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Ganancia Antena Base Típico 15dBi - 5dBi de till = 10dB"),
                        dcc.Input(id="ganancia-antena-base", type="number",
                                  value=10, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Pérdida de cable coaxial antena base -3 dB"),
                        dcc.Input(id="perdida-cable-coaxial-antena-base",
                                  type="number", value=-3, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                ], className='inputs'),

                # Campos de entrada
                html.Div([
                    html.H3("Salidas", className="calculadora-subtitle"),
                    html.Div([
                        html.Label(
                            "Resultado Densidad Rx Radio Altímetro/100MHz"),
                        html.Div(id="resultado-densidad",
                                 className="output-field"),
                        html.Label("dBm/MHz", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Aten. FDR del filtro del Rx 24 dB/octava"),
                        html.Div(id="resultado-aten-fdr",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Diferencia altura Centro Radiante y AGL"),
                        html.Div(id="resultado-diferencia-altura",
                                 className="output-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Distancia Centro Centro radiante y Aeronave"),
                        html.Div(id="resultado-distancia-centro-aeronave",
                                 className="output-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Ángulo de recepción con respecto a la vertical de la Antena RA"),
                        html.Div(id="resultado-angulo-recepcion",
                                 className="output-field"),
                        html.Label("Grados", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado Ganancia Antena Aeronave"),
                        html.Div(id="resultado-ganancia-antena-aeronave",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label(
                            "Resultado Insidencia de señal en la superficie Avión"),
                        html.Div(id="resultado-intensidad-senal",
                                 className="output-field"),
                        html.Label("dBm", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado Distancia Línea de vista"),
                        html.Div(id="resultado-distancia-linea-vista",
                                 className="output-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label(
                            "Resultado Pérdida por propagación en espacio libre UIT-R P525"),
                        html.Div(id="resultado-perdidas-espacio-libre",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label("Resultado PIRE"),
                        html.Div(id="resultado-pire-dbm",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado PIRE"),
                        html.Div(id="resultado-pire-w",
                                 className="output-field"),
                        html.Label("W", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label("Resultado Tx Base"),
                        html.Div(id="resultado-tx-base-dbm",
                                 className="output-field"),
                        html.Label("dBm", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado Tx Base"),
                        html.Div(id="resultado-tx-base-w",
                                 className="output-field"),
                        html.Label("W", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container")
                ], className="outputs"),
                html.Button("Calcular", id="calcular-button",
                            n_clicks=0, className="archivos-descargas-btn")
            ], className="calculadora-tab-container container")
        
    @app.callback(
        Output("selected-calculadora-content", "children"),
        [Input("calculadora-tabs", "value"),
         Input("calculadora-dropdown", "value")]
    )
    def update_calculadora(tab, value):
        limite_potencia_rx_radio_altimetro = 0
        ancho_banda_contemplado = 0
        frecuencia = 0
        perdida_cable_coaxial_antena_ra = 0
        margen_seguridad_icao = 0
        altura_agl_aeronave = 0
        altura_centro_radiante_aerodromo = 0
        distancia_estacion_centro_pista = 0
        deriva_aeronave = 0
        cabeceo_maximo_aeronave = 0
        correccion_tiempo_1_pct = 0
        margen_seguridad_femtocelda = 0
        ganancia_antena_base = 0
        perdida_cable_coaxial_antena_base = 0
        if tab == "UPB  UIT-R M.2059":
            if value == "< 3.35":
                limite_potencia_rx_radio_altimetro = -46.7
                ancho_banda_contemplado = 100
                frecuencia = 3.35
                perdida_cable_coaxial_antena_ra = -3
                margen_seguridad_icao = 6
                altura_agl_aeronave = 61
                altura_centro_radiante_aerodromo = 15
                distancia_estacion_centro_pista = 910
                deriva_aeronave = 10
                cabeceo_maximo_aeronave = 5
                correccion_tiempo_1_pct = 6
                margen_seguridad_femtocelda = 0
                ganancia_antena_base = 10
                perdida_cable_coaxial_antena_base = -3
            elif value == "3.35/3.45":
                limite_potencia_rx_radio_altimetro = -47.8
                ancho_banda_contemplado = 100
                frecuencia = 3.45
                perdida_cable_coaxial_antena_ra = -3
                margen_seguridad_icao = 6
                altura_agl_aeronave = 61
                altura_centro_radiante_aerodromo = 15
                distancia_estacion_centro_pista = 910
                deriva_aeronave = 10
                cabeceo_maximo_aeronave = 5
                correccion_tiempo_1_pct = 6
                margen_seguridad_femtocelda = 0
                ganancia_antena_base = 10
                perdida_cable_coaxial_antena_base = -3
            elif value == "3.45/3.55":
                limite_potencia_rx_radio_altimetro = -48.9
                ancho_banda_contemplado = 100
                frecuencia = 3.55
                perdida_cable_coaxial_antena_ra = -3
                margen_seguridad_icao = 6
                altura_agl_aeronave = 61
                altura_centro_radiante_aerodromo = 15
                distancia_estacion_centro_pista = 910
                deriva_aeronave = 10
                cabeceo_maximo_aeronave = 5
                correccion_tiempo_1_pct = 6
                margen_seguridad_femtocelda = 0
                ganancia_antena_base = 10
                perdida_cable_coaxial_antena_base = -3
            elif value == "3.55/3.65":
                limite_potencia_rx_radio_altimetro = -50
                ancho_banda_contemplado = 100
                frecuencia = 3.65
                perdida_cable_coaxial_antena_ra = -3
                margen_seguridad_icao = 6
                altura_agl_aeronave = 61
                altura_centro_radiante_aerodromo = 15
                distancia_estacion_centro_pista = 910
                deriva_aeronave = 10
                cabeceo_maximo_aeronave = 5
                correccion_tiempo_1_pct = 6
                margen_seguridad_femtocelda = 0
                ganancia_antena_base = 10
                perdida_cable_coaxial_antena_base = -3
            elif value == "3.65/3.75":
                limite_potencia_rx_radio_altimetro = -51.1
                ancho_banda_contemplado = 100
                frecuencia = 3.75
                perdida_cable_coaxial_antena_ra = 0
                margen_seguridad_icao = 6
                altura_agl_aeronave = 305
                altura_centro_radiante_aerodromo = 80
                distancia_estacion_centro_pista = 400
                deriva_aeronave = 91
                cabeceo_maximo_aeronave = 25
                correccion_tiempo_1_pct = 6
                margen_seguridad_femtocelda = 0
                ganancia_antena_base = 10
                perdida_cable_coaxial_antena_base = -3
            elif value == "3.75/3.85":
                limite_potencia_rx_radio_altimetro = -56
                ancho_banda_contemplado = 100
                frecuencia = 4.2
                perdida_cable_coaxial_antena_ra = -3
                margen_seguridad_icao = 6
                altura_agl_aeronave = 305
                altura_centro_radiante_aerodromo = 80
                distancia_estacion_centro_pista = 400
                deriva_aeronave = 91
                cabeceo_maximo_aeronave = 30
                correccion_tiempo_1_pct = 6
                margen_seguridad_femtocelda = 0
                ganancia_antena_base = 10
                perdida_cable_coaxial_antena_base = -3
            elif value == "3.85/3.95":
                limite_potencia_rx_radio_altimetro = -56
                ancho_banda_contemplado = 100
                frecuencia = 4.2
                perdida_cable_coaxial_antena_ra = -3
                margen_seguridad_icao = 6
                altura_agl_aeronave = 305
                altura_centro_radiante_aerodromo = 80
                distancia_estacion_centro_pista = 400
                deriva_aeronave = 91
                cabeceo_maximo_aeronave = 30
                correccion_tiempo_1_pct = 6
                margen_seguridad_femtocelda = 0
                ganancia_antena_base = 10
                perdida_cable_coaxial_antena_base = -3
        
        return html.Div([
                html.H2("CALCULADORA"),
                html.H3("Entradas", className="calculadora-subtitle"),
                html.Div([

                    html.Div([
                        html.Label("Límite de Potencia Rx Radio Altímetro"),
                        dcc.Input(id="limite-potencia", type="number",
                                  value=limite_potencia_rx_radio_altimetro, className="input-field"),
                        html.Label("dBm", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Ancho de banda contemplado"),
                        dcc.Input(id="ancho-banda-comtemplado", type="number",
                                  value=ancho_banda_contemplado, className="input-field"),
                        html.Label("MHz", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Frecuencia"),
                        dcc.Input(id="frecuancia", type="number",
                                  value=frecuencia, className="input-field"),
                        html.Label("GHz", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Pérdida Cable Coaxial Antena RA: -6 dB y/o -3 dB"),
                        dcc.Input(id="perdida-cable-coaxial-antena-ra",
                                  type="number", value=perdida_cable_coaxial_antena_ra, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Margen Seguridad ICAO 6 dB"),
                        dcc.Input(id="margen-seguridad-icao", type="number",
                                  value=margen_seguridad_icao, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Altura AGL de la aeronave"),
                        dcc.Input(id="altura-agl-aeronave", type="number",
                                  value=altura_agl_aeronave, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Altura centro Radiante sobre el Aérodromo ARLL"),
                        dcc.Input(id="altura-centro-radiante-aeronave",
                                  type="number", value=altura_centro_radiante_aerodromo, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Diferencia Estación a Centro de pista"),
                        dcc.Input(id="diferencia-estacion-centro-pista",
                                  type="number", value=distancia_estacion_centro_pista, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Deriva de la Aeronave"),
                        dcc.Input(id="derivada-aeronave", type="number",
                                  value=deriva_aeronave, className="input-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Cabeceo máximo de la aeronave ± 30º"),
                        dcc.Input(id="cabeceo-maximo-aeronave", type="number",
                                  value=cabeceo_maximo_aeronave, className="input-field"),
                        html.Label("Grados", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Corrección para un tiempo del 1% IUT-R P525 6dB"),
                        dcc.Input(id="correcion-para-tiempo", type="number",
                                  value=correccion_tiempo_1_pct, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label("Margen Seguridad Femtocelda u Otro"),
                        dcc.Input(id="margen-seguridad-femtocelda",
                                  type="number", value=margen_seguridad_femtocelda, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Ganancia Antena Base Típico 15dBi - 5dBi de till = 10dB"),
                        dcc.Input(id="ganancia-antena-base", type="number",
                                  value=ganancia_antena_base, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                    html.Div([
                        html.Label(
                            "Pérdida de cable coaxial antena base -3 dB"),
                        dcc.Input(id="perdida-cable-coaxial-antena-base",
                                  type="number", value=perdida_cable_coaxial_antena_base, className="input-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de entrada aquí con etiquetas y IDs correspondientes
                    ], className="input-container container"),
                ], className='inputs'),

                # Campos de entrada
                html.Div([
                    html.H3("Salidas", className="calculadora-subtitle"),
                    html.Div([
                        html.Label(
                            "Resultado Densidad Rx Radio Altímetro/100MHz"),
                        html.Div(id="resultado-densidad",
                                 className="output-field"),
                        html.Label("dBm/MHz", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Aten. FDR del filtro del Rx 24 dB/octava"),
                        html.Div(id="resultado-aten-fdr",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Diferencia altura Centro Radiante y AGL"),
                        html.Div(id="resultado-diferencia-altura",
                                 className="output-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Distancia Centro Centro radiante y Aeronave"),
                        html.Div(id="resultado-distancia-centro-aeronave",
                                 className="output-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label(
                            "Resultado Ángulo de recepción con respecto a la vertical de la Antena RA"),
                        html.Div(id="resultado-angulo-recepcion",
                                 className="output-field"),
                        html.Label("Grados", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado Ganancia Antena Aeronave"),
                        html.Div(id="resultado-ganancia-antena-aeronave",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label(
                            "Resultado Insidencia de señal en la superficie Avión"),
                        html.Div(id="resultado-intensidad-senal",
                                 className="output-field"),
                        html.Label("dBm", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado Distancia Línea de vista"),
                        html.Div(id="resultado-distancia-linea-vista",
                                 className="output-field"),
                        html.Label("mts", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label(
                            "Resultado Pérdida por propagación en espacio libre UIT-R P525"),
                        html.Div(id="resultado-perdidas-espacio-libre",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label("Resultado PIRE"),
                        html.Div(id="resultado-pire-dbm",
                                 className="output-field"),
                        html.Label("dB", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado PIRE"),
                        html.Div(id="resultado-pire-w",
                                 className="output-field"),
                        html.Label("W", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),

                    html.Div([
                        html.Label("Resultado Tx Base"),
                        html.Div(id="resultado-tx-base-dbm",
                                 className="output-field"),
                        html.Label("dBm", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container"),
                    html.Div([
                        html.Label("Resultado Tx Base"),
                        html.Div(id="resultado-tx-base-w",
                                 className="output-field"),
                        html.Label("W", className="units")
                        # Agrega más campos de salida aquí con etiquetas y IDs correspondientes
                    ], className="output-container container")
                ], className="outputs"),
                html.Button("Calcular", id="calcular-button",
                            n_clicks=0, className="archivos-descargas-btn")
            ], className="calculadora-tab-container container")

    @app.callback(
        [Output("resultado-densidad", "children"),
         Output("resultado-aten-fdr", "children"),
         Output("resultado-diferencia-altura", "children"),
         Output("resultado-distancia-centro-aeronave", "children"),
         Output("resultado-angulo-recepcion", "children"),
         Output("resultado-ganancia-antena-aeronave", "children"),
         Output("resultado-intensidad-senal", "children"),
         Output("resultado-distancia-linea-vista", "children"),
         Output("resultado-perdidas-espacio-libre", "children"),
         Output("resultado-pire-dbm", "children"),
         Output("resultado-pire-w", "children"),
         Output("resultado-tx-base-dbm", "children"),
         Output("resultado-tx-base-w", "children")],
        [Input("calcular-button", "n_clicks")],
        [State("limite-potencia", "value"),
         State("ancho-banda-comtemplado", "value"),
         State("frecuancia", "value"),
         State("perdida-cable-coaxial-antena-ra", "value"),
         State("margen-seguridad-icao", "value"),
         State("altura-agl-aeronave", "value"),
         State("altura-centro-radiante-aeronave", "value"),
         State("diferencia-estacion-centro-pista", "value"),
         State("derivada-aeronave", "value"),
         State("cabeceo-maximo-aeronave", "value"),
         State("correcion-para-tiempo", "value"),
         State("margen-seguridad-femtocelda", "value"),
         State("ganancia-antena-base", "value"),
         State("perdida-cable-coaxial-antena-base", "value")]
    )
    def update_output(n_clicks, limite_potencia, ancho_banda_contemplado, frecuencia,
                      perdida_cable_coaxial_antena_ra, margen_seguridad_icao, altura_agl_aeronave,
                      altura_centro_radiante_aeronave, diferencia_estacion_centro_pista,
                      derivada_aeronave, cabeceo_maximo_aeronave, correcion_para_tiempo,
                      margen_seguridad_femtocelda, ganancia_antena_base, perdida_cable_coaxial_antena_base):

        # Verificar si algún campo está vacío
        if None in [limite_potencia, ancho_banda_contemplado, frecuencia,
                    perdida_cable_coaxial_antena_ra, margen_seguridad_icao, altura_agl_aeronave,
                    altura_centro_radiante_aeronave, diferencia_estacion_centro_pista,
                    derivada_aeronave, cabeceo_maximo_aeronave, correcion_para_tiempo,
                    margen_seguridad_femtocelda, ganancia_antena_base, perdida_cable_coaxial_antena_base]:
            return "Por favor, complete todos los campos.", "", "", "", "", "", "", "", "", "", "", "", ""

        # Realizar cálculos
        densidad_rx, atenuacion_fdr, diferencia_altura, distancia_centro_aeronave, angulo_recepcion, \
            ganancia_antena_aeronave, intensidad_senal, distancia_linea_vista, perdidas_espacio_libre, \
            pire_dbm, pire_w, tx_base_dbm, tx_base_w = calcular(limite_potencia, ancho_banda_contemplado, frecuencia,
                                                                perdida_cable_coaxial_antena_ra, margen_seguridad_icao,
                                                                altura_agl_aeronave, altura_centro_radiante_aeronave,
                                                                diferencia_estacion_centro_pista, derivada_aeronave,
                                                                cabeceo_maximo_aeronave, correcion_para_tiempo,
                                                                margen_seguridad_femtocelda, ganancia_antena_base,
                                                                perdida_cable_coaxial_antena_base)

        return f"{densidad_rx}", \
            f"{atenuacion_fdr}", \
            f"{diferencia_altura}", \
            f"{distancia_centro_aeronave}", \
            f"{angulo_recepcion}", \
            f"{ganancia_antena_aeronave}", \
            f"{intensidad_senal}", \
            f"{distancia_linea_vista}", \
            f"{perdidas_espacio_libre}", \
            f"{pire_dbm}", \
            f"{pire_w}", \
            f"{tx_base_dbm}", \
            f"{tx_base_w}"
