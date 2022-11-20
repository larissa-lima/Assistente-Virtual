# Bibliotecas necessárias
import speech_recognition as sr

# Reconhecimento de voz
r = sr.Recognizer()

# Microfone habilitado
with sr.Microphone() as source:
    
    while True:
        audio = r.listen(source)      
        print(r.recognize_google(audio, language='pt')) # Detecta o audio em português
        
