import os
from flask import Flask
import google.generativeai as genai
from config import Config
from .extensions import db, migrate
from .api import api_bp
from .frontend import frontend_bp

def create_app(config_class=Config):
    """
    アプリケーションファクトリ関数。
    Flaskアプリケーションインスタンスを作成し、設定、拡張機能、ブループリントを初期化する。
    """
    # 【修正】デフォルトの static フォルダを無効化（frontendブループリントで制御するため）
    app = Flask(__name__, instance_relative_config=True, static_folder=None)
    
    app.config.from_object(config_class)

    # instanceフォルダが存在することを確認
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)

    # Google Gemini APIの設定
    try:
        genai.configure(api_key=app.config['GEMINI_API_KEY'])
    except Exception as e:
        app.logger.critical(f"Failed to configure Gemini API: {e}")
        # 開発中はAPIキーエラーで停止させない（環境変数忘れ対策）
        if not app.debug:
             raise RuntimeError(f"Could not configure Gemini API. Check your API key. Error: {e}")

    # ブループリントの登録
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(frontend_bp)

    return app