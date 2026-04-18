# 🕵️‍♂️ Rozwikłaj.To - Edycja Hackathon 

> **ETHSilesia 2026 Hackathon Submission**
> Grywalizacyjna aplikacja edukacyjna end-to-end napędzana przez GenAI.

## 🎯 Wybrane Ścieżki / Bounties
- **PKO XP: Gaming**
- **AI Challenge powered by Tauron**

## 👥 Członkowie Zespołu
- Daniel Prokopowicz
- Michał Glimos
- Wojciech Pilch
- Jakub Frydrych
- Szymon Molenda

## 🔗 Ważne Linki
- **🎬 Wideo (Pitch & Demo) - YouTube:** [Link do YouTube]
- **📊 Prezentacja (Pitch Deck):** [Link do prezentacji]
- **🌐 Działające Demo:** [Link, jeśli hostujecie aplikację np. na Vercel/Render]

---

## 💡 O Projekcie (MVP)

### Problem
Współcześni użytkownicy ignorują tradycyjne treści edukacyjne. Długie poradniki finansowe czy artykuły o oszczędzaniu przegrywają walkę o uwagę z TikTokiem i grami mobilnymi. Użytkownicy pragną szybkich, interaktywnych pętli z natychmiastową informacją zwrotną.

### Nasze Rozwiązanie: Mystery Solver
Przekształciliśmy klasyczną grę na myślenie ("Dark Stories") w potężne narzędzie edukacyjne oparte na GenAI. 
Gracze wcielają się w detektywów, zadając Sędziemu AI pytania, na które może on odpowiedzieć tylko "Tak", "Nie" lub "Nie ma znaczenia". Ich celem jest rozwiązanie absurdalnych, pozornie nielogicznych zagadek. Haczyk? Oprócz klasycznych Dark Stories te zagadki są także głęboko osadzone w rzeczywistych scenariuszach: atakach phishingowych, błędach instalacji fotowoltaicznych czy pułapkach finansowych.

Po rozwiązaniu zagadki, gracze odblokowują **"Pigułkę Wiedzy"** — krótką, bardzo wartościową ciekawostkę edukacyjną od sponsora (PKO BP lub Tauron).

### Kluczowe Funkcje
* 🧠 **Mistrz Gry AI:** System zasilany przez Google GenAI pełni rolę bezstronnego sędziego, dynamicznie analizując pytania graczy w czasie rzeczywistym.
* 🎲 **Dwa Tryby Gry:** * **Współpraca:** Zespół wspólnie próbuje rozwikłać sprawę - bez limitu czasu.
  * **Rywalizacja (do 8 graczy):** Tury z limitem czasowym. Wygrywa ten, kto pierwszy dojdzie do prawdy.
* ⚡ **Generowanie Spraw na Żywo:** Dedykowany generator AI tworzy nieskończoną liczbę nowych, unikalnych zagadek na żądanie, dopasowanych do konkretnych kategorii sponsorów.
* 🏷️ **Dynamiczne Filtry i Karty 3D:** W pełni responsywny frontend napisany w Vanilla JS z animacjami kart 3D dla płynnej eksploracji bazy.

---

## ⚖️ Spełnienie Kryteriów Oceny (Checklist)

* **Innowacyjność:** Zamiast nudnych quizów, wykorzystujemy myślenie lateralne i sztuczną inteligencję do grywalizacji wiedzy. Użytkownicy *chcą* rozwiązać zagadkę, co sprawia, że edukacyjna puenta na końcu jest traktowana jako nagroda, a nie obowiązek.
* **Wartość Dodana:** Aplikacja buduje nawyki. Krótkie rundy idealnie wpasowują się w czas dojazdów do pracy, "przypadkiem" ucząc kluczowych nawyków z zakresu bezpieczeństwa finansowego i efektywności energetycznej.
* **Kwestie Techniczne:** Czysta, lekka architektura. Backend w FastAPI zapewnia szybkie wnioskowanie AI poprzez Google GenAI SDK, współpracując z bardzo wydajnym frontendem (HTML/JS/CSS) pozbawionym ciężkich frameworków.
* **Kompletność:** To w pełni funkcjonalne MVP (end-to-end). Posiada bazę 36 starannie przygotowanych historii, integrację AI w czasie rzeczywistym, zarządzanie stanem gry dla wielu graczy oraz dopracowany interfejs.

---

## 🛠️ Technologie (Tech Stack)
- **Backend:** Python, FastAPI, Uvicorn
- **Integracja AI:** Google GenAI SDK (`gemma-3-27b-it`)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Baza Danych:** Lokalny plik JSON (gotowy do łatwego skalowania do NoSQL)

---

## 🚀 Jak uruchomić lokalnie

1. **Sklonuj repozytorium:**
   ```bash
   git clone [TWÓJ LINK DO GITHUBA]
   cd [NAZWA FOLDERU]
Zainstaluj zależności:

Bash
pip install -r requirements.txt
Skonfiguruj klucz API:
Upewnij się, że Twój klucz API Google GenAI jest podany w pliku backend/main.py. (Uwaga: w środowisku produkcyjnym klucz powinien zostać przeniesiony do pliku .env).

Uruchom serwer backendowy:

Bash
cd backend
python -m uvicorn main:app --reload
Zagraj!
Otwórz przeglądarkę i wejdź pod adres http://127.0.0.1:8000.