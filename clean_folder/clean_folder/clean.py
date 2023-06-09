import shutil 
from pathlib import Path
from re import sub
import sys

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
IMAGES = ('.jpeg', '.png', '.jpg', '.svg')
DOCUMENTS = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
AUDIO = ('.mp3', '.ogg', '.wav', '.amr')
VIDEO = ('.avi', '.mp4', '.mov', '.mkv')
ARCHIVES = ('.zip', '.gz', '.tar')

# Нормалізація імені
def normalize(file_name):
    file_name = sub(r"\W", "_", file_name)
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    file_name = ''.join(TRANS.get(ord(ch), ch) for ch in file_name)
    return file_name

# Обробка файлу (нормалізація + сортуваня)
def proccessing(item):
    if item.is_file():
        file_name, file_ext = item.stem, item.suffix 
        file_ext = file_ext.lower()
        file_name = normalize(file_name)
        norm_name = file_name + file_ext
        if file_ext in IMAGES:
            Path.mkdir(item.parent / 'images', exist_ok=True)
            item.rename(item.parent / 'images' / norm_name)
        elif file_ext in DOCUMENTS:
            Path.mkdir(item.parent / 'documents', exist_ok=True)
            item.rename(item.parent / 'documents' / norm_name) 
        elif file_ext in AUDIO:
            Path.mkdir(item.parent / 'audio', exist_ok=True)
            item.rename(item.parent / 'audio' / norm_name)    
        elif file_ext in VIDEO:
            Path.mkdir(item.parent / 'video', exist_ok=True)
            item.rename(item.parent / 'video' / norm_name)  
        elif file_ext in ARCHIVES:
            try:
                Path.mkdir(item.parent / 'archives', exist_ok=True)
                item.rename(item.parent / 'archives' / norm_name)
                shutil.unpack_archive(Path(item.parent / 'archives' / norm_name), Path(item.parent / 'archives' / file_name))
            except shutil.ReadError:
                print("File can't be procceeded, please check if it's archive.")      
  
# Перевірка директорі, видалення пустих
def sorter(path):
    ignore_list = ('archives', 'video', 'audio', 'documents', 'images')
    for item in path.glob('*'):
        if item.is_dir() and item.name not in ignore_list:
            sorter(item)
            if not list(item.glob('*')):
                item.rmdir()
        elif item.is_file():
            proccessing(item)
            
# Перевірка шляху чи введений аргумент чи ні, та наявності введеного шляху
def main():
    path = Path.cwd()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if Path(path).exists():
            sorter(Path(path))
            print(f'Шлях сортування {path}') 
        else:
            print('Шляху не існує')
    else:
        sorter(Path(path))
        print(f'Шлях сортування {path}')      
 
if __name__ == "__main__":
        main()