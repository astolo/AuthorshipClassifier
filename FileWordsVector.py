from numpy import *
import WordFrequencies

class FileWordsVector(object):
    """description of class"""

    vector = array([],dtype = int)

    def __init__(self, filePath, wordsList  ):
        wordFreq = WordFrequencies.WordFrequencies("")
        wordFreq.addFileToDictionary(filePath)
        index = 0
        for word in wordsList:
            if wordFreq.hasWordInDictionary(word):
                vector[index] = 1
            else:
                vector[index] = 0
            index = index + 1
        pass



