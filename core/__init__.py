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

    def noticias():
	site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
	noticias = BeautifulSoup(site.text, 'html.parser')
	for item in noticias.findAll('item')[:5]:
		mensagem = item.title.text
        return mensagem

    def cotacao(moeda):
        requisicao = get(f'https://economia.awesomeapi.com.br/all/{moeda}-BRL')
        cotacao = requisicao.json()
        nome = cotacao[moeda]['name']
        data = cotacao[moeda]['create_date']
        valor = cotacao[moeda]['bid']
        cria_audio("cotacao.mp3", f"Cotação do {nome} em {data} é {valor}")