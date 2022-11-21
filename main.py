import argparse
import queue
import sys
import sounddevice as sd
import pyttsx3
import json
import core
import webbrowser as browser
import urllib.request, json, requests

from bs4 import BeautifulSoup
from requests import get

'''

# Reconhecimento de voz Via Google:

import speech_recognition as sr
import vosk as v

r = sr.Recognizer()

# Microfone habilitado
with sr.Microphone() as source:
    
    while True:
        audio = r.listen(source)      
        print(r.recognize_google(audio, language='pt')) # Detecta o audio em português

'''

engine = pyttsx3.init()

from vosk import Model, KaldiRecognizer

# Reconhecimento de Fala
def speak(text):
    #Definindo voz em PT-BR
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[-2].id)
    engine.say(text)
    engine.runAndWait()

# Funções com API

def clima(cidade):
	token = '43a32010d6289258619902d62daf316f'
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	complete_url = base_url + "appid=" + token + "&q=" + cidade
	response = requests.get(complete_url)
	retorno = response.json()
	if retorno["cod"] == 200:
	    valor = retorno["main"]
icurrent_temperature = valor["temp"]
	    current_humidiy = valor["humidity"]
	    tempo = retorno["weather"]
	    weather_description = tempo[0]["description"]
	    clima = (f"Em {cidade} a temperatura é de {str(int(current_temperature - 273.15))} graus celcius e humidade de {str(current_humidiy)} %")
	    speak(clima)
	else:
		speak('Erro de compreensão, favor repetir')
	

# Loop do reconhecimento de fala, retirado da documentação do VOSK + adaptações
q = queue.Queue()

def int_or_str(text):
    '''Helper function for argument parsing.'''
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    '''This is called (from a separate thread) for each audio block.'''
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = Model(lang='pt')

    if args.filename:
        dump_fn = open(args.filename, 'wb')
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype='int16', channels=1, callback=callback):
        print('#' * 80)
        print('Pressione CTRL+C para parar de captar audio')
        print('#' * 80)

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result = json.loads(result)

                if result is not None:
                    text = result['text']

                    print(text)
                    # speak(text)

                    # Encerrar Assistente
                    if text == 'fechar assistente':
                    	sys.exit()

                    # Horario Atual
                    elif text == 'que horas são' or text == 'me diga as horas':
                        speak(core.SystemInfo.get_time())

                    # Musicas Spotify
                    elif text == 'musicas para limpar casa':
                        browser.open('https://open.spotify.com/playlist/6IUF76TPaDf27Ckc6cbtab?si=111cc1c70a5b4c48')

                    # Pesquisa de Clima
                    elif text == 'clima em curitiba':
                        text = text.replace('clima', '')
                        text = text.replace('em','')
                        clima(text[2:])

                    elif text == 'desligar computador em uma hora':
                        os.system("shutdown -s -t 3600")              
                    elif text == 'desligar computador em meia hora':
                        os.system("shutdown -s -t 1800")
                    elif text == 'desligar computador agora':
                        os.system("shutdown -s -t 5")
                    elif text == 'cancelar desligamento':
                        os.system("shutdown -a")

#            if dump_fn is not None:
#                dump_fn.write(data)
#


except KeyboardInterrupt:
    print('\nTerminamos')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))