from os import remove, listdir, scandir

def cleanup_files():
    for f in listdir("."):
        for i in ["index", "doc", "url"]:
            if f.startswith(i):
                print("Removing file {}".format(f))
                remove_file(f)

def write_bin(file_name : str, obj):
    '''Wrapper for writing to file
    '''
    with open(file_name, "wb") as f:
        pickle.dump(obj, f)

def load_bin(file_name : str):
    '''Wrapper for loading a file
    '''
    obj = None
    with open(file_name, "rb") as f:
        obj = pickle.load(f, encoding="UTF-8")
    return obj

def write_file(file_name : str, text : str):
    '''Wrapper for writing to file
    '''
    with open(file_name, "w") as f:
        # pickle.dump(obj, f)
        f.write(text)

def load_file(file_name : str):
    '''Wrapper for loading a file
    '''
    obj = None
    with open(file_name, "r") as f:
        obj = pickle.load(f, encoding="UTF-8")
    return obj

def remove_file(file_path: str):
    try:
        remove(file_path)
    except FileNotFoundError:
        print("File at {} not found.".format(file_path))
