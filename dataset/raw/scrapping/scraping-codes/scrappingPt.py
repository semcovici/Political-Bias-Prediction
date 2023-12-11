import requests
from bs4 import BeautifulSoup
from google.colab import files
import pandas as pd

# Para usar o script
#   1) Alterar a quantidade de noticias de sua escolha na variavel qtnNoticias
      # PRECISA SER UM MULTIPLO DE 13

qtnNoticias = 598
noticiasColetadas = []

url = 'https://pt.org.br/noticias/'
site = requests.get(url)

entendedorDeHtml = BeautifulSoup(site.text, 'html.parser')
titulos = entendedorDeHtml.find_all('h2', class_='news-card-title')
datas = entendedorDeHtml.find_all("time", class_="news-card-time")
urls = entendedorDeHtml.find_all("a", class_="news-card-link")

for titulo, data, link in zip(titulos, datas, urls):
      urlNoticia = link["href"]
      siteNoticia = requests.get(urlNoticia)

      entendedorDeHtmlNoticia = BeautifulSoup(siteNoticia.text, 'html.parser')

      divComConteudo = entendedorDeHtmlNoticia.find_all('div', class_='single-post-main-content')

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

urlProxPaginas = 'https://pt.org.br/noticias/page/'

page = 2
qtnNoticias = qtnNoticias +13
while page != qtnNoticias/13:
  urlCompleta = urlProxPaginas + str(page) + '/'
  siteProxPagina = requests.get(urlCompleta)

  entendedorDeHtmlProxPagina = BeautifulSoup(siteProxPagina.text, 'html.parser')
  titulosProxPagina = entendedorDeHtmlProxPagina.find_all('h2', class_='news-card-title')
  datasProxPagina = entendedorDeHtmlProxPagina.find_all("time", class_="news-card-time")
  urlsProxPagina = entendedorDeHtmlProxPagina.find_all("a", class_="news-card-link")

  for tituloProxPagina, dataProxPagina, linkProxPagina in zip(titulosProxPagina, datasProxPagina, urlsProxPagina):
        urlNoticiaProxPagina = linkProxPagina["href"]
        siteNoticiaProxPagina = requests.get(urlNoticiaProxPagina)

        entendedorDeHtmlNoticiaProxPagina = BeautifulSoup(siteNoticiaProxPagina.text, 'html.parser')

        divComConteudoProxPagina = entendedorDeHtmlNoticiaProxPagina.find_all('div', class_='single-post-main-content')

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

nome_arquivo = "pt.csv"

df = pd.DataFrame(noticiasColetadas[0:], columns=noticiasColetadas[0])
df.to_csv(nome_arquivo, index=False)

print(f'Os dados foram salvos em {nome_arquivo}')

arquivo = pd.read_csv(nome_arquivo)

files.download(nome_arquivo)
arquivo