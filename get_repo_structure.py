import os
import base64
import pathlib
import logging
from github import Github
import time
from typing import List, Tuple, Set
import argparse

# --- Настраиваемые константы ---
OUTPUT_FILE_NAME = "repo_structure.txt"
DEFAULT_IGNORE = (
    "%USERPROFILE%",
    "venv",
    ".git"
)
COMMON_FILE_EXTENSIONS = ('.py', '.txt', '.md', '.json', '.yaml', '.ini', '.xml', '.toml')
# -------------------------------

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

EXPANDED_IGNORE = [os.path.expandvars(ignore) for ignore in DEFAULT_IGNORE]

def process_file_content(item_path: str, indent: str, content_output: str, file_content: str = None) -> str:
    content_output += f"\n{indent}--- {item_path} ---\n"
    if file_content:
        content_output += f"{file_content}\n"
    else:
        content_output += "Binary file content not displayed.\n"
    return content_output

def should_process_item(item_path: str, include_option: str) -> bool:
    if include_option == 'all':
        return True
    if include_option == 'structure_only':
        return True
    if include_option == 'common_files' and not item_path.lower().endswith(COMMON_FILE_EXTENSIONS):
        return False
    if include_option == 'all_except_ignore' and any(item_path == ignore or item_path.startswith(ignore + '/') for ignore in EXPANDED_IGNORE):
        return False
    return True

def process_local_item(item_path: str, indent: str, include_option: str, visited_paths: Set[str], structure_output: str, content_output: str, ignore_read_errors: bool = True) -> Tuple[str, str]:
    if item_path in visited_paths:
        return structure_output, content_output
    visited_paths.add(item_path)
    
    if os.path.isfile(item_path):
        if not should_process_item(item_path, include_option):
            return structure_output, content_output
        if include_option == 'structure_only':
            structure_output += f"{indent}{item_path}\n"
            return structure_output, content_output
        try:
            with open(item_path, 'r', encoding='utf-8') as file:
                content = file.read()
                content_output = process_file_content(item_path, indent, content_output, content)
        except UnicodeDecodeError:
            if ignore_read_errors:
                logging.error(f"Error reading file (ignored): {item_path}, binary file")
                content_output = process_file_content(item_path, indent, content_output)
            else:
                logging.error(f"Error reading file: {item_path}, binary file")
                content_output = process_file_content(item_path, indent, content_output, f"Error reading file: {e}")
        except Exception as e:
            if ignore_read_errors:
                logging.error(f"Error reading file (ignored): {item_path}, {e}")
                content_output = process_file_content(item_path, indent, content_output, f"Error reading file (ignored): {e}")
            else:
                logging.error(f"Error reading file: {item_path}, {e}")
                content_output = process_file_content(item_path, indent, content_output, f"Error reading file: {e}")
    return structure_output, content_output


def process_local_tree(path: str, indent: str, include_option: str, visited_paths: Set[str], structure_output: str, content_output: str, ignore_read_errors: bool = True, processed_count: List[int] = None, total_count: int = None) -> Tuple[str, str]:
    try:
        items_count = 0
        for root, dirs, files in os.walk(path):
           
            for dir_name in dirs:
               
                item_path = os.path.join(root, dir_name).replace('\\', '/')
                if item_path == os.path.abspath(__file__).replace('\\', '/'):
                     continue
                if should_process_item(item_path, include_option):
                    structure_output += f"{indent}{item_path}/\n"
            for file_name in files:
                
                item_path = os.path.join(root, file_name).replace('\\', '/')
                if item_path == os.path.abspath(__file__).replace('\\', '/'):
                     continue
                
                if should_process_item(item_path, include_option):
                    structure_output, content_output = process_local_item(item_path, indent + "  ", include_option, visited_paths, structure_output, content_output, ignore_read_errors)
            items_count += len(dirs) + len(files)
            if processed_count is not None and total_count is not None:
                 processed_count[0] += len(dirs) + len(files)
                 progress = (processed_count[0] / total_count) * 100
                 print(f"Progress: {progress:.2f}%", end='\r')
           
    except Exception as e:
        logging.error(f"Error accessing directory: {path}, {e}")
    return structure_output, content_output
    

