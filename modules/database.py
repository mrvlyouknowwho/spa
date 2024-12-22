# modules/database.py
import sqlite3
import json
import os

class DatabaseManager:
    def __init__(self, db_name="spa_data.db"):
        print("DatabaseManager: Инициализация")
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self._create_tables()
    
    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("DatabaseManager: Успешное подключение к базе данных")
        except Exception as e:
            print(f"DatabaseManager: Ошибка подключения к базе данных: {e}")
            self.conn = None
            self.cursor = None
    
    def _create_tables(self):
        if self.cursor:
            try:
              self.cursor.execute("""
                  CREATE TABLE IF NOT EXISTS project_info (
                      key TEXT PRIMARY KEY,
                      value TEXT
                  )
              """)
              self.cursor.execute("""
                 CREATE TABLE IF NOT EXISTS past_actions (
                      timestamp TEXT,
                      action TEXT,
                      result TEXT
                 )
              """)
              self.conn.commit()
              print("DatabaseManager: Таблицы созданы или уже существуют")
            except Exception as e:
              print(f"DatabaseManager: Ошибка создания таблиц: {e}")

    def save_data(self, key, value):
        if self.cursor:
            try:
                value_json = json.dumps(value)
                self.cursor.execute("INSERT OR REPLACE INTO project_info (key, value) VALUES (?, ?)", (key, value_json))
                self.conn.commit()
                print(f"DatabaseManager: Данные сохранены. Key: {key}")
            except Exception as e:
               print(f"DatabaseManager: Ошибка сохранения данных: {e}")

    def load_data(self, key):
        if self.cursor:
            self.cursor.execute("SELECT value FROM project_info WHERE key = ?", (key,))
            result = self.cursor.fetchone()
            if result:
                print(f"DatabaseManager: Данные загружены. Key: {key}")
                return json.loads(result[0])
            else:
                print(f"DatabaseManager: Данные не найдены. Key: {key}")
                return None
        else:
            print(f"DatabaseManager: Нет подключения к базе данных, загрузка данных невозможна.")
            return None
        
    def add_past_action(self, timestamp, action, result):
       if self.cursor:
         try:
            self.cursor.execute("INSERT INTO past_actions (timestamp, action, result) VALUES (?, ?, ?)", (timestamp, action, result))
            self.conn.commit()
            print("DatabaseManager: Действие добавлено.")
         except Exception as e:
            print(f"DatabaseManager: Ошибка добавления действия: {e}")
       else:
            print(f"DatabaseManager: Нет подключения к базе данных, добавление действия невозможно.")
          
    def get_past_actions(self):
        if self.cursor:
          self.cursor.execute("SELECT * FROM past_actions")
          results = self.cursor.fetchall()
          return results
        else:
           print(f"DatabaseManager: Нет подключения к базе данных, получение действий невозможно.")
           return []

    def close(self):
        if self.conn:
            try:
               self.conn.close()
               print("DatabaseManager: Соединение с базой данных закрыто.")
            except Exception as e:
                print(f"DatabaseManager: Ошибка закрытия соединения с БД: {e}")
            self.conn = None
            self.cursor = None
    
    def clear(self):
      if self.cursor:
          try:
            self.cursor.execute("DELETE FROM project_info")
            self.cursor.execute("DELETE FROM past_actions")
            self.conn.commit()
            print("DatabaseManager: Данные успешно очищены.")
          except Exception as e:
            print(f"DatabaseManager: Ошибка очистки данных: {e}")
      else:
         print(f"DatabaseManager: Нет подключения к базе данных, очистка невозможна.")