# Python Version Compatibility Guide

## Recommended Python Versions

This project has been tested and works with:

- ✅ **Python 3.13** (Recommended) - Latest version with full support
- ✅ **Python 3.12** - Fully compatible
- ✅ **Python 3.11** - Fully compatible
- ✅ **Python 3.10** - Compatible
- ✅ **Python 3.9** - Minimum supported version

## Key Dependency Notes

### Manim (Video Rendering Engine)

- **Version**: 0.19.0+
- **Python Support**: 3.9 - 3.13
- Manim v0.19.0 (released January 20, 2025) was the first version to officially support Python 3.13

### ManimPango

- **Version**: 0.6.0+
- **Python Support**: 3.9 - 3.13
- ManimPango v0.6.0 (released November 4, 2024) added Python 3.13 support
- Earlier versions (< 0.6.0) do NOT support Python 3.13

### NumPy & SciPy

- **NumPy**: 2.3.5+
- **SciPy**: 1.16.3+
- Both fully support Python 3.13

## Installation Issues and Solutions

### Issue 1: ManimPango Version Error

**Error**: `Could not find a version that satisfies the requirement ManimPango>=0.6.2`

**Solution**:

- Latest available version is 0.6.1, not 0.6.2
- Use `ManimPango>=0.6.0` instead

### Issue 2: Python 3.13 Compatibility

**Error**: Various packages showing "Requires-Python" version conflicts

**Solution**:

- Ensure you're using Manim >= 0.19.0
- Ensure you're using ManimPango >= 0.6.0
- These are the minimum versions that support Python 3.13

### Issue 3: Virtual Environment

**Error**: `externally-managed-environment` on Arch Linux

**Solution**:

```bash
# Always use a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

## Verification

To verify your installation is working correctly:

```bash
# Activate your virtual environment
source .venv/bin/activate

# Check Python version
python --version

# Verify key packages
python -c "import manim; print(f'Manim: {manim.__version__}')"
python -c "import manimpango; print(f'ManimPango installed')"
python -c "import numpy; print(f'NumPy: {numpy.__version__}')"
python -c "import scipy; print(f'SciPy: {scipy.__version__}')"
python -c "import dash; print(f'Dash: {dash.__version__}')"
```

## System Dependencies (for Manim)

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

- Install FFmpeg from <https://ffmpeg.org/download.html>
- Add FFmpeg to your PATH

## Troubleshooting

### ModuleNotFoundError after installation

```bash
# Ensure you're in the virtual environment
which python  # Should show .venv/bin/python

# Reinstall if needed
pip install --force-reinstall -r requirements.txt
```

### Manim rendering issues

```bash
# Test manim installation
manim --version

# Try rendering a simple test
python -c "from manim import *; print('Manim works!')"
```

## Migration from Older Python Versions

If you were using Python < 3.9:

1. **Backup your current environment**

   ```bash
   pip freeze > old_requirements.txt
   ```

2. **Install Python 3.12 or 3.13**
   - Use your system package manager or download from python.org

3. **Create new virtual environment**

   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install from updated requirements**

   ```bash
   pip install -r requirements.txt
   ```

## Performance Notes

- Python 3.13 includes performance improvements (JIT compiler, better GC)
- Expect 5-10% faster rendering times with Manim on Python 3.13
- NumPy 2.x series is significantly faster than 1.x
- Consider using GPU acceleration for ModernGL if available

## Last Updated

- **Date**: 2025-11-24
- **Python Versions Tested**: 3.13.7
- **Manim Version**: 0.19.0
- **ManimPango Version**: 0.6.1
