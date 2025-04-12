#!/venvs/.venv/bin/python3
import ollama
import pandas as pd
import find_specialist
from geopy.distance import geodesic
import google_api as g_map


def ask_ai(user_question):
    prompt = """Jesteś Agentem AI. Użytkownik mówi: "%s"

Zachowuj się zgodnie z poniższymi zasadami:

1. Jeśli użytkownik chce udać się do lekarza specjalisty i interesuje go najkrótszy możliwy termin:
    - Odpowiedz wyłącznie nazwą większego miasta od tego który podał użytkownik w tym samym województwie z którego pochodzi oraz nazwą specjalizacji oddzielone przecinkiem. 
    - Przykład: Warszawa, Kardiolog czy Rzeszów Pneumolog

2. Jeśli użytkownik chce znaleźć przychodnię z małą kolejką:
    - Zwróć tylko nazwę lokalizacji, którą użytkownik podał (adres, ulica, okolica, punkt orientacyjny).
    - Przykład: Kwiatkowskiego 4 Rzeszów lub Parafia Królowej Jadwigi Rzeszów

Twoja odpowiedź musi być w formacie (nazwa_miasta, nazwa_specjalizacji) lub (adres) 
Nie pisz nic oprócz odpowiedzi we wskazanym formacie, bez żadnych opisów
    """ % user_question

    # Wywołanie modelu Bielik
    response = ollama.chat(
        model='SpeakLeash/bielik-11b-v2.3-instruct:Q4_K_M',
        messages=[{"role": "user", "content": prompt}])

    # sprawdzanie który case obsługujemy
    what_to_search = response['message']['content'].replace(')', '').replace('(', '')
    print(what_to_search)
    if ',' in what_to_search:
        try:  # case z szukaniem specjalisty
            specialist_name = what_to_search.split(',')[1].replace(' ', '')
            city_name = what_to_search.split(',')[0].replace(' ', '')
            print(specialist_name)

            found_specialists = find_specialist.return_specialists_times(city=city_name, doctor=specialist_name)
            print(found_specialists)
            prompt_for_recommending_specialist = """Jesteś Agentem AI, użytkownik wcześniej powiedział że %s
            ty wiesz że 

            %s

            zaproponuj mu umówienie się do specialisty, podaj nazwę kliniki, numer 
            telefonu do kliniki oraz czas oczekiwania
            """ % (user_question, found_specialists)

            final_response = ollama.chat(
                model='SpeakLeash/bielik-11b-v2.3-instruct:Q4_K_M',
                messages=[{"role": "user", "content": prompt_for_recommending_specialist}])
            final_response = final_response['message']['content']
            print(final_response)
        except Exception as e:
            final_response = "Napotkałem problem, nie mogę znaleźć specjalisty"
            print(e)


    else:
        try:  # case z sprawdzaniem obłożenia w przychodni
            print('case z sprawdzaniem obłożenia w przychodni')
            # Load log data
            df = pd.read_csv("cameras_prod/log_data.log", header=None, encoding="windows-1250",
                             names=["latitude", "longitude", "name", "people_in_queque", "timestamp"])

            print(df.head(1).to_string())
            print("przychodnie załadowane")

            # Reference point
            try:
                reference_point = g_map(what_to_search)
            except:
                reference_point = (50.03046007569683, 22.017204344515797)

            print(reference_point)
            # Calculate distance and filter within 1 km
            df["distance_km"] = df.apply(lambda row: geodesic(reference_point,
                                                              (row["latitude"], row["longitude"])).km, axis=1)

            # Filter within 1 km and return top 1 with lowest queue
            nearest_with_lowest_queue = df[df["distance_km"] <= 1].nsmallest(1, "people_in_queque").to_string()

            print(nearest_with_lowest_queue)

            prompt_for_finding_clinic = """Jesteś Agentem AI, użytkwonik wcześniej powiedział że %s
            ty wiesz że 

            %s

            zaproponuj mu wizytę w przychodni, powiedz ile aktualnie jest osób w kolejce
            """ % (user_question, nearest_with_lowest_queue)

            final_response = ollama.chat(
                model='SpeakLeash/bielik-11b-v2.3-instruct:Q4_K_M',
                messages=[{"role": "user", "content": prompt_for_finding_clinic}])
            final_response = final_response['message']['content']
            print(final_response)

        except:
            final_response = "Napotkałem problem, nie mogę znaleźćprzychodni z najmniejszą kolejką"

    return final_response





