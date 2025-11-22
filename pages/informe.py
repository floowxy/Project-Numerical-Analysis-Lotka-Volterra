import dash
from dash import html

dash.register_page(
    __name__,
    path="/informe",
    name="Informe",
    title="Informe Científico"
)

layout = html.Div(
    className="sim-new-root",
    children=[
        # HEADER
        html.Div(
            className="sim-header",
            children=[
                html.H2("INFORME CIENTÍFICO", className="sim-title"),
                html.P(
                    "DOCUMENTACIÓN MATEMÁTICA CLASIFICADA // NIVEL TÉCNICO",
                    className="sim-desc"
                ),
            ]
        ),

        # CONTENEDOR DEL PDF (GLASS)
        html.Div(
            className="input-panel-glass",
            style={"padding": "30px"},
            children=[
                
                # Barra superior dentro del panel
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "20px", "flexWrap": "wrap", "gap": "15px"},
                    children=[
                        html.H4("VISOR DE DOCUMENTO", className="group-title", style={"borderBottom": "none", "marginBottom": "0"}),
                        html.A(
                            "⬇ DESCARGAR ARCHIVO PDF",
                            href="/docs/informe/informe_final.pdf",
                            target="_blank",
                            className="btn-secondary-glow",
                            style={"textDecoration": "none", "fontSize": "0.9rem"}
                        )
                    ]
                ),

                # Iframe con borde neón sutil
                html.Iframe(
                    src="/docs/informe/informe_final.pdf",
                    style={
                        "width": "100%",
                        "height": "85vh",
                        "border": "1px solid rgba(188, 19, 254, 0.3)", # Borde Púrpura
                        "borderRadius": "8px",
                        "backgroundColor": "#02040a"
                    }
                ),
                
                html.P(
                    "FIGURA 1. VISTA INTEGRADA DEL INFORME FINAL LATEX.",
                    style={"textAlign": "center", "color": "#64748b", "marginTop": "20px", "fontFamily": "Rajdhani", "letterSpacing": "1px"}
                )
            ]
        ),
    ]
)