from flask import render_template, send_from_directory, current_app
import os
from . import frontend_bp

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/static/<path:filename>')
def serve_static(filename):
    static_dir = os.path.join(current_app.root_path, 'frontend', 'static')
    return send_from_directory(static_dir, filename)

@frontend_bp.route('/favicon.ico')
def favicon():
    static_dir = os.path.join(current_app.root_path, 'frontend', 'static')
    return send_from_directory(static_dir, 'favicon.ico')

# 【ここを修正】sw.js の場所を 'static/js' に変更
@frontend_bp.route('/sw.js')
def service_worker():
    # static フォルダの中の 'js' フォルダを参照するように修正
    static_dir = os.path.join(current_app.root_path, 'frontend', 'static', 'js')
    return send_from_directory(static_dir, 'sw.js', mimetype='application/javascript')