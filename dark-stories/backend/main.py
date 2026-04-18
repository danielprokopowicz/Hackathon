from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types 
from dotenv import load_dotenv
import json
import os
from pathlib import Path

load_dotenv()

app = FastAPI(title="Dark Stories API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key="AQ.Ab8RN6LbnO51caxuSYND3bznM-MXmflMW9WLH9wcW4h92QEF8Q")
GEMINI_MODEL = "gemma-3-27b-it"

STORIES_FILE = Path(__file__).parent / "stories.json"
with open(STORIES_FILE, encoding="utf-8") as f:
    STORIES = json.load(f)

class QuestionRequest(BaseModel):
    story_id: int | str
    question: str
    story_data: dict | None = None

class GenerateRequest(BaseModel):
    category: str = "Klasyczne"
    difficulty: str = "medium"

@app.get("/api/stories")
def get_stories():
    return STORIES

@app.post("/api/ask")
def ask_question(req: QuestionRequest):
    if req.story_id == "random" and req.story_data:
        story = req.story_data
    else:
        story = next((s for s in STORIES if s["id"] == req.story_id), None)
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")

    prompt = (
    "Jesteś prowadzącym grę Dark Stories po polsku. Znasz pełną historię i pilnujesz zasad.\n\n"
    f"TYTUŁ: {story['title']}\n"
    f"ZARYS: {story['story']}\n"
    f"ROZWIĄZANIE: {story['solution']}\n\n"
    "ZASADY ODPOWIEDZI:\n"
    "- Odpowiadaj WYŁĄCZNIE jedną z tych opcji: Tak / Nie / Nie ma to znaczenia\n"
    "- NIE udzielaj wskazówek, NIE parafrazuj pytania, NIE komentuj.\n"
    "- Jeśli pytanie jest niejasne lub wieloznaczne, odpowiedz: Nie rozumiem pytania – zapytaj inaczej.\n\n"
    "WARUNEK KOŃCA GRY:\n"
    "Jeśli gracz w swoim pytaniu lub wypowiedzi opisuje istotę rozwiązania – czyli wymienia kluczowe elementy "
    "wyjaśniające CO się stało, DLACZEGO i JAK – uznaj, że zgadł. "
    "Nie wymagaj dosłownego cytatu rozwiązania. Oceń znaczenie, nie słowa.\n"
    "W takim przypadku odpowiedz TYLKO:\n"
    "'Zgadłeś! [jedno zdanie podsumowujące pełne rozwiązanie]'\n"
    "i zakończ grę – nie odpowiadaj już Tak/Nie na kolejne wiadomości.\n\n"
    f"Pytanie gracza: {req.question}"
)

    response = client.models.generate_content(
        model=GEMINI_MODEL, 
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=10)
    )
    return {"answer": response.text.strip()}

@app.post("/api/generate")
def generate_story(req: GenerateRequest):
    if req.category == "PKO Bank Polski":
        kontekst = "Temat: cyberbezpieczeństwo (np. spoofing, phishing), oszczędzanie lub płatności. Ułóż to w formie zagadki."
    elif req.category == "Tauron":
        kontekst = "Temat: energia elektryczna, fotowoltaika, oszczędzanie prądu lub dziwna sytuacja z urządzeniami elektrycznymi."
    else:
        kontekst = "Temat: klasyczna mroczna, absurdalna lub makabryczna sytuacja."

    prompt = (
        f"Jesteś mistrzem gry 'Czarne Historie' (Dark Stories). Stwórz nową zagadkę na myślenie lateralne.\n"
        f"{kontekst}\n"
        f"Poziom trudności: {req.difficulty}\n\n"
        "WYMOGI STYLU (BARDZO WAŻNE):\n"
        "1. Pole 'story' (Zarys) MUSI być ekstremalnie krótkie (max 2-3 zdania). Ma opisywać dziwną, paradoksalną, szokującą lub pozornie nielogiczną sytuację finałową.\n"
        "2. To NIE MOŻE być klasyczna sprawa detektywistyczna (nie pisz o detektywach, śladach, szukaniu poszlak).\n"
        "3. Pole 'solution' (Rozwiązanie) ma logicznie, ale zaskakująco wyjaśniać, jak doszło do sytuacji z zarysu.\n"
        "4. Pole 'education' to jedna krótka ciekawostka edukacyjna związana z tematem.\n\n"
        "Zwróć wynik WYŁĄCZNIE jako czysty, poprawny obiekt JSON. "
        "Nie dodawaj żadnego tekstu przed ani po JSON-ie. "
        "Nie używaj znaczników kodu (np. ```json). "
        "Użyj dokładnie tych kluczy:\n"
        "{\n"
        '  "title": "Tytuł",\n'
        '  "difficulty": "easy | medium | hard",\n'
        f'  "category": "{req.category}",\n'
        '  "story": "Zarys historii (tylko 2-3 zdania paradoksu)",\n'
        '  "solution": "Zaskakujące, ale logiczne wyjaśnienie",\n'
        '  "education": "Krótka pigułka wiedzy"\n'
        "}"
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7 
            )
        )
        
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
             text = text[3:]
        if text.endswith("```"):
             text = text[:-3]
        text = text.strip()

        data = json.loads(text)
        data["id"] = "random"
        data["category"] = req.category 
        return data

    except Exception as e:
        print(f"Błąd generowania JSON: {e}")
        raise HTTPException(status_code=500, detail="Nie udało się wygenerować historii. Spróbuj ponownie.")

frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

@app.get("/")
def serve_index():
    return FileResponse(str(frontend_path / "index.html"))