import requests
from bs4 import BeautifulSoup

class Search:
    def search_internet(self, query):
        search_url = f"https://duckduckgo.com/?q={query}"
        try:
            response = requests.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', class_='result__a')
            results = []
            for link in links[:5]:
                results.append({"title": link.text, "url": link['href']})
            return results
        except requests.exceptions.RequestException as e:
            return f"Ошибка поиска: {e}"

    def extract_text_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            return text
        except requests.exceptions.RequestException as e:
            return f"Ошибка при извлечении текста: {e}"