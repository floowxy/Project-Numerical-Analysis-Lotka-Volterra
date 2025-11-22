import numpy as np

# ============================================================
#   PARÁMETROS POR DEFECTO
# ============================================================

DEFAULT_PARAMS = {
    "alpha": 0.8,
    "beta": 0.05,
    "delta": 0.02,
    "gamma": 0.6,
    "P0": 80.0,
    "D0": 20.0,
    "t_max": 50.0,
    "dt": 0.05,
}

# ============================================================
#   1. CAMPO DEL SISTEMA (OPTIMIZADO)
# ============================================================

def lotka_volterra_rhs(P, D, a, b, d, g):
    """Campo vectorial del sistema LV, optimizado."""
    dP = a * P - b * P * D
    dD = d * P * D - g * D
    return dP, dD

# ============================================================
#   2. INTEGRADOR RK4 ULTRA OPTIMIZADO
# ============================================================

def rk4_step(P, D, h, a, b, d, g):
    """Un paso RK4 optimizado sin arreglos temporales."""
    k1P, k1D = lotka_volterra_rhs(P, D, a, b, d, g)
    k2P, k2D = lotka_volterra_rhs(P + 0.5*h*k1P, D + 0.5*h*k1D, a, b, d, g)
    k3P, k3D = lotka_volterra_rhs(P + 0.5*h*k2P, D + 0.5*h*k2D, a, b, d, g)
    k4P, k4D = lotka_volterra_rhs(P + h*k3P, D + h*k3D, a, b, d, g)

    P_new = P + (h/6)*(k1P + 2*k2P + 2*k3P + k4P)
    D_new = D + (h/6)*(k1D + 2*k2D + 2*k3D + k4D)

    return max(P_new, 0), max(D_new, 0)

# ============================================================
#   3. SIMULACIÓN PRINCIPAL (RK4)
# ============================================================

def simulate_lotka_volterra(
    alpha=DEFAULT_PARAMS["alpha"],
    beta=DEFAULT_PARAMS["beta"],
    delta=DEFAULT_PARAMS["delta"],
    gamma=DEFAULT_PARAMS["gamma"],
    P0=DEFAULT_PARAMS["P0"],
    D0=DEFAULT_PARAMS["D0"],
    t_max=DEFAULT_PARAMS["t_max"],
    dt=DEFAULT_PARAMS["dt"],
):
    """
    Simulación científica clásica usando RK4 optimizado.
    Ideal para dashboards (rápido + preciso).
    """

    n = int(t_max / dt) + 1
    t = np.linspace(0, t_max, n)

    P = np.zeros(n)
    D = np.zeros(n)
    P[0], D[0] = P0, D0

    a, b, d, g = alpha, beta, delta, gamma
    Pi, Di = P0, D0

    for k in range(1, n):
        Pi, Di = rk4_step(Pi, Di, dt, a, b, d, g)
        P[k], D[k] = Pi, Di

    return {"t": t, "P": P, "D": D}
