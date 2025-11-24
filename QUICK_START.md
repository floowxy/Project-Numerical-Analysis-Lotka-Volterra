# 🚀 Quick Start Installation Guide

This guide will help you set up the Lotka-Volterra Simulation System on your machine.

## ✅ Prerequisites Check

Before starting, make sure you have:

- [ ] Python 3.9 or higher (3.12+ recommended)
- [ ] Git installed
- [ ] At least 2GB of free disk space
- [ ] Internet connection for downloading dependencies

Check your Python version:

```bash
python3 --version
# Should show: Python 3.9.x or higher
```

## 📦 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/floowxy/Project-Numerical-Analysis-Lotka-Volterra.git
cd Project-Numerical-Analysis-Lotka-Volterra
```

### 2. Create Virtual Environment

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

You should see `(.venv)` in your terminal prompt.

### 3. Upgrade pip

```bash
pip install --upgrade pip
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will take 3-5 minutes depending on your internet connection.

### 5. Verify Installation

```bash
python verify_installation.py
```

You should see all green checkmarks ✅ if everything is installed correctly.

## 🎯 Running the Application

You need **TWO terminals** running simultaneously:

### Terminal 1 - Start Backend (FastAPI)

```bash
source .venv/bin/activate  # Don't forget to activate!
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Terminal 2 - Start Frontend (Dash)

Open a **new** terminal:

```bash
cd Project-Numerical-Analysis-Lotka-Volterra
source .venv/bin/activate  # Activate here too!
python app.py
```

You should see:

```
Dash is running on http://0.0.0.0:8050/
```

### 3. Open the Application

Open your web browser and go to:

```
http://localhost:8050
```

## 🎬 Testing Video Generation

1. Navigate to **Simulador** page
2. Adjust the parameters (or use defaults)
3. Click **"GENERAR VIDEO"**
4. Wait for the video to render (30-60 seconds)
5. Click **"DESCARGAR VIDEO"**

## 🐛 Common Issues

### Issue: `ModuleNotFoundError`

**Solution:**

```bash
# Make sure you're in the virtual environment
source .venv/bin/activate
# Verify which Python you're using
which python  # Should show .venv/bin/python
```

### Issue: `Connection refused` when generating video

**Solution:**

- Make sure **both** terminals are running
- Backend should be on port 8000
- Frontend should be on port 8050

### Issue: Virtual environment not activating on Windows

**Solution:**

```powershell
# If using PowerShell, you might need to enable scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then activate
.venv\Scripts\Activate.ps1
```

### Issue: Python 3.13 compatibility errors

**Solution:**
See [PYTHON_VERSION_COMPATIBILITY.md](PYTHON_VERSION_COMPATIBILITY.md) for detailed information.

The key requirements are:

- Manim >= 0.19.0
- ManimPango >= 0.6.0

## 📊 System Requirements

### Minimum

- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 2GB free space
- **OS**: Linux, macOS, or Windows 10+

### Recommended (for fast video rendering)

- **CPU**: 4+ cores
- **RAM**: 8GB+
- **GPU**: OpenGL 3.3+ compatible
- **Storage**: 5GB+ free space (for video files)

## 🔧 Optional: System Dependencies for Manim

For better video quality and performance, install system dependencies:

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

1. Download FFmpeg from <https://ffmpeg.org/download.html>
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your PATH environment variable

## 🎓 Next Steps

Once everything is running:

1. 📖 Read the full [README.md](README.md) for detailed documentation
2. 🧪 Experiment with different parameters in the simulator
3. 📊 Explore the different visualization types
4. 🎬 Generate your first animated video
5. 📄 Check out the included LaTeX documents (Informe and Beamer)

## 💡 Pro Tips

1. **Keep terminals organized**: Use terminal tabs or a terminal multiplexer like `tmux`
2. **Use default parameters first**: Start with the default values to ensure everything works
3. **Video quality**: First test with default settings, then increase quality if needed
4. **Performance**: Close other applications when rendering videos
5. **Backups**: The system auto-cleans old videos, but save important ones

## 📞 Need Help?

- Check [PYTHON_VERSION_COMPATIBILITY.md](PYTHON_VERSION_COMPATIBILITY.md) for version issues
- Review the full [README.md](README.md) for detailed information
- GitHub Issues: <https://github.com/floowxy/Project-Numerical-Analysis-Lotka-Volterra/issues>

## ✨ You're All Set

If you see the application in your browser, congratulations! 🎉

You're now running a professional Lotka-Volterra simulation system with:

- ✅ Interactive web interface
- ✅ Real-time parameter adjustment
- ✅ Multiple visualization types
- ✅ Professional video generation
- ✅ LaTeX documentation integration

Happy simulating! 🦊
