import secrets
import time
import datetime
from flask import request, jsonify, session, current_app
import google.generativeai as genai

from . import api_bp
from app.models import User, ChatMessage, LongTermMemory
from app.extensions import db
from bot import engine, evolution, memory, prompts
from bot.events import EventManager

# Rate limiting cache
request_timestamps = {}

def check_rate_limit(identifier, max_requests, window_seconds=60):
    now = time.time()
    if identifier not in request_timestamps:
        request_timestamps[identifier] = []
    request_timestamps[identifier] = [ts for ts in request_timestamps[identifier] if now - ts < window_seconds]
    if len(request_timestamps[identifier]) >= max_requests:
        return False
    request_timestamps[identifier].append(now)
    return True

def get_or_create_user() -> User:
    if 'session_id' not in session or 'security_token' not in session:
        session['session_id'] = secrets.token_hex(16)
        session['security_token'] = secrets.token_hex(32)
        session.permanent = True
    
    user = db.session.scalar(db.select(User).where(User.session_id == session['session_id']))
    
    if not user:
        user = User(session_id=session['session_id'], security_token=session['security_token'])
        db.session.add(user)
        db.session.commit()
        current_app.logger.info(f"New user created: {user.session_id}")
    else:
        if user.security_token != session['security_token']:
            new_token = user.refresh_security_token()
            session['security_token'] = new_token
            db.session.commit()
    return user

@api_bp.route('/chat', methods=['POST'])
def chat():
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip, current_app.config['MAX_REQUESTS_PER_MINUTE']):
        return jsonify({"error": "Rate limit exceeded"}), 429

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400

    user_message = data['message'].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        user = get_or_create_user()

        # Demo command
        if user_message == '#evolve_now' and current_app.config.get('DEMO_MODE'):
            user.affection = 100
            user.tsundere_score = 50
            evolution_triggered, new_personality = evolution.check_evolution(user)
            return jsonify({
                "ai_response": "⚡ Demo evolution triggered!",
                "evolution_triggered": evolution_triggered,
                "new_personality": new_personality,
                "current_status": user.to_dict()
            })

        cleaned_msg, _ = memory.handle_long_term_memory(db.session, user, user_message)
        
        user_msg = ChatMessage(user_id=user.id, role='user', content=cleaned_msg)
        db.session.add(user_msg)

        context = memory.get_context(user)
        event_manager = EventManager()
        current_themes = event_manager.get_current_themes()
        
        # 【修正】親愛度(affection)をプロンプトに渡す
        system_prompt = prompts.get_event_enhanced_prompt(
            user.personality_type, 
            user.evolved, 
            themes=current_themes,
            affection=user.affection  # 追加
        ).format(
            long_term_memories=context['long_term_memories'],
            time_context=context['time_context']
        )

        model = genai.GenerativeModel('gemini-2.5-flash')
        
        ai_response_content, analysis_result = engine.generate_response_with_analysis(
            model, system_prompt, context['chat_history'], cleaned_msg
        )
        
        if not ai_response_content.strip():
            ai_response_content = "..."

        ai_msg = ChatMessage(user_id=user.id, role='ai', content=ai_response_content)
        db.session.add(ai_msg)

        evolution.update_scores_and_affection(user, analysis_result, context['chat_history'])
        evolution_triggered, new_personality = evolution.check_evolution(user)
        
        ChatMessage.cleanup_old_messages(user.id, keep_last=100)
        db.session.commit()

        return jsonify({
            "ai_response": ai_response_content,
            "evolution_triggered": evolution_triggered,
            "new_personality": new_personality,
            "current_status": user.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Chat error: {e}", exc_info=True)
        return jsonify({"error": "Internal error"}), 500

@api_bp.route('/status', methods=['GET'])
def get_status():
    try:
        user = get_or_create_user()
        return jsonify(user.to_dict())
    except Exception as e:
        current_app.logger.error(f"Status error: {e}", exc_info=True)
        return jsonify({"error": "Internal error"}), 500

@api_bp.route('/events/current', methods=['GET'])
def get_current_events():
    try:
        event_manager = EventManager()
        return jsonify({
            "active_events": event_manager.get_active_events(),
            "current_themes": event_manager.get_current_themes(),
            "affection_bonus": event_manager.get_affection_bonus(),
            "event_icons": event_manager.get_event_icons(),
            "welcome_message": event_manager.get_welcome_message(),
            "server_time": datetime.datetime.now().isoformat()
        })
    except Exception as e:
        current_app.logger.error(f"Event error: {e}")
        return jsonify({"error": "Failed to get event data"}), 500

@api_bp.route('/reset', methods=['POST'])
def reset_user():
    try:
        session.clear()
        new_user = get_or_create_user()
        db.session.commit()
        return jsonify(new_user.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Reset failed"}), 500

@api_bp.route('/demo/quick-start', methods=['POST'])
def demo_quick_start():
    try:
        user = get_or_create_user()
        user.affection = 28
        user.tsundere_score = 25
        user.yandere_score = 10
        db.session.commit()
        return jsonify({
            "message": "Demo mode initialized!",
            "current_status": user.to_dict()
        })
    except Exception as e:
        return jsonify({"error": "Demo failed"}), 500