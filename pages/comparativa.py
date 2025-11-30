import dash
from dash import html, dcc, callback, Input, Output, State
import numpy as np

dash.register_page(
    __name__,
    path="/comparativa",
    name="Comparativa",
    title="Comparativa · Euler vs RK4"
)

# =============================================================================
# FUNCIONES DE SIMULACIÓN
# =============================================================================

def lotka_volterra_rhs(P, D, a, b, d, g):
    """Campo vectorial del sistema Lotka-Volterra."""
    dP = a * P - b * P * D
    dD = d * P * D - g * D
    return dP, dD

def euler_step(P, D, h, a, b, d, g):
    """Un paso del método de Euler."""
    dP, dD = lotka_volterra_rhs(P, D, a, b, d, g)
    P_new = P + h * dP
    D_new = D + h * dD
    return max(P_new, 0), max(D_new, 0)

def rk4_step(P, D, h, a, b, d, g):
    """Un paso del método RK4."""
    k1P, k1D = lotka_volterra_rhs(P, D, a, b, d, g)
    k2P, k2D = lotka_volterra_rhs(P + 0.5*h*k1P, D + 0.5*h*k1D, a, b, d, g)
    k3P, k3D = lotka_volterra_rhs(P + 0.5*h*k2P, D + 0.5*h*k2D, a, b, d, g)
    k4P, k4D = lotka_volterra_rhs(P + h*k3P, D + h*k3D, a, b, d, g)
    
    P_new = P + (h/6) * (k1P + 2*k2P + 2*k3P + k4P)
    D_new = D + (h/6) * (k1D + 2*k2D + 2*k3D + k4D)
    return max(P_new, 0), max(D_new, 0)

def generate_comparison_data(P0, D0, h, n_steps, a, b, d, g):
    """Genera datos comparativos entre Euler y RK4."""
    # Arrays para almacenar resultados
    t = np.arange(0, (n_steps + 1) * h, h)[:n_steps + 1]
    
    euler_P, euler_D = [P0], [D0]
    rk4_P, rk4_D = [P0], [D0]
    
    # Euler
    P_e, D_e = P0, D0
    for _ in range(n_steps):
        P_e, D_e = euler_step(P_e, D_e, h, a, b, d, g)
        euler_P.append(P_e)
        euler_D.append(D_e)
    
    # RK4
    P_r, D_r = P0, D0
    for _ in range(n_steps):
        P_r, D_r = rk4_step(P_r, D_r, h, a, b, d, g)
        rk4_P.append(P_r)
        rk4_D.append(D_r)
    
    return {
        't': t,
        'euler_P': euler_P,
        'euler_D': euler_D,
        'rk4_P': rk4_P,
        'rk4_D': rk4_D
    }

# =============================================================================
# COMPONENTES DE UI
# =============================================================================

def make_iteration_row(i, t, euler_P, euler_D, rk4_P, rk4_D):
    """Crea una fila de la tabla de iteraciones."""
    diff_P = abs(euler_P - rk4_P)
    diff_D = abs(euler_D - rk4_D)
    
    # Determinar clase según la diferencia
    diff_class = ""
    if diff_P > 5 or diff_D > 5:
        diff_class = "diff-high"
    elif diff_P > 1 or diff_D > 1:
        diff_class = "diff-medium"
    else:
        diff_class = "diff-low"
    
    return html.Tr([
        html.Td(f"{i}", className="iter-cell iter-num"),
        html.Td(f"{t:.2f}", className="iter-cell"),
        html.Td(f"{euler_P:.4f}", className="iter-cell euler-cell"),
        html.Td(f"{euler_D:.4f}", className="iter-cell euler-cell"),
        html.Td(f"{rk4_P:.4f}", className="iter-cell rk4-cell"),
        html.Td(f"{rk4_D:.4f}", className="iter-cell rk4-cell"),
        html.Td(f"{diff_P:.4f}", className=f"iter-cell {diff_class}"),
        html.Td(f"{diff_D:.4f}", className=f"iter-cell {diff_class}"),
    ])

def create_comparison_table(data):
    """Crea la tabla de comparación completa."""
    rows = []
    for i in range(len(data['t'])):
        rows.append(make_iteration_row(
            i, 
            data['t'][i],
            data['euler_P'][i], 
            data['euler_D'][i],
            data['rk4_P'][i], 
            data['rk4_D'][i]
        ))
    
    return html.Table(
        className="comparison-table",
        children=[
            html.Thead([
                html.Tr([
                    html.Th("n", className="th-iter", rowSpan=2),
                    html.Th("t", className="th-time", rowSpan=2),
                    html.Th("EULER", className="th-euler", colSpan=2),
                    html.Th("RK4", className="th-rk4", colSpan=2),
                    html.Th("DIFERENCIA", className="th-diff", colSpan=2),
                ]),
                html.Tr([
                    html.Th("P(t)", className="th-sub euler-header"),
                    html.Th("D(t)", className="th-sub euler-header"),
                    html.Th("P(t)", className="th-sub rk4-header"),
                    html.Th("D(t)", className="th-sub rk4-header"),
                    html.Th("|ΔP|", className="th-sub diff-header"),
                    html.Th("|ΔD|", className="th-sub diff-header"),
                ])
            ]),
            html.Tbody(rows)
        ]
    )

