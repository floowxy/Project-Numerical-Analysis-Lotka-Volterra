# 🚀 Guía Rápida de Instalación

Esta guía te ayudará a configurar el Sistema de Simulación Lotka-Volterra en tu máquina.

## ✅ Verificación de Prerequisitos

Antes de comenzar, asegúrate de tener:

- [ ] Python 3.9 o superior (3.12+ recomendado)
- [ ] Git instalado
- [ ] Al menos 2GB de espacio libre en disco
- [ ] Conexión a internet para descargar dependencias

Verifica tu versión de Python:

```bash
python3 --version
# Debe mostrar: Python 3.9.x o superior
```

## 📦 Pasos de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/floowxy/Project-Numerical-Analysis-Lotka-Volterra.git
cd Project-Numerical-Analysis-Lotka-Volterra
```

### 2. Crear Entorno Virtual

**IMPORTANTE:** Especifica la versión de Python que deseas usar.

**Linux/macOS:**

```bash
# Primero, verifica qué versiones de Python tienes
python3 --version
python3.13 --version  # Si tienes Python 3.13
python3.12 --version  # Si tienes Python 3.12

# Opción A: Usar Python 3.13 (Recomendado)
python3.13 -m venv .venv

# Opción B: Usar Python 3.12 (También compatible)
python3.12 -m venv .venv

# Opción C: Usar la versión por defecto (asegúrate que sea 3.9+)
python3 -m venv .venv

# Activar el entorno virtual
source .venv/bin/activate

# VERIFICAR la versión dentro del venv
python --version  # Debe mostrar la versión que especificaste
```

**Windows:**

```cmd
# Verificar versión
python --version

# Crear venv con versión específica (si tienes múltiples versiones)
py -3.13 -m venv .venv
# O usa la versión por defecto
python -m venv .venv

# Activar
.venv\Scripts\activate

# Verificar versión dentro del venv
python --version
```

> ⚠️ **Nota Importante:** El venv usará la versión de Python con la que lo crees. Si usas `python3.13 -m venv .venv`, el venv usará Python 3.13 para todas las instalaciones.

Deberías ver `(.venv)` en tu prompt de la terminal.

### 3. Actualizar pip

```bash
pip install --upgrade pip
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto tomará 3-5 minutos dependiendo de tu conexión a internet.

### 5. Verificar Instalación

```bash
python verify_installation.py
```

Deberías ver todas las marcas verdes ✅ si todo está instalado correctamente.

## 🎯 Ejecutar la Aplicación

Necesitas **DOS terminales** ejecutándose simultáneamente:

### Terminal 1 - Iniciar Backend (FastAPI)

```bash
source .venv/bin/activate  # ¡No olvides activar!
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

Deberías ver:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2 - Iniciar Frontend (Dash)

Abre una terminal **nueva**:

```bash
cd Project-Numerical-Analysis-Lotka-Volterra
source .venv/bin/activate  # ¡Activar aquí también!
python app.py
```

Deberías ver:

```
Dash is running on http://0.0.0.0:8050/
```

### 3. Abrir la Aplicación

Abre tu navegador web y ve a:

```
http://localhost:8050
```

## 🎬 Probar Generación de Videos

1. Navega a la página **Simulador**
2. Ajusta los parámetros (o usa los valores por defecto)
3. Haz clic en **"GENERAR VIDEO"**
4. Espera a que el video se renderice (30-60 segundos)
5. Haz clic en **"DESCARGAR VIDEO"**

## 🐛 Problemas Comunes

### Problema: `ModuleNotFoundError`

**Solución:**

```bash
# Asegúrate de estar en el entorno virtual
source .venv/bin/activate
# Verifica qué Python estás usando
which python  # Debe mostrar .venv/bin/python
```

### Problema: `Connection refused` al generar video

**Solución:**

- Asegúrate de que **ambas** terminales estén ejecutándose
- Backend debe estar en el puerto 8000
- Frontend debe estar en el puerto 8050

### Problema: El entorno virtual no se activa en Windows

**Solución:**

```powershell
# Si usas PowerShell, puede que necesites habilitar scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Luego activar
.venv\Scripts\Activate.ps1
```

### Problema: Errores de compatibilidad con Python 3.13

**Solución:**
Ver [PYTHON_VERSION_COMPATIBILITY.md](PYTHON_VERSION_COMPATIBILITY.md) para información detallada.

Los requisitos clave son:

- Manim >= 0.19.0
- ManimPango >= 0.6.0

## 📊 Requisitos del Sistema

### Mínimo

- **CPU**: 2 núcleos
- **RAM**: 4GB
- **Almacenamiento**: 2GB de espacio libre
- **SO**: Linux, macOS, o Windows 10+

### Recomendado (para renderizado rápido de videos)

- **CPU**: 4+ núcleos
- **RAM**: 8GB+
- **GPU**: Compatible con OpenGL 3.3+
- **Almacenamiento**: 5GB+ de espacio libre (para archivos de video)

## 🔧 Opcional: Dependencias del Sistema para Manim

Para mejor calidad de video y rendimiento, instala las dependencias del sistema:

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra
```

### Linux (Arch)

```bash
sudo pacman -S ffmpeg cairo pango texlive-core texlive-bin
```

### macOS

```bash
brew install cairo pango ffmpeg
```

### Windows

1. Descargar FFmpeg desde <https://ffmpeg.org/download.html>
2. Extraer a `C:\ffmpeg`
3. Agregar `C:\ffmpeg\bin` a tu variable de entorno PATH

## 🎓 Próximos Pasos

Una vez que todo esté funcionando:

1. 📖 Lee el [README.md](README.md) completo para documentación detallada
2. 🧪 Experimenta con diferentes parámetros en el simulador
3. 📊 Explora los diferentes tipos de visualización
4. 🎬 Genera tu primer video animado
5. 📄 Revisa los documentos LaTeX incluidos (Informe y Beamer)

## 💡 Consejos Profesionales

1. **Organiza las terminales**: Usa pestañas de terminal o un multiplexor como `tmux`
2. **Usa primero los parámetros por defecto**: Comienza con los valores predeterminados para asegurar que todo funcione
3. **Calidad de video**: Primero prueba con configuración por defecto, luego aumenta la calidad si es necesario
4. **Rendimiento**: Cierra otras aplicaciones al renderizar videos
5. **Respaldos**: El sistema limpia automáticamente videos antiguos, pero guarda los importantes

## 📞 ¿Necesitas Ayuda?

- Revisa [PYTHON_VERSION_COMPATIBILITY.md](PYTHON_VERSION_COMPATIBILITY.md) para problemas de versiones
- Consulta el [README.md](README.md) completo para información detallada
- GitHub Issues: <https://github.com/floowxy/Project-Numerical-Analysis-Lotka-Volterra/issues>

## ✨ ¡Todo Listo

Si ves la aplicación en tu navegador, ¡felicitaciones! 🎉

Ahora estás ejecutando un sistema profesional de simulación Lotka-Volterra con:

- ✅ Interfaz web interactiva
- ✅ Ajuste de parámetros en tiempo real
- ✅ Múltiples tipos de visualización
- ✅ Generación profesional de videos
- ✅ Integración de documentación LaTeX

¡Feliz simulación! 🦊
