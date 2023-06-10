import shutil 
from pathlib import Path
from re import sub
from datetime import datetime
import sys

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
CATEGORIES = {'images': ('.jpeg', '.png', '.jpg', '.svg'),
              'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
              'audio': ('.mp3', '.ogg', '.wav', '.amr'),
              'video': ('.avi', '.mp4', '.mov', '.mkv'),
              'archives': ('.zip', '.gz', '.tar')}

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
    file_name, file_ext = item.stem, item.suffix 
    file_ext = file_ext.lower()
    file_name = normalize(file_name)
    norm_name = file_name + file_ext
    if file_ext in CATEGORIES['archives']:
        try:
            Path.mkdir(main_path / 'archives', exist_ok=True)
            item.rename(main_path / 'archives' / norm_name)
            shutil.unpack_archive(main_path / 'archives' / norm_name, main_path / 'archives' / file_name)
            return
        except shutil.ReadError:
            print("File can't be procceeded, please check if it's archive.")
    try:
        for cat, ext in CATEGORIES.items():
            if file_ext in ext and file_ext not in CATEGORIES['archives']:
                Path.mkdir(main_path / cat , exist_ok=True)
                item.rename(main_path / cat / norm_name)
                return
            if file_ext not in ext:
                Path.mkdir(main_path / 'other' , exist_ok=True)
                item.rename(main_path / 'other' / norm_name)
                return
    except FileExistsError:
        timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M")
        norm_name = f'{file_name}{timestamp}{file_ext}'
        item.rename(main_path / cat / norm_name)
        print(f'File already exsists {item} file was moved and renamed to {norm_name}')   

# Перевірка директорі, видалення пустих
def sorter(path):
    ignore_list = ('archives', 'video', 'audio', 'documents', 'images','other')
    for item in path.glob('*'):
        if item.is_dir() and item.name not in ignore_list:
            sorter(item)
            if not list(item.glob('*')):
                item.rmdir()
        elif item.is_file():
            proccessing(item)
            
# Перевірка шляху чи введений аргумент чи ні, та наявності введеного шляху
def path():
    path = Path.cwd()
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if Path(path).exists():
            print(f'1Шлях сортування {path}')
            return Path(path) 
        else:
            print('Шляху не існує')
    else:
        print(f'Шлях сортування {path}')
        return Path(path)

main_path = path()

def main():
    sorter(main_path)    
 
if __name__ == "__main__":
        main()