def create_method_card(title, formula, error, evaluations, color_class):
    """Crea una tarjeta explicativa del método."""
    return html.Div(
        className=f"method-card {color_class}",
        children=[
            html.H3(title, className="method-title"),
            html.Div([
                html.P("Fórmula:", className="method-label"),
                html.Code(formula, className="method-formula"),
            ]),
            html.Div(className="method-stats", children=[
                html.Div([
                    html.Span("Error Global:", className="stat-label"),
                    html.Span(error, className="stat-value"),
                ]),
                html.Div([
                    html.Span("Evaluaciones/paso:", className="stat-label"),
                    html.Span(evaluations, className="stat-value"),
                ]),
            ])
        ]
    )

# =============================================================================
# LAYOUT PRINCIPAL
# =============================================================================

layout = html.Div(
    className="sim-new-root",
    children=[
        # HEADER
        html.Div(
            className="sim-header",
            children=[
                html.H1("COMPARATIVA NUMÉRICA", className="sim-title"),
                html.P(
                    "EULER vs RUNGE-KUTTA 4 // ANÁLISIS DE PRECISIÓN",
                    className="sim-desc"
                ),
            ]
        ),

        # TARJETAS DE MÉTODOS
        html.Div(
            className="methods-grid",
            children=[
                create_method_card(
                    "MÉTODO DE EULER",
                    "yₙ₊₁ = yₙ + h·f(tₙ, yₙ)",
                    "O(h)",
                    "1",
                    "euler-card"
                ),
                create_method_card(
                    "RUNGE-KUTTA 4",
                    "yₙ₊₁ = yₙ + (h/6)·(k₁ + 2k₂ + 2k₃ + k₄)",
                    "O(h⁴)",
                    "4",
                    "rk4-card"
                ),
            ]
        ),

        # PANEL DE PARÁMETROS
        html.Div(
            className="params-panel-modern",
            children=[
                html.H2("⚙️ PARÁMETROS DE SIMULACIÓN", className="group-title"),
                html.Div(
                    className="params-columns",
                    children=[
                        # Columna izquierda - Condiciones iniciales
                        html.Div([
                            html.H3("Condiciones Iniciales", className="subgroup-title"),
                            html.Div(className="param-item", children=[
                                html.Label("P₀ (Presas iniciales)"),
                                dcc.Input(
                                    id="comp-P0",
                                    type="number",
                                    value=80,
                                    min=1,
                                    max=500,
                                    className="param-input-modern"
                                ),
                            ]),
                            html.Div(className="param-item", children=[
                                html.Label("D₀ (Depredadores iniciales)"),
                                dcc.Input(
                                    id="comp-D0",
                                    type="number",
                                    value=20,
                                    min=1,
                                    max=500,
                                    className="param-input-modern"
                                ),
                            ]),
                            html.Div(className="param-item", children=[
                                html.Label("h (Paso temporal)"),
                                dcc.Input(
                                    id="comp-h",
                                    type="number",
                                    value=0.5,
                                    min=0.01,
                                    max=2.0,
                                    step=0.01,
                                    className="param-input-modern"
                                ),
                            ]),
                            html.Div(className="param-item", children=[
                                html.Label("Número de iteraciones"),
                                dcc.Input(
                                    id="comp-n",
                                    type="number",
                                    value=10,
                                    min=3,
                                    max=50,
                                    className="param-input-modern"
                                ),
                            ]),
                        ]),
                        
                        # Columna derecha - Parámetros del modelo
                        html.Div([
                            html.H3("Parámetros Lotka-Volterra", className="subgroup-title"),
                            html.Div(className="param-item", children=[
                                html.Label("α (Crecimiento presas)"),
                                dcc.Input(
                                    id="comp-alpha",
                                    type="number",
                                    value=0.8,
                                    min=0.01,
                                    max=5.0,
                                    step=0.01,
                                    className="param-input-modern"
                                ),
                            ]),
                            html.Div(className="param-item", children=[
                                html.Label("β (Tasa depredación)"),
                                dcc.Input(
                                    id="comp-beta",
                                    type="number",
                                    value=0.05,
                                    min=0.001,
                                    max=1.0,
                                    step=0.001,
                                    className="param-input-modern"
                                ),
                            ]),
                            html.Div(className="param-item", children=[
                                html.Label("δ (Eficacia reproductiva)"),
                                dcc.Input(
                                    id="comp-delta",
                                    type="number",
                                    value=0.02,
                                    min=0.001,
                                    max=1.0,
                                    step=0.001,
                                    className="param-input-modern"
                                ),
                            ]),
                            html.Div(className="param-item", children=[
                                html.Label("γ (Mortalidad depredador)"),
                                dcc.Input(
                                    id="comp-gamma",
                                    type="number",
                                    value=0.6,
                                    min=0.01,
                                    max=5.0,
                                    step=0.01,
                                    className="param-input-modern"
                                ),
                            ]),
                        ]),
                    ]
                ),
                
                # Botón de calcular
                html.Div(
                    className="action-bar",
                    children=[
                        html.Button(
                            "⚡ CALCULAR COMPARATIVA",
                            id="btn-calculate",
                            className="btn-primary-glow pulse-effect"
                        ),
                    ]
                ),
            ]
        ),

        # CONTENEDOR DE RESULTADOS
        html.Div(
            id="comparison-results",
            className="results-container"
        ),

        # LEYENDA
        html.Div(
            className="legend-box",
            children=[
                html.H4("📊 LEYENDA DE DIFERENCIAS", className="legend-title"),
                html.Div(className="legend-items", children=[
                    html.Div([
                        html.Span(className="legend-dot diff-low"),
                        html.Span("Diferencia < 1 (Excelente)")
                    ]),
                    html.Div([
                        html.Span(className="legend-dot diff-medium"),
                        html.Span("Diferencia 1-5 (Aceptable)")
                    ]),
                    html.Div([
                        html.Span(className="legend-dot diff-high"),
                        html.Span("Diferencia > 5 (Significativa)")
                    ]),
                ])
            ]
        ),

        # BOTÓN VOLVER
        html.Div(
            className="action-bar",
            style={"marginTop": "40px"},
            children=[
                dcc.Link("← VOLVER AL INICIO", href="/", className="btn-secondary-glow"),
            ]
        ),
    ]
)

