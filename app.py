from dash.dependencies import Output, Input, State
import dash
from dash import dcc
from dash import html
from pages import mediciones_page
from pages import inicio_page
from pages import informe_tecnico_page
from pages import informe_legal_page
from pages import informe_final_page
from pages import archivos_page
from pages import linea_de_tiempo_page


external_scripts_dict = [
    {
        "src": "https://kit.fontawesome.com/d147d1adc0.js",
        "crossorigin": "anonymous"
    }
]

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_scripts=external_scripts_dict)

# Definir el estilo CSS para los contenedores principales
app.layout = html.Div(className="main-container", id="my-body",
                      children=[
                          dcc.Location(id='url', refresh=False),
                          html.Header(
                              html.Div([
                                  html.I(className="fa-solid fa-bars",
                                         id="btn-open-close"),
                                  html.H3("Proyecto ANE")],
                                  className="icon-menu")
                          ),
                          # Menú
                          html.Div(
                              children=[
                                  html.Div(
                                      [
                                          html.A(href='/', children=[
                                              html.I(
                                                  className="fa-solid fa-house"),
                                              html.H3(children="Inicio")
                                          ])
                                      ],
                                      className="page-title"
                                  ),
                                  html.Div([
                                      html.A(href='/linea-de-tiempo', className="selected", children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-timeline", title="Línea de tiempo"),
                                              html.H4("Línea de tiempo")
                                          ], className="opt")
                                      ]),
                                      html.A(href='/mediciones', children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-chart-line", title="Mediciones"),
                                              html.H4("Mediciones")
                                          ], className="opt")
                                      ]),
                                      html.A(href='/simulaciones', children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-chart-line", title="Simulaciones"),
                                              html.H4("Simulaciones")
                                          ], className="opt")
                                      ]),
                                      html.A(href='/nueva-opt', className="selected", children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-chart-area", title="Nueva Opción"),
                                              html.H4("Nueva opción")
                                          ], className="opt")
                                      ]),
                                      html.A(href='/informe-tecnico', children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-file-pdf", title="Informe técnico"),
                                              html.H4("Informe técnico")
                                          ], className="opt")
                                      ]),
                                      html.A(href='/informe-legal', children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-file-pdf", title="Informe legal"),
                                              html.H4("Informe legal")
                                          ], className="opt")
                                      ]),
                                      html.A(href='/informe-final', children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-file-pdf", title="Informe final"),
                                              html.H4("Informe final")
                                          ], className="opt")
                                      ]),
                                      html.A(href='/archivos', children=[
                                          html.Div([
                                              html.I(
                                                  className="fa-solid fa-file", title="Archivos"),
                                              html.H4("Archivos")
                                          ], className="opt")
                                      ]),
                                  ],
                                      className="opts-menu"
                                  )
                              ], className="menu-container", id="menu-container"
                          ),
                          # Contenido dinámico
                          html.Div(
                              id='content',
                              children=[
                                  html.H2('Bienvenido'),
                                  html.P(
                                      'Selecciona una opción del menú para ver el contenido correspondiente.')
                              ], className="content-container container"
                          )
                      ]
                      )

app._favicon = ("assets\favicon.ico")


@app.callback(
    Output('content', 'children'),
    [Input('url', 'pathname')]
)
def display_content(pathname):
    if pathname == '/mediciones':
        return mediciones_page.layout()
    elif pathname == '/simulaciones':
        return html.Div([
            html.H2('Simulaciones'),
        ])
    elif pathname == '/informe-tecnico':
        return informe_tecnico_page.layout()
    elif pathname == '/informe-legal':
        return informe_legal_page.layout()
    elif pathname == '/informe-final':
        return informe_final_page.layout()
    elif pathname == '/archivos':
        return archivos_page.layout()
    elif pathname == '/linea-de-tiempo':
        return linea_de_tiempo_page.layout()
    elif pathname == '/nueva-opt':
        return html.Div([
            html.H2('Nueva opción'),
            html.P("Un párrafo")
        ])
    else:
        return inicio_page.layout()


@app.callback(
    Output('menu-container', 'className'),
    Output('my-body', 'className'),
    Input('btn-open-close', 'n_clicks'),
    State('menu-container', 'className'),
    State('my-body', 'className')
)
def update_classnames(n_clicks, menu_container_classname, body_classname):
    if 'menu-container-moved' in menu_container_classname:
        menu_container_classname = menu_container_classname.replace(
            'menu-container-moved', '')
    else:
        menu_container_classname += ' menu-container-moved'

    if 'body-moved' in body_classname:
        body_classname = body_classname.replace('body-moved', '')
    else:
        body_classname += ' body-moved'

    return menu_container_classname, body_classname


if __name__ == '__main__':
    mediciones_page.register_callbacks(app)
    archivos_page.register_callbacks(app)
    linea_de_tiempo_page.register_callbacks(app)
    app.run_server(debug=True)
