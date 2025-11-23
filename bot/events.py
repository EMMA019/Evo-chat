import datetime
import random
from typing import Dict, List, Optional
from enum import Enum

class EventType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    SEASONAL = "seasonal"
    SPECIAL = "special"

class EventManager:
    def __init__(self):
        self.current_events = {}
        self.load_events()
    
    def load_events(self):
        """Load event data"""
        self.events = {
            # Daily events
            "monday_motivation": {
                "type": EventType.DAILY,
                "condition": lambda: datetime.datetime.now().weekday() == 0,
                "name": "Monday Motivation",
                "theme": "motivation",
                "affection_bonus": 2,
                "prompt_modifier": "It's Monday! Let's start the week with positive energy and motivation.",
                "icon": "🚀"
            },
            "friday_excitement": {
                "type": EventType.DAILY,
                "condition": lambda: datetime.datetime.now().weekday() == 4,
                "name": "Friday Excitement",
                "theme": "weekend",
                "affection_bonus": 1,
                "prompt_modifier": "It's Friday! The weekend is almost here. Any exciting plans?",
                "icon": "🎉"
            },
            "weekend_chill": {
                "type": EventType.DAILY,
                "condition": lambda: datetime.datetime.now().weekday() in [5, 6],
                "name": "Weekend Chill",
                "theme": "relaxation",
                "affection_bonus": 1,
                "prompt_modifier": "It's the weekend! Time to relax and enjoy some quiet moments.",
                "icon": "😌"
            },
            
            # Seasonal events
            "spring": {
                "type": EventType.SEASONAL,
                "condition": lambda: 3 <= datetime.datetime.now().month <= 5,
                "name": "Spring Festival",
                "theme": "spring",
                "affection_bonus": 1,
                "prompt_modifier": "Spring is here! The flowers are blooming and everything feels fresh and new.",
                "icon": "🌸"
            },
            "summer": {
                "type": EventType.SEASONAL,
                "condition": lambda: 6 <= datetime.datetime.now().month <= 8,
                "name": "Summer Adventure",
                "theme": "summer",
                "affection_bonus": 1,
                "prompt_modifier": "Summer vibes! Perfect time for adventures and making memories.",
                "icon": "☀️"
            },
            "autumn": {
                "type": EventType.SEASONAL,
                "condition": lambda: 9 <= datetime.datetime.now().month <= 11,
                "name": "Autumn Colors",
                "theme": "autumn",
                "affection_bonus": 1,
                "prompt_modifier": "Autumn leaves are falling. There's something nostalgic about this season.",
                "icon": "🍂"
            },
            "winter": {
                "type": EventType.SEASONAL,
                "condition": lambda: datetime.datetime.now().month in [12, 1, 2],
                "name": "Winter Wonderland",
                "theme": "winter",
                "affection_bonus": 1,
                "prompt_modifier": "Winter is here! Cozy days and warm conversations.",
                "icon": "⛄"
            },
            
            # Special events
            "new_year": {
                "type": EventType.SPECIAL,
                "condition": lambda: datetime.datetime.now().month == 1 and datetime.datetime.now().day <= 7,
                "name": "New Year Celebration",
                "theme": "celebration",
                "affection_bonus": 2,
                "prompt_modifier": "Happy New Year! This is a time for new beginnings and fresh starts.",
                "icon": "🎊"
            },
            "christmas": {
                "type": EventType.SPECIAL,
                "condition": lambda: datetime.datetime.now().month == 12 and 20 <= datetime.datetime.now().day <= 26,
                "name": "Christmas Season",
                "theme": "holiday",
                "affection_bonus": 2,
                "prompt_modifier": "Merry Christmas! The most wonderful time of the year for sharing joy.",
                "icon": "🎄"
            },
            
            # Time-based events
            "morning": {
                "type": EventType.DAILY,
                "condition": lambda: 5 <= datetime.datetime.now().hour < 12,
                "name": "Good Morning",
                "theme": "morning",
                "affection_bonus": 1,
                "prompt_modifier": "Good morning! A new day is full of possibilities.",
                "icon": "🌅"
            },
            "evening": {
                "type": EventType.DAILY,
                "condition": lambda: 18 <= datetime.datetime.now().hour < 22,
                "name": "Evening Relaxation",
                "theme": "evening",
                "affection_bonus": 1,
                "prompt_modifier": "Evening time... perfect for relaxing conversations.",
                "icon": "🌙"
            },
            "night": {
                "type": EventType.DAILY,
                "condition": lambda: 22 <= datetime.datetime.now().hour or datetime.datetime.now().hour < 5,
                "name": "Late Night",
                "theme": "night",
                "affection_bonus": 1,
                "prompt_modifier": "Late night hours... time for deep and meaningful talks.",
                "icon": "🌃"
            }
        }
    
    def get_active_events(self) -> List[Dict]:
        """Get currently active events"""
        active_events = []
        for event_id, event_data in self.events.items():
            if event_data["condition"]():
                # Create a copy of event data without the condition function
                # Functions are not JSON serializable
                event_info = event_data.copy()
                if 'condition' in event_info:
                    del event_info['condition']
                
                # Enum is also not JSON serializable by default, convert to value
                if 'type' in event_info and hasattr(event_info['type'], 'value'):
                    event_info['type'] = event_info['type'].value
                    
                active_events.append({
                    "id": event_id,
                    **event_info
                })
        return active_events
    
    def get_event_prompt_modifiers(self) -> str:
        """Get prompt modifiers based on active events"""
        # Re-implement logic to access raw events since get_active_events strips conditions
        active_events = []
        for event_id, event_data in self.events.items():
            if event_data["condition"]():
                active_events.append(event_data)
                
        modifiers = []
        for event in active_events:
            modifiers.append(event["prompt_modifier"])
            
        return " ".join(modifiers) if modifiers else ""
    
    def get_affection_bonus(self) -> int:
        """Calculate affection bonus from events"""
        # Re-implement logic to access raw events
        active_events = []
        for event_id, event_data in self.events.items():
            if event_data["condition"]():
                active_events.append(event_data)
                
        bonus = 0
        for event in active_events:
            bonus += event["affection_bonus"]
            
        return min(bonus, 10)  # Cap bonus at 10
    
    def get_current_themes(self) -> List[str]:
        """Get current themes"""
        # Re-implement logic to access raw events
        active_events = []
        for event_id, event_data in self.events.items():
            if event_data["condition"]():
                active_events.append(event_data)
                
        return [event["theme"] for event in active_events]
    
    def get_event_icons(self) -> List[str]:
        """Get event icons for display"""
        # Re-implement logic to access raw events
        active_events = []
        for event_id, event_data in self.events.items():
            if event_data["condition"]():
                active_events.append(event_data)
                
        return [event["icon"] for event in active_events]
    
    def get_welcome_message(self) -> str:
        """Get welcome message based on active events"""
        # Use get_active_events which returns safe dicts
        active_events = self.get_active_events()
        if not active_events:
            return "Welcome back! How are you today?"
        
        # Use the first event for welcome message
        # Access ID from the dictionary returned by get_active_events
        event_id = active_events[0]["id"]
        
        welcome_messages = {
            "monday_motivation": "Happy Monday! Ready to conquer the week? 🚀",
            "friday_excitement": "It's Friday! Any fun plans for the weekend? 🎉",
            "weekend_chill": "Happy weekend! Time to relax and recharge. 😌",
            "spring": "Spring is in the air! Everything feels fresh and new. 🌸",
            "summer": "Summer vibes! Perfect weather for adventures. ☀️",
            "autumn": "Beautiful autumn day... the leaves are changing colors. 🍂",
            "winter": "Winter wonderland! Cozy up and stay warm. ⛄",
            "new_year": "Happy New Year! New beginnings and fresh starts. 🎊",
            "christmas": "Merry Christmas! 'Tis the season for joy. 🎄",
            "morning": "Good morning! Hope you have a wonderful day ahead. 🌅",
            "evening": "Good evening! Perfect time to unwind. 🌙",
            "night": "Up late? Perfect time for deep conversations. 🌃"
        }
        
        return welcome_messages.get(event_id, "Welcome back! How are you today?")