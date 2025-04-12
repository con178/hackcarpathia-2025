import asyncio
import edge_tts

text = 'Witaj, jeśli potrzebujesz wizyty u lekarza pierwszego kontaktu polecam przychodnię "Kwiatuszek". Znajduje się 1km od twojej lokalizacji. Aktualnie w kolejce jest tylko 5 osób a w przychodni jest dwóch lekarzy pierwszego kontaktu.'

async def amain() -> None:
    communicate = edge_tts.Communicate(text, 'pl-PL-ZofiaNeural')
    await communicate.save('output.mp3')

loop = asyncio.get_event_loop_policy().get_event_loop()
try:
    loop.run_until_complete(amain())
finally:
    loop.close()