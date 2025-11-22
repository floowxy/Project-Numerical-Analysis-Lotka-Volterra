import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/",
    name="Inicio",
    title="Inicio · Volterra"
)

def make_card(icon, title, desc, link_text, link_href, btn_class="btn-primary-glow"):
    return html.Div(
        className="home-card", # Esta clase ahora define la "Caja"
        children=[
            # Parte superior: Icono y Textos
            html.Div([
                html.Div(icon, className="card-icon"),
                html.H3(title, className="card-title"),
                html.P(desc, className="card-desc"),
            ]),
            # Parte inferior: Botón (centrado por el CSS del padre)
            html.Div(
                dcc.Link(link_text, href=link_href, className=btn_class)
            )
        ]
    )

layout = html.Div(
    className="sim-new-root",
    children=[
        # TÍTULO PRINCIPAL
        html.Div(
            className="sim-header",
            children=[
                html.H1("PROYECTO LOTKA-VOLTERRA", className="sim-title"),
                html.P(
                    "SISTEMA AVANZADO DE SIMULACIÓN BIOLÓGICA // ANÁLISIS DINÁMICO",
                    className="sim-desc"
                ),
            ]
        ),

        # GRID DE TARJETAS (Ahora sí se verán como cajas)
        html.Div(
            className="home-grid",
            children=[
                make_card(
                    "📊", 
                    "SIMULADOR QUANTUM", 
                    "Entorno interactivo para visualización de órbitas en tiempo real y renderizado de video.", 
                    "ENTRAR AL SIMULADOR", 
                    "/simulador", 
                    "btn-primary-glow"
                ),

                make_card(
                    "📑", 
                    "INFORME TÉCNICO", 
                    "Documentación matemática detallada, deducciones y análisis de estabilidad.", 
                    "LEER INFORME", 
                    "/informe", 
                    "btn-secondary-glow"
                ),

                make_card(
                    "📺", 
                    "PRESENTACIÓN", 
                    "Diapositivas oficiales del proyecto en formato LaTeX Beamer para sustentación.", 
                    "VER SLIDES", 
                    "/beamer", 
                    "btn-secondary-glow"
                ),
            ]
        )
    ]
)