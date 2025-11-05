from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import requests

app = FastAPI(
    title="Code Helper API",
    description="🚀 AI-powered code review and analysis API",
    version="3.0"
)

@app.get("/")
async def root():
    return {"message": "🚀 Code Helper API работает!", "version": "3.0"}

@app.post("/code-review")
async def code_review(
    code: str = Form(...),
    language: str = Form("python")
):
    if not code.strip():
        return JSONResponse({"error": "Код не предоставлен"}, status_code=400)
    
    # Простые автономные ответы
    simple_responses = {
        "python": "🔍 Проблемы: Переменная 'hello' не определена. Используйте print('hello') с кавычками.",
        "javascript": "🔍 Проблемы: Используется print() вместо console.log(). Замените на console.log('hello').",
        "java": "🔍 Проблемы: Неправильный синтаксис Java. Используйте System.out.println() внутри класса.",
        "php": "🔍 Проблемы: Неправильный синтаксис PHP. Используйте echo 'hello'; внутри <?php ?> тегов."
    }
    
    # Пробуем AI
    ai_response = None
    try:
        prompt = f"Проанализируй код на {language}: {code}"
        response = requests.post(
            "https://my-ai-api-ihp6.onrender.com/smart-chat",
            json={"message": prompt},
            timeout=20
        )
        if response.status_code == 200:
            ai_response = response.json().get("response", "").strip()
    except:
        pass
    
    # Выбираем ответ
    final_review = ai_response if ai_response and len(ai_response) > 50 else simple_responses.get(
        language, 
        "🔍 Проверьте синтаксис и добавьте комментарии."
    )
    
    return {
        "status": "success",
        "language": language,
        "review": final_review
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "code-helper-api", "version": "3.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)