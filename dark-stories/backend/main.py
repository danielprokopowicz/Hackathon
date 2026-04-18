from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import json
import os
import random
from pathlib import Path

load_dotenv()

app = FastAPI(title="Dark Stories API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = "gemma-3-27b-it"

STORIES = [
    {
        "id": 1,
        "title": "Ostatni posilek",
        "difficulty": "easy",
        "category": "dark",
        "story": "Mezczyzna zamowil zupe w restauracji. Sprobowal jej raz, wyszedl na zewnatrz i zastrzelil sie.",
        "solution": "Mezczyzna byl rozbitkiem, ktory przezyil katastrofe statku razem z partnerem. Gdy kelner przynioss mu zupe, smak sprawil ze przypomnial sobie, z czego byla zrobiona zupa ktora jadl na tratwie - z miesa swojego martwego przyjaciela. Nie mogl zyc z ta wiedza.",
    },
    {
        "id": 2,
        "title": "Muzyk",
        "difficulty": "easy",
        "category": "dark",
        "story": "Mezczyzna zagral melodie i wszyscy w pokoju zamarli w bezruchu.",
        "solution": "Byl to muzyk wojskowy grajacy hymn narodowy na pogrzebie wojskowym. Obecni zolnierze i goscie staneli na bacznosc zgodnie z protokolem.",
    },
    {
        "id": 3,
        "title": "Winda",
        "difficulty": "medium",
        "category": "dark",
        "story": "Kobieta mieszka na 30. pietrze. Rano jedzie winda na dol i idzie do pracy. Wieczorem jedzie winda tylko do 15. pietra, a reszte drogi pokonuje pieszo - chyba ze pada deszcz lub ktos jest z nia w windzie.",
        "solution": "Kobieta jest osoba niskiego wzrostu i nie dossiega przycisku wyzszego niz 15. pietro. Gdy pada deszcz, ma przy sobie parasol i moze nim nacisnac wyzszy przycisk. Gdy ktos jest z nia w windzie, prosi go o nacisniecie przycisku 30.",
    },
    {
        "id": 4,
        "title": "Trzecia smierc",
        "difficulty": "medium",
        "category": "dark",
        "story": "Detektyw przybywa na miejsce zbrodni. Widzi troje zwlok i garsc kart do gry na stole. Natychmiast wie, ze to samobojstwa.",
        "solution": "Troje przyjaciol zawarlo pakt: kto przegra w pokera, odbierze sobie zycie. Wszyscy troje dostali rownie slabe karty i uznali, ze kazdy z nich przegral. Detektyw, widzac rozklad kart, zrozumial ze byl to remis - wszyscy poczuli sie przegranymi jednoczesnie.",
    },
    {
        "id": 5,
        "title": "Pokoj z widokiem",
        "difficulty": "hard",
        "category": "dark",
        "story": "Kobieta zamieszkala w hotelu na 10. pietrze. Rano, lezac w lozku, uslyszala deszcz. Otworzyala okno, spojrzala w dol i skoczyla.",
        "solution": "Kobieta byla niewidoma od urodzenia i glucha od kilku lat. W tej nocy odzyskala sluch - uslyszala deszcz po raz pierwszy od lat. Rano, gdy otworzyala okno, odzyskala tez wzrok. Ujrzala swiat po raz pierwszy w zyciu. Widok z 10. pietra byl tak przytlaczajacy, ze stracila rownowage i spadla - byl to wypadek, nie samobojstwo.",
    },
    {
        "id": 6,
        "title": "Telegram",
        "difficulty": "hard",
        "category": "dark",
        "story": "Mezczyzna otrzymal telegram. Przeczytal go, usmiechnal sie i zastrzelil swojego najlepszego przyjaciela.",
        "solution": "Obaj mezczyzni zostali porwani przez terrorystow, ktorzy zapowiedzieli tortury na smierc. Przyjaciel przemycil telegram: 'Zrob to dla mnie. Prosze.' Mezczyzna usmiechnal sie ze smutku - wiedzial, ze spelnia ostatnie zyczenie przyjaciela, oszczedzajac mu cierpien.",
    },
]

RANDOM_THEMES = {
    "dark": [
        "sobowtór", "amnezja", "fałszywa tożsamość", "choroba terminalna", "wypadek samochodowy",
        "katastrofa lotnicza", "tonięcie", "pożar", "trucizna", "wyrok śmierci",
        "więzienie", "szpital psychiatryczny", "klasztor", "latarnia morska", "dżungla",
        "śnieżyca", "epidemia", "oszustwo ubezpieczeniowe", "testament", "zaginięcie dziecka",
    ],
    "pko": [
        "turniej esportowy", "speed-run", "cheating w grze", "wirtualna waluta", "skin za milion",
        "streaming 24h", "uzależnienie od gier", "sponsor drużyny", "hackathon gamingowy", "VR headset",
        "subskrypcja premium", "ban konta", "guild war", "NFT w grze", "konto bankowe gracza",
    ],
    "tauron": [
        "blackout całego miasta", "inteligentny licznik", "farma wiatrowa w nocy", "panele solarne na dachu",
        "ładowarka EV", "AI zarządzające siecią", "kradzież prądu", "awaria elektrowni",
        "smart home bez prądu", "magazyn energii", "turbina wiatrowa", "hydroelektrownia",
        "inspektor sieci", "nielegalny kabel", "transformator",
    ],
}

GENERATE_PROMPTS = {
    "dark": (
        "Wygeneruj oryginalną, mroczną historyjkę-zagadkę do gry Dark Stories po polsku.\n"
        "Styl: tajemniczy, psychologiczny, zaskakujący. Może dotyczyć śmierci, zbrodni, niewyjaśnionych zdarzeń.\n"
        "Rozwiązanie powinno być logiczne ale zupełnie nieoczywiste — gracz musi zadać wiele pytań żeby dojść do prawdy.\n"
        "Wzoruj się na klasycznych zagadkach Dark Stories jak 'Ostatni posiłek' czy 'Winda'.\n"
    ),
    "pko": (
        "Wygeneruj oryginalną historyjkę-zagadkę do gry Dark Stories po polsku.\n"
        "TEMATYKA: gaming, gry wideo, esport, gracze, turnieje, wirtualne światy, mikrotransakcje, uzależnienie od gier, streamerzy.\n"
        "Historia ma być osadzona w świecie gier lub bankowości dla graczy (PKO BP XP Gaming).\n"
        "Może dotyczyć gracza, streamera, turnieju esportowego, wirtualnej waluty, in-game zakupów.\n"
        "Powinna być zaskakująca i wymagać zadania wielu pytań Tak/Nie żeby ją rozwiązać.\n"
    ),
    "tauron": (
        "Wygeneruj oryginalną historyjkę-zagadkę do gry Dark Stories po polsku.\n"
        "TEMATYKA: energia elektryczna, panele słoneczne, wiatraki, sieć energetyczna, prąd, odnawialne źródła energii, smart home, AI w energetyce, liczniki, elektrownie, blackout.\n"
        "Historia ma być osadzona w świecie energetyki lub technologii AI (Tauron AI Challenge).\n"
        "Może dotyczyć inżyniera energetyki, awarii sieci, inteligentnego domu, farmy wiatrowej, paneli PV.\n"
        "Powinna być zaskakująca i wymagać zadania wielu pytań Tak/Nie żeby ją rozwiązać.\n"
    ),
}


class QuestionRequest(BaseModel):
    story_id: int | str
    question: str
    story_data: dict | None = None


class HintRequest(BaseModel):
    story_id: int | str
    hint_num: int = 1
    max_hints: int = 3
    story_data: dict | None = None


class GenerateRequest(BaseModel):
    category: str = "dark"


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
        "Jestes prowadzacym gre Dark Stories po polsku. Znasz pelna historie i rozwiazanie zagadki.\n\n"
        f"TYTUL: {story['title']}\n"
        f"ZARYS HISTORII (widoczny dla gracza): {story['story']}\n"
        f"PELNE ROZWIAZANIE (tajne): {story['solution']}\n\n"
        "Zasady odpowiedzi:\n"
        "- Jesli gracz w swoim pytaniu/stwierdzeniu trafnie opisuje KLUCZOWE elementy pelnego rozwiazania (wie co sie stalo i dlaczego), odpowiedz TYLKO slowem: ROZWIAZANE\n"
        "- W przeciwnym razie odpowiadaj TYLKO jednym z: Tak, Nie, Nie ma to znaczenia, Tak i nie\n"
        "- Mozesz dodac maksymalnie jedno krotkie zdanie (do 8 slow) jako wskazowke - tylko jesli pytanie jest bardzo blisko rozwiazania (ale jeszcze nie ROZWIAZANE)\n"
        "- Nigdy nie zdradzaj rozwiazania wprost ani nie parafrazuj go\n"
        "- Odpowiadaj zgodnie z PELNYM rozwiazaniem, nie tylko zarysem\n"
        "- Zawsze odpowiadaj po polsku\n\n"
        f"Pytanie gracza: {req.question}"
    )

    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        answer = response.text
        if not answer:
            raise HTTPException(status_code=502, detail="Brak odpowiedzi od modelu AI")
        answer = answer.strip()
        solved = answer.upper().startswith("ROZWIAZANE")
        return {"answer": answer, "solved": solved}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Błąd API Gemini: {str(e)}")