def get_local_structure(repo_path: str, include_option: str, ignore_read_errors: bool = True) -> str:
    start_time = time.time()
    visited_paths = set()
    structure_output = ""
    content_output = ""
    
    # Получаем список всех файлов и папок в репозитории
    all_items = []
    for root, dirs, files in os.walk(repo_path):
        for dir_name in dirs:
                item_path = os.path.join(root, dir_name).replace('\\', '/')
                if item_path == os.path.abspath(__file__).replace('\\', '/'):
                     continue
                all_items.append(item_path)
        for file_name in files:
                item_path = os.path.join(root, file_name).replace('\\', '/')
                if item_path == os.path.abspath(__file__).replace('\\', '/'):
                     continue
                all_items.append(item_path)
    total_count = len(all_items)
    processed_count = [0]
    
    structure_output, content_output = process_local_tree(repo_path, "", include_option, visited_paths, structure_output, content_output, ignore_read_errors, processed_count, total_count)
    
    
    output = structure_output + "\n" + "--- СТРУКТУРА ЗАКОНЧЕНА ---\n\n" + content_output
    end_time = time.time()
    execution_time = end_time - start_time
    output += f"\nВремя выполнения: {execution_time:.2f} секунд"
    return output

def process_github_item(item, indent: str, include_option: str, repo, structure_output: str, content_output: str) -> Tuple[str, str]:
    item_path = item.path.replace('\\', '/')
    if item.type == "tree":
        if include_option == 'all_except_ignore' and any(item_path.startswith(ignore) for ignore in EXPANDED_IGNORE):
            return structure_output, content_output
        structure_output += f"{indent}{item_path}/\n"
        sub_tree = repo.get_git_tree(item.sha)
        structure_output, content_output = process_github_tree(sub_tree, indent + "  ", include_option, repo, structure_output, content_output)
    elif item.type == "blob":
        if include_option == 'py_files' and not item_path.endswith('.py'):
            return structure_output, content_output
        if include_option == 'all_except_ignore' and any(item_path.startswith(ignore) for ignore in EXPANDED_IGNORE):
            return structure_output, content_output
        try:
            blob = repo.get_git_blob(item.sha)
            content = blob.content
            try:
                decoded_content = base64.b64decode(content).decode('utf-8', errors='ignore')
                content_output = process_file_content(item_path, indent, content_output, decoded_content)
            except UnicodeDecodeError:
                content_output = process_file_content(item_path, indent, content_output)
        except Exception as e:
            logging.error(f"Error reading file from github: {item_path}, {e}")
            content_output = process_file_content(item_path, indent, content_output, f"Error reading file: {e}")
    return structure_output, content_output

def process_github_tree(tree, indent: str, include_option: str, repo, structure_output: str, content_output: str, processed_count: List[int] = None, total_count: int = None) -> Tuple[str, str]:
    for item in tree.tree:
        structure_output, content_output = process_github_item(item, indent, include_option, repo, structure_output, content_output)
        if processed_count is not None and total_count is not None:
            processed_count[0] += 1
            progress = (processed_count[0] / total_count) * 100
            print(f"Progress: {progress:.2f}%", end='\r')
    return structure_output, content_output

