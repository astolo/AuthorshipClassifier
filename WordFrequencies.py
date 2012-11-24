import os
import operator

class WordFrequencies(object):
    """This class calculates word frequencies"""

    def __init__(self, iniFilePath):
        self.wordDict = {u'':0}
        self.numOfTotalWords = 0
        pass

    def addRecursiveDirectoriesToDictionary(self, directroyPath):
        for root, subFolders, files in os.walk(directroyPath):
            for filename in files:
                filePath = os.path.join(root, filename)
                self.addFileToDictionary(filePath)
                print 'Added file: %s. Total words: %d' % (filePath,self.numOfTotalWords)
        pass

    def addFileToDictionary(self, wordFilePath):
        with open(wordFilePath) as wordsFile:
            wordsList = wordsFile.read().split()
            self.numOfTotalWords += len(wordsList)
            for word in wordsList:
                if (len(word) == 1):
                    continue
                unicodeWord = unicode(word, 'utf-8')
                if unicodeWord in self.wordDict:
                    self.wordDict[unicodeWord] +=1
                else:
                    self.wordDict[unicodeWord] = 1

        pass

    def getFequencyDictionary(self, minFrequency = 0, maxFreqency = 1):
        freq_dict = dict()
        numOfUniqueWords = len(self.wordDict)
        print 'Number Of Words: %s' % (self.numOfTotalWords)
        print 'Number Of Unique Words: %s' % (numOfUniqueWords)
        for word, num_of_instances in self.wordDict.iteritems():
            wordFreqency = float(num_of_instances) / self.numOfTotalWords
            if (( maxFreqency > wordFreqency) and ( minFrequency < wordFreqency )):
                freq_dict[word] = wordFreqency
        return freq_dict

    def hasWordInDictionary(self, word):
        return self.wordDict.has_key(word)

    def printFreqencyDictionaryToFileSorted(self, dictionary, filePath, printFrequencies = True):
        with open(filePath,'w') as dictionayFile:
            sortedDict = sorted(dictionary.iteritems(), key=operator.itemgetter(1), reverse=True)
            for word, frequency in sortedDict:
                wordLine = word
                if (printFrequencies):
                    wordLine += '\t' + '%f' % (frequency)
                dictionayFile.write(wordLine.encode('utf-8') + '\n')
        pass
