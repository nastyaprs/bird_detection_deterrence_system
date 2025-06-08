from flask import Flask, send_from_directory
from routes.auth import login, register, logout
from routes.dashboard import index, detections, videos, deterrence, toggle_mode, control_view, grant_permission, deny_permission
import threading
import initial_program

app = Flask(__name__)
app.secret_key = "your_super_secret_key"

def run_video_loop():
    initial_program.main()

threading.Thread(target=run_video_loop, daemon=True).start()

@app.route('/saved_videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('saved_videos', filename)

app.add_url_rule("/", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/register", view_func=register, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)

app.add_url_rule("/dashboard", view_func=index)
app.add_url_rule("/detections", view_func=detections)
app.add_url_rule("/videos", view_func=videos)
app.add_url_rule("/deterrence", view_func=deterrence)
app.add_url_rule("/toggle_mode", view_func=toggle_mode, methods=["GET", "POST"])
app.add_url_rule('/control', view_func=control_view)
app.add_url_rule('/grant_permission', view_func=grant_permission, methods=['POST'])
app.add_url_rule('/deny_permission', view_func=deny_permission, methods=['POST'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

