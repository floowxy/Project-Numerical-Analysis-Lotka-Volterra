from manim import *
import numpy as np
import json
import os

# ============================================================
# CONFIGURACIÓN DE ESTILO (BASE)
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

def make_glowing(vmobject, color, width=3, glow_factor=4):
    glow = vmobject.copy()
    glow.set_stroke(color=color, width=width * glow_factor, opacity=0.25)
    vmobject.set_stroke(color=color, width=width, opacity=1)
    vmobject.set_z_index(1)
    return VGroup(glow, vmobject)

def create_label_with_background(text, font_size=20, color=TEXT_MAIN, bg_color=BG_COLOR, padding=0.2):
    """Crea un label con fondo para evitar superposición"""
    label = Text(text, font_size=font_size, color=color)
    bg = BackgroundRectangle(label, color=bg_color, fill_opacity=0.9, buff=padding)
    return VGroup(bg, label)

# ============================================================
# ESCENA PRINCIPAL
# ============================================================

class VideoLotkaProV2(Scene):

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

        base = os.path.dirname(os.path.dirname(__file__))      
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
        # SLIDE 1 — INTRODUCCIÓN MEJORADA
        # =====================================================

        title = Text("MODELO LOTKA-VOLTERRA", font_size=64, weight=BOLD, color=TEXT_MAIN)
        title.to_edge(UP, buff=1.2)
        
        subtitle = Text("Dinámica de Sistemas No Lineales", font_size=26, color=TEXT_SUB)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        line_start = Line(ORIGIN, ORIGIN, color=COL_PREY, stroke_width=3)
        line_start.next_to(subtitle, DOWN, buff=0.4)
        line_end = Line(LEFT*5.5, RIGHT*5.5, color=COL_PREY, stroke_width=3)
        line_end.move_to(line_start)

        p_style = {"font_size": 22, "color": TEXT_SUB}
        v_style = {"font_size": 24, "color": TEXT_MAIN, "weight": BOLD}

        param_title_left = Text("PARÁMETROS DEL MODELO", font_size=18, color=COL_PREY, weight=BOLD)
        
        params_left = VGroup(
            VGroup(
                Text("α (tasa de crecimiento):", **p_style), 
                Text(f"{a:.2f}", **v_style)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("β (eficiencia depredación):", **p_style), 
                Text(f"{b:.2f}", **v_style)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("δ (eficiencia conversión):", **p_style), 
                Text(f"{d:.2f}", **v_style)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("γ (tasa de mortalidad):", **p_style), 
                Text(f"{g:.2f}", **v_style)
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        left_panel = VGroup(param_title_left, params_left).arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        param_title_right = Text("CONDICIONES INICIALES", font_size=18, color=COL_PRED, weight=BOLD)
        
        params_right = VGroup(
            VGroup(
                Text("P₀ (población presas):", **p_style), 
                Text(f"{int(P0)}", **v_style)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("D₀ (población depredadores):", **p_style), 
                Text(f"{int(D0)}", **v_style)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                Text("Tiempo de simulación:", **p_style), 
                Text(f"{int(tmax)} unidades", **v_style)
            ).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        right_panel = VGroup(param_title_right, params_right).arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        eq_info = VGroup(
            Text("PUNTO DE EQUILIBRIO TEÓRICO", font_size=18, color=COL_EQ, weight=BOLD),
            VGroup(
                Text(f"P* = {P_eq:.2f}", font_size=22, color=TEXT_MAIN),
                Text(f"D* = {D_eq:.2f}", font_size=22, color=TEXT_MAIN)
            ).arrange(RIGHT, buff=1)
        ).arrange(DOWN, buff=0.3)

        params_group = VGroup(left_panel, right_panel).arrange(RIGHT, buff=2)
        params_group.next_to(line_start, DOWN, buff=0.6)
        
        eq_info.next_to(params_group, DOWN, buff=0.5)

        self.play(Write(title, run_time=1.5), rate_func=smooth)
        self.wait(0.3)
        self.play(FadeIn(subtitle, shift=UP*0.3), run_time=0.8)
        self.play(Transform(line_start, line_end), run_time=1.2, rate_func=smooth)
        self.play(
            LaggedStart(
                FadeIn(left_panel, shift=RIGHT*0.5),
                FadeIn(right_panel, shift=LEFT*0.5),
                lag_ratio=0.3
            ),
            run_time=1.5
        )
        self.play(FadeIn(eq_info, shift=UP*0.3), run_time=1)
        self.wait(2.5)
        self.play(FadeOut(Group(title, subtitle, line_start, params_group, eq_info)), run_time=1)

        # =====================================================
        # SLIDE 2 — DINÁMICAS AISLADAS MEJORADAS
        # =====================================================

        t2 = Text("DINÁMICAS AISLADAS", font_size=36, color=TEXT_MAIN, weight=BOLD)
        t2.to_edge(UP, buff=0.8)
        t2_sub = Text("Comportamiento sin interacción", font_size=22, color=TEXT_SUB)
        t2_sub.next_to(t2, DOWN, buff=0.2)

        self.play(Write(t2), FadeIn(t2_sub, shift=UP*0.2))

        ax_config = {
            "include_numbers": True, 
            "font_size": 14, 
            "color": COL_AXIS, 
            "include_tip": True,
            "tip_width": 0.15,
            "tip_height": 0.15
        }

        axL = Axes(
            x_range=[0, 8, 2], 
            y_range=[0, P0*4, 100], 
            x_length=5.5, 
            y_length=3.5, 
            axis_config=ax_config
        )
        
        curveL_raw = axL.plot(lambda t: P0 * np.exp(0.15 * t), color=COL_PREY, stroke_width=3)
        curveL = make_glowing(curveL_raw, COL_PREY)
        
        labL = Text("Crecimiento Exponencial de Presas", font_size=20, color=COL_PREY, weight=BOLD)
        labL.next_to(axL, UP, buff=0.3)
        
        eq_L = MathTex(r"\frac{dP}{dt} = \alpha P", color=TEXT_SUB, font_size=32)
        eq_L.next_to(axL, DOWN, buff=0.3)
        
        x_lab_L = Text("Tiempo (t)", font_size=14, color=TEXT_SUB)
        x_lab_L.next_to(axL.x_axis, DOWN, buff=0.2)
        y_lab_L = Text("Población", font_size=14, color=TEXT_SUB)
        y_lab_L.next_to(axL.y_axis, LEFT, buff=0.2).rotate(90*DEGREES)
        
        groupL = VGroup(labL, axL, x_lab_L, y_lab_L, curveL, eq_L)

        axR = Axes(
            x_range=[0, 8, 2], 
            y_range=[0, D0, 5], 
            x_length=5.5, 
            y_length=3.5, 
            axis_config=ax_config
        )
        
        curveR_raw = axR.plot(lambda t: D0 * np.exp(-0.3 * t), color=COL_PRED, stroke_width=3)
        curveR = make_glowing(curveR_raw, COL_PRED)
        
        labR = Text("Decaimiento de Depredadores", font_size=20, color=COL_PRED, weight=BOLD)
        labR.next_to(axR, UP, buff=0.3)
        
        eq_R = MathTex(r"\frac{dD}{dt} = -\gamma D", color=TEXT_SUB, font_size=32)
        eq_R.next_to(axR, DOWN, buff=0.3)
        
        x_lab_R = Text("Tiempo (t)", font_size=14, color=TEXT_SUB)
        x_lab_R.next_to(axR.x_axis, DOWN, buff=0.2)
        y_lab_R = Text("Población", font_size=14, color=TEXT_SUB)
        y_lab_R.next_to(axR.y_axis, LEFT, buff=0.2).rotate(90*DEGREES)
        
        groupR = VGroup(labR, axR, x_lab_R, y_lab_R, curveR, eq_R)

        scene_group = VGroup(groupL, groupR).arrange(RIGHT, buff=1.2).shift(DOWN*0.3)

        self.play(
            LaggedStart(
                FadeIn(groupL, shift=RIGHT*0.5),
                FadeIn(groupR, shift=LEFT*0.5),
                lag_ratio=0.4
            ),
            run_time=1.5
        )
        self.play(Create(curveL_raw), Create(curveR_raw), run_time=3, rate_func=smooth)
        self.wait(2)
        self.play(FadeOut(Group(t2, t2_sub, scene_group)), run_time=1)

        # =====================================================
        # SLIDE 3 — SERIE TEMPORAL MEJORADA
        # =====================================================

        t_arr, P_arr, D_arr = rk4_lotka(a, b, d, g, P0, D0, 0, tmax)
        max_val = max(np.max(P_arr), np.max(D_arr)) * 1.15

        t3 = Text("EVOLUCIÓN TEMPORAL", font_size=36, color=TEXT_MAIN, weight=BOLD)
        t3.to_edge(UP, buff=0.6)
        
        t3_sub = Text("Interacción presa-depredador en el tiempo", font_size=22, color=TEXT_SUB)
        t3_sub.next_to(t3, DOWN, buff=0.2)

        info_panel = VGroup(
            Text("DATOS EN TIEMPO REAL", font_size=16, color=TEXT_MAIN, weight=BOLD),
            VGroup(
                Text("t = ", font_size=18, color=TEXT_SUB),
                DecimalNumber(0, num_decimal_places=2, color=COL_PREY, font_size=18)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("P(t) = ", font_size=18, color=COL_PREY),
                DecimalNumber(P0, num_decimal_places=2, color=COL_PREY, font_size=18)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("D(t) = ", font_size=18, color=COL_PRED),
                DecimalNumber(D0, num_decimal_places=2, color=COL_PRED, font_size=18)
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        info_bg = BackgroundRectangle(info_panel, color=BG_COLOR, fill_opacity=0.95, buff=0.3)
        info_group = VGroup(info_bg, info_panel).to_corner(UR, buff=0.3)

        time_tracker = info_panel[1][1]
        prey_tracker = info_panel[2][1]
        pred_tracker = info_panel[3][1]

        self.play(Write(t3), FadeIn(t3_sub, shift=UP*0.2))
        self.play(FadeIn(info_group))

        axT = Axes(
            x_range=[0, tmax, 10], 
            y_range=[0, max_val, max_val/5], 
            x_length=11, 
            y_length=5, 
            axis_config={
                "include_numbers": True,
                "font_size": 14,
                "color": COL_AXIS,
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2
            }
        ).shift(DOWN*0.8)

        grid = NumberPlane(
            x_range=[0, tmax, 5],
            y_range=[0, max_val, max_val/10],
            x_length=11,
            y_length=5,
            background_line_style={
                "stroke_color": COL_AXIS, 
                "stroke_width": 0.5, 
                "stroke_opacity": 0.2
            },
            axis_config={"stroke_opacity": 0}
        ).move_to(axT)

        pts_P = [axT.c2p(t, p) for t, p in zip(t_arr, P_arr)]
        plotP_raw = VMobject().set_points_smoothly(pts_P).set_color(COL_PREY).set_stroke(width=4)
        plotP = make_glowing(plotP_raw, COL_PREY)

        pts_D = [axT.c2p(t, d) for t, d in zip(t_arr, D_arr)]
        plotD_raw = VMobject().set_points_smoothly(pts_D).set_color(COL_PRED).set_stroke(width=4)
        plotD = make_glowing(plotD_raw, COL_PRED)

        scan_line = DashedLine(
            axT.c2p(0, 0), 
            axT.c2p(0, max_val), 
            stroke_width=2, 
            color=WHITE,
            dash_length=0.1
        ).set_opacity(0.6)

        dotP = Dot(color=COL_PREY, radius=0.08).move_to(pts_P[0])
        dotP_glow = dotP.copy().scale(2).set_opacity(0.3)
        
        dotD = Dot(color=COL_PRED, radius=0.08).move_to(pts_D[0])
        dotD_glow = dotD.copy().scale(2).set_opacity(0.3)

        x_lab = Text("Tiempo (t)", font_size=16, color=TEXT_SUB)
        x_lab.next_to(axT.x_axis, DOWN, buff=0.2)
        
        y_lab = Text("Población", font_size=16, color=TEXT_SUB)
        y_lab.next_to(axT.y_axis, LEFT, buff=0.2).rotate(90*DEGREES)

        legend = VGroup(
            VGroup(
                Line(ORIGIN, RIGHT*0.4, color=COL_PREY, stroke_width=4),
                Text("Presas (P)", font_size=16, color=COL_PREY)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Line(ORIGIN, RIGHT*0.4, color=COL_PRED, stroke_width=4),
                Text("Depredadores (D)", font_size=16, color=COL_PRED)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        legend_bg = BackgroundRectangle(legend, color=BG_COLOR, fill_opacity=0.9, buff=0.2)
        legend_group = VGroup(legend_bg, legend).to_corner(DR, buff=0.3)

        self.play(Create(axT), FadeIn(grid), Write(x_lab), Write(y_lab), FadeIn(legend_group), run_time=1.5)

        self.add(dotP_glow, dotD_glow)
        
        self.play(
            Create(plotP_raw), 
            MoveAlongPath(dotP, plotP_raw),
            Create(plotD_raw), 
            MoveAlongPath(dotD, plotD_raw),
            dotP_glow.animate.move_to(pts_P[-1]),
            dotD_glow.animate.move_to(pts_D[-1]),
            UpdateFromFunc(scan_line, lambda m: m.move_to(axT.c2p(axT.p2c(dotP.get_center())[0], max_val/2))),
            UpdateFromFunc(time_tracker, lambda m: m.set_value(axT.p2c(dotP.get_center())[0])),
            UpdateFromFunc(prey_tracker, lambda m: m.set_value(axT.p2c(dotP.get_center())[1])),
            UpdateFromFunc(pred_tracker, lambda m: m.set_value(axT.p2c(dotD.get_center())[1])),
            run_time=8,
            rate_func=linear
        )

        self.wait(2)

        self.play(
            FadeOut(Group(t3, t3_sub, axT, grid, plotP, plotD, dotP, dotD, dotP_glow, dotD_glow, scan_line, x_lab, y_lab, info_group, legend_group)),
            run_time=1
        )

        # =====================================================
        # SLIDE 4 — PLANO DE FASES MEJORADO
        # =====================================================

        t4 = Text("PLANO DE FASES", font_size=36, color=TEXT_MAIN, weight=BOLD)
        t4.to_edge(UP, buff=0.6)
        
        t4_sub = Text("Análisis de la dinámica orbital", font_size=22, color=TEXT_SUB)
        t4_sub.next_to(t4, DOWN, buff=0.2)

        self.play(Write(t4), FadeIn(t4_sub, shift=UP*0.2))

        axPh = Axes(
            x_range=[min(P_arr)*0.6, max(P_arr)*1.4, 20],
            y_range=[min(D_arr)*0.6, max(D_arr)*1.4, 10],
            x_length=8,
            y_length=5.5,
            axis_config={
                "include_numbers": True,
                "font_size": 14,
                "color": COL_AXIS,
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2
            }
        ).shift(DOWN*0.5)

        label_x = create_label_with_background("Presas (P)", 18, COL_PREY)
        label_x.next_to(axPh.x_axis, DOWN, buff=0.2)
        
        label_y = create_label_with_background("Depredadores (D)", 18, COL_PRED)
        label_y.next_to(axPh.y_axis, LEFT, buff=0.2).rotate(90*DEGREES)

        v_nullcline = DashedLine(
            start=axPh.c2p(P_eq, axPh.y_range[0]),
            end=axPh.c2p(P_eq, axPh.y_range[1]),
            color=COL_NULL,
            stroke_width=2,
            dash_length=0.15
        )
        
        h_nullcline = DashedLine(
            start=axPh.c2p(axPh.x_range[0], D_eq),
            end=axPh.c2p(axPh.x_range[1], D_eq),
            color=COL_NULL,
            stroke_width=2,
            dash_length=0.15
        )

        v_null_label = create_label_with_background("dP/dt = 0", 14, COL_NULL)
        v_null_label.next_to(v_nullcline.get_top(), DOWN, buff=0.15)
        
        h_null_label = create_label_with_background("dD/dt = 0", 14, COL_NULL)
        h_null_label.next_to(h_nullcline.get_right(), LEFT, buff=0.15)

        pt_eq_coords = axPh.c2p(P_eq, D_eq)
        
        dot_eq = Dot(point=pt_eq_coords, color=COL_EQ, radius=0.12)
        dot_eq.set_z_index(10)
        
        eq_glow = Circle(radius=0.3, color=COL_EQ, stroke_width=2).move_to(pt_eq_coords)
        eq_glow.set_fill(COL_EQ, opacity=0.2)
        
        label_eq = create_label_with_background(f"Equilibrio ({P_eq:.2f}, {D_eq:.2f})", 14, COL_EQ)
        label_eq.next_to(dot_eq, UR, buff=0.15)

        pts_phase = [axPh.c2p(p, d) for p, d in zip(P_arr, D_arr)]
        orbit_raw = VMobject().set_points_smoothly(pts_phase)
        orbit_raw.set_color(WHITE).set_stroke(width=4)
        orbit = make_glowing(orbit_raw, COL_PREY)

        dot_orb = Dot(color=WHITE, radius=0.1).move_to(pts_phase[0])
        dot_orb_glow = dot_orb.copy().scale(2.5).set_opacity(0.4)

        vector_arrow = Arrow(
            start=ORIGIN, 
            end=RIGHT, 
            color=YELLOW, 
            buff=0, 
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25
        )

        def update_arrow(mob):
            coords = axPh.p2c(dot_orb.get_center())
            cur_P, cur_D = coords[0], coords[1]
            derivs = rhs_lotka(0, [cur_P, cur_D], a, b, d, g)
            scale_factor = 0.6
            vector = np.array([derivs[0], derivs[1], 0]) * scale_factor
            if np.linalg.norm(vector) > 0.01:
                mob.put_start_and_end_on(dot_orb.get_center(), dot_orb.get_center() + vector)

        vector_arrow.add_updater(update_arrow)
        
        trace = TracedPath(dot_orb.get_center, stroke_color=COL_PREY, stroke_width=3, dissipating_time=2)

        self.play(Create(axPh), Write(label_x), Write(label_y), run_time=1.5)
        self.play(Create(v_nullcline), Create(h_nullcline), FadeIn(v_null_label), FadeIn(h_null_label), run_time=1.5)
        self.play(FadeIn(eq_glow), FadeIn(dot_eq), Write(label_eq), run_time=1.2)
        self.wait(0.5)

        self.add(trace, dot_orb_glow, dot_orb, vector_arrow)
        
        self.play(
            Create(orbit_raw), 
            MoveAlongPath(dot_orb, orbit_raw),
            dot_orb_glow.animate.move_to(pts_phase[-1]),
            run_time=8, 
            rate_func=linear
        )

        vector_arrow.remove_updater(update_arrow)
        
        self.wait(2)
        
        self.play(
            FadeOut(Group(t4, t4_sub, axPh, label_x, label_y, orbit, dot_orb, dot_orb_glow, trace, vector_arrow, v_nullcline, h_nullcline, dot_eq, eq_glow, label_eq, v_null_label, h_null_label)),
            run_time=1
        )

        # =====================================================
        # SLIDE 5 — ESTABILIDAD ORBITAL MEJORADA
        # =====================================================

        t5 = Text("ESTABILIDAD ORBITAL", font_size=36, color=TEXT_MAIN, weight=BOLD)
        t5.to_edge(UP, buff=0.6)
        
        t5_sub = Text("Múltiples trayectorias convergen al ciclo límite", font_size=22, color=TEXT_SUB)
        t5_sub.next_to(t5, DOWN, buff=0.2)

        self.play(Write(t5), FadeIn(t5_sub, shift=UP*0.2))

        axM = Axes(
            x_range=[0, max(P_arr)*1.5, 50],
            y_range=[0, max(D_arr)*1.5, 25],
            x_length=10,
            y_length=6,
            axis_config={
                "include_numbers": True,
                "font_size": 14,
                "color": COL_AXIS,
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2
            }
        ).shift(DOWN*0.3)

        label_x_m = create_label_with_background("Presas (P)", 18, COL_PREY)
        label_x_m.next_to(axM.x_axis, DOWN, buff=0.2)
        
        label_y_m = create_label_with_background("Depredadores (D)", 18, COL_PRED)
        label_y_m.next_to(axM.y_axis, LEFT, buff=0.2).rotate(90*DEGREES)

        dot_eq_M = Dot(point=axM.c2p(P_eq, D_eq), color=COL_EQ, radius=0.12)
        glow_eq = Circle(radius=0.4, color=COL_EQ, stroke_width=3).move_to(axM.c2p(P_eq, D_eq))
        glow_eq.set_fill(COL_EQ, opacity=0.15)
        
        label_eq_M = create_label_with_background("Equilibrio", 14, COL_EQ)
        label_eq_M.next_to(dot_eq_M, UR, buff=0.15)

        CIs = [
            (P0, D0, COL_PREY, "Inicial"),
            (P0*1.5, D0*1.5, "#a3be8c", "Alto-Alto"),
            (P0*0.5, D0*0.5, "#ebcb8b", "Bajo-Bajo"),
            (P0*0.4, D0*1.3, "#b48ead", "Bajo-Alto"),
            (P0*1.3, D0*0.6, "#d08770", "Alto-Bajo")
        ]

        orbits = VGroup()
        dots_start = VGroup()
        
        for pi, di, col, label_text in CIs:
            _, p_vals, d_vals = rk4_lotka(a, b, d, g, pi, di, 0, tmax*1.2)
            pts = [axM.c2p(p, d) for p, d in zip(p_vals, d_vals)]
            orb = VMobject().set_points_smoothly(pts).set_color(col).set_stroke(width=3, opacity=0.8)
            orbits.add(orb)
            
            dot_start = Dot(point=pts[0], color=col, radius=0.08)
            dots_start.add(dot_start)

        legend_orbits = VGroup()
        for i, (_, _, col, label_text) in enumerate(CIs):
            item = VGroup(
                Circle(radius=0.08, color=col, fill_opacity=1),
                Text(label_text, font_size=14, color=col)
            ).arrange(RIGHT, buff=0.15)
            legend_orbits.add(item)
        
        legend_orbits.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        legend_bg = BackgroundRectangle(legend_orbits, color=BG_COLOR, fill_opacity=0.95, buff=0.25)
        legend_group_m = VGroup(legend_bg, legend_orbits).to_corner(UR, buff=0.3)

        self.play(Create(axM), Write(label_x_m), Write(label_y_m), run_time=1.5)
        self.play(FadeIn(glow_eq), FadeIn(dot_eq_M), Write(label_eq_M), run_time=1)
        self.play(FadeIn(legend_group_m), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(dot) for dot in dots_start], lag_ratio=0.15), run_time=1.5)
        self.play(LaggedStart(*[Create(o) for o in orbits], lag_ratio=0.25), run_time=6)
        self.wait(2.5)

        final_text = VGroup(
            Text("Sistema en Equilibrio Dinámico", font_size=32, color=TEXT_MAIN, weight=BOLD),
            Text("Las poblaciones oscilan periódicamente", font_size=24, color=TEXT_SUB),
            Text("alrededor del punto de equilibrio", font_size=24, color=TEXT_SUB)
        ).arrange(DOWN, buff=0.3)
        
        final_bg = BackgroundRectangle(final_text, color=BG_COLOR, fill_opacity=0.95, buff=0.5)
        final_group = VGroup(final_bg, final_text)

        self.play(FadeOut(Group(dots_start, legend_group_m, label_eq_M)), run_time=0.8)
        self.play(orbits.animate.set_opacity(0.3), FadeIn(final_group), run_time=1.5)
        self.wait(3)
        self.play(FadeOut(Group(t5, t5_sub, axM, label_x_m, label_y_m, orbits, dot_eq_M, glow_eq, final_group)), run_time=1.5)