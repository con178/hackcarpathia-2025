import speech_recognition as sr
import pyttsx3
import os

r=sr.Recognizer()

print(os.getcwd())

def record_text():
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=5)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2, language = 'pl')
            return MyText 

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Unknown error")

    return ""
    

def output_text(text):
    f = open('output.txt', 'a', encoding='utf-8')
    f.write(text)
    f.write('\n')
    f.close()
    return

while(1):
    text = record_text()
    output_text(text)

    print("Output saved!")