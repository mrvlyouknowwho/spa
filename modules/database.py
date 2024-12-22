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
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
    def _create_tables(self):
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

    def save_data(self, key, value):
        try:
            value_json = json.dumps(value)
            self.cursor.execute("INSERT OR REPLACE INTO project_info (key, value) VALUES (?, ?)", (key, value_json))
            self.conn.commit()
        except Exception as e:
           print(f"Ошибка сохранения данных: {e}")

    def load_data(self, key):
        self.cursor.execute("SELECT value FROM project_info WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        if result:
            return json.loads(result[0])
        else:
            return None
        
    def add_past_action(self, timestamp, action, result):
       try:
          self.cursor.execute("INSERT INTO past_actions (timestamp, action, result) VALUES (?, ?, ?)", (timestamp, action, result))
          self.conn.commit()
       except Exception as e:
          print(f"Ошибка добавления действия: {e}")
          
    def get_past_actions(self):
        self.cursor.execute("SELECT * FROM past_actions")
        results = self.cursor.fetchall()
        return results

    def close(self):
        if self.conn:
            self.conn.close()
    
    def clear(self):
      try:
        self.cursor.execute("DELETE FROM project_info")
        self.cursor.execute("DELETE FROM past_actions")
        self.conn.commit()
      except Exception as e:
        print(f"Ошибка очистки данных {e}")