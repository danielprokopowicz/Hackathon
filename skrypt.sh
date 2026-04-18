#!/bin/bash

echo "Tworzenie wirtualnego środowiska (venv)..."
python3 -m venv venv

echo "Aktywacja środowiska..."
source venv/bin/activate

echo "Instalacja zależności..."
pip install -r requirements.txt

echo "Uruchamianie aplikacji..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000