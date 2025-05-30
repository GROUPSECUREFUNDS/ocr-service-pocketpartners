from ..settings import settings_service
from groq import Groq
import json

class GroqService:
    apiKey:str = settings_service.settings.GROQ_API_KEY
    client:Groq
    model:str = "llama-3.3-70b-versatile"
    
    def __init__(self):
        self.client = Groq(api_key=self.apiKey)
    
    def getJsonFromOcrText(self,text:str)->str:
        question:str = f"Ordena el siguiente texto y retornalo en un json por clave-valor: {text}"
        role:str = "user"
        
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content": question
                }
            ],
            model= self.model
        )
        result = chat_completion.choices[0].message.content
        return result
    
    @staticmethod
    def extract_json_from_text(text: str) -> dict:
        start = text.find('{')
        if start == -1:
            raise ValueError("No opening brace found")

        # Pila para encontrar el cierre correcto
        stack = []
        for i in range(start, len(text)):
            if text[i] == '{':
                stack.append('{')
            elif text[i] == '}':
                stack.pop()
                if not stack:
                    end = i + 1
                    json_str = text[start:end]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Error decoding JSON: {e}")
        raise ValueError("No valid JSON object found")