from dash.dependencies import Output, Input
import dash
from dash import dcc
from dash import html

def layout():
    return html.Div([
        html.H2("LÍNEA DE TIEMPO"),
        dcc.Slider(
            id='timeline-slider',
            min=1,
            max=5,
            marks={
                1: 'Fecha 1',
                2: 'Fecha 2',
                3: 'Fecha 3',
                4: 'Fecha 4',
                5: 'Fecha 5'
            },
            value=1,
            className="timeline-slider",
            # updatemode="mouseup"
        ),
        html.Div(id='timeline-content', className="timeline-content")
    ], className="linea-de-tiempo-container container")


def register_callbacks(app):
    @app.callback(
    Output('timeline-content', 'children'),
    [Input('timeline-slider', 'value')]
    )
    def update_timeline_content(value):
        value = int(value)
        title = html.H3(f"Opción seleccionada: {value}", className="linea-de-tiempo-titulo-secundario")
        paragraphs = [html.P(f"Párrafo {i+1}") for i in range(value)]
        return [title] + paragraphs