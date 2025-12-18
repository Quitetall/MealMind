# Running MealMind

## Backend
```bash
cd backend
cp .env.example .env
# add your API key
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
