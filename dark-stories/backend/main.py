from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types # Potrzebne do optymalizacji i wymuszenia JSON
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

    # Kaganiec prędkości dla szybkiej odpowiedzi
    response = client.models.generate_content(
        model=GEMINI_MODEL, 
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0, max_output_tokens=10)
    )
    return {"answer": response.text.strip()}

@app.post("/api/generate")
def generate_story(req: GenerateRequest):
    if req.category == "PKO Bank Polski":
        kontekst = "Stwórz zagadkę o edukacji finansowej, bezpieczeństwie w sieci (np. phishing), oszczędzaniu lub aplikacji mobilnej. Rozwiązanie ma pokazywać mądrą decyzję finansową."
    elif req.category == "Tauron":
        kontekst = "Stwórz zagadkę o czystej energii, fotowoltaice, oszczędzaniu prądu lub innowacjach Taurona."
    else:
        kontekst = "Stwórz mroczną, zaskakującą zagadkę w stylu klasycznych 'Czarnych Historii'."

    # Znacznie wzmocniony prompt wymuszający czysty JSON
    prompt = (
        f"{kontekst}\n"
        f"Poziom trudności: {req.difficulty}\n"
        "Zwróć wynik WYŁĄCZNIE jako czysty, poprawny obiekt JSON. "
        "Nie dodawaj żadnego tekstu przed ani po JSON-ie. "
        "Nie używaj znaczników kodu (np. ```json). "
        "Użyj dokładnie tych kluczy:\n"
        "{\n"
        '  "title": "Tytuł historii",\n'
        '  "difficulty": "easy | medium | hard",\n'
        '  "category": "Kategoria",\n'
        '  "story": "Krótki zarys historii",\n'
        '  "solution": "Logiczne rozwiązanie",\n'
        '  "education": "Cenna pigułka wiedzy związana z zagadką"\n'
        "}"
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL, # Używamy głównego modelu Gemma
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7 # Odrobinę kreatywności, ale zachowaj strukturę
                # Usunęliśmy response_mime_type
            )
        )
        
        # Agresywne czyszczenie odpowiedzi
        text = response.text.strip()
        # Usuń potencjalne znaczniki markdown (nawet jeśli prosiliśmy by ich nie było)
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
        # Przechwycenie błędu, jeśli odpowiedź nie jest poprawnym JSONem
        print(f"Błąd generowania JSON: {e}")
        print(f"Odpowiedź modelu: {response.text if 'response' in locals() else 'Brak odpowiedzi'}")
        raise HTTPException(status_code=500, detail="Nie udało się wygenerować poprawnego formatu historii. Spróbuj ponownie.")

frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

@app.get("/")
def serve_index():
    return FileResponse(str(frontend_path / "index.html"))