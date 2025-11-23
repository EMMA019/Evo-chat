import pytest
import os
import sys

# ----------------------------------------------------
# 【重要】以前の sys.path.insert(0, ...) は削除しました。
# Pythonの実行環境に依存してインポートを行います。
# ----------------------------------------------------

# ルートからの絶対参照でインポート
from app import create_app
from app.extensions import db
from app.models import User, ChatMessage
from config import Config
from bot.memory_analyzer import MemoryAnalyzer
from bot.prompts import get_prompt

class TestConfig(Config):
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    GEMINI_API_KEY = 'test-key'
    SECRET_KEY = 'test-secret-key'

@pytest.fixture
def app():
    """Create test application"""
    # config.pyでValueErrorが発生しないように、ここで環境変数をセット
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['GEMINI_API_KEY'] = 'test-key'
    
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_user_creation(app):
    """Test user creation"""
    with app.app_context():
        user = User(session_id='test-session', security_token='test-token')
        db.session.add(user)
        db.session.commit()
        
        # SQLAlchemy 2.0の推奨方法を使用
        retrieved_user = db.session.scalar(db.select(User).filter_by(session_id='test-session'))
        assert retrieved_user is not None
        assert retrieved_user.personality_type == 'Natural'
        assert retrieved_user.affection == 0

def test_chat_message_cleanup(app):
    """Test message cleanup"""
    with app.app_context():
        user = User(session_id='test-session', security_token='test-token')
        db.session.add(user)
        db.session.commit()
        
        # Create test messages
        for i in range(150):
            msg = ChatMessage(user_id=user.id, role='user', content=f'Message {i}')
            db.session.add(msg)
        
        db.session.commit()
        
        # Execute cleanup
        ChatMessage.cleanup_old_messages(user.id, keep_last=100)
        
        # Check remaining message count
        remaining_messages = db.session.scalar(db.select(db.func.count()).select_from(ChatMessage).filter_by(user_id=user.id))
        assert remaining_messages == 100

def test_evolution_threshold_config(app):
    """Test evolution threshold configuration"""
    assert app.config['EVOLUTION_AFFECTION_THRESHOLD'] == 30
    assert app.config['EVOLUTION_SCORE_DIFFERENCE'] == 5

def test_demo_mode_config(app):
    """Test demo mode configuration"""
    assert app.config['DEMO_MODE'] == False
    assert app.config['DEMO_EVOLUTION_THRESHOLD'] == 3
    assert app.config['DEMO_SCORE_DIFFERENCE'] == 2

def test_memory_analyzer_keywords():
    """Test memory analyzer keyword detection"""
    
    analyzer = MemoryAnalyzer()
    memories = ["I feel lonely", "I'm so happy today"]
    result = analyzer.analyze_memories(memories)
    
    # 少なくとも主要なキーが存在し、スコアが0以上であることを確認（分析ロジックの詳細なテストは省略）
    assert 'tsundere' in result
    assert 'yandere' in result
    assert 'kuudere' in result
    assert 'dandere' in result
    assert result['yandere'] >= 0

def test_personality_prompts():
    """Test personality prompt retrieval"""
    
    # Test normal personality prompts
    natural_prompt = get_prompt('Natural')
    tsundere_prompt = get_prompt('Tsundere')
    
    assert 'long_term_memories' in natural_prompt
    assert 'Tsundere' in tsundere_prompt
    
    # Test evolved prompts
    evolved_tsundere = get_prompt('Tsundere', evolved=True)
    assert 'strong' in evolved_tsundere.lower() # 強いツンデレプロンプトが適用されたことを確認

if __name__ == '__main__':
    pytest.main([__file__, '-v'])