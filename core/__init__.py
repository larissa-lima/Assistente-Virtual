import datetime
import webbrowser

from bs4 import BeautifulSoup

class SystemInfo:
    
    def __init__(self):
        pass

    @staticmethod
    def get_time():
        agora = datetime.datetime.now()
        resposta = 'São {} horas e {} minutos'.format(agora.hour, agora.minute)
        return resposta