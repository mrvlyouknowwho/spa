# modules/search.py
import requests
from bs4 import BeautifulSoup
import requests.exceptions
import socket

class Search:
    def __init__(self):
        print("Search: Инициализация")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        self.search_engines = {
          "duckduckgo": "https://duckduckgo.com/?q={query}",
          "google" : "https://www.google.com/search?q={query}"
        }
        self.current_engine = "duckduckgo"
    def check_internet_connection(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=5)
            return True
        except OSError:
            return False

    def set_search_engine(self, engine_name):
        if engine_name in self.search_engines:
            self.current_engine = engine_name
        else:
            print("Search: Неизвестная поисковая система.")
        
    def search_internet(self, query):
        print(f"Search: Поиск в интернете: {query} через {self.current_engine}")
        if not self.check_internet_connection():
            print("Search: Нет подключения к интернету.")
            return "Нет подключения к интернету", "Нет подключения к интернету"

        search_url = self.search_engines[self.current_engine].format(query=query)
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', class_='result__a' if self.current_engine == "duckduckgo" else "yuRUbf")
            results = []
            for link in links[:5]:
               if self.current_engine == "duckduckgo":
                  results.append({"title": link.text, "url": link['href']})
               else:
                 results.append({"title": link.find('h3').text if link.find('h3') else link.text , "url": link.get('href')})
            if not results:
              print(f"Search: Поиск не дал результатов.")
              return f"Поиск не дал результатов.", "Ошибка поиска"
            print(f"Search: Успешный поиск, найдено {len(results)} результатов.")
            return results, "ok"
        except requests.exceptions.RequestException as e:
            print(f"Search: Ошибка поиска: {e}")
            return f"Ошибка поиска: {e}", "Ошибка поиска"

    def extract_text_from_url(self, url):
      print(f"Search: Извлечение текста из URL: {url}")
      try:
          response = requests.get(url, headers=self.headers, timeout=10)
          response.raise_for_status()
          soup = BeautifulSoup(response.content, 'html.parser')
          text = soup.get_text(separator=' ', strip=True)
          print(f"Search: Успешное извлечение текста из URL: {url}")
          return text
      except requests.exceptions.RequestException as e:
          print(f"Search: Ошибка при извлечении текста: {e}")
          return f"Ошибка при извлечении текста: {e}"