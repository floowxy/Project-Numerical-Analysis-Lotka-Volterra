# 🦊 Proyecto Lotka-Volterra - Sistema de Simulación Quantum

Sistema avanzado de simulación y visualización del modelo depredador-presa de Lotka-Volterra con interfaz web interactiva y generación de videos animados.

## 📋 Descripción

Este proyecto implementa una simulación completa del sistema de ecuaciones diferenciales de Lotka-Volterra, utilizado para modelar la dinámica poblacional entre especies depredadoras y presas. Incluye:

- 🎮 **Simulador interactivo** con visualización en tiempo real
- 📊 **Múltiples gráficos** (temporal, plano de fases, órbitas)
- 🎬 **Generación de videos** animados con Manim
- 📑 **Documentación técnica** integrada (informe y presentación)
- ⚡ **Interfaz moderna** con diseño quantum/neon

## 🚀 Características

### Simulador

- Ajuste de parámetros biológicos (α, β, δ, γ)
- Condiciones iniciales personalizables
- Validación robusta de inputs
- Visualización de punto de equilibrio
- Análisis de estabilidad orbital

### Visualizaciones

1. **Crecimiento exponencial** (sin depredador)
2. **Decaimiento** (sin presas)
3. **Dinámica temporal** (evolución de poblaciones)
4. **Plano de fases** (con punto de equilibrio)
5. **Órbitas múltiples** (análisis de estabilidad)

### Renderizado de Videos

- Generación automática con Manim
- Calidad HD (1080p)
- Descarga directa desde la interfaz
- Limpieza automática de archivos antiguos

## 🛠️ Tecnologías

- **Frontend**: Dash (Plotly) + HTML/CSS
- **Backend**: FastAPI + Uvicorn
- **Simulación**: NumPy + SciPy (método RK4)
- **Animación**: Manim Community
- **Servidor**: Flask (integrado con Dash)

## 📦 Instalación

### Requisitos Previos

- Python 3.8+
- pip
- Sistema operativo: Linux/macOS/Windows

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/TU_USUARIO/Project-Numerical-Analysis-Lotka-Volterra.git
cd Project-Numerical-Analysis-Lotka-Volterra
```

2. **Crear entorno virtual**

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Iniciar el Sistema

Necesitas **2 terminales** abiertas:

**Terminal 1 - Backend (API de videos)**

```bash
source .venv/bin/activate
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Aplicación Principal**

```bash
source .venv/bin/activate
python app.py
```

### Acceder a la Aplicación

Abre tu navegador en: **<http://localhost:8050>**

### Navegación

- **Inicio**: Página principal con acceso a todas las secciones
- **Simulador**: Laboratorio interactivo de simulación
- **Informe**: Documentación técnica en PDF
- **Beamer**: Presentación del proyecto

## 📐 Modelo Matemático

El sistema de Lotka-Volterra se define por:

```
dP/dt = αP - βPD
dD/dt = δPD - γD
```

Donde:

- **P**: Población de presas
- **D**: Población de depredadores
- **α**: Tasa de crecimiento de presas
- **β**: Tasa de depredación
- **δ**: Eficacia reproductiva del depredador
- **γ**: Tasa de mortalidad del depredador

### Punto de Equilibrio

```
P* = γ/δ
D* = α/β
```

## 🗂️ Estructura del Proyecto

```
Project-Numerical-Analysis-Lotka-Volterra/
├── app.py                  # Aplicación principal Dash
├── requirements.txt        # Dependencias
├── assets/                 # CSS y recursos estáticos
├── pages/                  # Páginas de la aplicación
│   ├── inicio.py
│   ├── simulador.py
│   ├── informe.py
│   └── beamer.py
├── backend/               # Backend FastAPI y lógica
│   ├── app.py            # API FastAPI
│   ├── simulation.py     # Motor de simulación RK4
│   ├── validators.py     # Validación centralizada
│   ├── video_tools.py    # Renderizado de videos
│   ├── scenes/           # Escenas de Manim
│   └── videos/           # Videos generados
├── docs/                 # Documentación PDF
└── media/                # Recursos multimedia
```

## ⚙️ Configuración

### Límites de Validación

Edita `backend/validators.py`:

```python
MAX_TIME = 300          # Tiempo máximo de simulación
MIN_TIME = 5            # Tiempo mínimo
MAX_POPULATION = 5000   # Población máxima inicial
```

### Limpieza de Videos

Edita `backend/video_tools.py`:

```python
MAX_VIDEOS_TO_KEEP = 15  # Número de videos a mantener
```

## 🧪 Optimizaciones Implementadas

- ✅ Validación centralizada (DRY)
- ✅ Limpieza automática de videos antiguos
- ✅ Validación en backend con códigos HTTP apropiados
- ✅ Optimización de gráficos (25% menos cálculos)
- ✅ Método RK4 optimizado para simulación

## 📝 Licencia

Este proyecto fue desarrollado como parte de un curso de Análisis Numérico.

## 👤 Autor

**floowxy**

- Email: <alejsot1234@gmail.com>
- GitHub: [@TU_USUARIO](https://github.com/TU_USUARIO)

## 🙏 Agradecimientos

- Comunidad de Manim
- Plotly/Dash
- FastAPI
- Curso de Análisis Numérico

---

**⚡ QUANTUM SIMULATION SYSTEM · ONLINE 2025**
