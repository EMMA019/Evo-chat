import secrets
from datetime import datetime, timezone
from .extensions import db

class User(db.Model):
    """
    Model for managing user state.
    Identified by session ID, stores AI personality, affection, and personality scores.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), unique=True, nullable=False)
    
    # Security enhancement: token for refresh
    security_token = db.Column(db.String(64), nullable=False, default=lambda: secrets.token_hex(32))
    
    # AI's current personality
    personality_type = db.Column(db.String(50), nullable=False, default='Natural')
    evolved = db.Column(db.Boolean, nullable=False, default=False)

    # Affection level
    affection = db.Column(db.Integer, nullable=False, default=0)

    # Personality scores
    tsundere_score = db.Column(db.Integer, nullable=False, default=0)
    yandere_score = db.Column(db.Integer, nullable=False, default=0)
    kuudere_score = db.Column(db.Integer, nullable=False, default=0)
    dandere_score = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    long_term_memories = db.relationship('LongTermMemory', backref='user', lazy=True, cascade="all, delete-orphan")
    chat_messages = db.relationship('ChatMessage', backref='user', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        """Return user data as dictionary."""
        return {
            "user_id": self.session_id,
            "personality": self.personality_type,
            "affection": self.affection,
            "scores": {
                "tsundere": self.tsundere_score,
                "yandere": self.yandere_score,
                "kuudere": self.kuudere_score,
                "dandere": self.dandere_score
            },
            "long_term_memories": [mem.content for mem in self.long_term_memories]
        }
    
    def refresh_security_token(self):
        """Refresh security token"""
        self.security_token = secrets.token_hex(32)
        return self.security_token

class LongTermMemory(db.Model):
    """
    Model for storing long-term memories associated with users.
    """
    __tablename__ = 'long_term_memories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

class ChatMessage(db.Model):
    """
    Model for storing conversation history.
    """
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'ai'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    @classmethod
    def cleanup_old_messages(cls, user_id, keep_last=100):
        """
        Delete old messages, keeping only the latest N messages.
        
        Args:
            user_id: User ID
            keep_last: Number of recent messages to keep
        """
        try:
            # Identify old messages to delete
            subquery = cls.query.filter_by(user_id=user_id)\
                .order_by(cls.id.desc())\
                .offset(keep_last)\
                .subquery()
            
            # Execute deletion
            db.session.query(cls).filter(
                cls.id.in_(db.select(subquery.c.id))
            ).delete(synchronize_session=False)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            from flask import current_app
            current_app.logger.error(f"Failed to cleanup old messages for user {user_id}: {e}")
            return False