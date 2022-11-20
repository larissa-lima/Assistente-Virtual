# Síntese de voz

import pyttsx3
engine = pyttsx3.init()

#Definindo voz em PT-BR
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-2].id)

engine.say("Cachorro caramelo patrimônio brasileiro")
engine.runAndWait()