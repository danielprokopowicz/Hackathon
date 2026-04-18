# Dark Stories 🕯️

Webowa gra w stylu Dark Stories z podpiętym AI (Claude) odpowiadającym na pytania Tak/Nie.

## Struktura projektu

```
dark-stories/
├── backend/
│   ├── main.py            # FastAPI server + Anthropic API
│   └── requirements.txt
└── frontend/
    ├── index.html
    └── static/
        ├── css/style.css
        └── js/app.js
```

## Uruchomienie

### 1. Klucz API

Ustaw zmienną środowiskową z kluczem Anthropic:

```bash
# Linux / macOS
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

Klucz API możesz wygenerować na: https://console.anthropic.com/

### 2. Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Serwer będzie dostępny na: http://localhost:8000

Frontend jest serwowany automatycznie przez FastAPI ze ścieżki `../frontend`.

### 3. Gotowe!

Otwórz przeglądarkę i wejdź na: **http://localhost:8000**

---

## API Endpoints

| Metoda | Ścieżka | Opis |
|--------|---------|------|
| GET | `/api/stories` | Lista historyjek (bez rozwiązań) |
| POST | `/api/ask` | Zadaj pytanie do historyjki |
| POST | `/api/generate` | Wygeneruj losową historyjkę przez AI |

### Przykład `/api/ask`

```json
POST /api/ask
{
  "story_id": 1,
  "question": "Czy ofiara znała sprawcę?"
}
```

Odpowiedź:
```json
{
  "answer": "Tak. To ważny trop."
}
```

### Przykład dla historyjki wygenerowanej przez AI

```json
POST /api/ask
{
  "story_id": "random",
  "story_data": {
    "title": "Tytuł",
    "story": "Zarys...",
    "solution": "Rozwiązanie..."
  },
  "question": "Czy to było zabójstwo?"
}
```

---

## Jak to działa

1. **Lista historyjek** – 6 predefiniowanych zagadek w 3 poziomach trudności
2. **Widok gry** – po lewej zarys historii, po prawej czat z AI
3. **AI odpowiada** – Claude zna pełne rozwiązanie i odpowiada Tak/Nie/Nie ma to znaczenia
4. **Rozwiązanie** – ukryte, dostępne po kliknięciu przycisku
5. **Generator losowy** – AI generuje nową oryginalną historyjkę on-the-fly

## Dodawanie własnych historyjek

W pliku `backend/main.py` w liście `STORIES` dodaj nowy obiekt:

```python
{
    "id": 7,
    "title": "Tytuł zagadki",
    "difficulty": "easy",  # easy / medium / hard
    "story": "Krótki zarys historii widoczny dla gracza...",
    "solution": "Pełne rozwiązanie znane tylko AI...",
}
```
