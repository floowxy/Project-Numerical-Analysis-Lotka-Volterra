# 📦 Guía de Instalación - Lotka-Volterra Numerical Analysis

Esta guía te ayudará a instalar y ejecutar el proyecto en cualquier computadora.

## 📋 Requisitos Previos

- **Python 3.9 - 3.12** (recomendado: 3.11)
  - ⚠️ **Nota**: Python 3.13 puede tener problemas de compatibilidad con algunas dependencias
- **pip** (gestor de paquetes de Python)
- **ffmpeg** (para renderizado de videos con Manim)

## 🔧 Instalación de FFmpeg

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install ffmpeg
```

### Linux (Arch)

```bash
sudo pacman -S ffmpeg
```

### macOS

```bash
brew install ffmpeg
```

### Windows

Descarga desde: <https://ffmpeg.org/download.html>

## 🚀 Instalación del Proyecto

### Paso 1: Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Project-Numerical-Analysis-Lotka-Volterra
```

### Paso 2: Crear entorno virtual

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Actualizar pip

```bash
pip install --upgrade pip
```

### Paso 4: Instalar dependencias

#### Opción A: Instalación estándar

```bash
pip install -r requirements.txt
```

#### Opción B: Si hay errores, instalar por partes

```bash
# 1. Primero las dependencias básicas
pip install dash plotly Flask numpy scipy requests

# 2. Luego FastAPI
pip install fastapi uvicorn[standard]

# 3. Finalmente Manim (puede tardar)
pip install manim pydub

# 4. Utilidades adicionales
pip install tqdm rich pillow
```

## ▶️ Ejecutar el Proyecto

### Backend (FastAPI)

```bash
cd backend
uvicorn app:app --reload --port 8000
```

### Frontend (Dash)

En otra terminal:

```bash
python app.py
```

Luego abre tu navegador en: <http://localhost:8050>

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'cairo'"

**Linux:**

```bash
sudo apt install libcairo2-dev pkg-config python3-dev
pip install pycairo
```

**Arch:**

```bash
sudo pacman -S cairo pkgconf
pip install pycairo
```

### Error: "No module named 'gi'"

```bash
pip install PyGObject
```

### Error con NumPy en Python 3.13

Si estás usando Python 3.13, instala una versión específica:

```bash
pip install numpy==1.26.4
```

### Error: "Microsoft Visual C++ 14.0 is required" (Windows)

Descarga e instala: <https://visualstudio.microsoft.com/visual-cpp-build-tools/>

### Problemas con Manim

Si Manim no se instala correctamente:

```bash
# Desinstalar e intentar de nuevo
pip uninstall manim
pip install manim==0.18.0
```

## 🔄 Actualizar Dependencias

Si necesitas actualizar las dependencias después de cambios:

```bash
pip freeze > requirements_full.txt
```

## 💻 Versiones Recomendadas

- Python: 3.11.x
- pip: 23.0+
- Sistema operativo: Linux (Ubuntu 22.04+), macOS (12+), Windows 10/11

## 📝 Notas Adicionales

- El primer renderizado de video con Manim puede tardar varios minutos
- Asegúrate de tener al menos 2GB de espacio libre en disco
- Se recomienda tener al menos 4GB de RAM disponible

## 🆘 Ayuda

Si continúas teniendo problemas, verifica:

1. Versión de Python correcta: `python --version`
2. Entorno virtual activado (deberías ver `(venv)` en tu terminal)
3. FFmpeg instalado: `ffmpeg -version`
4. Todos los comandos ejecutados desde el directorio raíz del proyecto
