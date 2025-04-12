#!/venvs/.venv/bin/python3
import ollama

def ask_ai(user_question):
        print(user_question)
        # Wywołanie modelu Bielik
        response = ollama.chat(
                model='SpeakLeash/bielik-11b-v2.3-instruct:Q4_K_M',
                messages=[{"role": "user", "content": user_question}])

        # Wyświetlenie odpowiedzi
        print("Odpowiedź:", response['message']['content'])
        return response['message']['content']