def get_repo_structure_from_github(repo_owner: str, repo_name: str, github_token: str, include_option: str) -> str:
    start_time = time.time()
    g = Github(github_token)
    repo = g.get_user(repo_owner).get_repo(repo_name)
    
    structure_output = ""
    content_output = ""
    
    main_branch = repo.get_branch(repo.default_branch)
    base_tree = repo.get_git_tree(main_branch.commit.sha)
    
    if include_option == 'all':
        structure_output, content_output = process_github_tree(base_tree, "", include_option, repo, structure_output, content_output)
    else:
        
        all_items = []
        def collect_items(tree, indent=""):
            nonlocal all_items
            for item in tree.tree:
                item_path = item.path.replace('\\', '/')
                all_items.append((item, indent))
                if item.type == "tree":
                    sub_tree = repo.get_git_tree(item.sha)
                    collect_items(sub_tree, indent + "  ")
        collect_items(base_tree)
        
        total_count = len(all_items)
        processed_count = [0]
        
        structure_output, content_output = process_github_tree(base_tree, "", include_option, repo, structure_output, content_output, processed_count, total_count)
    
    temp_structure_output = ""
    def temp_process_tree(tree, indent=""):
        nonlocal temp_structure_output
        for item in tree.tree:
            item_path = item.path.replace('\\', '/')
            if item.type == "tree":
                if include_option == 'all_except_ignore' and any(item_path.startswith(os.path.expandvars(ignore)) for ignore in DEFAULT_IGNORE):
                    continue
                temp_structure_output += f"{indent}{item_path}/\n"
                sub_tree = repo.get_git_tree(item.sha)
                temp_process_tree(sub_tree, indent + "  ")
            elif item.type == "blob":
                 if include_option == 'all_except_ignore' and any(item_path.startswith(os.path.expandvars(ignore)) for ignore in DEFAULT_IGNORE):
                    continue
                 temp_structure_output += f"{indent}{item_path}\n"

    temp_process_tree(base_tree)
    output = temp_structure_output + "\n" + "--- СТРУКТУРА ЗАКОНЧЕНА ---\n\n" + content_output
    end_time = time.time()
    execution_time = end_time - start_time
    output += f"\nВремя выполнения: {execution_time:.2f} секунд"
    return output

def create_output_file(repo_path: str, output: str, output_path: str = None) -> None:
    if output_path:
        output_file_path = os.path.join(os.path.expandvars(output_path), OUTPUT_FILE_NAME)
    else:
        output_file_path = os.path.join(pathlib.Path(__file__).parent, OUTPUT_FILE_NAME)
    try:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(output)
        print(f"Структура репозитория успешно сохранена в: {output_file_path}")
    except Exception as e:
        logging.error(f"Ошибка при создании файла: {e}")

def get_user_choice() -> str:
    while True:
        print("Выберите опцию для включения в вывод:")
        print("1. Только структура")
        print("2. Распространенные файлы и структура")
        print("3. Всё, кроме игнорируемых")
        print("4. Всё")
        choice = input("Введите номер опции: ")

        if choice == '1':
            return 'structure_only'
        elif choice == '2':
            return 'common_files'
        elif choice == '3':
            return 'all_except_ignore'
        elif choice == '4':
            return 'all'
        else:
            print("Неверная опция, попробуйте еще раз.")

def get_repo_path() -> str:
    return str(pathlib.Path(__file__).parent)

def main() -> None:
    repo_owner = "mrvlyouknowwho"
    repo_name = "spa"
    github_token = os.environ.get("GITHUB_TOKEN")
    output_path = None # Можно задать путь сохранения файла
    ignore_read_errors = True # Добавлена опция для игнорирования ошибок чтения
    
    print("Выберите источник данных:")
    print("1. GitHub")
    print("2. Локальная папка")
    source_choice = input("Введите номер опции: ")
    
    include_option = get_user_choice()
    
    if source_choice == '1':
        if github_token:
            repo_path = get_repo_path()
            output = get_repo_structure_from_github(repo_owner, repo_name, github_token, include_option)
            create_output_file(repo_path, output, output_path)
        else:
            print("Необходимо задать переменную окружения GITHUB_TOKEN")
    elif source_choice == '2':
        repo_path = get_repo_path()
        output = get_local_structure(repo_path, include_option, ignore_read_errors)
        create_output_file(repo_path, output, output_path)
    else:
        print("Неверный выбор источника данных.")

if __name__ == "__main__":
    main()