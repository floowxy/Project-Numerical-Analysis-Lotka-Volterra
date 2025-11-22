import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import numpy as np
import requests
from backend.simulation import simulate_lotka_volterra
from backend.validators import validate_inputs

# ===========================================================
# ⚙️ CONFIGURACIÓN DE RED
# ===========================================================
INTERNAL_API_URL = "http://127.0.0.1:8000"
PUBLIC_DOWNLOAD_ROUTE = "/dash_download"

dash.register_page(__name__, path="/simulador", name="Simulador", title="Simulador · Proyecto Lotka–Volterra")

# ===========================================================
# 🎨 HELPERS VISUALES (ESTILO NEON)
# ===========================================================
GRAPH_HEIGHT = 380
C_CYAN = "#00f3ff"
C_PINK = "#ff0055"
C_GREEN = "#00ff9d"
C_YELLOW = "#fcee0a"
C_TEXT = "#e0e6ed"
C_ERROR = "#ff3333"

def base_fig():
    """Configuración base limpia"""
    fig = go.Figure()
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        height=GRAPH_HEIGHT,
        margin=dict(l=40, r=20, t=40, b=40),
        font=dict(family="Rajdhani, sans-serif", color="#94a3b8", size=14),
        title_font=dict(size=16, color="white", family="Orbitron, sans-serif"),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', linecolor=C_CYAN, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', linecolor=C_CYAN, zeroline=False),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=1)
    )
    return fig

# ===========================================================
# 🛡️ SISTEMA DE VALIDACIÓN DE ERRORES
# ===========================================================
# Validación ahora centralizada en backend.validators


# ===========================================================
# 📊 GENERADORES DE GRÁFICOS
# ===========================================================

def graph_no_predators(alpha, P0):
    t = np.linspace(0, 10, 300)
    P = P0 * np.exp(alpha * t)
    fig = base_fig()
    fig.add_trace(go.Scatter(x=t, y=P, mode="lines", line=dict(color=C_CYAN, width=3), name="Presas"))
    fig.update_layout(title="1A // CRECIMIENTO EXPONENCIAL (SIN DEPREDADOR)", xaxis_title="TIEMPO", yaxis_title="POBLACIÓN")
    return fig

def graph_no_prey(gamma, D0):
    t = np.linspace(0, 10, 300)
    D = D0 * np.exp(-gamma * t)
    fig = base_fig()
    fig.add_trace(go.Scatter(x=t, y=D, mode="lines", line=dict(color=C_PINK, width=3), name="Depredadores"))
    fig.update_layout(title="1B // DECAIMIENTO (SIN PRESAS)", xaxis_title="TIEMPO", yaxis_title="POBLACIÓN")
    return fig

def graph_temporal(t, P, D):
    fig = base_fig()
    fig.add_trace(go.Scatter(x=t, y=P, mode="lines", name="Presas", line=dict(color=C_CYAN, width=2)))
    fig.add_trace(go.Scatter(x=t, y=D, mode="lines", name="Depredadores", line=dict(color=C_PINK, width=2)))
    fig.update_layout(title="FIG 2 // DINÁMICA TEMPORAL", xaxis_title="TIEMPO", yaxis_title="POBLACIÓN")
    return fig

def graph_phase(P, D, a, b, d, g):
    """Plano de Fases MEJORADO con Punto de Equilibrio"""
    fig = base_fig()
    
    # 1. Ciclo Límite
    fig.add_trace(go.Scatter(
        x=P, y=D, mode="lines", 
        line=dict(color=C_GREEN, width=3), 
        name="Ciclo"
    ))
    
    # 2. Punto de Inicio (Blanco)
    fig.add_trace(go.Scatter(
        x=[P[0]], y=[D[0]], mode="markers", 
        marker=dict(color="white", size=8),
        name="Inicio"
    ))

    # 3. Punto de Equilibrio (Amarillo)
    # P* = gamma/delta, D* = alpha/beta
    if d != 0 and b != 0:
        eq_P = g / d
        eq_D = a / b
        fig.add_trace(go.Scatter(
            x=[eq_P], y=[eq_D], mode="markers",
            marker=dict(color=C_YELLOW, size=10, symbol="x"),
            name="Equilibrio"
        ))

    fig.update_layout(title="FIG 3 // PLANO DE FASES (Con Equilibrio)", xaxis_title="PRESAS (P)", yaxis_title="DEPREDADORES (D)")
    return fig

