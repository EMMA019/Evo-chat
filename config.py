import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# プロジェクトのルートディレクトリの絶対パスを取得
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration management class for the application.
    Reads values from environment variables and raises errors if not set.
    """
    # --- Security ---
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        # Fallback for development if .env is not read correctly
        SECRET_KEY = 'dev-secret-key' 
    
    # Enhanced session settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'  # HTTPS required in production
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

    # --- Database ---
    # Ensure instance folder exists
    instance_path = os.path.join(basedir, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path, exist_ok=True)

    # SQLite configuration for Windows
    # Windowsでは絶対パスを指定する場合、スラッシュは3本ではなく4本(sqlite:////)にするか
    # または os.path.join で生成されたパスをそのまま使う形式が安全です。
    
    db_path = os.path.join(instance_path, 'project.db')
    
    # Windowsパスのバックスラッシュ対策
    if os.name == 'nt':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////' + db_path
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- External APIs ---
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("No GEMINI_API_KEY set. Please set it in .env file.")

    # --- Application Behavior ---
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Evolution parameters (configurable)
    EVOLUTION_AFFECTION_THRESHOLD = int(os.getenv('EVOLUTION_AFFECTION_THRESHOLD', '30'))
    EVOLUTION_SCORE_DIFFERENCE = int(os.getenv('EVOLUTION_SCORE_DIFFERENCE', '5'))
    
    # Message retention limits
    MAX_CHAT_MESSAGES_PER_USER = int(os.getenv('MAX_CHAT_MESSAGES_PER_USER', '100'))
    
    # API limits
    MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', '60'))
    
    # Demo mode settings
    DEMO_MODE = os.getenv('DEMO_MODE', 'False').lower() == 'true'
    DEMO_EVOLUTION_THRESHOLD = int(os.getenv('DEMO_EVOLUTION_THRESHOLD', '3'))
    DEMO_SCORE_DIFFERENCE = int(os.getenv('DEMO_SCORE_DIFFERENCE', '2'))