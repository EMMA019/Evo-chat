import re
from datetime import datetime, timezone
from typing import Tuple, Dict, Any, List
from sqlalchemy.orm import Session
from app.models import User, LongTermMemory, ChatMessage

MEMORY_TAG_PATTERN = re.compile(r'#memory\s+(.+)')

def handle_long_term_memory(db_session: Session, user: User, user_message: str) -> Tuple[str, bool]:
    """
    Detect #memory tag in user message and save as long-term memory in DB.
    Remove tag and content from returned message.

    Args:
        db_session: SQLAlchemy session.
        user: Target User object.
        user_message: Raw user message.

    Returns:
        Tuple (cleaned_message, memory_added).
        cleaned_message: Message with tag removed.
        memory_added: Boolean indicating if memory was added.
    """
    match = MEMORY_TAG_PATTERN.search(user_message)
    if match:
        memory_content = match.group(1).strip()
        new_memory = LongTermMemory(user_id=user.id, content=memory_content)
        db_session.add(new_memory)
        
        # Remove #memory tag from message
        cleaned_message = MEMORY_TAG_PATTERN.sub('', user_message).strip()
        return cleaned_message, True
    
    return user_message, False

def get_context(user: User) -> Dict[str, Any]:
    """
    Format context needed for AI response generation (long-term memories, time info, chat history).

    Args:
        user: Target User object.

    Returns:
        Dictionary containing context information.
    """
    # 1. Get and format long-term memories
    memories = user.long_term_memories
    if memories:
        formatted_memories = "You have the following long-term memories:\n" + "\n".join(f"- {mem.content}" for mem in memories)
    else:
        formatted_memories = "No long-term memories yet."

    # 2. Get and format time information
    now = datetime.now(timezone.utc)
    last_message = user.chat_messages[-1] if user.chat_messages else None
    
    time_context_parts = [f"Current date and time is {now.strftime('%Y-%m-%d %H:%M')}."]
    if last_message:
        time_since_last_message = now - last_message.created_at
        seconds = time_since_last_message.total_seconds()
        if seconds > 3600:
            time_context_parts.append(f"About {int(seconds / 3600)} hours have passed since the last conversation.")
        elif seconds > 60:
            time_context_parts.append(f"About {int(seconds / 60)} minutes have passed since the last conversation.")
    
    formatted_time_context = " ".join(time_context_parts)

    # 3. Get and format chat history (last 10 messages)
    recent_messages = ChatMessage.query.filter_by(user_id=user.id).order_by(ChatMessage.id.desc()).limit(10).all()
    recent_messages.reverse() # Restore chronological order
    
    chat_history = [
        {'role': msg.role if msg.role == 'user' else 'model', 'parts': [msg.content]}
        for msg in recent_messages
    ]

    return {
        "long_term_memories": formatted_memories,
        "time_context": formatted_time_context,
        "chat_history": chat_history
    }