def graph_orbits(alpha, beta, delta, gamma, P0, D0, t_max, main_solution=None):
    """Muestra múltiples órbitas para ver cómo cambian"""
    fig = base_fig()
    
    # Diferentes condiciones iniciales basadas en la entrada del usuario
    escalas = [
        (1.0, 1.0, C_CYAN, "Actual", main_solution),   # Reutilizar la simulación principal
        (1.5, 1.5, C_GREEN, "+50%", None),    # Más población
        (0.5, 0.5, C_PINK, "-50%", None),     # Menos población
        (0.2, 0.2, C_YELLOW, "Mínimo", None)  # Cerca al equilibrio
    ]
    
    for eP, eD, color, lbl, precomputed in escalas:
        # Si ya tenemos la solución precomputada (caso Actual), usarla
        if precomputed is not None:
            sol = precomputed
        else:
            # Simular caso hipotético
            sol = simulate_lotka_volterra(alpha, beta, delta, gamma, P0*eP, D0*eD, t_max)
        
        fig.add_trace(go.Scatter(
            x=sol["P"], y=sol["D"], 
            mode="lines", 
            line=dict(color=color, width=2),
            name=lbl,
            opacity=0.8
        ))
        
    fig.update_layout(title="FIG 4 // ESTABILIDAD ORBITAL (Multi-Escenario)", xaxis_title="PRESAS", yaxis_title="DEPREDADORES")
    return fig

# ===========================================================
#   LAYOUT PRINCIPAL
# ===========================================================

layout = html.Div(
    className="sim-new-root",
    children=[
        html.Div(className="sim-header", children=[
            html.H2("LABORATORIO DE SIMULACIÓN", className="sim-title"),
            html.P("AJUSTE DE PARÁMETROS Y RENDERIZADO EN TIEMPO REAL", className="sim-desc")
        ]),

        html.Div(className="input-panel-glass", children=[
            html.Div(className="params-columns", children=[
                # Columna 1: Tasas
                html.Div([
                    html.H4("VARIABLES BIOLÓGICAS", className="group-title"),
                    html.Div([html.Label("α — Crecimiento Presas"), dcc.Slider(id="alpha", min=0.1, max=2.0, step=0.1, value=0.8, marks={0.5:'0.5', 1.0:'1.0', 1.5:'1.5'}, className="custom-slider")], className="param-item"),
                    html.Div([html.Label("β — Tasa Depredación"), dcc.Input(id="beta", type="number", min=0.01, value=0.05, step=0.01, className="param-input-modern")], className="param-item"),
                    html.Div([html.Label("δ — Eficacia Reproductiva"), dcc.Input(id="delta", type="number", min=0.01, value=0.02, step=0.01, className="param-input-modern")], className="param-item"),
                    html.Div([html.Label("γ — Mortalidad Depredador"), dcc.Input(id="gamma", type="number", min=0.1, value=0.6, step=0.1, className="param-input-modern")], className="param-item"),
                ], className="params-group"),

                # Columna 2: Iniciales
                html.Div([
                    html.H4("CONDICIONES INICIALES", className="group-title"),
                    html.Div([html.Label("P₀ — Presas Iniciales"), dcc.Input(id="P0", type="number", min=1, value=80, className="param-input-modern")], className="param-item"),
                    html.Div([html.Label("D₀ — Depredadores Iniciales"), dcc.Input(id="D0", type="number", min=1, value=20, className="param-input-modern")], className="param-item"),
                    html.Div([html.Label("Tiempo (t)"), dcc.Slider(id="tmax", min=20, max=200, step=10, value=50, marks={50:'50', 100:'100', 200:'Max'}, className="custom-slider")], className="param-item"),
                ], className="params-group"),
            ]),

            # Botones
            html.Div(className="action-bar", children=[
                html.Button("⚡ ACTUALIZAR GRÁFICOS", id="sim-button", className="btn-primary-glow"),
                html.Button("🎬 GENERAR VIDEO", id="video-button", className="btn-secondary-glow"),
            ]),

            # Zona de Carga (Barra Quantum)
            html.Div(children=[
                dcc.Loading(
                    id="loading-video",
                    type="default",
                    className="quantum-loader-box",
                    children=[html.Div(id="video-status"), html.Div(id="video-download", style={"textAlign": "center"})]
                )
            ])
        ]),

        # Aquí se pintarán los gráficos (o el error)
        html.Div(id="graphs-output", className="graphs-grid-modern"),
    ]
)

