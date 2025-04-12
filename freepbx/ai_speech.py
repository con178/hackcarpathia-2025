#!/venvs/.venv/bin/python3
import speech_recognition as sr

r = sr.Recognizer()
# Opcjonalnie możesz dostosować wartość pause_threshold (domyślnie około 0.8 sekundy)
r.pause_threshold = 0.8  # lub większa wartość, jeśli chcesz bardziej opóźnione zakończenie

def record_text(audio_file_path):
    try:
        # Używamy AudioFile do odczytania nagrania (w środowisku AGI nagranie powinno być wykonane przez Asterisk)
        with sr.AudioFile(audio_file_path) as source:
            audio_data = r.record(source)
        MyText = r.recognize_google(audio_data, language='pl')
        return MyText
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Nie udało się rozpoznać mowy")
    return ""