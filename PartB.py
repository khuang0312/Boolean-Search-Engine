from PartA import *

if __name__ == "__main__":
    file1Text = set(tokenize(sys.argv[1]))
    file2Text = set(tokenize(sys.argv[2]))
    commonWords = file1Text.intersection(file2Text)
    print(len(commonWords))