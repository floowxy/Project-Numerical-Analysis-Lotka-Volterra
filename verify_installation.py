#!/usr/bin/env python3
"""
Verification script for Lotka-Volterra project dependencies
Tests that all critical dependencies are installed and working correctly
"""

import sys

def test_import(module_name, display_name=None):
    """Test importing a module and return success status"""
    if display_name is None:
        display_name = module_name
    
    try:
        mod = __import__(module_name)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✅ {display_name:20s} - v{version}")
        return True
    except ImportError as e:
        print(f"❌ {display_name:20s} - FAILED: {e}")
        return False

def main():
    """Run all dependency tests"""
    print("=" * 70)
    print("LOTKA-VOLTERRA PROJECT - DEPENDENCY VERIFICATION")
    print("=" * 70)
    
    print(f"\n📍 Python Version: {sys.version}")
    print(f"📍 Python Executable: {sys.executable}\n")
    
    # Core dependencies
    print("🔬 SCIENTIFIC COMPUTING:")
    all_ok = True
    all_ok &= test_import('numpy', 'NumPy')
    all_ok &= test_import('scipy', 'SciPy')
    all_ok &= test_import('sympy', 'SymPy')
    
    # Web framework
    print("\n🌐 WEB FRAMEWORK:")
    all_ok &= test_import('dash', 'Dash')
    all_ok &= test_import('plotly', 'Plotly')
    all_ok &= test_import('flask', 'Flask')
    
    # API Backend
    print("\n🚀 API BACKEND:")
    all_ok &= test_import('fastapi', 'FastAPI')
    all_ok &= test_import('uvicorn', 'Uvicorn')
    all_ok &= test_import('pydantic', 'Pydantic')
    
    # Manim (Video Rendering)
    print("\n🎬 VIDEO RENDERING (MANIM):")
    all_ok &= test_import('manim', 'Manim')
    all_ok &= test_import('manimpango', 'ManimPango')
    all_ok &= test_import('cairo', 'PyCairo')
    all_ok &= test_import('moderngl', 'ModernGL')
    
    # Utilities
    print("\n🛠️  UTILITIES:")
    all_ok &= test_import('requests', 'Requests')
    all_ok &= test_import('tqdm', 'TQDM')
    all_ok &= test_import('rich', 'Rich')
    
    # Summary
    print("\n" + "=" * 70)
    if all_ok:
        print("✅ ALL DEPENDENCIES INSTALLED SUCCESSFULLY!")
        print("\n🎉 Your environment is ready to run the Lotka-Volterra project!")
        print("\n📖 Next steps:")
        print("   1. Start backend:  uvicorn backend.app:app --host 0.0.0.0 --port 8000")
        print("   2. Start frontend: python app.py")
        print("   3. Open browser:   http://localhost:8050")
    else:
        print("❌ SOME DEPENDENCIES FAILED TO INSTALL")
        print("\n🔧 Try reinstalling:")
        print("   pip install --force-reinstall -r requirements.txt")
        return 1
    
    print("=" * 70)
    return 0

if __name__ == "__main__":
    sys.exit(main())
