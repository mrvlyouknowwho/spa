import requests
from bs4 import BeautifulSoup

class Search:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def search_internet(self, query):
        search_url = f"https://duckduckgo.com/?q={query}"
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
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
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            return text
        except requests.exceptions.RequestException as e:
            return f"Ошибка при извлечении текста: {e}"