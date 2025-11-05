from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from typing import Optional

app = FastAPI(
    title="Code Helper API",
    description="🚀 AI-powered code review and analysis API",
    version="1.0"
)

# Остальной код остается без изменений...

class CodeRequest(BaseModel):
    code: str
    language: str = "python"
    task: str = None

class ExplanationRequest(BaseModel):
    code: str
    language: str = "python"

# Эндпоинт 1: Ревью кода
@app.post("/code-review")
async def code_review(request: CodeRequest):
    """
    Анализирует код и дает рекомендации по улучшению
    """
    prompt = f"""
    Проанализируй этот код на {request.language} и дай конструктивный фидбек:
    
    Код:
    {request.code}
    
    Ответь в формате:
    🔍 Проблемы: [список проблем]
    💡 Рекомендации: [список улучшений]
    ✅ Сильные стороны: [что хорошо]
    """
    
    try:
        # Используем твой существующий AI API
        response = requests.post(
            "https://my-ai-api-ihp6.onrender.com/smart-chat",
            json={"message": prompt}
        )
        
        if response.status_code == 200:
            return {
                "status": "success",
                "review": response.json().get("response", "Ошибка анализа"),
                "language": request.language
            }
        else:
            return {
                "status": "error", 
                "review": "Сервис временно недоступен",
                "fallback_advice": "Проверьте отступы, названия переменных и обработку ошибок"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Эндпоинт 2: Объяснение кода
@app.post("/code-explainer")
async def explain_code(request: ExplanationRequest):
    """
    Объясняет что делает код простыми словами
    """
    prompt = f"""
    Объясни что делает этот код на {request.language} простыми словами:
    
    {request.code}
    
    Ответь в формате:
    🎯 Что делает: [краткое описание]
    🔧 Как работает: [пошаговое объяснение]
    💡 Пример использования: [практический пример]
    """
    
    # Аналогичная реализация как выше
    return {"explanation": "Объяснение кода..."}

@app.get("/")
async def root():
    return {"message": "Code Helper API - Документация по /docs"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "code-helper-api"}