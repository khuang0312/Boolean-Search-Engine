from os import remove, listdir, scandir
import pickle

def cleanup_files():
    '''Deletes all files created by the code...
    '''
    for f in listdir("."):
        for i in ["index", "doc", "url"]:
            if f.startswith(i):
                print("Removing file {}".format(f))
                remove_file(f)

def count_partial_indexes():
    '''Counts partial indexes in the file...
    '''
    count = 0 
    for f in listdir("."):
        if f.startswith("partial_index_file"):
            count += 1
    return count
            

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


# not sure if we need but they might come in handy
def load_posting(filename : str, token : str):
    ''' loads posting of given token '''
    result = list()
    with open(filename, "r") as f:
        pos = index_index[token]
        f.seek(pos)
        line = f.readline()
        result = eval(line)
    return result

# given a query, see if we have it on the dictionary structure
def contains_query(query : str, word_dict : dict) -> bool :
    query = query.lower()
    lst_words = query.split("and")
    for word in lst_words:
        if word not in word_dict: 
            return False
    return True


