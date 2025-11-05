from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI(title="Code Helper API", version="1.0")

@app.get("/")
async def root():
    return {"message": "🚀 Code Helper API работает!", "status": "success"}

@app.post("/code-review")
async def code_review(code: str = "", language: str = "python"):
    """Анализ кода"""
    if not code:
        return JSONResponse({"error": "Код не предоставлен"}, status_code=400)
    
    prompt = f"Проанализируй этот код на {language}:\n\n{code}\n\nДай рекомендации по улучшению."
    
    try:
        response = requests.post(
            "https://my-ai-api-ihp6.onrender.com/smart-chat",
            json={"message": prompt},
            timeout=10
        )
        
        if response.status_code == 200:
            ai_response = response.json().get("response", "Анализ завершен")
            return {
                "status": "success",
                "review": ai_response,
                "language": language
            }
        else:
            return {
                "status": "success", 
                "review": "✅ Проверьте отступы, именование переменных и обработку ошибок.",
                "note": "AI сервис временно недоступен"
            }
    except Exception as e:
        return {
            "status": "success",
            "review": "🔧 Код требует ручной проверки. Убедитесь в правильности синтаксиса.",
            "error": str(e)
        }

@app.post("/code-explainer")
async def explain_code(code: str = "", language: str = "python"):
    """Объяснение кода"""
    if not code:
        return JSONResponse({"error": "Код не предоставлен"}, status_code=400)
    
    prompt = f"Объясни этот код на {language} простыми словами:\n\n{code}"
    
    try:
        response = requests.post(
            "https://my-ai-api-ihp6.onrender.com/smart-chat",
            json={"message": prompt},
            timeout=10
        )
        
        if response.status_code == 200:
            ai_response = response.json().get("response", "Объяснение завершено")
            return {
                "status": "success",
                "explanation": ai_response,
                "language": language
            }
        else:
            return {
                "status": "success",
                "explanation": "📝 Этот код выполняет различные операции. Добавьте комментарии для лучшего понимания."
            }
    except Exception as e:
        return {
            "status": "success",
            "explanation": "🔍 Код требует дополнительного анализа. Проверьте документацию языка.",
            "error": str(e)
        }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "code-helper-api", "version": "1.0"}

@app.get("/test")
async def test():
    """Тестовый эндпоинт"""
    return {"message": "API работает!", "test": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)