# =============================================================================
# CALLBACKS
# =============================================================================

@callback(
    Output("comparison-results", "children"),
    Input("btn-calculate", "n_clicks"),
    State("comp-P0", "value"),
    State("comp-D0", "value"),
    State("comp-h", "value"),
    State("comp-n", "value"),
    State("comp-alpha", "value"),
    State("comp-beta", "value"),
    State("comp-delta", "value"),
    State("comp-gamma", "value"),
    prevent_initial_call=False
)
def update_comparison(n_clicks, P0, D0, h, n_steps, alpha, beta, delta, gamma):
    """Actualiza la tabla de comparación."""
    # Valores por defecto si están vacíos
    P0 = P0 or 80
    D0 = D0 or 20
    h = h or 0.5
    n_steps = n_steps or 10
    alpha = alpha or 0.8
    beta = beta or 0.05
    delta = delta or 0.02
    gamma = gamma or 0.6
    
    # Generar datos
    data = generate_comparison_data(P0, D0, h, int(n_steps), alpha, beta, delta, gamma)
    
    # Calcular estadísticas finales
    final_diff_P = abs(data['euler_P'][-1] - data['rk4_P'][-1])
    final_diff_D = abs(data['euler_D'][-1] - data['rk4_D'][-1])
    
    # Crear resumen
    summary = html.Div(
        className="summary-box",
        children=[
            html.H3("📈 RESUMEN DE RESULTADOS", className="summary-title"),
            html.Div(className="summary-grid", children=[
                html.Div(className="summary-item", children=[
                    html.Span("Tiempo final:", className="summary-label"),
                    html.Span(f"t = {data['t'][-1]:.2f}", className="summary-value"),
                ]),
                html.Div(className="summary-item euler-summary", children=[
                    html.Span("Euler final:", className="summary-label"),
                    html.Span(f"P = {data['euler_P'][-1]:.2f}, D = {data['euler_D'][-1]:.2f}", className="summary-value"),
                ]),
                html.Div(className="summary-item rk4-summary", children=[
                    html.Span("RK4 final:", className="summary-label"),
                    html.Span(f"P = {data['rk4_P'][-1]:.2f}, D = {data['rk4_D'][-1]:.2f}", className="summary-value"),
                ]),
                html.Div(className="summary-item diff-summary", children=[
                    html.Span("Diferencia total:", className="summary-label"),
                    html.Span(f"|ΔP| = {final_diff_P:.4f}, |ΔD| = {final_diff_D:.4f}", className="summary-value"),
                ]),
            ])
        ]
    )
    
    return html.Div([
        summary,
        html.Div(className="table-container", children=[
            html.H3("📋 TABLA DE ITERACIONES", className="table-title"),
            create_comparison_table(data)
        ])
    ])