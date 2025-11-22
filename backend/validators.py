"""
Módulo de validación centralizado para parámetros de Lotka-Volterra.
Usado tanto en frontend (Dash) como backend (FastAPI).
"""

# ============================================================
# CONSTANTES DE VALIDACIÓN
# ============================================================

MAX_TIME = 300
MIN_TIME = 5
MAX_POPULATION = 5000

# ============================================================
# FUNCIÓN DE VALIDACIÓN PRINCIPAL
# ============================================================

def validate_inputs(a, b, d, g, P0, D0, tmax):
    """
    Valida los parámetros de entrada para la simulación Lotka-Volterra.
    
    Args:
        a (float): Alpha - Tasa de crecimiento de presas
        b (float): Beta - Tasa de depredación
        d (float): Delta - Eficacia reproductiva del depredador
        g (float): Gamma - Tasa de mortalidad del depredador
        P0 (float): Población inicial de presas
        D0 (float): Población inicial de depredadores
        tmax (float): Tiempo máximo de simulación
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
            - (True, "") si todos los parámetros son válidos
            - (False, "mensaje de error") si hay algún problema
    """
    
    # 1. Validar Vacíos
    if None in [a, b, d, g, P0, D0, tmax]:
        return False, "⛔ ERROR: Todos los campos son obligatorios."

    # 2. Validar Negativos (Imposible biológicamente)
    if any(x < 0 for x in [a, b, d, g, P0, D0, tmax]):
        return False, "⛔ ERROR BIOLÓGICO: No se aceptan valores negativos."

    # 3. Validar Ceros Críticos (Evitar división por cero en el equilibrio)
    if b == 0 or d == 0:
        return False, "⛔ ERROR MATEMÁTICO: Beta y Delta no pueden ser 0 (División por cero)."

    # 4. Validar Límites de Seguridad (Evitar colgar el navegador)
    if tmax > MAX_TIME:
        return False, f"⚠️ ALERTA: Tiempo máximo excedido (Límite: {MAX_TIME})."
    
    if tmax < MIN_TIME:
        return False, f"⚠️ ALERTA: El tiempo es muy corto para simular (Mínimo: {MIN_TIME})."

    if P0 > MAX_POPULATION or D0 > MAX_POPULATION:
        return False, f"⚠️ ALERTA: Poblaciones iniciales demasiado altas (Máximo: {MAX_POPULATION})."

    return True, ""


def validate_params_dict(params: dict):
    """
    Versión para diccionarios (útil para FastAPI).
    
    Args:
        params (dict): Diccionario con claves: alpha, beta, delta, gamma, P0, D0, tmax
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    try:
        return validate_inputs(
            params.get("alpha"),
            params.get("beta"),
            params.get("delta"),
            params.get("gamma"),
            params.get("P0"),
            params.get("D0"),
            params.get("tmax")
        )
    except (KeyError, TypeError) as e:
        return False, f"⛔ ERROR: Parámetros inválidos o faltantes - {str(e)}"
