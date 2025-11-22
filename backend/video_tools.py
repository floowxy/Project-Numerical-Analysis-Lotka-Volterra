import os
import json
import subprocess
import shutil
from datetime import datetime

# =================================================
# CONFIGURACIÓN DE RUTAS (ABSOLUTAS)
# =================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Carpeta backend/
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
OUTPUT_DIR = os.path.join(VIDEOS_DIR, "output")       # Aquí TIENEN que terminar los videos
CONFIG_PATH = os.path.join(VIDEOS_DIR, "lotka_config.json")

# Referencia a tu escena
SCENE_FILE = os.path.join(BASE_DIR, "scenes", "video3.py")
SCENE_CLASS = "VideoLotkaProV2"

# Configuración de limpieza
MAX_VIDEOS_TO_KEEP = 15  # Mantener solo los últimos 15 videos

def save_params(alpha, beta, delta, gamma, P0, D0, tmax):
    """Guarda la configuración para que Manim la lea."""
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    data = {
        "alpha": float(alpha), "beta": float(beta),
        "delta": float(delta), "gamma": float(gamma),
        "P0": float(P0), "D0": float(D0), "tmax": float(tmax)
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)
    return True

def cleanup_old_videos():
    """
    Limpia videos antiguos manteniendo solo los más recientes.
    Mantiene MAX_VIDEOS_TO_KEEP archivos ordenados por fecha de modificación.
    """
    if not os.path.exists(OUTPUT_DIR):
        return
    
    # Obtener todos los archivos .mp4 en output
    video_files = [
        os.path.join(OUTPUT_DIR, f) 
        for f in os.listdir(OUTPUT_DIR) 
        if f.endswith('.mp4')
    ]
    
    # Si hay más videos que el límite
    if len(video_files) > MAX_VIDEOS_TO_KEEP:
        # Ordenar por fecha de modificación (más reciente primero)
        video_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Eliminar los más antiguos
        files_to_delete = video_files[MAX_VIDEOS_TO_KEEP:]
        for old_file in files_to_delete:
            try:
                os.remove(old_file)
                print(f"🗑️ Video antiguo eliminado: {os.path.basename(old_file)}")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {old_file}: {e}")
        
        print(f"✅ Limpieza completada. Videos mantenidos: {MAX_VIDEOS_TO_KEEP}")


def render_video():
    """Renderiza, BUSCA el archivo y lo MUEVE a output."""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Generar nombre único con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"lotka_{timestamp}.mp4"
    
    # 2. Comando Manim
    # -o fuerza el nombre del archivo
    # --media_dir le dice dónde guardar los temporales
    cmd = [
        "manim", "-qh", "--disable_caching",
        SCENE_FILE, SCENE_CLASS,
        "--media_dir", VIDEOS_DIR, 
        "-o", filename
    ]
    
    print(f"🎬 Iniciando Manim: {filename}")
    
    try:
        # Ejecutar y esperar
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error crítico en Manim:\n{e.stderr.decode()}")
        return None

    # ---------------------------------------------------------
    # 🔍 OPERACIÓN DE RESCATE (FIX DOWNLOAD)
    # ---------------------------------------------------------
    # Manim suele guardar en: videos/VideoLotkaProV2/1080p60/archivo.mp4
    # O a veces en: videos/archivo.mp4
    # Vamos a buscarlo donde sea.
    
    found_path = None
    
    # Buscamos recursivamente en toda la carpeta backend/videos
    for root, dirs, files in os.walk(VIDEOS_DIR):
        if filename in files:
            found_path = os.path.join(root, filename)
            break
    
    target_path = os.path.join(OUTPUT_DIR, filename)
    
    if found_path:
        # Si lo encontramos, lo movemos a la carpeta de descarga
        shutil.move(found_path, target_path)
        print(f"✅ Video rescatado y movido a: {target_path}")
        
        # Limpieza automática de videos antiguos
        cleanup_old_videos()
        
        return filename
    else:
        print(f"❌ Manim terminó, pero no encuentro el archivo: {filename}")
        return None