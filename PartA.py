# functions here
import sys
import re

# runtime: O(N) where N is the size of the file in terms of characters
def tokenize(textFile):
    # [a-zA-Z0-9] only for english
    tokenList = []
    try:
        with open(textFile, 'r') as file:
            isEndOfFile = False
            while not isEndOfFile:
                for index in range(500):
                    line = file.readline()
                    if line == "":
                        isEndOfFile = True
                        break
                    tokenList.extend(re.findall(r'[a-zA-Z0-9]+', line.lower()))
            return tokenList
    except:
        return tokenList

# runtime: O(N) since we are looping through the list of size N
def computeWordFrequencies(tokenList):
    if type(tokenList) is list:
        tokenDict = dict()
        for word in tokenList:
            if word not in tokenDict:
                tokenDict[word] = 1
            else:
                tokenDict[word] += 1
        return tokenDict
    else:
        return dict()

#runtime: O(NlogN) since sorted function inherits this runtime in the worse-cases
def printDict(freqDict):
    for key, val in sorted(freqDict.items(), key = lambda item: item[1], reverse = True):
        print(str(key) + " -> " + str(val))


if __name__ == "__main__":
    textList = tokenize(sys.argv[1])
    wordFreqDict = (computeWordFrequencies(textList))
    printDict(wordFreqDict)