# ===========================================================
# CALLBACKS (CON VALIDACIÓN)
# ===========================================================

@callback(
    Output("graphs-output", "children"),
    Input("sim-button", "n_clicks"),
    State("alpha", "value"), State("beta", "value"), 
    State("delta", "value"), State("gamma", "value"),
    State("P0", "value"), State("D0", "value"), 
    State("tmax", "value"),
)
def update_graphs(click, a, b, d, g, P0, D0, tmax):
    # 1. Validar Inputs
    is_valid, error_msg = validate_inputs(a, b, d, g, P0, D0, tmax)
    
    if not is_valid:
        # Mostrar tarjeta de error visual
        return html.Div(
            className="graph-card wide",
            style={"border": f"1px solid {C_ERROR}", "textAlign": "center", "padding": "40px"},
            children=[
                html.H3("ERROR DE PARÁMETROS", style={"color": C_ERROR, "fontFamily": "Orbitron"}),
                html.P(error_msg, style={"color": "#fff", "fontSize": "1.2rem"})
            ]
        )

    # 2. Calcular si es válido
    # IMPORTANTE: Convertir a float para evitar errores de numpy con enteros
    a, b, d, g = float(a), float(b), float(d), float(g)
    P0, D0, tmax = float(P0), float(D0), float(tmax)

    sol = simulate_lotka_volterra(a, b, d, g, P0, D0, tmax)
    t, P, D = sol["t"], sol["P"], sol["D"]

    # 3. Retornar Gráficos (Optimizado: reutilizamos 'sol' en graph_orbits)
    return [
        html.Div([dcc.Graph(figure=graph_no_predators(a, P0))], className="graph-card"),
        html.Div([dcc.Graph(figure=graph_no_prey(g, D0))], className="graph-card"),
        html.Div([dcc.Graph(figure=graph_temporal(t, P, D))], className="graph-card wide"),
        # Pasamos parámetros extra a graph_phase para calcular el equilibrio
        html.Div([dcc.Graph(figure=graph_phase(P, D, a, b, d, g))], className="graph-card"),
        # OPTIMIZACIÓN: Pasamos 'sol' para evitar recalcular la simulación principal
        html.Div([dcc.Graph(figure=graph_orbits(a, b, d, g, P0, D0, tmax, main_solution=sol))], className="graph-card"),
    ]

@callback(
    Output("video-status", "children"), Output("video-download", "children"),
    Input("video-button", "n_clicks"),
    State("alpha", "value"), State("beta", "value"), State("delta", "value"), State("gamma", "value"),
    State("P0", "value"), State("D0", "value"), State("tmax", "value"),
    prevent_initial_call=True
)
def generate_video(click, a, b, d, g, P0, D0, tmax):
    if not click: return "", ""

    # 1. Validar también aquí para proteger el backend
    is_valid, error_msg = validate_inputs(a, b, d, g, P0, D0, tmax)
    if not is_valid:
        return html.Div(f"❌ {error_msg}", style={"color": C_ERROR, "fontWeight": "bold"}), ""

    payload = {"alpha": a, "beta": b, "delta": d, "gamma": g, "P0": P0, "D0": D0, "tmax": tmax}
    try:
        r = requests.post(f"{INTERNAL_API_URL}/render-video", json=payload)
        data = r.json()
        if data.get("status") != "ok": return html.Div("❌ ERROR INTERNO", style={"color":C_PINK}), ""
        
        video_name = data["filename"]
        download_link = f"{PUBLIC_DOWNLOAD_ROUTE}/{video_name}"
        
        download_btn = html.A(
            children=[html.I(className="fas fa-download"), " ⬇ DESCARGAR VIDEO"],
            href=download_link, target="_blank", className="btn-download-mega"
        )
        
        success_msg = html.Div(className="success-card", children=[html.Div("✅ RENDERIZADO COMPLETADO", className="success-title")])
        return success_msg, download_btn
    except Exception as e:
        return html.Div(f"⚠️ ERROR DE CONEXIÓN: {str(e)}", style={"color": C_PINK}), ""