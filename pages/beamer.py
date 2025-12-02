import dash
from dash import html

dash.register_page(
    __name__,
    path="/beamer",
    name="Beamer",
    title="Presentación Beamer"
)

layout = html.Div(
    className="sim-new-root",
    children=[
        # HEADER
        html.Div(
            className="sim-header",
            children=[
                html.H2("PRESENTACIÓN ACADÉMICA", className="sim-title"),
                html.P(
                    "DIAPOSITIVAS DE SUSTENTACIÓN // FORMATO BEAMER",
                    className="sim-desc"
                ),
            ]
        ),

        # CONTENEDOR DEL PDF
        html.Div(
            className="input-panel-glass",
            style={"padding": "30px"},
            children=[
                
                # Barra superior
                html.Div(
                    style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "20px", "flexWrap": "wrap", "gap": "15px"},
                    children=[
                        html.H4("VISUALIZADOR DE SLIDES", className="group-title", style={"borderBottom": "none", "marginBottom": "0"}),
                        html.A(
                            "⬇ DESCARGAR SLIDES PDF",
                            href="/docs/beamer/BEAMER FINAL.pdf",
                            target="_blank",
                            className="btn-secondary-glow",
                            style={"textDecoration": "none", "fontSize": "0.9rem"}
                        )
                    ]
                ),

                # Iframe
                html.Iframe(
                    src="/docs/beamer/BEAMER FINAL.pdf",
                    style={
                        "width": "100%",
                        "height": "85vh",
                        "border": "1px solid rgba(0, 243, 255, 0.3)", # Borde Cyan
                        "borderRadius": "8px",
                        "backgroundColor": "#02040a"
                    }
                ),

                html.P(
                    "FIGURA 2. PRESENTACIÓN OFICIAL DEL PROYECTO.",
                    style={"textAlign": "center", "color": "#64748b", "marginTop": "20px", "fontFamily": "Rajdhani", "letterSpacing": "1px"}
                )
            ]
        ),
    ]
)