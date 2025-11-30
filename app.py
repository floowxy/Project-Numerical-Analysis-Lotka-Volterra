import dash
from dash import html, dcc
from flask import send_from_directory, abort
import os

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="VOLTERRA · Simulation System",
    assets_folder="assets",
    assets_url_path="/assets",
    requests_pathname_prefix=None,
    routes_pathname_prefix="/",
)

server = app.server
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------
# 1. SERVIR DOCUMENTOS (PDFs)
# ---------------------------------------------------------
DOCS_DIR = os.path.join(BASE_DIR, "docs")

@server.route("/docs/<path:subpath>")
def serve_docs(subpath):
    file_path = os.path.join(DOCS_DIR, subpath)
    if not os.path.isfile(file_path):
        return abort(404)
    return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))

# ---------------------------------------------------------
# 2. SERVIR VIDEOS (Bypass Cloudflare)
# ---------------------------------------------------------
VIDEOS_OUTPUT_DIR = os.path.join(BASE_DIR, "backend", "videos", "output")

@server.route("/dash_download/<path:filename>")
def serve_video_download(filename):
    full_path = os.path.join(VIDEOS_OUTPUT_DIR, filename)
    if not os.path.exists(full_path):
        return abort(404)
    return send_from_directory(
        VIDEOS_OUTPUT_DIR, 
        filename, 
        as_attachment=True, 
        mimetype="video/mp4"
    )

# ---------------------------------------------------------
# NAVEGACIÓN
# ---------------------------------------------------------
def make_nav():
    order = ["Inicio", "Informe", "Beamer", "Simulador","Comparativa"]
    pages = {p["name"]: p for p in dash.page_registry.values()}
    items = []
    for name in order:
        if name in pages:
            items.append(
                dcc.Link(name.upper(), href=pages[name]["path"], className="nav-link")
            )
    return items

# ---------------------------------------------------------
# LAYOUT PRINCIPAL (ESTRUCTURA QUANTUM)
# ---------------------------------------------------------
app.layout = html.Div(
    children=[
        # 1. EFECTO DE PANTALLA CRT (Scanlines)
        html.Div(className="scanlines"),

        # 2. BARRA DE NAVEGACIÓN (Glass)
        html.Nav(
            className="glass-navbar",
            children=[
                html.Div(
                    children=[
                        html.Span("VOL", style={"color": "#00f3ff"}), # Cyan
                        html.Span("TERRA", style={"color": "#bc13fe"}) # Purple
                    ],
                    className="nav-logo"
                ),
                html.Div(
                    children=make_nav(),
                    className="nav-links-container"
                )
            ]
        ),

        # 3. CONTENIDO DE LAS PÁGINAS
        html.Main(
            className="app-main-content",
            children=dash.page_container
        ),

        # 4. FOOTER
        html.Footer(
            className="app-footer",
            children=html.Small("QUANTUM SIMULATION SYSTEM · ONLINE 2025")
        )
    ]
)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=False,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )