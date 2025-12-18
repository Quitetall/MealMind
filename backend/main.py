import os, json
from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

from prices import PRICE_TABLE
from prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

COMPAT_URL = os.getenv("COMPAT_BASE_URL")
COMPAT_KEY = os.getenv("COMPAT_API_KEY")
COMPAT_MODEL = os.getenv("COMPAT_MODEL")

app = FastAPI(title="MealMind")

class MealRequest(BaseModel):
    calories: int
    protein: int
    meals: int
    budget: float
    include: list[str] = []
    exclude: list[str] = []

async def call_llm(messages):
    if AI_PROVIDER == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
        payload = {
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0.4
        }
    else:
        url = f"{COMPAT_URL}/chat/completions"
        headers = {"Authorization": f"Bearer {COMPAT_KEY}"}
        payload = {
            "model": COMPAT_MODEL,
            "messages": messages,
            "temperature": 0.4
        }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

@app.get("/health")
def health():
    return {"status": "ok", "provider": AI_PROVIDER}

@app.post("/mealplan")
async def mealplan(req: MealRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(req.dict(), PRICE_TABLE)}
    ]

    output = await call_llm(messages)

    try:
        return json.loads(output)
    except:
        return {"error": "Model returned invalid JSON", "raw": output}
