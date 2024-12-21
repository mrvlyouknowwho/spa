import PyPDF2
from PyQt6.QtWidgets import QFileDialog

class Files:
    def extract_text_from_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                return text
        except Exception as e:
            return f"Ошибка при извлечении текста из PDF: {e}"

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Выберите PDF файл", "", "PDF Files (*.pdf)")
        if file_path:
            return file_path
        return None

    def save_file(self, text):
        file_path, _ = QFileDialog.getSaveFileName(None, "Сохранить файл", "", "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(text)
                return f"Файл сохранен в {file_path}"
            except Exception as e:
                return f"Ошибка при сохранении файла: {e}"
        return None