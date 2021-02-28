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
        return line[0:line.find(" ")], eval(line[line.find(" "):])

def process_index_segment(index_arr : list, positions : [int], LINES=10) -> [int]:
    '''Seek to the last known positions in the indexes
        Read m lines from n files
        Create merged index
        Merge all postings lists for each token
        Write the completed mereged index to a new file...
 
    '''
    for index, last_pos in zip(index_arr, positions):
        if last_pos != -1:
            index.seek(last_pos)
    # read the first line from every index
    
    # figure out what word each file is currently on
    # figure out the minimum word

    # if a index file is not on that minimum word... skip it
    # merge the postings of the index files on the minimum word
   
    # write to disk
    # then readline on the files that had the minimum word (this "catches them up")
    merged_index = SortedDict()
    lines = [process_line(i.readline()) for i in index_arr] 
    for i in range(LINES):
        min_word = min(lines, key=lambda x : x[0] if x != None else "{")
        
        for j in range(len(lines)):
            # empty or whitespace-only line means we hit end of file
            if lines[j] == None:
                positions[j] = -1
                next_lines.append("")
            else: 
                token, postings = lines[j]
                if token == min_word:
                    if token not in merged_index:
                        merged_index[token] = postings
                    else:
                        merged_index[token] += postings
                    positions[j] = index_arr[j].tell()
                    lines[j] = process_line(index_arr[j].readline())
    
    # write to file
    
    return positions      
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

if __name__ == "__main__":

    remove_file("merged_index.txt")
    remove_file("index_index.bin")
    
    # open index files
    POSITION = 0
    indexes = []
    index_index = SortedDict()
    INDEX_COUNT = 3 # represents the amount of indexes...
    for i in range(0,INDEX_COUNT):
        try:
            index_path = "index" + str(i+1) + ".txt"
            print(index_path)
            indexes.append(open(index_path, "r"))
        except FileNotFoundError:
            print("{} not found!".format(index_path))


    # recurse through all files to merge them
    positions = [0 for i in range(INDEX_COUNT)]

        input()    while not no_more_lines(positions):
        print(positions)
        positions = process_index_segment(indexes, positions)
    while not no_more_lines(positions):
        print(positions)
        positions = process_index_segment(indexes, positions)
    while not no_more_lines(positions):
        print(positions)
        positions = process_index_segment(indexes, positions)
    
    write_bin("index_index.bin", index_index)
    

