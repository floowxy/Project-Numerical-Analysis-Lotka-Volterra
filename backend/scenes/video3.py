from manim import *
import numpy as np
import json
import os

# ============================================================
# CONFIGURACIÓN DE ESTILO (CYBERPUNK / PRO)
# ============================================================

BG_COLOR = "#0b0e13"
TEXT_MAIN = "#eceff4"
TEXT_SUB = "#81a1c1"

COL_PREY = "#00f2ff"
COL_PRED = "#ff0055"
COL_AXIS = "#2e3440"
COL_GLOW = "#ffffff"
COL_NULL = "#4c566a"
COL_EQ = "#ebcb8b"

# ============================================================
# MOTORES MATEMÁTICOS (RK4)
# ============================================================

def rhs_lotka(t, y, a, b, d, g):
    P, D = y
    return np.array([
        a * P - b * P * D,
        d * P * D - g * D
    ])

def rk4_lotka(a, b, d, g, P0, D0, t0=0, tf=50, h=0.05):
    t = np.arange(t0, tf + h, h)
    Y = np.zeros((len(t), 2))
    Y[0] = [P0, D0]

    for i in range(1, len(t)):
        ti = t[i - 1]
        yi = Y[i - 1]
        k1 = rhs_lotka(ti, yi, a, b, d, g)
        k2 = rhs_lotka(ti + h/2, yi + h*k1/2, a, b, d, g)
        k3 = rhs_lotka(ti + h/2, yi + h*k2/2, a, b, d, g)
        k4 = rhs_lotka(ti + h, yi + h*k3, a, b, d, g)
        Y[i] = yi + (h/6)*(k1 + 2*k2 + 2*k3 + k4)

    return t, Y[:,0], Y[:,1]

# ============================================================
# UTILIDADES VISUALES (EFECTOS)
# ============================================================

def format_number(value):
    """
    Formatea números grandes con K (miles) y M (millones).
    Limita decimales a máximo 2.
    
    Ejemplos:
    - 30000 -> 30K
    - 1000000 -> 1M
    - 1234.5678 -> 1234.57
    - 0.05 -> 0.05
    """
    if abs(value) >= 1_000_000:
        num = value / 1_000_000
        if num == int(num):
            return f"{int(num)}M"
        return f"{num:.2f}".rstrip('0').rstrip('.') + "M"
    elif abs(value) >= 1_000:
        num = value / 1_000
        if num == int(num):
            return f"{int(num)}K"
        return f"{num:.2f}".rstrip('0').rstrip('.') + "K"
    elif value == int(value):
        return str(int(value))
    else:
        # Limitar a 2 decimales
        formatted = f"{value:.2f}"
        # Eliminar ceros finales innecesarios
        if '.' in formatted:
            formatted = formatted.rstrip('0').rstrip('.')
        return formatted

def make_glowing(vmobject, color, width=3, glow_factor=4):
    glow = vmobject.copy()
    glow.set_stroke(color=color, width=width * glow_factor, opacity=0.25)
    vmobject.set_stroke(color=color, width=width, opacity=1)
    vmobject.set_z_index(1)
    return VGroup(glow, vmobject)

# ============================================================
# ESCENA PRINCIPAL
# ============================================================

