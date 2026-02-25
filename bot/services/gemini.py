import google.generativeai as genai
from typing import List, Dict
from bot.config import GEMINI_API_KEY, GEMINI_MODEL

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """Ты персональный ассистент в Telegram. Ты помогаешь пользователю с задачами, 
ответами на вопросы, планированием и анализом. Отвечай кратко и по делу."""

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.conversations: Dict[int, List[dict]] = {}
    
    def get_history(self, user_id: int) -> List[dict]:
        return self.conversations.get(user_id, [])
    
    def add_to_history(self, user_id: int, role: str, text: str):
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({
            "role": role,
            "parts": [text]
        })
        
        if len(self.conversations[user_id]) > 10:
            self.conversations[user_id] = self.conversations[user_id][-10:]
    
    def clear_history(self, user_id: int):
        self.conversations[user_id] = []
    
    async def chat(self, user_id: int, message: str) -> str:
        try:
            # Добавляем системный промпт в начало, если история пустая
            history = self.get_history(user_id)
            if not history:
                full_message = f"{SYSTEM_PROMPT}\n\nПользователь: {message}"
            else:
                full_message = message
            
            self.add_to_history(user_id, "user", message)
            
            chat = self.model.start_chat(history=self.get_history(user_id)[:-1])
            response = await chat.send_message_async(full_message)
            answer = response.text
            
            self.add_to_history(user_id, "model", answer)
            return answer
            
        except Exception as e:
            return f"Ошибка: {str(e)}. Попробуй позже."

gemini_service = GeminiService()
