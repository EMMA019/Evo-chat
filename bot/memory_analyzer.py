import re
import math
from typing import Dict, List
from collections import defaultdict

class MemoryAnalyzer:
    """
    Advanced Memory Analyzer with Exponential Decay and Stylistic Analysis.
    """
    
    def __init__(self):
        # Emotion/keyword mappings based on personality roots
        self.keyword_mappings = {
            'tsundere': {
                # Root: Intense Emotion & Duality
                'positive': ['lonely', 'miss you', 'help', 'happy', 'want', 'need', 'bother', 'idiot', 'dummy'],
                'negative': ['annoying', 'hate', 'stupid', 'disliked', 'ignore', 'bored', 'scary', 'bad', 'weird', 'noisy']
            },
            'yandere': {
                # Root: Dependence & Obsession
                'positive': ['love', 'forever', 'possess', 'destiny', 'mine', 'obsessed', 'always', 'together', 'only you', 'stay'],
                'negative': ['cheat', 'leave', 'betray', 'escape', 'others', 'busy', 'freedom', 'friend']
            },
            'kuudere': {
                # Root: Reason & Objectivity
                'positive': ['calm', 'smart', 'analyze', 'logical', 'rational', 'objective', 'study', 'book', 'read', 'reason', 'understand', 'efficient', 'data'],
                'negative': ['emotional', 'panic', 'irrational', 'confused', 'impulsive', 'childish', 'loud', 'chaos']
            },
            'dandere': {
                # Root: Anxiety & Modesty
                'positive': ['shy', 'nervous', 'quiet', 'introverted', 'kindness', 'sorry', 'worry', 'careful', 'safe', 'listen', 'wait', 'gentle', 'thanks'],
                'negative': ['social', 'bold', 'proactive', 'assertive', 'flashy', 'party', 'public']
            }
        }
        
        # Multipliers for negative keywords (Logic Inversion)
        self.negative_logic_multiplier = {
            'tsundere': 1.2,  # Negative words fuel Tsundere strongly
            'yandere': 1.5,   # Rejection fuels Yandere obsession significantly
            'kuudere': -1.0,  # Chaos reduces Kuudere score
            'dandere': -1.0   # Aggression reduces Dandere score
        }

        self.intensity_scores = {'weak': 1, 'medium': 2, 'strong': 3}
    
    def analyze_memories(self, memories: List[str]) -> Dict[str, int]:
        """Analyze memory content with Exponential Decay"""
        score_impact = defaultdict(float)
        
        # Process newest memories first
        recent_first_memories = list(reversed(memories))
        
        for index, memory in enumerate(recent_first_memories):
            # Exponential Decay: e.g., 1.0, 0.85, 0.72, 0.61...
            decay_factor = math.pow(0.85, index)
            if decay_factor < 0.1: break # Stop processing if impact is negligible
            
            memory_lower = memory.lower()
            
            for persona, keywords in self.keyword_mappings.items():
                # Positive impact
                pos_count = self._count_keywords(memory_lower, keywords['positive'])
                if pos_count > 0:
                    base_impact = min(pos_count * 2, 3) # Cap per memory
                    score_impact[persona] += base_impact * decay_factor
                
                # Negative impact
                neg_count = self._count_keywords(memory_lower, keywords['negative'])
                if neg_count > 0:
                    base_impact = min(neg_count * 1, 2)
                    multiplier = self.negative_logic_multiplier.get(persona, -1)
                    score_impact[persona] += base_impact * decay_factor * multiplier
        
        return {k: int(v) for k, v in score_impact.items()}

    def _count_keywords(self, text: str, keywords: List[str]) -> int:
        """Count exact word matches using regex boundaries"""
        count = 0
        for keyword in keywords:
            # \b ensures "read" doesn't match "bread"
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            count += len(re.findall(pattern, text))
        return count
    
    def analyze_conversation_context(self, conversation_history: List[Dict]) -> Dict[str, int]:
        """Analyze short-term context including Stylistic Features"""
        if not conversation_history:
            return {}
            
        recent_msgs = [msg.get('parts', [''])[0] for msg in conversation_history[-3:]] # Last 3 msgs
        recent_text = " ".join(recent_msgs).lower()
        
        context_impact = defaultdict(int)
        
        def check_pattern(patterns):
            return self._count_keywords(recent_text, patterns) > 0

        # 1. Keyword Analysis (Refined for better accuracy)
        patterns = {
            'lonely': ['lonely', 'alone', 'miss', 'bored', 'nobody'],
            'happy': ['happy', 'fun', 'joy', 'laugh', 'glad', 'great', 'lol', 'haha', 'rofl'],
            'angry': ['angry', 'mad', 'hate', 'shut up', 'annoying'],
            'sad': ['sad', 'cry', 'pain', 'sorry', 'depressed', 'hurt'],
            # 【修正】ヤンデレ判定ワードを強化 (always, together, stay)
            'love': ['love', 'adore', 'cute', 'marry', 'kiss', 'always', 'together', 'forever', 'stay', 'mine'],
            # 【修正】日常会話で出る how, think, why を削除し、ガチの知的ワードのみに
            'smart': ['analyze', 'understand', 'explain', 'study', 'logic', 'theory', 'calculate'],
            'scared': ['scared', 'help', 'nervous', 'anxious', 'afraid']
        }

        if check_pattern(patterns['lonely']):
            context_impact['yandere'] += 2; context_impact['tsundere'] += 1
        if check_pattern(patterns['happy']):
            context_impact['tsundere'] += 1; context_impact['dandere'] += 1 
            # Kuudere bonus removed from generic happiness
        if check_pattern(patterns['angry']):
            context_impact['tsundere'] += 3; context_impact['yandere'] += 1
        if check_pattern(patterns['sad']):
            context_impact['dandere'] += 2; context_impact['kuudere'] += 1
        if check_pattern(patterns['love']):
            context_impact['yandere'] += 3; context_impact['tsundere'] += 2
        if check_pattern(patterns['smart']):
            context_impact['kuudere'] += 3
        if check_pattern(patterns['scared']):
            context_impact['dandere'] += 3

        # 2. Stylistic Analysis (文体特徴量)
        # Exclamation marks -> Emotional intensity (Tsundere/Yandere)
        exclamation_count = recent_text.count('!')
        if exclamation_count >= 2:
            context_impact['tsundere'] += 1
            context_impact['yandere'] += 1
            context_impact['kuudere'] -= 1 # Kuudere dislikes noise
        
        # Question marks -> Curiosity or Uncertainty (Kuudere/Dandere)
        question_count = recent_text.count('?')
        if question_count >= 2:
            context_impact['kuudere'] += 1 # Intellectual curiosity
            context_impact['dandere'] += 1 # Uncertainty
            
        # Length analysis
        avg_len = sum(len(m) for m in recent_msgs) / len(recent_msgs) if recent_msgs else 0
        if avg_len > 50: # Long text -> Yandere (Obsessive) or Kuudere (Explanatory)
            context_impact['yandere'] += 1
            context_impact['kuudere'] += 1
        elif avg_len < 10: # Short text -> Tsundere (Blunt) or Dandere (Shy)
            context_impact['tsundere'] += 1
            context_impact['dandere'] += 1

        # 3. Winner Bonus (競合解消)
        if context_impact:
            winner = max(context_impact, key=context_impact.get)
            context_impact[winner] += 1  # Boost the winner to clarify direction

        return dict(context_impact)