class VideoLotkaProV2(Scene):

    # ======================================================
    # 🔥 ÚNICO CAMBIO AÑADIDO (NO SE TOCÓ NADA MÁS)
    # ======================================================
    def load_params(self):
        """
        Lee parámetros generados por el backend en lotka_config.json.
        Si no existe → usa tus valores por defecto.
        """
        default = {
            "alpha": 0.8,
            "beta": 0.05,
            "delta": 0.02,
            "gamma": 0.6,
            "P0": 80,
            "D0": 20,
            "tmax": 50
        }

        # Ruta al JSON del backend:
        base = os.path.dirname(os.path.dirname(__file__))      # backend/
        path = os.path.join(base, "videos", "lotka_config.json")

        if not os.path.exists(path):
            return default

        try:
            with open(path, "r") as f:
                data = json.load(f)
            default.update(data)
        except:
            pass

        return default
    # ======================================================

    def construct(self):

        # ---------------------- parámetros dinámicos ----------------------
        params = self.load_params()
        a, b, d, g = params["alpha"], params["beta"], params["delta"], params["gamma"]
        P0, D0, tmax = params["P0"], params["D0"], params["tmax"]

        # Punto de equilibrio
        P_eq = g / d
        D_eq = a / b

        self.camera.background_color = BG_COLOR

        # =====================================================
        # SLIDE 1 — INTRODUCCIÓN (CON ANIMACIONES PREMIUM)
        # =====================================================

        title = Text("MODELO LOTKA-VOLTERRA", font_size=64, weight=BOLD, color=TEXT_MAIN).to_edge(UP, buff=1.5)
        title_glow = make_glowing(title, TEXT_MAIN, width=1, glow_factor=5)

        subtitle = Text("Dinámica de Sistemas No Lineales", font_size=24, color=TEXT_SUB).next_to(title, DOWN)
        line = Line(LEFT*0.1, RIGHT*0.1, color=COL_PREY).next_to(subtitle, DOWN, buff=0.5)

        p_style = {"font_size": 24, "color": TEXT_SUB}
        v_style = {"font_size": 24, "color": TEXT_MAIN, "weight": BOLD}

        params_left = VGroup(
            Text("PARÁMETROS", font_size=20, color=COL_PREY, weight=BOLD),
            VGroup(Text("α (Crecimiento):", **p_style), Text(f"{format_number(a)}", **v_style)).arrange(RIGHT),
            VGroup(Text("β (Depredación):", **p_style), Text(f"{format_number(b)}", **v_style)).arrange(RIGHT),
            VGroup(Text("δ (Reproducción):", **p_style), Text(f"{format_number(d)}", **v_style)).arrange(RIGHT),
            VGroup(Text("γ (Mortalidad):", **p_style), Text(f"{format_number(g)}", **v_style)).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        params_right = VGroup(
            Text("INICIO", font_size=20, color=COL_PRED, weight=BOLD),
            VGroup(Text("P₀ (Presas):", **p_style), Text(f"{format_number(P0)}", **v_style)).arrange(RIGHT),
            VGroup(Text("D₀ (Depredadores):", **p_style), Text(f"{format_number(D0)}", **v_style)).arrange(RIGHT),
            VGroup(Text("Tiempo:", **p_style), Text(f"{format_number(tmax)}", **v_style)).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        params_group = VGroup(params_left, params_right).arrange(RIGHT, buff=2).next_to(line, DOWN, buff=1)

        # 🔥 ANIMACIONES MEJORADAS
        self.play(Write(title, run_time=1.5, rate_func=smooth))
        self.play(FadeIn(subtitle, shift=UP*0.5, scale=0.8), rate_func=rush_from)
        
        # Crear la línea completa directamente
        full_line = Line(LEFT*5, RIGHT*5, color=COL_PREY).next_to(subtitle, DOWN, buff=0.5)
        self.play(GrowFromCenter(full_line), run_time=1)
        
        # Animación en cascada de parámetros
        self.play(
            LaggedStart(
                *[FadeIn(item, shift=DOWN*0.3, scale=0.9) for item in params_group],
                lag_ratio=0.15,
                run_time=2
            )
        )
        self.wait(2)
        
        # Transición suave de salida - ELIMINAR TODO
        self.play(
            FadeOut(title, shift=UP*0.5, scale=1.1),
            FadeOut(subtitle, shift=UP*0.5),
            FadeOut(full_line, scale=0),  # Eliminar la línea correctamente
            FadeOut(params_group, shift=DOWN*0.5, scale=0.9),
            run_time=1
        )

        # =====================================================
        # SLIDE 2 — DINÁMICAS AISLADAS
        # =====================================================

        t2 = Text("DINÁMICAS AISLADAS", font_size=32, color=TEXT_SUB).to_corner(UL)
        self.add(t2)

        ax_config = {"include_numbers": True, "font_size": 16, "color": COL_AXIS, "include_tip": False, "line_to_number_buff": 0.1}

        # Gráfico izquierdo: Crecimiento exponencial de PRESAS (usa alpha real)
        # P(t) = P0 * exp(alpha * t)
        t_max_isolated = min(10, tmax)  # Usar máximo 10 o tmax si es menor
        P_max_preview = P0 * np.exp(a * t_max_isolated)
        
        # Calcular rango Y dinámico
        y_max_L = P_max_preview * 1.2
        y_step_L = max(10, int(y_max_L / 5))
        
        axL = Axes(
            x_range=[0, t_max_isolated, 2], 
            y_range=[0, y_max_L, y_step_L], 
            x_length=5, 
            y_length=3, 
            axis_config=ax_config
        )
        curveL_raw = axL.plot(lambda t: P0 * np.exp(a * t), color=COL_PREY)
        curveL = make_glowing(curveL_raw, COL_PREY)
        labL = Text("Crecimiento Exponencial (Presas)", font_size=20, color=COL_PREY).next_to(axL, UP)
        stat_L = Text(f"P(t) = {format_number(P0)} × e^({format_number(a)}t)", font_size=14, color=TEXT_SUB).next_to(axL, DOWN, buff=0.2)
        groupL = VGroup(labL, axL, curveL, stat_L)

        # Gráfico derecho: Decaimiento exponencial de DEPREDADORES (usa gamma real)
        # D(t) = D0 * exp(-gamma * t)
        D_min_preview = D0 * np.exp(-g * t_max_isolated)
        y_step_R = max(1, int(D0 / 4))
        
        axR = Axes(
            x_range=[0, t_max_isolated, 2], 
            y_range=[0, D0 * 1.2, y_step_R], 
            x_length=5, 
            y_length=3, 
            axis_config=ax_config
        )
        curveR_raw = axR.plot(lambda t: D0 * np.exp(-g * t), color=COL_PRED)
        curveR = make_glowing(curveR_raw, COL_PRED)
        labR = Text("Decaimiento Exponencial (Depredadores)", font_size=20, color=COL_PRED).next_to(axR, UP)
        stat_R = Text(f"D(t) = {format_number(D0)} × e^(-{format_number(g)}t)", font_size=14, color=TEXT_SUB).next_to(axR, DOWN, buff=0.2)
        groupR = VGroup(labR, axR, curveR, stat_R)

        scene_group = VGroup(groupL, groupR).arrange(RIGHT, buff=1.5).shift(DOWN*0.5)

        # 🔥 ANIMACIONES MEJORADAS - Entrada elegante con fade
        self.play(
            LaggedStart(
                FadeIn(groupL, shift=RIGHT*0.5, scale=0.9),
                FadeIn(groupR, shift=LEFT*0.5, scale=0.9),
                lag_ratio=0.2,
                run_time=1.5
            )
        )
        
        # Animación de trazado suave
        self.play(
            Create(curveL_raw, run_time=2.5, rate_func=smooth),
            Create(curveR_raw, run_time=2.5, rate_func=smooth),
        )
        self.wait(1.5)
        
        # Salida suave
        self.play(
            FadeOut(t2, shift=UP*0.3),
            FadeOut(scene_group, scale=0.95),
            run_time=1
        )

        # =====================================================
        # SLIDE 3 — SERIE TEMPORAL
        # =====================================================

        t_arr, P_arr, D_arr = rk4_lotka(a, b, d, g, P0, D0, 0, tmax)
        max_val = max(np.max(P_arr), np.max(D_arr)) * 1.1
        
        # Calcular steps dinámicos para los ejes
        x_step = max(5, int(tmax / 5))
        y_step = max(10, int(max_val / 5))

        t3 = Text("EVOLUCIÓN TEMPORAL", font_size=32, color=TEXT_SUB).to_corner(UL)
        time_label = Text("Tiempo t = ", font_size=24, font="Monospace", color=TEXT_MAIN).to_corner(UR).shift(LEFT*1)
        time_tracker = DecimalNumber(0, num_decimal_places=1, color=COL_PREY, font_size=24).next_to(time_label, RIGHT)

        self.add(t3)

        axT = Axes(
            x_range=[0, tmax, x_step], 
            y_range=[0, max_val, y_step], 
            x_length=11, 
            y_length=4.5, 
            axis_config=ax_config
        ).shift(DOWN*0.5)

        grid = NumberPlane(
            x_range=[0, tmax, 10],
            y_range=[0, max_val, 50],
            x_length=11,
            y_length=4.5,
            background_line_style={"stroke_color": COL_AXIS, "stroke_width": 1, "stroke_opacity": 0.3},
            axis_config={"stroke_opacity": 0}
        ).move_to(axT)

        pts_P = [axT.c2p(t, p) for t, p in zip(t_arr, P_arr)]
        plotP_raw = VMobject().set_points_smoothly(pts_P).set_color(COL_PREY).set_stroke(width=3)
        plotP = make_glowing(plotP_raw, COL_PREY)

        pts_D = [axT.c2p(t, d) for t, d in zip(t_arr, D_arr)]
        plotD_raw = VMobject().set_points_smoothly(pts_D).set_color(COL_PRED).set_stroke(width=3)
        plotD = make_glowing(plotD_raw, COL_PRED)

        scan_line = Line(axT.c2p(0,0), axT.c2p(0, max_val), stroke_width=2, color=WHITE).set_opacity(0.5)
        dotP = Dot(color=COL_PREY).scale(0.8).move_to(pts_P[0])
        dotD = Dot(color=COL_PRED).scale(0.8).move_to(pts_D[0])

        x_lab = Text("Tiempo", font_size=16, color=TEXT_SUB).next_to(axT.x_axis, DOWN)
        y_lab = Text("Población", font_size=16, color=TEXT_SUB).next_to(axT.y_axis, LEFT).rotate(90*DEGREES)

        # 🔥 Entrada con zoom in
        self.play(
            Create(axT, run_time=1.2),
            FadeIn(grid, scale=0.8, run_time=1),
            rate_func=smooth
        )
        self.play(
            Write(x_lab), 
            Write(y_lab),
            LaggedStart(FadeIn(time_label, shift=LEFT*0.5), Write(time_tracker), lag_ratio=0.3),
            run_time=1
        )

        # 🔥 Animación del trazado con efectos
        self.play(
            Create(plotP_raw, run_time=6, rate_func=linear), 
            MoveAlongPath(dotP, plotP_raw, run_time=6, rate_func=linear),
            Create(plotD_raw, run_time=6, rate_func=linear), 
            MoveAlongPath(dotD, plotD_raw, run_time=6, rate_func=linear),
            UpdateFromFunc(scan_line, lambda m: m.move_to(axT.c2p(axT.p2c(dotP.get_center())[0], max_val/2))),
            ChangeDecimalToValue(time_tracker, tmax, run_time=6),
        )
        
        # Efecto de énfasis al finalizar
        self.play(
            Flash(dotP, color=COL_PREY, flash_radius=0.3),
            Flash(dotD, color=COL_PRED, flash_radius=0.3),
            run_time=0.5
        )
        self.wait(0.5)

        # Salida suave con fade y scale
        self.play(
            FadeOut(Group(t3, axT, grid, plotP, plotD, dotP, dotD, scan_line, x_lab, y_lab, time_label, time_tracker), scale=0.95),
            run_time=1
        )

        # =====================================================
        # SLIDE 4 — PLANO DE FASES
        # =====================================================

        t4 = Text("PLANO DE FASES: CICLOS LÍMITE", font_size=32, color=TEXT_SUB).to_corner(UL)
        self.add(t4)

        axPh = Axes(
            x_range=[min(P_arr)*0.7, max(P_arr)*1.3, max(20, int((max(P_arr) - min(P_arr)) / 5))],
            y_range=[min(D_arr)*0.7, max(D_arr)*1.3, max(5, int((max(D_arr) - min(D_arr)) / 5))],
            x_length=7,
            y_length=5,
            axis_config=ax_config
        ).shift(DOWN*0.5)

        labelsPh = VGroup(
            Text("Presas (P)", font_size=18, color=COL_PREY).next_to(axPh.x_axis, DOWN),
            Text("Depredadores (D)", font_size=18, color=COL_PRED).next_to(axPh.y_axis, LEFT).rotate(90*DEGREES)
        )

        pt_eq_coords = axPh.c2p(P_eq, D_eq)

        # Nullclines con labels descriptivos
        v_nullcline = DashedLine(
            start=axPh.c2p(P_eq, axPh.y_range[0]),
            end=axPh.c2p(P_eq, axPh.y_range[1]),
            color=COL_NULL,
            stroke_width=2
        )
        h_nullcline = DashedLine(
            start=axPh.c2p(axPh.x_range[0], D_eq),
            end=axPh.c2p(axPh.x_range[1], D_eq),
            color=COL_NULL,
            stroke_width=2
        )
        
        # Labels para nullclines
        v_null_label = Text("dP/dt = 0", font_size=12, color=COL_NULL).next_to(v_nullcline, RIGHT, buff=0.2)
        h_null_label = Text("dD/dt = 0", font_size=12, color=COL_NULL).next_to(h_nullcline, UP, buff=0.2)

        dot_eq = Dot(point=pt_eq_coords, color=COL_EQ, radius=0.12)
        dot_eq.set_z_index(10)
        label_eq = Text(f"Equilibrio ({format_number(P_eq)}, {format_number(D_eq)})", font_size=14, color=COL_EQ).next_to(dot_eq, UR, buff=0.1)

        pts_phase = [axPh.c2p(p, d) for p, d in zip(P_arr, D_arr)]
        orbit_raw = VMobject().set_points_smoothly(pts_phase).set_color(WHITE).set_stroke(width=3)
        orbit = make_glowing(orbit_raw, COL_PREY)

        dot_orb = Dot(color=WHITE).move_to(pts_phase[0])
        dot_orb.set_shadow(1.5)
        
        # Label para la órbita actual
        orbit_label = Text(f"Órbita: P₀={format_number(P0)}, D₀={format_number(D0)}", 
                          font_size=14, color=WHITE).to_corner(UR, buff=0.5)

        vector_arrow = Arrow(start=ORIGIN, end=RIGHT, color=YELLOW, buff=0, stroke_width=3, max_tip_length_to_length_ratio=0.3)

        def update_arrow(mob):
            coords = axPh.p2c(dot_orb.get_center())
            cur_P, cur_D = coords[0], coords[1]
            derivs = rhs_lotka(0, [cur_P, cur_D], a, b, d, g)
            scale_factor = 0.5
            vector = np.array([derivs[0], derivs[1], 0]) * scale_factor
            mob.put_start_and_end_on(dot_orb.get_center(), dot_orb.get_center() + vector)

        vector_arrow.add_updater(update_arrow)
        trace = TracedPath(dot_orb.get_center, stroke_color=COL_PREY, stroke_width=2, dissipating_time=1.5)

        # 🔥 Entrada con zoom y fade
        self.play(
            Create(axPh, run_time=1.2),
            Write(labelsPh),
            rate_func=smooth
        )
        
        # Nullclines con animación de crecimiento y labels
        self.play(
            GrowFromPoint(v_nullcline, point=axPh.c2p(P_eq, 0)),
            GrowFromPoint(h_nullcline, point=axPh.c2p(0, D_eq)),
            FadeIn(v_null_label, shift=LEFT*0.2),
            FadeIn(h_null_label, shift=DOWN*0.2),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Punto de equilibrio con efecto de pulsación
        self.play(
            GrowFromCenter(dot_eq),
            Write(label_eq),
            run_time=1
        )
        self.play(
            dot_eq.animate.scale(1.5).scale(1/1.5),
            rate_func=there_and_back,
            run_time=0.8
        )
        self.wait(0.3)

        # 🔥 Órbita con trazado dinámico
        self.play(FadeIn(orbit_label, shift=DOWN*0.3))
        self.add(trace, dot_orb, vector_arrow)
        self.play(
            Create(orbit_raw, run_time=6, rate_func=linear), 
            MoveAlongPath(dot_orb, orbit_raw, run_time=6, rate_func=linear)
        )

        vector_arrow.remove_updater(update_arrow)
        
        # Flash final en el ciclo
        self.play(
            Indicate(orbit_raw, color=COL_PREY, scale_factor=1.1),
            run_time=1
        )
        self.wait(0.5)
        
        # Salida con morphing
        self.play(
            FadeOut(Group(t4, axPh, labelsPh, orbit, dot_orb, trace, vector_arrow, v_nullcline, h_nullcline, 
                         dot_eq, label_eq, v_null_label, h_null_label, orbit_label), shift=DOWN*0.5, scale=0.9),
            run_time=1
        )

        # =====================================================
        # SLIDE 5 — ESTABILIDAD ORBITAL
        # =====================================================

        t5 = Text("ESTABILIDAD ORBITAL", font_size=32, color=TEXT_SUB).to_corner(UL)
        self.add(t5)

        # Calcular rangos dinámicos para múltiples órbitas
        max_P_all = max(P_arr) * 1.5
        max_D_all = max(D_arr) * 1.5
        x_step_orbital = max(20, int(max_P_all / 5))
        y_step_orbital = max(10, int(max_D_all / 5))
        
        axM = Axes(
            x_range=[0, max_P_all, x_step_orbital],
            y_range=[0, max_D_all, y_step_orbital],
            x_length=10,
            y_length=5,
            axis_config=ax_config
        ).shift(DOWN*0.5)

        dot_eq_M = Dot(point=axM.c2p(P_eq, D_eq), color=COL_EQ, radius=0.1)
        glow_eq = dot_eq_M.copy().set_color(COL_EQ).set_opacity(0.3).scale(3)
        
        # Labels de ejes
        x_label_M = Text("Presas (P)", font_size=16, color=COL_PREY).next_to(axM.x_axis, DOWN)
        y_label_M = Text("Depredadores (D)", font_size=16, color=COL_PRED).next_to(axM.y_axis, LEFT).rotate(90*DEGREES)

        # Condiciones iniciales con descripciones
        CIs = [
            (P0, D0, COL_PREY, "Actual"),
            (P0*1.5, D0*1.5, "#a3be8c", "+50%"),
            (P0*0.5, D0*0.5, "#ebcb8b", "-50%"),
            (P0*0.3, D0*1.2, "#b48ead", "Variante")
        ]

        orbits = VGroup()
        legend_items = []
        
        for pi, di, col, label in CIs:
            _, p_vals, d_vals = rk4_lotka(a, b, d, g, pi, di, 0, tmax)
            pts = [axM.c2p(p, d) for p, d in zip(p_vals, d_vals)]
            orb = VMobject().set_points_smoothly(pts).set_color(col).set_stroke(width=2, opacity=0.8)
            orbits.add(orb)
            
            # Crear item de leyenda
            legend_line = Line(ORIGIN, RIGHT*0.3, color=col, stroke_width=3)
            legend_text = Text(f"{label}: P₀={format_number(pi)}, D₀={format_number(di)}", 
                             font_size=12, color=col)
            legend_text.next_to(legend_line, RIGHT, buff=0.1)
            legend_item = VGroup(legend_line, legend_text)
            legend_items.append(legend_item)
        
        # Crear leyenda agrupada
        legend = VGroup(*legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend.to_corner(UR, buff=0.3)
        legend.set_z_index(10)

        # 🔥 Entrada con zoom dramático
        self.play(
            Create(axM, run_time=1.2),
            Write(x_label_M),
            Write(y_label_M),
            rate_func=smooth
        )
        
        # Punto de equilibrio con glow pulsante
        self.play(
            FadeIn(glow_eq, scale=0.5),
            GrowFromCenter(dot_eq_M),
            run_time=1
        )
        self.play(
            glow_eq.animate.scale(1.3).scale(1/1.3).set_opacity(0.5),
            rate_func=there_and_back_with_pause,
            run_time=1.5
        )
        
        # 🔥 Órbitas en cascada con efectos
        self.play(
            LaggedStart(
                *[Create(o, run_time=2, rate_func=smooth) for o in orbits], 
                lag_ratio=0.25, 
                run_time=5
            )
        )
        
        # Mostrar leyenda
        self.play(FadeIn(legend, shift=LEFT*0.5), run_time=1)
        
        # Efecto de enfoque en todas las órbitas
        self.play(
            *[Indicate(o, scale_factor=1.05, color=o.get_color()) for o in orbits],
            run_time=1.5
        )
        self.wait(1)

        # Salida con fade elegante
        self.play(
            FadeOut(Group(t5, axM, orbits, dot_eq_M, glow_eq, legend, x_label_M, y_label_M), shift=UP*0.3, scale=1.1),
            run_time=1.2
        )