import requests
import time
import locale
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd

date_format = "%d de %B de %Y"

def translate_month(date_string):
  month_translation = {
    'janeiro': 'January',
    'fevereiro': 'February',
    'março': 'March',
    'abril': 'April',
    'maio': 'May',
    'junho': 'June',
    'julho': 'July',
    'agosto': 'August',
    'setembro': 'September',
    'outubro': 'October',
    'novembro': 'November',
    'dezembro': 'December'
  }

  for pt_month, en_month in month_translation.items():
    date_string = date_string.replace(pt_month, en_month)

  return date_string

def process_raw_articles(base_soup, source):
  articles = []

  if source == "pv":
    raw_articles = base_soup.find_all('div', class_ = "post-entry-content")
    for article in raw_articles:
      title = article.find('a').text
      date = article.find('time')['datetime']
      url = article.find('a')['href']

      content_response = requests.get(url, verify=False)
      content_soup = BeautifulSoup(content_response.content, 'html.parser')
      raw_contents = content_soup.find('div', class_="entry-content")
      content = ''

      if not raw_contents is None:
        for raw_content in raw_contents:
          if not raw_content.text is None:
            content += raw_content.text.replace("\n","")

      articles.append({
        'title': title,
        'date': date,
        'url': url,
        'content': content
      })

  elif source == "psb":
    raw_articles = base_soup.find_all('div', class_="wf-cell")
    for article in raw_articles:
      title = article.get('data-name')
      date = article.get('data-date')
      url = article.find('a')['href']

      content_response = requests.get(url, verify=False)
      content_soup = BeautifulSoup(content_response.content, 'html.parser')
      raw_contents = content_soup.find_all('div', class_="entry-content")
      content = ''

      if not raw_contents is None:
        for half_part in raw_contents:
          for raw_content in half_part:
            if not raw_content.text is None:
              content += raw_content.text.replace("\n","")

      articles.append({
        'title': title,
        'date': date,
        'url': url,
        'content': content
      })
  
  elif source == "mdb":
    raw_articles = base_soup.find_all('div', class_="card")
    for article in raw_articles:
      title = article.find('h3', class_="card__title").text
      date_string = article.find('div', class_="card__info").text.split("|")[1].strip()
      translated_date_string = translate_month(date_string)
      raw_date = datetime.strptime(translated_date_string, date_format)
      date = raw_date.strftime("%Y-%m-%dT%H:%M:%S%z-03:00")
      url = article.find('a')['href']

      content_response = requests.get(url, verify=False)
      content_soup = BeautifulSoup(content_response.content, 'html.parser')
      raw_contents = content_soup.find('article', class_="article")
      content = ''

      if not raw_contents is None:
        for raw_content in raw_contents:
          if not raw_content.text is None:
            content += raw_content.text.replace("\n","")

      articles.append({
        'title': title,
        'date': date,
        'url': url,
        'content': content
      })

  elif source == "rede":
    raw_articles = base_soup.find_all('div', class_="blog-entry-inner")
    for article in raw_articles:
      title = article.find('a', rel="bookmark").text
      date_string = article.find('div', class_="blog-entry-date").text.strip()
      translated_date_string = translate_month(date_string)
      raw_date = datetime.strptime(translated_date_string, date_format)
      date = raw_date.strftime("%Y-%m-%dT%H:%M:%S%z-03:00")
      url = article.find('a', rel="bookmark")['href']

      content_response = requests.get(url, verify=False)
      content_soup = BeautifulSoup(content_response.content, 'html.parser')
      raw_contents = content_soup.find('div', class_="entry-content")
      content = ''

      if not raw_contents is None:
        for raw_content in raw_contents:
          if not raw_content.text is None:
            content += raw_content.text.replace("\n","")

      articles.append({
        'title': title,
        'date': date,
        'url': url,
        'content': content
      })

  else:
    return False

  return articles

def get_articles_from_journal(source, page=1):
  if source == "pv":
    url = f'https://pv.org.br/noticias/page/{page}'
  elif source == "psb":
    url = f'https://psb40.org.br/noticias/page/{page}'
  elif source == "mdb":
    url = f'https://www.mdb.org.br/noticias/page/{page}'
  elif source == "rede":
    url = f'https://redesustentabilidade.org.br/blog/page/{page}'
  else:
    return False

  response = requests.get(url, verify=False);
  soup = BeautifulSoup(response.content, 'html.parser')

  articles = process_raw_articles(soup, source)

  create_csv(articles, source)

def create_csv(articles, source):
  non_duplicates = pd.DataFrame()
  new_data = pd.DataFrame(articles)
  existing_data = pd.read_csv(f"{source}_output.csv")

  if not new_data.empty:
    non_duplicates = pd.concat([non_duplicates, new_data[~new_data['title'].isin(existing_data['title'])]], ignore_index=True)

  combined_data = pd.concat([existing_data, non_duplicates], ignore_index=True)

  if 'Unnamed: 0' in combined_data.columns:
    combined_data = combined_data.drop(columns=['Unnamed: 0'])

  combined_data.to_csv(f"{source}_output.csv", index=False)

def iterate_get_articles_from_journal(source, start_page, end_page):
  for current_page in range(start_page, end_page + 1):
    get_articles_from_journal(source, current_page)
    time.sleep(2)

def main():
  #generates csv from the first page
  get_articles_from_journal("rede")

  #generates csv from the third page
  #get_articles_from_journal("psb", 3)

  #generates csv from the second page to the tenth page
  #iterate_get_articles_from_journal("mdb", 2, 10)

  #generates csv from the fifth page to the seventh page
  #iterate_get_articles_from_journal("rede", 5, 7)

  #iterate_get_articles_from_journal("pv", 1, 80)
  #iterate_get_articles_from_journal("psb", 1, 80)
  #iterate_get_articles_from_journal("mdb", 1, 80)
  #iterate_get_articles_from_journal("rede", 1, 80)

if __name__ == "__main__":
  main()
