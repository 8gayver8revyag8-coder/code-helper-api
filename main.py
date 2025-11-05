from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "🚀 Code Helper API работает!"}

@app.get("/code-review")
async def code_review(code: str, language: str = "python"):
    if not code:
        return {"error": "Код не предоставлен"}
    
    responses = {
        "python": "🔍 Проблемы: Переменная не определена. Используйте кавычки: print('hello')",
        "javascript": "🔍 Проблемы: Используйте console.log('hello') вместо print()",
        "java": "🔍 Проблемы: Используйте System.out.println() внутри класса",
        "php": "🔍 Проблемы: Используйте echo 'hello'; внутри <?php ?>"
    }
    
    return {
        "status": "success",
        "language": language,
        "review": responses.get(language, "🔍 Проверьте синтаксис")
    }

@app.post("/code-review")
async def code_review_post(code: str, language: str = "python"):
    return await code_review(code, language)

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)