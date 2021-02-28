import pickle
from itertools import zip_longest
from pickled_index import load_bin, remove_file, write_bin
from sortedcontainers import SortedDict



def append_index(index : 'SortedDict', index_filename : str):
    ''' appends index to merged_index.txt
        Keeps track of position
    '''
    global POSITION
    with open(index_filename, "a") as f:
        for key in index:
            line = "{} {}\n".format(key, index[key])
            f.write(line)
            index_index[key] = POSITION
            POSITION += len(line)

def process_line(line : str) -> (str, [(int)]):
    '''A helper function made to process lines in each index file
        A valid line is "token [(m, n, ...), ...]"

        Returns a tuple of the token and a posting if the line is valid
    '''
    if line.isspace() or line == "":
        return None

    line = line.strip()
    return line[:line.find(" ")], eval(line[line.find(" "):])

def find_min_word(lines : [(str, [(int)])]) -> str:
    ''' Returns the minimum word in lines, not counting empty string
    '''
    min_word = "{" # first character after alphanumerics in ASCII table
    for l in lines:
        if l != None:
            if l[0] < min_word:
                min_word = l[0]
    return min_word

def process_index_segment(index_arr : list, positions) -> [int]:
    '''Seek to the last known positions in the indexes
        Read m lines from n files
        Create merged index
        Merge all postings lists for each token
        Write the completed mereged index to a new file...
 
    '''
    for index, last_pos in zip(index_arr, positions):
        if last_pos != -1:
            index.seek(last_pos)
    
    merged_index = SortedDict()
    lines = [process_line(i.readline()) for i in index_arr]
    min_word = find_min_word(lines)
    for j in range(len(lines)):
        # empty or whitespace-only line means we hit end of file
        if lines[j] == None:
            positions[j] = -1
        else:
            token, postings = lines[j]
            if token == min_word:
                if token not in merged_index:
                    merged_index[token] = postings
                else:
                    merged_index[token] += postings
                positions[j] = index_arr[j].tell()
    
    # write to file
    append_index(merged_index, "merged_index.txt")
    return positions      
    

def no_more_lines(positions : [int]) -> bool:
    '''If all file positions are -1...
        We have no more merging to do...
    '''
    for i in positions:
        if i != -1:
            return False
    return True

def open_files(INDEX_COUNT=3) -> "[File]":
    # open index files
    indexes = []
    # INDEX_COUNT = 3 # represents the amount of indexes...
    for i in range(0,INDEX_COUNT):
        try:
            index_path = "index" + str(i+1) + ".txt"
            print(index_path)
            indexes.append(open(index_path, "r"))
        except FileNotFoundError:
            print("{} not found!".format(index_path))
    return indexes

def close_files(files : '[File]') -> None:
    for f in files:
        f.close()

if __name__ == "__main__":

    POSITION = 0
    index_index = SortedDict()

    remove_file("merged_index.txt")
    remove_file("index_index.bin")
    
    INDEX_COUNT = 3
    indexes = open_files()

    # recurse through all files to merge them
    positions = [0 for i in range(INDEX_COUNT)]
    while not no_more_lines(positions):
        print(positions)
        print(POSITION)
        positions = process_index_segment(indexes, positions)
    
    close_files(indexes)
    write_bin("index_index.bin", index_index)
    

