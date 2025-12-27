import os

EXCLUDED_DIRS = {'.git', '__pycache__', '.venv', 'venv', 'env', '.idea', '.vscode'}
EXCLUDED_FILES = {'db.sqlite3', 'collect_code.py', 'consolidated_project.txt'}
ALLOWED_EXTENSIONS = {'.py', '.txt', '.md', '.html'}

def consolidate_files(output_filename="consolidated_project.txt"):
    root_dir = os.getcwd()
    
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for file in files:
                if file in EXCLUDED_FILES:
                    continue
                
                # Проверяем расширение
                if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, root_dir)
                    
                    outfile.write(f"\n{'='*50}\n")
                    outfile.write(f"FILE: {relative_path}\n")
                    outfile.write(f"{'='*50}\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"[ОШИБКА ЧТЕНИЯ ФАЙЛА: {e}]")
                    
                    outfile.write("\n\n")

    print(f"Готово! Все файлы собраны в: {output_filename}")

if __name__ == "__main__":
    consolidate_files()