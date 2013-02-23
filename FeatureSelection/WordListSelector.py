#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      stoloa
#
# Created:     22/01/2013
# Copyright:   (c) stoloa 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import math
import sys
import Config
import os
import codecs
import re
import string

def findWholeWordInString(word, str, startIx):
    index = str.find(word, startIx)
    if index == -1:
        return -1
    if index != 0 and str[index-1] not in string.whitespace:
        return -1
    L = index + len(word)
    if L < len(str) and str[L] not in string.whitespace:
        return -1
    return index

def findEndSection(wordList, fileContent, startIx ):
        substrIndex = sys.maxint
        for seperationWord in wordList:
            #tempIndex = fileContent.find(" " + seperationWord + " ", startIx)
            tempIndex = findWholeWordInString(seperationWord, fileContent, startIx)
            if tempIndex < substrIndex and tempIndex != -1:
                substrIndex = tempIndex
        return substrIndex

def findEndSection2(wordList, fileContent, startIx ):
    return re.search('|'.join(wordList), fileContent[startIx:]).start()

def findEndSection3(wordList, fileContent, startIx ):
    indexes = [fileContent.find(" "+ word + " ", startIx) for word in wordList]
    foundIndexes = [index for index in indexes if index != -1]
    if len(foundIndexes) != 0:
        return min(foundIndexes)
    else:
        return sys.maxint

class WordListSelector(object):
    """description of class"""

    def __init__(self):
        #with open(wordListFilePath) as wordsListFile:

        pass

    def addRecursiveDirectories(self, directroyPath):
        config = Config.Config(Config.getConfigIniFilePath())
        with codecs.open(config.getMemraWordListFile(), 'r', 'utf-8-sig') as memraListFile:
            memraList = [memraword.rstrip() for memraword in memraListFile.readlines()]
        with codecs.open(config.getStamaWordListFile(), 'r', 'utf-8-sig') as stamaListFile:
            stamaList = [stamaword.rstrip() for stamaword in stamaListFile.readlines()]
        for root, subFolders, files in os.walk(directroyPath):
            for filename in files:
                filePath = os.path.join(root, filename)
                self.splitFile(filePath, memraList, stamaList)
        pass

    def splitFile(self, filePath, memraWordList, stamaWordList):
        config = Config.Config(Config.getConfigIniFilePath())
        memraSectionList = []
        stamaSectionList = []
        isMemra = True
        isFinished = False
        subStartIx = 0
        subEndIx = sys.maxint
        with codecs.open(filePath, 'r', 'utf-8-sig') as sectionFile:
            fileContent = sectionFile.read()
            while (not isFinished):
                if(isMemra):
                    subEndIx = findEndSection3(stamaWordList, fileContent, subStartIx)
                    if (subEndIx != sys.maxint) :
                        memraSection = fileContent[subStartIx:subEndIx]
                        memraSectionList.append(memraSection)
                        subStartIx = subEndIx
                        isMemra = False
                    else:
                        isFinished = True
                else:
                    subEndIx = findEndSection3(memraWordList, fileContent, subStartIx)
                    if (subEndIx != sys.maxint) :
                        stamaSection = fileContent[subStartIx:subEndIx]
                        stamaSectionList.append(stamaSection)
                        subStartIx = subEndIx
                        isMemra = True
                    else:
                        isFinished = True
        with codecs.open(config.getMemraFilePath(filePath), 'w', 'utf-8-sig') as memraFile:
            memraFile.writelines(memraSectionList)

        with codecs.open(config.getStamaFilePath(filePath), 'w', 'utf-8-sig') as stamaFile:
            stamaFile.writelines(stamaSectionList)

        with codecs.open(config.getMemraFile(), 'a+', 'utf-8-sig') as memraFile:
            memraFile.writelines(memraSectionList)

        with codecs.open(config.getStamaFile(), 'a+', 'utf-8-sig') as stamaFile:
            stamaFile.writelines(stamaSectionList)

        pass