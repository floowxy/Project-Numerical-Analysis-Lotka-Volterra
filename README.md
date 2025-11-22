# 🦊 Proyecto Lotka-Volterra - Sistema de Simulación Quantum

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-3.3.0-00D4FF.svg)](https://dash.plotly.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.121.2-009688.svg)](https://fastapi.tiangolo.com/)
[![Manim](https://img.shields.io/badge/Manim-0.19.0-FF6188.svg)](https://www.manim.community/)

Sistema avanzado de simulación y visualización del modelo depredador-presa de Lotka-Volterra con interfaz web interactiva, tema cyberpunk quantum, y generación de videos animados profesionales.

[![Live Demo](https://img.shields.io/badge/🌐_Demo_Live-proyectovolterra.flowxy.org-00f3ff?style=for-the-badge)](https://proyectovolterra.flowxy.org)

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

---

## 📦 Instalación

### Requisitos Previos

- **Python** 3.8+ (recomendado 3.13)
- **pip** actualizado
- **Sistema operativo**: Linux/macOS/Windows
- **Opcional**: GPU compatible con OpenGL (para Manim)

### Instalación Completa

```bash
# 1. Clonar el repositorio
git clone https://github.com/floowxy/Project-Numerical-Analysis-Lotka-Volterra.git
cd Project-Numerical-Analysis-Lotka-Volterra

# 2. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Instalar todas las dependencias
pip install -r requirements.txt
```

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

## 🌐 Despliegue

### Cloudflare Tunnel (Recomendado)

```bash
# Instalar Cloudflare Tunnel
cloudflared tunnel create lotka-volterra

# Configurar túnel para puerto 8050
cloudflared tunnel route dns lotka-volterra proyectovolterra.flowxy.org

# Ejecutar túnel
cloudflared tunnel run lotka-volterra
```

### Producción (Docker - Futuro)

```dockerfile
# Ejemplo básico
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8050 8000
CMD ["python", "app.py"]
```

---

## 📝 Licencia

Este proyecto fue desarrollado como parte del curso de **Análisis Numérico** en la **Universidad Nacional Mayor de San Marcos (UNMSM)**.

---

## 👥 Autores

**Equipo de Desarrollo:**

- Diego Sotelo
- Alexis Gonzales  
- Paolo Villavicencio
- Álvaro Salazar

**Mantenedor Principal:**

- 📧 Email: <alejsot1234@gmail.com>
- 🐙 GitHub: [@floowxy](https://github.com/floowxy)

---

## 🙏 Agradecimientos

- **3Blue1Brown** - Por crear Manim
- **Comunidad Manim** - Documentación y soporte
- **Plotly/Dash** - Framework web Python
- **FastAPI** - Framework API moderno
- **Dr. Richard Cubas Becerra** - Curso de Análisis Numérico

---

## 📚 Referencias

1. Burden, R. L., & Faires, J. D. (2011). *Análisis Numérico*. Cengage Learning.
2. Chapra, S. C., & Canale, R. P. (2015). *Métodos Numéricos para Ingenieros*. McGraw-Hill.
3. The Manim Community. (2024). *Manim Documentation*. <https://www.manim.community/>

---

<p align="center">
  <b>⚡ QUANTUM SIMULATION SYSTEM · ONLINE 2025 ⚡</b><br>
  <i>Developed with 💙 for UNMSM - Facultad de Ingeniería de Sistemas e Informática</i>
</p>
