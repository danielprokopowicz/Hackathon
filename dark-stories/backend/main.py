from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types # Potrzebne do optymalizacji i wymuszenia JSON
import json
import os
from pathlib import Path

app = FastAPI(title="Dark Stories API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Twój poprawny klucz API
client = genai.Client(api_key="AQ.Ab8RN6LbnO51caxuSYND3bznM-MXmflMW9WLH9wcW4h92QEF8Q")
GEMINI_MODEL = "gemini-2.5-flash-lite"

STORIES = [
    {
        "id": 1,
        "title": "Przyciski w windzie",
        "category": "Klasyczne",
        "difficulty": "easy",
        "story": "Każdego dnia rano mężczyzna zjeżdża windą z 20. piętra na parter, by iść do pracy. Gdy wraca, zazwyczaj wjeżdża tylko na 12. piętro i resztę drogi pokonuje schodami. Dlaczego?",
        "solution": "Mężczyzna jest bardzo niski i nie sięga do przycisków powyżej 12. piętra. Wyjątkiem są deszczowe dni – wtedy ma ze sobą parasol, którym może nacisnąć właściwy guzik swojego piętra.",
    },
    {
        "id": 2,
        "title": "Tragedia w windzie",
        "category": "Klasyczne",
        "difficulty": "medium",
        "story": "Mężczyzna wsiadł do windy, a kilka sekund później zrozumiał, że jego żona nie żyje. Jak?",
        "solution": "Jego żona była podłączona do aparatury podtrzymującej życie w tym samym budynku. W windzie nagle zgasło światło i mechanizm stanął – mężczyzna zrozumiał, że nastąpiła awaria prądu, która zabiła też jego żonę.",
    },
    {
        "id": 3,
        "title": "Pustynny pechowiec",
        "category": "Klasyczne",
        "difficulty": "medium",
        "story": "Mężczyzna znajduje się na środku pustyni z plecakiem na plecach. Jest martwy. Gdyby otworzył plecak, wciąż by żył.",
        "solution": "W plecaku znajdował się spadochron, który nie otworzył się podczas skoku.",
    },
    {
        "id": 4,
        "title": "Krótka zapałka",
        "category": "Klasyczne",
        "difficulty": "hard",
        "story": "Całkowicie nagi mężczyzna leży martwy na środku spalonej słońcem pustyni. W dłoni trzyma ułamaną zapałkę. W pobliżu nie ma żadnych śladów stóp.",
        "solution": "Mężczyzna leciał balonem turystycznym z grupą ludzi. Balon nagle zaczął tracić wysokość i groziło im rozbicie. Wyrzucili za burtę wszystkie bagaże, a potem nawet ubrania, ale to nie pomogło. Zdecydowali się ciągnąć zapałki – ten, kto wyciągnie najkrótszą, musi wyskoczyć, by uratować resztę. Ten mężczyzna miał pecha.",
    },
    {
        "id": 5,
        "title": "Ostatnia audycja",
        "category": "Klasyczne",
        "difficulty": "easy",
        "story": "Kobieta włączyła radio w swoim samochodzie i natychmiast zrozumiała, że jej mąż nie żyje.",
        "solution": "Jej mąż był prezenterem radiowym prowadzącym audycję na żywo. Po włączeniu radia kobieta usłyszała strzały, krzyki i nagłą ciszę w studiu nagraniowym.",
    },
    {
        "id": 6,
        "title": "Romeo i Julia",
        "category": "Klasyczne",
        "difficulty": "hard",
        "story": "Martwy Romeo i martwa Julia leżą na podłodze w kałuży wody. Obok leży rozbite szkło. Okno jest szeroko otwarte.",
        "solution": "Romeo i Julia to złote rybki. Kot wszedł przez otwarte okno i zrzucił ich akwarium ze stołu na podłogę. Szkło to rozbite akwarium, a kałuża to woda z niego.",
    },
    {
        "id": 7,
        "title": "Dom bez grosza",
        "category": "PKO Bank Polski",
        "difficulty": "easy",
        "story": "Marek odebrał klucze do wymarzonego domu, chociaż rano na jego koncie było równe zero złotych.",
        "solution": "Marek skorzystał z doskonałego doradztwa w PKO Banku Polskim i otrzymał kredyt hipoteczny, który sfinansował zakup.",
    },
    {
        "id": 8,
        "title": "Nocne Słońce",
        "category": "Tauron",
        "difficulty": "medium",
        "story": "W całym mieście zgasły światła z powodu potężnej burzy, ale u Ani w domu wszystko działało normalnie.",
        "solution": "Ania posiadała nowoczesne panele fotowoltaiczne i pojemny magazyn energii dostarczony przez Tauron, co uniezależniło ją od awarii sieci.",
    }
]

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
        "Jesteś prowadzącym grę Dark Stories po polsku. Znasz pełną historię.\n\n"
        f"TYTUŁ: {story['title']}\n"
        f"ZARYS: {story['story']}\n"
        f"ROZWIĄZANIE: {story['solution']}\n\n"
        "Odpowiadaj TYLKO: Tak, Nie, Nie ma to znaczenia, Zgadłeś.\n"
        f"Pytanie: {req.question}"
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
        kontekst = "Stwórz pozytywną zagadkę o sukcesie finansowym, oszczędzaniu lub innowacjach w PKO BP."
    elif req.category == "Tauron":
        kontekst = "Stwórz pozytywną zagadkę o czystej energii, fotowoltaice lub innowacjach Taurona."
    else:
        kontekst = "Stwórz mroczną, zaskakującą zagadkę w stylu klasycznych 'Czarnych Historii'."

    prompt = (
        f"{kontekst}\n"
        f"Poziom trudności: {req.difficulty}\n"
        'Zwróć wynik WYŁĄCZNIE jako JSON używając dokładnie tych kluczy: "title", "difficulty", "category", "story", "solution".\n'
        'Zarys ma być krótki, rozwiązanie logiczne.'
    )

    # Wymuszenie czystego JSONa w nowym API od Google
    response = client.models.generate_content(
        model=GEMINI_MODEL, 
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.7
        )
    )
    
    text = response.text.strip().replace("```json", "").replace("```", "").strip()
    data = json.loads(text)
    data["id"] = "random"
    # Upewniamy się, że kategoria to ta wybrana
    data["category"] = req.category 
    return data

frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")

@app.get("/")
def serve_index():
    return FileResponse(str(frontend_path / "index.html"))