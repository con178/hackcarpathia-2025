#!/venvs/.venv/bin/python3
import os
import time
import shutil
import subprocess
import sys
import asyncio
import edge_tts
# Funkcję record_text można usunąć, jeśli nie jest już potrzebna,
# ale zostanie ona pozostawiona dla ewentualnych innych zastosowań.
from ai_speech import record_text
from ai_ollama import ask_ai

async def generate_tts(text, mp3_file):
    """
    Asynchronicznie generuje plik MP3 przy użyciu edge_tts i głosu 'pl-PL-ZofiaNeural'.
    """
    communicate = edge_tts.Communicate(text, 'pl-PL-ZofiaNeural')
    await communicate.save(mp3_file)

def main():
    # Jeśli nie potrzebujesz nagrywania wypowiedzi użytkownika,
    # można pominąć odczytywanie pliku.
    input_audio_file = "/tmp/caller_input.wav"
    user_text = record_text(input_audio_file)

    # Nazwy plików wynikowych (bez timestampów)
    mp3_file = "/tmp/ai_response.mp3"
    ulaw_file = "/var/lib/asterisk/sounds/ai_response.ulaw"  # Stała nazwa pliku

    response_text = ask_ai(user_text)
    # Generowanie pliku MP3 przy użyciu edge_tts
    try:
        asyncio.run(generate_tts(response_text, mp3_file))
    except Exception as e:
        print("Błąd podczas generowania mowy:", e, file=sys.stderr)
        sys.exit(1)

    # Konwersja pliku MP3 do formatu ulaw (wav, 8000Hz, mono) z użyciem ffmpeg
    result = subprocess.run([
        "ffmpeg", "-y", "-i", mp3_file,
        "-ar", "8000", "-ac", "1",
        "-f", "wav", "-c:a", "pcm_mulaw",
        ulaw_file
    ], capture_output=True, text=True)

    # Komunikaty diagnostyczne wysyłamy na stderr
    print(result.stdout, file=sys.stderr)
    print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print("ffmpeg zwrócił błąd:", result.returncode, file=sys.stderr)

    # Wypisanie AGI command (jedyna linia wyjścia) ustawiającej zmienną odpowiedzi
    print("SET VARIABLE response_file ai_response")
    sys.stdout.flush()

if __name__ == '__main__':
    main()