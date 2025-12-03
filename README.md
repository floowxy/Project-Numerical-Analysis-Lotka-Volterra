# 🦊 Proyecto Lotka-Volterra - Sistema de Simulación Quantum

[![Python](https://img.shields.io/badge/Python-3.9--3.13-blue.svg)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-3.3.0-00D4FF.svg)](https://dash.plotly.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Manim](https://img.shields.io/badge/Manim-0.19.0+-FF6188.svg)](https://www.manim.community/)

Sistema avanzado de simulación y visualización del modelo depredador-presa de Lotka-Volterra con interfaz web interactiva, tema cyberpunk quantum, y generación de videos animados profesionales.

---

## 📋 Descripción

Este proyecto implementa una simulación numérica completa del sistema de ecuaciones diferenciales de Lotka-Volterra mediante el **método de Runge-Kutta de 4to orden (RK4)**, utilizado para modelar la dinámica poblacional entre especies depredadoras y presas.

### ✨ Características Principales

- 🎮 **Simulador interactivo** con visualización en tiempo real
- 📊 **5 tipos de gráficos** especializados (temporal, plano de fases, órbitas)
- 🎬 **Videos animados HD** con Manim (calidad profesional)
- 📑 **Documentación técnica** integrada (informe LaTeX y presentación Beamer)
- ⚡ **Interfaz premium** con diseño cyberpunk/quantum y efectos glassmorphism
- 🔢 **Formato inteligente** de números (30K, 1M) en animaciones
- 🎯 **Leyendas dinámicas** y labels descriptivos en videos

---

## 🚀 Características Técnicas

### Motor de Simulación (RK4)

- Implementación optimizada de Runge-Kutta de 4to orden
- Error global O(h⁴), error local O(h⁵)
- Paso temporal adaptativo (h = 0.05)
- Validación de no-negatividad biológica
- Optimización sin arrays temporales (+30% velocidad)

### Visualizaciones Interactivas

1. **Crecimiento exponencial** (modelo sin depredador): P(t) = P₀ eᵅᵗ
2. **Decaimiento exponencial** (modelo sin presas): D(t) = D₀ e⁻ᵞᵗ
3. **Dinámica temporal** (evolución completa del sistema)
4. **Plano de fases** (órbitas con punto de equilibrio y nullclines)
5. **Estabilidad orbital** (múltiples condiciones iniciales)

### Sistema de Videos (Manim)

- **5 slides animados** con transiciones profesionales
- **Efectos dinámicos**: FadeIn, GrowFromCenter, LaggedStart, Flash, Indicate
- **Leyendas completas** en todos los gráficos
- **Formateo numérico** automático (K/M para miles/millones)
- **Rangos adaptativos** calculados dinámicamente
- **Calidad**: 1080p HD, 60fps (configurable)

---

## 🛠️ Stack Tecnológico

### Cómputo Científico

- **NumPy** ≥2.3.5 - Operaciones vectoriales y arrays
- **SciPy** ≥1.16.3 - Funciones científicas avanzadas
- **SymPy** ≥1.14.0 - Matemáticas simbólicas

### Framework Web

- **Dash** ≥3.3.0 - Framework web reactivo para Python
- **Flask** ≥3.1.2 - Servidor web subyacente
- **Plotly** ≥6.5.0 - Gráficos interactivos

### Backend API

- **FastAPI** ≥0.121.2 - API REST de alto rendimiento
- **Uvicorn** ≥0.38.0 - Servidor ASGI
- **Pydantic** ≥2.12.4 - Validación de datos

### Renderizado de Video

- **Manim** ≥0.19.0 - Motor de animación matemática
- **Cairo/Pango** ≥0.6.1 - Renderizado de gráficos
- **ModernGL** ≥5.12.0 - Aceleración GPU

### Herramientas de Despliegue

- **Cloudflare Tunnel** - Exposición segura de servidores locales (opcional)

---

## 📦 Instalación

### Requisitos Previos

- **Python** 3.9-3.13 (recomendado 3.12 o 3.13)
  - ⚠️ **Importante**: Para Python 3.13, asegúrate de usar Manim >= 0.19.0 y ManimPango >= 0.6.0
  - Ver [PYTHON_VERSION_COMPATIBILITY.md](PYTHON_VERSION_COMPATIBILITY.md) para más detalles
- **pip** actualizado (25.0+)
- **Sistema operativo**: Linux/macOS/Windows
- **Opcional**: GPU compatible con OpenGL (para renderizado acelerado con Manim)

### Instalación Completa

```bash
### Instalación Completa (Windows / Linux / macOS)

1. Clonar el repositorio
git clone https://github.com/floowxy/Project-Numerical-Analysis-Lotka-Volterra.git
cd Project-Numerical-Analysis-Lotka-Volterra

2. Verificar versión de Python (debe ser 3.9 – 3.13)
python --version          # o: python3 --version / py --version

3. Crear entorno virtual .venv

   # Opción A: usar una versión específica (ej. 3.13 recomendada)
   # Linux / macOS
   python3.13 -m venv .venv
   # Windows
   py -3.13 -m venv .venv

   # Opción B: usar la versión por defecto (asegurarse de que es 3.9+)
   python -m venv .venv    # o: python3 -m venv .venv / py -3 -m venv .venv

4. Activar el entorno virtual

   # Linux / macOS
   source .venv/bin/activate

   # Windows (CMD)
   .venv\Scripts\activate

5. Verificar que estás usando la versión correcta DENTRO del venv
python --version          # Debe mostrar la versión con la que creaste el venv

6. Actualizar pip
python -m pip install --upgrade pip

7. Instalar dependencias del proyecto
pip install -r requirements.txt

8. Verificar instalación de dependencias
python verify_installation.py

9. Lanzar el backend (FastAPI + Uvicorn) ─ TERMINAL 1
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload

10. Lanzar el frontend (Dash) ─ TERMINAL 2
# Abrir otra terminal y repetir activación del entorno:

# Linux / macOS
cd /ruta/al/proyecto/Project-Numerical-Analysis-Lotka-Volterra
source .venv/bin/activate

# Windows (CMD)
cd C:\ruta\al\proyecto\Project-Numerical-Analysis-Lotka-Volterra
.venv\Scripts\activate

python app.py

11. Abrir en el navegador
# Ir a:
#   http://localhost:8050
```

> 📚 **Documentación adicional:**
>
> - 🚀 [QUICK_START.md](QUICK_START.md) - Guía rápida de instalación paso a paso
> - 🐍 [PYTHON_VERSION_COMPATIBILITY.md](PYTHON_VERSION_COMPATIBILITY.md) - Compatibilidad de versiones Python

---

## 🎯 Uso

### Ejecución Local

Necesitas **2 terminales** simultáneas:

**Terminal 1 - Backend (API FastAPI)**

```bash
source .venv/bin/activate
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend (Dash)**

```bash
source .venv/bin/activate
python app.py
```

### Acceder a la Aplicación

Abre tu navegador en: **<http://localhost:8050>**

### Navegación del Sistema

- **🏠 Inicio**: Landing page con acceso a todas las secciones
- **🧪 Simulador**: Laboratorio interactivo con controles de parámetros
- **📄 Informe**: Visualizador del informe técnico (PDF)
- **📊 Beamer**: Visualizador de la presentación (PDF)

---

## 📐 Modelo Matemático

### Sistema de Ecuaciones

El modelo de Lotka-Volterra se define por el sistema de EDOs:

```
dP/dt = αP - βPD    (Ecuación de presas)
dD/dt = δPD - γD    (Ecuación de depredadores)
```

**Variables:**

- **P(t)**: Población de presas en el tiempo t
- **D(t)**: Población de depredadores en el tiempo t

**Parámetros biológicos:**

- **α** (alpha): Tasa de crecimiento de presas
- **β** (beta): Tasa de depredación
- **δ** (delta): Eficacia reproductiva del depredador
- **γ** (gamma): Tasa de mortalidad del depredador

### Punto de Equilibrio

El sistema tiene un punto de equilibrio no trivial:

```
P* = γ/δ
D* = α/β
```

Este punto es un **centro** (órbitas cerradas) en el plano de fases.

### Método Numérico: RK4

El método de Runge-Kutta de 4to orden calcula la evolución mediante:

```
k₁ = f(tₙ, yₙ)
k₂ = f(tₙ + h/2, yₙ + hk₁/2)
k₃ = f(tₙ + h/2, yₙ + hk₂/2)
k₄ = f(tₙ + h, yₙ + hk₃)

yₙ₊₁ = yₙ + (h/6)(k₁ + 2k₂ + 2k₃ + k₄)
```

Donde h = 0.05 (paso temporal optimizado).

---

## 🗂️ Estructura del Proyecto

```
Project-Numerical-Analysis-Lotka-Volterra/
│
├── app.py                      # 🎯 Aplicación principal Dash
├── requirements.txt            # 📦 Dependencias Python
│
├── assets/                     # 🎨 Recursos estáticos
│   ├── base.css               # Estilos principales (tema quantum)
│   └── effects.css            # Efectos y animaciones CSS
│
├── pages/                      # 📄 Páginas de la aplicación
│   ├── inicio.py              # Landing page
│   ├── simulador.py           # Interfaz del simulador
│   ├── informe.py             # Visor de informe PDF
│   └── beamer.py              # Visor de presentación
│
├── backend/                    # ⚙️ Backend y lógica
│   ├── app.py                 # API REST con FastAPI
│   ├── simulation.py          # Motor RK4 optimizado
│   ├── validators.py          # Validación de inputs
│   ├── video_tools.py         # Gestor de renderizado Manim
│   ├── render_state.py        # Control de estado
│   │
│   ├── scenes/                # 🎬 Scripts de Manim
│   │   └── video3.py          # Animación principal (5 slides)
│   │
│   └── videos/                # 📹 Videos generados
│       ├── output/            # MP4 finales
│       └── lotka_config.json  # Parámetros dinámicos
│
└── docs/                       # 📚 Documentación
    ├── informe/               # Informe LaTeX
    └── beamer/                # Presentación Beamer
```

---

## ⚙️ Configuración Avanzada

### Validación de Parámetros

Edita `backend/validators.py`:

```python
# Límites de simulación
MAX_TIME = 500              # Tiempo máximo (unidades de tiempo)
MIN_TIME = 1                # Tiempo mínimo
MAX_POPULATION = 10000      # Población máxima inicial
MIN_POPULATION = 1          # Población mínima inicial

# Límites de coeficientes
MAX_COEFFICIENT = 10.0      # Máximo para α, β, δ, γ
MIN_COEFFICIENT = 0.001     # Mínimo (debe ser > 0)
```

### Limpieza Automática de Videos

Edita `backend/video_tools.py`:

```python
MAX_VIDEOS_TO_KEEP = 15     # Videos más recientes a mantener
```

### Calidad de Video (Manim)

Opciones disponibles:

- `-ql`: Low quality (480p) - Rápido
- `-qm`: Medium quality (720p)
- `-qh`: High quality (1080p) - Por defecto
- `-qk`: 4K (2160p) - Muy lento

---

## 🧪 Optimizaciones Implementadas

### Rendimiento

- ✅ Motor RK4 sin arrays temporales (+30% velocidad)
- ✅ Cálculo de gráficos optimizado (-25% operaciones)
- ✅ Validación centralizada (DRY principle)
- ✅ Limpieza automática de archivos temporales

### Experiencia de Usuario

- ✅ Formato inteligente de números (30K, 1M)
- ✅ Rangos de ejes adaptativos
- ✅ Leyendas descriptivas automáticas
- ✅ Validación en tiempo real
- ✅ Mensajes de error informativos

### Visual

- ✅ Tema cyberpunk/quantum con CSS3
- ✅ Glassmorphism effects
- ✅ Animaciones suaves (cubic-bezier)
- ✅ Responsive design
- ✅ Gráficos interactivos (Plotly)

---

## 🎨 Paleta de Colores

El diseño utiliza una paleta neón sobre fondo oscuro:

```css
--neon-cyan:    #00f3ff  /* Elementos primarios */
--neon-pink:    #ff0055  /* Elementos secundarios */
--neon-purple:  #bc13fe  /* Acentos */
--neon-green:   #00ff9d  /* Estados exitosos */
--bg-dark:      #0b0e13  /* Fondo principal */
```

---

## 📝 Licencia

Este proyecto fue desarrollado como parte del curso de **Análisis Numérico** en la **Universidad Nacional Mayor de San Marcos (UNMSM)**.

---

## 👤 Autor

**floowxy**

- 📧 Email: <alejsot1234@gmail.com>
- 🐙 GitHub: [@floowxy](https://github.com/floowxy)

---

**⚡ QUANTUM SIMULATION SYSTEM · ONLINE 2025 ⚡**
