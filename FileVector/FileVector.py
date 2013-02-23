import WordFrequencies
import numpy

MIN_FREQUENCY = 0.0001

class FileVector(object):
    """description of class"""

    def computeFeatureVector(self, wordList, isHistogram):
        # make the next 3 lines as a template function.
        wordFreq = WordFrequencies.WordFrequencies(r'')
        wordFreq.addFileToDictionary(self.filePath)
        fileWordsList = map(lambda word: int(wordFreq.hasWordInDictionary(word, MIN_FREQUENCY)) , wordList)
        self.sum = sum(fileWordsList)
        self.featureVector = numpy.array(fileWordsList)

    def __init__(self, filePath, wordsList, featureVector=None, cluster=0, isHistogram=False ):
        self.filePath = filePath
        self.cluster = cluster
        self.sum = 0
        if (featureVector != None):
            self.featureVector = featureVector
        else:
            self.computeFeatureVector(wordsList, isHistogram)
        pass

    def __str__(self):
        return "%s\t%s\t%s\t%d\n" % (str(self.featureVector.tolist()), self.filePath, self.cluster, self.sum)

    def clusterString(self):
        return "%s\t%s\t%d\n" % (self.filePath, self.cluster, self.sum)

    def setCluster(self, cluster):
        self.cluster = cluster




