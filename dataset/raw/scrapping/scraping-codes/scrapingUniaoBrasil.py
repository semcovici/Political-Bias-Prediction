import requests
from bs4 import BeautifulSoup
from google.colab import files
import pandas as pd

# Para usar o script
#   1) Alterar a quantidade de noticias de sua escolha na variavel qtnNoticias
      # PRECISA SER UM MULTIPLO DE 10

qtnNoticias = 200
nome_arquivo = "uniaoBrasil"
noticiasColetadas = []

url = 'https://uniaobrasil.org.br/blog/category/geral/'
site = requests.get(url)

entendedorDeHtml = BeautifulSoup(site.text, 'html.parser')
titulos = entendedorDeHtml.find_all('h3', class_='elementor-post__title')
datas = entendedorDeHtml.find_all("span", class_="elementor-post-date")
urls = entendedorDeHtml.find_all("a", class_="elementor-post__read-more")

for titulo, data, link in zip(titulos, datas, urls):
      urlNoticia = link["href"]
      siteNoticia = requests.get(urlNoticia)

      entendedorDeHtmlNoticia = BeautifulSoup(siteNoticia.text, 'html.parser')

      divComConteudo = entendedorDeHtmlNoticia.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

      entendedorDeHtmlDaDivDeConteudo = BeautifulSoup(str(divComConteudo), 'html.parser')

      paragrafos = entendedorDeHtmlDaDivDeConteudo.find_all('p')

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

urlProxPaginas = 'https://uniaobrasil.org.br/blog/category/geral/page/'

page = 2
qtnNoticias = qtnNoticias +10
while page != 8:
  urlCompleta = urlProxPaginas + str(page) + '/'
  siteProxPagina = requests.get(urlCompleta)

  entendedorDeHtmlProxPagina = BeautifulSoup(siteProxPagina.text, 'html.parser')
  titulosProxPagina = entendedorDeHtmlProxPagina.find_all('h3', class_='elementor-post__title')
  datasProxPagina = entendedorDeHtmlProxPagina.find_all("span", class_="elementor-post-date")
  urlsProxPagina = entendedorDeHtmlProxPagina.find_all("a", class_="elementor-post__read-more")

  for tituloProxPagina, dataProxPagina, linkProxPagina in zip(titulosProxPagina, datasProxPagina, urlsProxPagina):
        urlNoticiaProxPagina = linkProxPagina["href"]
        siteNoticiaProxPagina = requests.get(urlNoticiaProxPagina)

        entendedorDeHtmlNoticiaProxPagina = BeautifulSoup(siteNoticiaProxPagina.text, 'html.parser')

        divComConteudoProxPagina = entendedorDeHtmlNoticiaProxPagina.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

        entendedorDeHtmlDaDivDeConteudoProxPagina = BeautifulSoup(str(divComConteudoProxPagina), 'html.parser')

        paragrafosProxPagina = entendedorDeHtmlDaDivDeConteudoProxPagina.find_all('p')

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

#Executivo
url = 'https://uniaobrasil.org.br/blog/category/executivo/'
site = requests.get(url)

entendedorDeHtml = BeautifulSoup(site.text, 'html.parser')
titulos = entendedorDeHtml.find_all('h3', class_='elementor-post__title')
datas = entendedorDeHtml.find_all("span", class_="elementor-post-date")
urls = entendedorDeHtml.find_all("a", class_="elementor-post__read-more")

for titulo, data, link in zip(titulos, datas, urls):
      urlNoticia = link["href"]
      siteNoticia = requests.get(urlNoticia)

      entendedorDeHtmlNoticia = BeautifulSoup(siteNoticia.text, 'html.parser')

      divComConteudo = entendedorDeHtmlNoticia.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

      entendedorDeHtmlDaDivDeConteudo = BeautifulSoup(str(divComConteudo), 'html.parser')

      paragrafos = entendedorDeHtmlDaDivDeConteudo.find_all('p')

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

urlProxPaginas = 'https://uniaobrasil.org.br/blog/category/executivo/page/'