@app.post("/api/hint")
def get_hint(req: HintRequest):
    if req.story_id == "random" and req.story_data:
        story = req.story_data
    else:
        story = next((s for s in STORIES if s["id"] == req.story_id), None)
        if not story:
            raise HTTPException(status_code=404, detail="Story not found")

    prompt = (
        "Jestes prowadzacym gre Dark Stories po polsku. Znasz pelna historie i rozwiazanie zagadki.\n\n"
        f"TYTUL: {story['title']}\n"
        f"ZARYS HISTORII (widoczny dla gracza): {story['story']}\n"
        f"PELNE ROZWIAZANIE (tajne): {story['solution']}\n\n"
        f"Gracz prosi o podpowiedz numer {req.hint_num} z {req.max_hints} dostepnych.\n"
        "Zasady podpowiedzi:\n"
        "- Napisz jedna krotka podpowiedz (max 2 zdania) ktora naprowadza gracza na rozwiazanie\n"
        "- Podpowiedz powinna byc tajemnicza ale pomocna\n"
        "- NIE zdradzaj rozwiazania wprost\n"
        "- Podpowiedzi powinny byc coraz bardziej konkretne (podpowiedz 1 = ogolna, ostatnia = bardzo konkretna)\n"
        "- Odpowiadaj po polsku\n"
        "- Zacznij od 'Wskazowka:' "
    )

    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        hint = response.text
        if not hint:
            raise HTTPException(status_code=502, detail="Brak odpowiedzi od modelu AI")
        return {"hint": hint.strip()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Błąd API Gemini: {str(e)}")


@app.post("/api/generate")
def generate_story(req: GenerateRequest):
    category = req.category if req.category in GENERATE_PROMPTS else "dark"
    base_prompt = GENERATE_PROMPTS[category]
    theme = random.choice(RANDOM_THEMES[category])

    prompt = (
        base_prompt
        + f"Motyw przewodni tej historii: '{theme}'. Użyj go kreatywnie.\n"
        + f"Losowy seed dla unikalności: {random.randint(10000, 99999)}\n"
        + "Odpowiedz TYLKO w formacie JSON, bez zadnego dodatkowego tekstu, bez backticks, bez komentarzy.\n"
        + 'Format: {"title":"...","difficulty":"easy|medium|hard","story":"...krotki tajemniczy zarys, max 2-3 zdania...","solution":"...pelne zaskakujace rozwiazanie..."}\n'
        + "Zarys ma byc niepelny i tajemniczy. Rozwiazanie powinno zaskakiwac i wyjasniać wszystkie elementy zarysu."
    )

    try:
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        text = response.text
        if not text:
            raise HTTPException(status_code=502, detail="Brak odpowiedzi od modelu AI")
        text = text.strip().replace("```json", "").replace("```", "").strip()
        data = json.loads(text)
        data["id"] = "random"
        data["category"] = category
        return data
    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail=f"Nieprawidłowy JSON od modelu AI: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Błąd API Gemini: {str(e)}")


frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")


@app.get("/")
def serve_index():
    return FileResponse(str(frontend_path / "index.html"))