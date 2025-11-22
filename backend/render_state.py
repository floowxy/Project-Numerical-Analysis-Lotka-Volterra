import time

render_status = {
    "started": False,
    "progress": 0,
    "start_time": 0,
    "estimated_time": 30   # segundos aproximados
}

def start_render_timer():
    render_status["started"] = True
    render_status["progress"] = 0
    render_status["start_time"] = time.time()

def get_progress():
    if not render_status["started"]:
        return 0

    elapsed = time.time() - render_status["start_time"]
    progress = min(100, int((elapsed / render_status["estimated_time"]) * 100))
    render_status["progress"] = progress
    return progress

def finish_render():
    render_status["progress"] = 100
    render_status["started"] = False