page = 2
qtnNoticias = qtnNoticias +10
while page != 6:
  urlCompleta = urlProxPaginas + str(page) + '/'
  siteProxPagina = requests.get(urlCompleta)

  entendedorDeHtmlProxPagina = BeautifulSoup(siteProxPagina.text, 'html.parser')
  titulosProxPagina = entendedorDeHtmlProxPagina.find_all('h3', class_='elementor-post__title')
  datasProxPagina = entendedorDeHtmlProxPagina.find_all("span", class_="elementor-post-date")
  urlsProxPagina = entendedorDeHtmlProxPagina.find_all("a", class_="elementor-post__read-more")

  for tituloProxPagina, dataProxPagina, linkProxPagina in zip(titulosProxPagina, datasProxPagina, urlsProxPagina):
        urlNoticiaProxPagina = linkProxPagina["href"]
        siteNoticiaProxPagina = requests.get(urlNoticiaProxPagina)

        entendedorDeHtmlNoticiaProxPagina = BeautifulSoup(siteNoticiaProxPagina.text, 'html.parser')

        divComConteudoProxPagina = entendedorDeHtmlNoticiaProxPagina.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

        entendedorDeHtmlDaDivDeConteudoProxPagina = BeautifulSoup(str(divComConteudoProxPagina), 'html.parser')

        paragrafosProxPagina = entendedorDeHtmlDaDivDeConteudoProxPagina.find_all('p')

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

#Legislativo
url = 'https://uniaobrasil.org.br/blog/category/legislativo/'
site = requests.get(url)

entendedorDeHtml = BeautifulSoup(site.text, 'html.parser')
titulos = entendedorDeHtml.find_all('h3', class_='elementor-post__title')
datas = entendedorDeHtml.find_all("span", class_="elementor-post-date")
urls = entendedorDeHtml.find_all("a", class_="elementor-post__read-more")

for titulo, data, link in zip(titulos, datas, urls):
      urlNoticia = link["href"]
      siteNoticia = requests.get(urlNoticia)

      entendedorDeHtmlNoticia = BeautifulSoup(siteNoticia.text, 'html.parser')

      divComConteudo = entendedorDeHtmlNoticia.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

      entendedorDeHtmlDaDivDeConteudo = BeautifulSoup(str(divComConteudo), 'html.parser')

      paragrafos = entendedorDeHtmlDaDivDeConteudo.find_all('p')

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

urlProxPaginas = 'https://uniaobrasil.org.br/blog/category/legislativo/page/'

page = 2
qtnNoticias = qtnNoticias +10
while page != 11:
  urlCompleta = urlProxPaginas + str(page) + '/'
  siteProxPagina = requests.get(urlCompleta)

  entendedorDeHtmlProxPagina = BeautifulSoup(siteProxPagina.text, 'html.parser')
  titulosProxPagina = entendedorDeHtmlProxPagina.find_all('h3', class_='elementor-post__title')
  datasProxPagina = entendedorDeHtmlProxPagina.find_all("span", class_="elementor-post-date")
  urlsProxPagina = entendedorDeHtmlProxPagina.find_all("a", class_="elementor-post__read-more")

  for tituloProxPagina, dataProxPagina, linkProxPagina in zip(titulosProxPagina, datasProxPagina, urlsProxPagina):
        urlNoticiaProxPagina = linkProxPagina["href"]
        siteNoticiaProxPagina = requests.get(urlNoticiaProxPagina)

        entendedorDeHtmlNoticiaProxPagina = BeautifulSoup(siteNoticiaProxPagina.text, 'html.parser')

        divComConteudoProxPagina = entendedorDeHtmlNoticiaProxPagina.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

        entendedorDeHtmlDaDivDeConteudoProxPagina = BeautifulSoup(str(divComConteudoProxPagina), 'html.parser')

        paragrafosProxPagina = entendedorDeHtmlDaDivDeConteudoProxPagina.find_all('p')

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

#UniaoMulher
url = 'https://uniaobrasil.org.br/blog/category/uniao-mulher/'
site = requests.get(url)

entendedorDeHtml = BeautifulSoup(site.text, 'html.parser')
titulos = entendedorDeHtml.find_all('h3', class_='elementor-post__title')
datas = entendedorDeHtml.find_all("span", class_="elementor-post-date")
urls = entendedorDeHtml.find_all("a", class_="elementor-post__read-more")

for titulo, data, link in zip(titulos, datas, urls):
      urlNoticia = link["href"]
      siteNoticia = requests.get(urlNoticia)

      entendedorDeHtmlNoticia = BeautifulSoup(siteNoticia.text, 'html.parser')

      divComConteudo = entendedorDeHtmlNoticia.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

      entendedorDeHtmlDaDivDeConteudo = BeautifulSoup(str(divComConteudo), 'html.parser')

      paragrafos = entendedorDeHtmlDaDivDeConteudo.find_all('p')

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

