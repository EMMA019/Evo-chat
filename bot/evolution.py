import logging
from typing import Dict, Tuple, Optional, List
from app.models import User
from .memory_analyzer import MemoryAnalyzer
from .events import EventManager

# Logger setup
logger = logging.getLogger(__name__)

def update_scores_and_affection(user: User, analysis_result: Dict[str, int], conversation_context: List[Dict] = None):
    """
    Update user's personality scores and affection based on analysis results and memory.
    """
    # Apply event bonuses
    event_manager = EventManager()
    affection_bonus = event_manager.get_affection_bonus()
    
    # 親愛度の上限なし（無限に加算）
    user.affection += 1 + affection_bonus
    
    score_multiplier = 1
    user.tsundere_score += analysis_result.get('tsundere', 0) * score_multiplier
    user.yandere_score += analysis_result.get('yandere', 0) * score_multiplier
    user.kuudere_score += analysis_result.get('kuudere', 0) * score_multiplier
    user.dandere_score += analysis_result.get('dandere', 0) * score_multiplier
    
    # Memory impact
    memory_impact = update_scores_based_on_memory(user, conversation_context)
    
    if affection_bonus > 0:
        logger.info(f"Affection bonus: +{affection_bonus} from active events")
    logger.debug(f"Updated scores for user {user.session_id}: Affection={user.affection}")

def update_scores_based_on_memory(user: User, conversation_context: List[Dict] = None) -> Dict[str, int]:
    """
    Update scores based on memory and conversation context
    """
    analyzer = MemoryAnalyzer()
    
    memory_contents = [mem.content for mem in user.long_term_memories]
    memory_impact = analyzer.analyze_memories(memory_contents)
    
    context_impact = {}
    if conversation_context:
        context_impact = analyzer.analyze_conversation_context(conversation_context)
    
    total_impact = {}
    for impact_dict in [memory_impact, context_impact]:
        for persona, impact in impact_dict.items():
            total_impact[persona] = total_impact.get(persona, 0) + impact
    
    user.tsundere_score += total_impact.get('tsundere', 0)
    user.yandere_score += total_impact.get('yandere', 0)
    user.kuudere_score += total_impact.get('kuudere', 0)
    user.dandere_score += total_impact.get('dandere', 0)
    
    return total_impact

def check_evolution(user: User) -> Tuple[bool, Optional[str]]:
    """
    Check evolution conditions. 
    Includes Hysteresis logic: Re-evolution requires a larger score gap.
    """
    from flask import current_app
    
    is_demo = current_app.config.get('DEMO_MODE')
    
    if is_demo:
        threshold = current_app.config.get('DEMO_EVOLUTION_THRESHOLD', 3)
        base_score_diff = current_app.config.get('DEMO_SCORE_DIFFERENCE', 2)
    else:
        threshold = current_app.config.get('EVOLUTION_AFFECTION_THRESHOLD', 30)
        base_score_diff = current_app.config.get('EVOLUTION_SCORE_DIFFERENCE', 5)

    # 親愛度が足りなければ進化しない
    if user.affection < threshold:
        return False, None

    scores = {
        'Tsundere': user.tsundere_score,
        'Yandere': user.yandere_score,
        'Kuudere': user.kuudere_score,
        'Dandere': user.dandere_score,
    }

    # スコア順にソート
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_personality, top_score = sorted_scores[0]
    second_personality, second_score = sorted_scores[1]

    # 【重要修正】ヒステリシス（履歴効果）の実装
    # 既に進化済みなら、性格を変えるのにより大きなエネルギー（スコア差）を必要とする
    # 通常: 5点差 -> 再進化: 10点差
    # デモ: 2点差 -> 再進化: 5点差
    required_diff = base_score_diff
    if user.evolved:
         required_diff = base_score_diff * 2 if not is_demo else base_score_diff + 3

    # 判定ロジック
    is_re_evolution = user.evolved and (user.personality_type != top_personality)
    is_initial_evolution = not user.evolved

    if (top_score - second_score) >= required_diff:
        if is_initial_evolution or is_re_evolution:
            old_persona = user.personality_type
            user.personality_type = top_personality
            user.evolved = True
            
            if is_re_evolution:
                logger.info(f"Re-Evolution triggered! User {user.session_id}: {old_persona} -> {top_personality} (Diff: {top_score - second_score})")
            else:
                logger.info(f"Initial Evolution triggered! User {user.session_id} -> {top_personality}")
                
            return True, top_personality
            
    return False, None