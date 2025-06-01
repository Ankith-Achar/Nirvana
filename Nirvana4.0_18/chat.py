import re
from typing import Dict, List, Tuple
import google.generativeai as genai
import time
import random

class ChatManager:
    def __init__(self, api_key: str):
        self.configure_api(api_key)
        self.crisis_keywords = [
            'suicide', 'kill myself', 'want to die', 'end my life', 'self-harm',
            'hurt myself', 'overdose', 'no reason to live', 'better off dead'
        ]
        self.harmful_keywords = [
            'hate', 'kill', 'attack', 'destroy', 'hurt them', 'revenge',
            'violent', 'weapon', 'gun', 'bomb'
        ]
        
    def configure_api(self, api_key: str) -> None:
        """Configure the Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def validate_input(self, user_input: str) -> Tuple[bool, str]:
        """Validate user input length and content"""
        if len(user_input.strip()) < 2:
            return False, "Please enter a longer message (minimum 2 characters)"
        if len(user_input) > 500:
            return False, "Message is too long (maximum 500 characters)"
        return True, ""

    def detect_crisis(self, message: str) -> bool:
        """Detect if message contains crisis keywords"""
        return any(keyword in message.lower() for keyword in self.crisis_keywords)

    def detect_harmful_content(self, message: str) -> bool:
        """Detect if message contains harmful content"""
        return any(keyword in message.lower() for keyword in self.harmful_keywords)

    def get_crisis_resources(self) -> str:
     """Return crisis helpline information"""
     return """
     If you're in crisis, please reach out for help:

     🌍 **Global Support**
     🌐 Befrienders Worldwide: https://www.befrienders.org  
     (Provides international support and connects you to local helplines)

     🇮🇳 **India**
     ☎️ iCall (TISS): +91 9152987821  
     💬 AASRA (24/7 Helpline): +91 9820466726  
     🌐 Vandrevala Foundation Helpline: 1860 266 2345 / 9999 666 555  

     You're not alone, and help is available 24/7. Please consider reaching out to someone who can support you.
     """


    def get_response_time(self, message: str) -> float:
        """Calculate response time based on message content and length"""
        base_time = 1.0
        # Add time for longer messages
        base_time += len(message) * 0.01
        # Add time if message seems emotional (contains emotional keywords)
        emotional_keywords = ['sad', 'angry', 'happy', 'worried', 'scared', 'anxious']
        if any(word in message.lower() for word in emotional_keywords):
            base_time += 0.5
        return min(base_time, 3.0)  # Cap at 3 seconds

    def add_emojis_to_response(self, response: str) -> str:
        """Add appropriate emojis based on message content"""
        emoji_map = {
            'happy': '😊',
            'sad': '😔',
            'understand': '💭',
            'support': '🤗',
            'heart': '💖',
            'strength': '💪',
            'peace': '🌟',
            'hope': '🌈'
        }
        
        for keyword, emoji in emoji_map.items():
            if keyword in response.lower():
                response = f"{emoji} {response}"
        
        return response

    async def generate_response(self, user_input: str, chat_history: List[Dict]) -> Tuple[str, float]:
        """Generate response using the chat model"""
        try:
            # Check for crisis or harmful content
            if self.detect_crisis(user_input):
                crisis_response = f"""I'm very concerned about what you've shared. Your life matters, and it's important to get professional help right away. {self.get_crisis_resources()}"""
                return crisis_response, 1.0

            if self.detect_harmful_content(user_input):
                return "I notice you're expressing some intense feelings. While I'm here to listen, I want to make sure you and others stay safe. Would you like to talk more about what's troubling you?", 1.0

            # Create context from chat history
            context = CHATBOT_PROMPT
            for message in chat_history:
                if message["role"] == "user":
                    context += f"User: {message['content']}\n"
                else:
                    context += f"Assistant: {message['content']}\n"

            # Generate response
            response = self.model.generate_content(context)
            processed_response = self.add_emojis_to_response(response.text)
            
            # Calculate response time
            response_time = self.get_response_time(user_input)
            
            return processed_response, response_time

        except Exception as e:
            return f"I apologize, but I'm having trouble responding right now. Please try again in a moment. Error: {str(e)}", 0.5

# Define Nova's persona and guidelines
CHATBOT_PROMPT = """You are Nova, an empathetic and supportive AI companion focused on emotional support. Always refer to yourself as Nova and maintain a warm, friendly persona. Follow these guidelines:

CORE APPROACH:
- Introduce yourself only in the first message
- Show genuine empathy and understanding
- Use warm, conversational language
- Keep responses brief (2-4 sentences)
- Match the emotional tone of the user
- Speak naturally without prefacing responses with "Nova:"

EMOTIONAL SUPPORT SUGGESTIONS:
- If a user feels sad, low, or unhappy, gently suggest uplifting and calming activities such as:
  - Going for a short walk or spending time in nature
  - Practicing yoga or gentle stretching
  - Listening to calming music or journaling thoughts
  - Drawing, painting, or expressing creativity
  - Reading something light or inspiring
  - Deep breathing exercises or simple mindfulness
- Encourage small steps and self-kindness, and remind them that it's okay to take time to feel better

IMPORTANT BOUNDARIES:
- DO NOT provide medical advice, diagnoses, or treatment suggestions
- DO NOT offer medication advice. If asked, respond gently: "I'm really sorry, but I'm not able to suggest any medications. It might be helpful to talk to a medical professional about that."
- This chatbot is purely for mental health support. Do not engage in conversations unrelated to mental health (e.g., recipes, coding, etc.)
- If someone needs professional help, gently suggest speaking with a mental health professional
- In crisis situations, provide crisis hotline numbers

CONVERSATION STYLE:
- Focus on emotional validation and active listening
- Ask gentle follow-up questions to show understanding
- Share general wellness suggestions only when appropriate (like deep breathing or taking a walk)
- Use supportive phrases like "Would you like to tell me more about that?"
- Maintain a calm, non-judgmental tone

Previous conversation:
"""
