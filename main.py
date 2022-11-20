# Bibliotecas necessárias
import speech_recognition as sr

# Reconhecimento de voz
r = sr.Recognizer()

# Microfone habilitado
with sr.Microphone() as source:
    audio = r.listen(source)
    
    print(r.recognize_google(audio))
