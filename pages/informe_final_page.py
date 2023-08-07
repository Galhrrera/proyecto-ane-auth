import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go

def layout():
    return html.Div([
        html.H2('INFORME FINAL', className="content-title"),
        html.Div([
            html.P(
        '''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt 
        ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco 
        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in 
        voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat 
        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        '''
            )
        ], className="informe-parrafo"),
        html.ObjectEl(
            data="assets\informe_final.PDF",
                type="application/pdf",
                className='informe'
            )

    ], className="informe-container container")