urlProxPaginas = 'https://uniaobrasil.org.br/blog/category/uniao-mulher/page/'

page = 2
qtnNoticias = qtnNoticias +10
while page != 6:
  urlCompleta = urlProxPaginas + str(page) + '/'
  siteProxPagina = requests.get(urlCompleta)

  entendedorDeHtmlProxPagina = BeautifulSoup(siteProxPagina.text, 'html.parser')
  titulosProxPagina = entendedorDeHtmlProxPagina.find_all('h3', class_='elementor-post__title')
  datasProxPagina = entendedorDeHtmlProxPagina.find_all("span", class_="elementor-post-date")
  urlsProxPagina = entendedorDeHtmlProxPagina.find_all("a", class_="elementor-post__read-more")

  for tituloProxPagina, dataProxPagina, linkProxPagina in zip(titulosProxPagina, datasProxPagina, urlsProxPagina):
        urlNoticiaProxPagina = linkProxPagina["href"]
        siteNoticiaProxPagina = requests.get(urlNoticiaProxPagina)

        entendedorDeHtmlNoticiaProxPagina = BeautifulSoup(siteNoticiaProxPagina.text, 'html.parser')

        divComConteudoProxPagina = entendedorDeHtmlNoticiaProxPagina.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

        entendedorDeHtmlDaDivDeConteudoProxPagina = BeautifulSoup(str(divComConteudoProxPagina), 'html.parser')

        paragrafosProxPagina = entendedorDeHtmlDaDivDeConteudoProxPagina.find_all('p')

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

#UniaoJovem
url = 'https://uniaobrasil.org.br/blog/category/uniao-jovem/'
site = requests.get(url)

entendedorDeHtml = BeautifulSoup(site.text, 'html.parser')
titulos = entendedorDeHtml.find_all('h3', class_='elementor-post__title')
datas = entendedorDeHtml.find_all("span", class_="elementor-post-date")
urls = entendedorDeHtml.find_all("a", class_="elementor-post__read-more")

for titulo, data, link in zip(titulos, datas, urls):
      urlNoticia = link["href"]
      siteNoticia = requests.get(urlNoticia)

      entendedorDeHtmlNoticia = BeautifulSoup(siteNoticia.text, 'html.parser')

      divComConteudo = entendedorDeHtmlNoticia.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

      entendedorDeHtmlDaDivDeConteudo = BeautifulSoup(str(divComConteudo), 'html.parser')

      paragrafos = entendedorDeHtmlDaDivDeConteudo.find_all('p')

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

urlProxPaginas = 'https://uniaobrasil.org.br/blog/category/uniao-jovem/page/'

page = 2
qtnNoticias = qtnNoticias +10
while page != 6:
  urlCompleta = urlProxPaginas + str(page) + '/'
  siteProxPagina = requests.get(urlCompleta)

  entendedorDeHtmlProxPagina = BeautifulSoup(siteProxPagina.text, 'html.parser')
  titulosProxPagina = entendedorDeHtmlProxPagina.find_all('h3', class_='elementor-post__title')
  datasProxPagina = entendedorDeHtmlProxPagina.find_all("span", class_="elementor-post-date")
  urlsProxPagina = entendedorDeHtmlProxPagina.find_all("a", class_="elementor-post__read-more")

  for tituloProxPagina, dataProxPagina, linkProxPagina in zip(titulosProxPagina, datasProxPagina, urlsProxPagina):
        urlNoticiaProxPagina = linkProxPagina["href"]
        siteNoticiaProxPagina = requests.get(urlNoticiaProxPagina)

        entendedorDeHtmlNoticiaProxPagina = BeautifulSoup(siteNoticiaProxPagina.text, 'html.parser')

        divComConteudoProxPagina = entendedorDeHtmlNoticiaProxPagina.find_all('div', class_='elementor-element elementor-element-b006974 elementor-widget elementor-widget-theme-post-content')

        entendedorDeHtmlDaDivDeConteudoProxPagina = BeautifulSoup(str(divComConteudoProxPagina), 'html.parser')

        paragrafosProxPagina = entendedorDeHtmlDaDivDeConteudoProxPagina.find_all('p')

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

nome_arquivo = "uniaoBrasil.csv"

df = pd.DataFrame(noticiasColetadas[1:], columns=noticiasColetadas[0])
df.to_csv(nome_arquivo, index=False)

print(f'Os dados foram salvos em {nome_arquivo}')

arquivo = pd.read_csv(nome_arquivo)

files.download(nome_arquivo)

arquivo