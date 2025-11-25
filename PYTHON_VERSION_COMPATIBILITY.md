# Guía de Compatibilidad de Versiones Python

## Versiones de Python Recomendadas

Este proyecto ha sido probado y funciona con:

- ✅ **Python 3.13** (Recomendado) - Última versión con soporte completo
- ✅ **Python 3.12** - Totalmente compatible
- ✅ **Python 3.11** - Totalmente compatible
- ✅ **Python 3.10** - Compatible
- ✅ **Python 3.9** - Versión mínima soportada

## Notas sobre Dependencias Clave

### Manim (Motor de Renderizado de Videos)

- **Versión**: 0.19.0+
- **Soporte Python**: 3.9 - 3.13
- Manim v0.19.0 (lanzado el 20 de enero 2025) fue la primera versión en soportar oficialmente Python 3.13

### ManimPango

- **Versión**: 0.6.0+
- **Soporte Python**: 3.9 - 3.13
- ManimPango v0.6.0 (lanzado el 4 de noviembre 2024) agregó soporte para Python 3.13
- Versiones anteriores (< 0.6.0) NO soportan Python 3.13

### NumPy & SciPy

- **NumPy**: 2.3.5+
- **SciPy**: 1.16.3+
- Ambas tienen soporte completo para Python 3.13

## Problemas Comunes y Soluciones

### Problema 1: Error de Versión de ManimPango

**Error**: `Could not find a version that satisfies the requirement ManimPango>=0.6.2`

**Solución**:

- La última versión disponible es 0.6.1, no 0.6.2
- Usar `ManimPango>=0.6.0` en su lugar

### Problema 2: Incompatibilidad con Python 3.13

**Error**: Varios paquetes mostrando conflictos de versión "Requires-Python"

**Solución**:

- Asegurarse de usar Manim >= 0.19.0
- Asegurarse de usar ManimPango >= 0.6.0
- Estas son las versiones mínimas que soportan Python 3.13

### Problema 3: Entorno Virtual

**Error**: `externally-managed-environment` en Arch Linux

**Solución**:

```bash
# Siempre usar un entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# O
.venv\Scripts\activate     # Windows
```

## Verificación

Para verificar que tu instalación funciona correctamente:

```bash
# Activar tu entorno virtual
source .venv/bin/activate

# Verificar versión de Python
python --version

# Verificar paquetes clave
python -c "import manim; print(f'Manim: {manim.__version__}')"
python -c "import manimpango; print(f'ManimPango instalado')"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import scipy; print(f'SciPy: {scipy.__version__}')"
python -c "import dash; print(f'Dash: {dash.__version__}')"
```

## Dependencias del Sistema (para Manim)

### Linux (Debian/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg libcairo2-dev libpango1.0-dev texlive texlive-latex-extra
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

- Instalar FFmpeg desde <https://ffmpeg.org/download.html>
- Agregar FFmpeg a tu PATH

## Solución de Problemas

### ModuleNotFoundError después de la instalación

```bash
# Asegurarse de estar en el entorno virtual
which python  # Debe mostrar .venv/bin/python

# Reinstalar si es necesario
pip install --force-reinstall -r requirements.txt
```

### Problemas de renderizado con Manim

```bash
# Probar instalación de manim
manim --version

# Intentar renderizar una prueba simple
python -c "from manim import *; print('¡Manim funciona!')"
```

## Migración desde Versiones Antiguas de Python

Si estabas usando Python < 3.9:

1. **Respaldar tu entorno actual**

   ```bash
   pip freeze > old_requirements.txt
   ```

2. **Instalar Python 3.12 o 3.13**
   - Usar el gestor de paquetes de tu sistema o descargar desde python.org

3. **Crear nuevo entorno virtual**

   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```

4. **Instalar desde requirements actualizado**

   ```bash
   pip install -r requirements.txt
   ```

## Notas de Rendimiento

- Python 3.13 incluye mejoras de rendimiento (compilador JIT, mejor GC)
- Espera tiempos de renderizado 5-10% más rápidos con Manim en Python 3.13
- NumPy 2.x es significativamente más rápido que 1.x
- Considera usar aceleración GPU para ModernGL si está disponible

## Última Actualización

- **Fecha**: 2025-11-24
- **Versiones de Python Probadas**: 3.13.7
- **Versión de Manim**: 0.19.0
- **Versión de ManimPango**: 0.6.1
