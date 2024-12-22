# modules/files.py
import PyPDF2
from PyQt6.QtWidgets import QFileDialog

class Files:
    def __init__(self):
      print("Files: Инициализация")
    
    def extract_text_from_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                print(f"Files: Текст из PDF успешно извлечен: {file_path}")
                return text
        except Exception as e:
            print(f"Files: Ошибка при извлечении текста из PDF: {e}")
            return f"Ошибка при извлечении текста из PDF: {e}"

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Выберите PDF файл", "", "PDF Files (*.pdf)")
        if file_path:
            print(f"Files: Файл выбран: {file_path}")
            return file_path
        print("Files: Файл не выбран.")
        return None

    def save_file(self, text):
        file_path, _ = QFileDialog.getSaveFileName(None, "Сохранить файл", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(text)
                print(f"Files: Файл сохранен в: {file_path}")
                return f"Файл сохранен в {file_path}"
            except Exception as e:
                print(f"Files: Ошибка при сохранении файла: {e}")
                return f"Ошибка при сохранении файла: {e}"
        print("Files: Файл не сохранен.")
        return None