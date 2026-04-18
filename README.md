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

## 🔗 Linki
- **🎬 Wideo (Demo) - YouTube:** https://youtu.be/BezeR4qzNyU

---

## 💡 O Projekcie (MVP)

### Problem
Współcześni użytkownicy ignorują tradycyjne treści edukacyjne. Długie poradniki finansowe czy artykuły o oszczędzaniu przegrywają walkę o uwagę z TikTokiem i grami mobilnymi. Użytkownicy pragną szybkich, interaktywnych pętli z informacją zwrotną.

### Nasze Rozwiązanie: Mystery Solver
Przekształciliśmy klasyczną grę na myślenie ("Dark Stories") w potężne narzędzie edukacyjne oparte na GenAI. 
Gracze wcielają się w detektywów, zadając Sędziemu AI pytania, na które może on odpowiedzieć tylko "Tak", "Nie" lub "Nie ma znaczenia". Ich celem jest rozwiązanie absurdalnych, pozornie nielogicznych zagadek. Haczyk? Oprócz klasycznych Dark Stories te zagadki są także głęboko osadzone w rzeczywistych scenariuszach: atakach phishingowych, błędach instalacji fotowoltaicznych czy pułapkach finansowych.

Po rozwiązaniu zagadki, gracze odblokowują **"Pigułkę Wiedzy"** — krótką, bardzo wartościową ciekawostkę edukacyjną.

### Kluczowe Funkcje
* 🧠 **Mistrz Gry AI:** System zasilany przez Google GenAI pełni rolę bezstronnego sędziego, dynamicznie analizując pytania graczy w czasie rzeczywistym.
* 🎲 **Dwa Tryby Gry:** 
  * **Współpraca:** Zespół wspólnie próbuje rozwikłać sprawę - bez limitu czasu.
  * **Rywalizacja (do 8 graczy):** Tury z limitem czasowym. Wygrywa ten, kto pierwszy dojdzie do prawdy.
* ⚡ **Generowanie Spraw na Żywo:** Dedykowany generator AI tworzy nieskończoną liczbę nowych, unikalnych zagadek na żądanie, dopasowanych do konkretnych kategorii.
* 🏷️ **Dynamiczne Filtry i Karty 3D:** W pełni responsywny frontend napisany w JS z animacjami kart 3D dla płynnej eksploracji bazy.

---

## ⚖️ Spełnienie Kryteriów Oceny (Checklist)

* **Innowacyjność:** Zamiast nudnych quizów, wykorzystujemy myślenie lateralne i sztuczną inteligencję do grywalizacji wiedzy. Użytkownicy chcą rozwiązać zagadkę, co sprawia, że edukacyjna puenta na końcu jest traktowana jako nagroda, a nie obowiązek.
* **Wartość Dodana:** Aplikacja buduje nawyki. Krótkie rundy idealnie wpasowują się w czas wolny, przy okazji ucząc kluczowych nawyków z zakresu bezpieczeństwa finansowego i efektywności energetycznej.
* **Kwestie Techniczne:** Czysta, lekka architektura. Backend w FastAPI zapewnia szybkie wnioskowanie AI poprzez Google GenAI SDK, współpracując z bardzo wydajnym frontendem (HTML/JS/CSS).
* **Kompletność:** To w pełni funkcjonalne MVP (end-to-end). Posiada bazę 36 starannie przygotowanych historii, integrację AI w czasie rzeczywistym, zarządzanie stanem gry dla wielu graczy oraz dopracowany interfejs.

---

## 🛠️ Technologie
- **Backend:** Python, FastAPI
- **Integracja AI:** Google GenAI SDK (`gemma-3-27b-it`)
- **Frontend:** HTML5, CSS3, JavaScript

---

## 🚀 Jak uruchomić projekt:

### Przygotowanie

1. **Włącz Docker Engine**  
Upewnij się, że aplikacja Docker Desktop jest włączona i działa w tle - powinien być widoczny status "Engine running"
<br></br>

2. **Wygeneruj klucz API:**  
    * Zaloguj się na stronie Google AI Studio,
    * Wejdź w zakładkę 'API keys', a następnie kliknij w przycisk 'Create API key',
    * Podaj dowolną nazwę oraz w sekcji 'Choose an imported project' wybierz 'Default Gemini Project',
    * Kliknij przycisk 'Create key',
    * Skopiuj zawartość pod wierszem 'API Key'.

### Uruchamianie projektu

1. **Sklonuj Repozytorium**  
Otwórz terminal i sklonuj repozytorium na swój komputer:
```git clone <LINK DO REPO>```
<br></br>
2. **Przejdź do głównego folderu**  
Wejdź do głównego katalogu, poleceniem:
```cd Hackathon```
<br></br>
3. **Skonfiguruj klucz API**  
Nasza aplikacja korzysta z modelu Google Gemini, dlatego potrzebuje klucza API do działania.
   * Otwórz plik, zlokalizowany w głównym katalogu projektu (Hackathon), ```docker-compose.yml``` w dowolnym edytorze tekstu,
   * Znajdź sekcję ```environment:```,
   * Podmień wartość w linijce ```GEMINI_API_KEY=XXXX```, zastępując 'XXXX' swoim wygenerowanym kluczem API z Google AI Studio.
<br></br>
4. **Uruchom aplikację**  
Będąc w terminalu w folderze projektu, wpisz poniższą komendę:
```docker compose up -d```  
Docker pobierze niezbędne pliki i uruchomi środowisko w tle.
<br></br>

5. **Korzystaj z aplikacji**  
Aplikacja jest teraz dostępna w przeglądarce po wpisaniu:```localhost:8000```    
**(Aby wyłączyć aplikację, należy wpisać w terminalu: ```docker compose down```)**