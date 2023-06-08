import shutil, re
from pathlib import Path


def normalize(file_name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    file_name = re.sub(r"\W", "_", file_name)
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    file_name = ''.join(TRANS.get(ord(ch), ch) for ch in file_name)
    return file_name


def proccessing(item):
    if item.is_file():
        file_name, file_ext = item.stem, item.suffix 
        file_ext = file_ext.lower()
        images = ('.jpeg', '.png', '.jpg', '.svg')
        documents = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')
        audio = ('.mp3', '.ogg', '.wav', '.amr')
        video = ('.avi', '.mp4', '.mov', '.mkv')
        archives = ('.zip', '.gz', '.tar')
        file_name = normalize(file_name)
        
        norm_name = file_name + file_ext
        if file_ext in images:
            Path.mkdir(item.parent / 'images', exist_ok=True)
            item.rename(item.parent / 'images' / norm_name)
        elif file_ext in documents:
            Path.mkdir(item.parent / 'documents', exist_ok=True)
            item.rename(item.parent / 'documents' / norm_name) 
        elif file_ext in audio:
            Path.mkdir(item.parent / 'audio', exist_ok=True)
            item.rename(item.parent / 'audio' / norm_name)    
        elif file_ext in video:
            Path.mkdir(item.parent / 'video', exist_ok=True)
            item.rename(item.parent / 'video' / norm_name)  
        elif file_ext in archives:
            try:
                Path.mkdir(item.parent / 'archives', exist_ok=True)
                item.rename(item.parent / 'archives' / norm_name)
                shutil.unpack_archive(Path(item.parent / 'archives' / norm_name), Path(item.parent / 'archives' / file_name))
            except shutil.ReadError:
                print("File can't be procceeded, please check if it's archive.")
            
  
def sorter(path):
    ignore_list = ('archives', 'video', 'audio', 'documents', 'images')
    for item in path.glob('*'):
        if item.is_dir() and item.name not in ignore_list:
            sorter(item)
            if not list(item.glob('*')):
                item.rmdir()
        elif item.is_file():
            print(f'file {item}')
            print(item.parent)
            proccessing(item)
            
            
path = Path(input('Ввведіть будь-ласка шлях до папки: '))
sorter(path)


