import requests
from bs4 import BeautifulSoup
from google.colab import files
import pandas as pd

# Para usar o script
#   1) Alterar a quantidade de noticias de sua escolha na variavel qtnNoticias
      # PRECISA SER UM MULTIPLO DE 12

qtnNoticias = 600
noticiasColetadas = []

url = 'https://psb40.org.br/noticias/'
site = requests.get(url)

entendedorDeHtml = BeautifulSoup(site.text, 'html.parser')
h3ComTiuloEUrl = entendedorDeHtml.find_all('h3', class_='entry-title')
datas = entendedorDeHtml.find_all("time", class_="entry-date updated")
entendedorDeh3ComTiuloEUrl = BeautifulSoup(str(h3ComTiuloEUrl), 'html.parser')
urls = entendedorDeh3ComTiuloEUrl.find_all("a")
titulos = entendedorDeh3ComTiuloEUrl.find_all("a")
for titulo, data, link in zip(titulos, datas, urls):
      urlNoticia = link["href"]
      siteNoticia = requests.get(urlNoticia)

      entendedorDeHtmlNoticia = BeautifulSoup(siteNoticia.text, 'html.parser')

      divComConteudo = entendedorDeHtmlNoticia.find_all('div', class_='entry-content')

      entendedorDeHtmlDaDivDeConteudo = BeautifulSoup(str(divComConteudo), 'html.parser')

      paragrafos = entendedorDeHtmlDaDivDeConteudo.find_all('p', class_='')


      conteudoCompleto = ''

      for paragrafo in paragrafos:
          texto = paragrafo.get_text()
          conteudoCompleto = conteudoCompleto + texto

      noticia = {
            "Título": titulo.text.strip(),
            "Data": data.text.strip(),
            "URL": link["href"],
            "Conteudo": conteudoCompleto
        }

      noticiasColetadas.append(noticia)

urlProxPaginas = 'https://psb40.org.br/noticias/'

page = 2
qtnNoticias = qtnNoticias +12

while page != qtnNoticias/12:
  urlCompleta = urlProxPaginas + str(page) + '/'
  siteProxPagina = requests.get(urlCompleta)

  entendedorDeHtmlProxPagina = BeautifulSoup(site.text, 'html.parser')
  h3ComTiuloEUrlProxPagina = entendedorDeHtmlProxPagina.find_all('h3', class_='entry-title')
  datasProxPagina = entendedorDeHtmlProxPagina.find_all("time", class_="entry-date updated")
  entendedorDeh3ComTiuloEUrlProxPagina = BeautifulSoup(str(h3ComTiuloEUrlProxPagina), 'html.parser')
  urlsProxPagina = entendedorDeh3ComTiuloEUrlProxPagina.find_all("a")
  titulosProxPagina = entendedorDeh3ComTiuloEUrlProxPagina.find_all("a")

  for tituloProxPagina, dataProxPagina, linkProxPagina in zip(titulosProxPagina, datasProxPagina, urlsProxPagina):
        urlNoticiaProxPagina = linkProxPagina["href"]
        siteNoticiaProxPagina = requests.get(urlNoticiaProxPagina)

        entendedorDeHtmlNoticiaProxPagina = BeautifulSoup(siteNoticiaProxPagina.text, 'html.parser')

        divComConteudoProxPagina = entendedorDeHtmlNoticiaProxPagina.find_all('div', class_='entry-content')

        entendedorDeHtmlDaDivDeConteudoProxPagina = BeautifulSoup(str(divComConteudoProxPagina), 'html.parser')

        paragrafosProxPagina = entendedorDeHtmlDaDivDeConteudoProxPagina.find_all('p', class_='')


        conteudoCompletoProxPagina = ''
        for paragrafoProxPagina in paragrafosProxPagina:
            textoProxPagina = paragrafoProxPagina.get_text()
            conteudoCompletoProxPagina = conteudoCompletoProxPagina + textoProxPagina

        noticiaProxPagina = {
              "Título": tituloProxPagina.text.strip(),
              "Data": dataProxPagina.text.strip(),
              "URL": linkProxPagina["href"],
              "Conteudo": conteudoCompletoProxPagina
          }
        noticiasColetadas.append(noticiaProxPagina)

  page=page+1

nome_arquivo = "psb.csv"

df = pd.DataFrame(noticiasColetadas[0:], columns=noticiasColetadas[0])
df.to_csv(nome_arquivo, index=False)

print(f'Os dados foram salvos em {nome_arquivo}')

arquivo = pd.read_csv(nome_arquivo)

files.download(nome_arquivo)
arquivo