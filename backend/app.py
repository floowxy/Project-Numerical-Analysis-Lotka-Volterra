from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from backend.video_tools import save_params, render_video
from backend.validators import validate_params_dict

app = FastAPI()

# Permitir peticiones desde cualquier lado (Dash, IP pública, etc)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
#  RENDERIZAR (POST)
# =====================================================
@app.post("/render-video")
def api_render(params: dict):
    try:
        # 1. Validar parámetros primero
        is_valid, error_msg = validate_params_dict(params)
        if not is_valid:
            return JSONResponse(
                {"status": "error", "msg": error_msg}, 
                status_code=400  # Bad Request
            )
        
        # 2. Guardar JSON
        save_params(
            params["alpha"], params["beta"],
            params["delta"], params["gamma"],
            params["P0"], params["D0"], params["tmax"]
        )
        
        # 3. Renderizar y Mover
        video_name = render_video()
        
        if video_name:
            return {"status": "ok", "filename": video_name}
        else:
            return JSONResponse({"status": "error", "msg": "No se generó el archivo"}, status_code=500)
            
    except Exception as e:
        return JSONResponse({"status": "error", "msg": str(e)}, status_code=500)


# =====================================================
#  DESCARGAR (GET)
# =====================================================
@app.get("/download/{video_name}")
def download(video_name: str):
    
    # Definir ruta absoluta: backend/videos/output/video_name
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "videos", "output", video_name)

    # Verificar existencia
    if os.path.exists(file_path):
        return FileResponse(
            file_path, 
            media_type="video/mp4", 
            filename=video_name
        )
    else:
        print(f"⚠️ Intento de descarga fallido. No existe: {file_path}")
        return JSONResponse({"error": "Archivo no encontrado", "path": file_path}, status_code=404)