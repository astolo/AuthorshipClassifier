
#from numpy import *
import numpy
import numpy.linalg
import scipy
import scipy.spatial.distance
import math
import os
import codecs
import WordFrequencies

ADJENCY_GRAPH_FILE_NAME = 'graph.txt'
FILE_VECTORS_FILE_NAME = 'fileVectors.txt'
FILE_NAMES_FILE_NAME = 'names.txt'

GRACLUS_EXTENSION = '.part.2'

TOP_ANGLE = math.sqrt(2)
BOTOM_ANGLE = 0.1

def cosine(vector1, vector2):
    """ related documents j and q are in the concept space by comparing the vectors :
    cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
    #cosine = float(numpy.dot(vector1, vector2) / (numpy.linalg.norm(vector1) * numpy.linalg.norm(vector2)))
    cosine = scipy.spatial.distance.cosine(vector1, vector2)
    return cosine

def euclidean(vector1, vector2):
    euclidean = abs(numpy.linalg.norm(vector1 - vector2))
    if (euclidean != 0):
        euclidean = 1.0 / euclidean
    else:
        euclidean = 1.0
    return euclidean

def angle(vector1, vector2):
    return numpy.arccos(cosine(vector1,vector2))

def angleIsInRange(i, matrix, angleVector, coreMatrix):
    if ( angleVector[i] < TOP_ANGLE and angleVector[i] > BOTOM_ANGLE ):
        if (coreMatrix == None):
            coreMatrix = numpy.array(matrix[i])
        else:
            coreMatrix = numpy.vstack((coreMatrix, matrix[i]))
    pass

def alongAxis(array1, matrix, metric):
    row = numpy.apply_along_axis(metric, 1, matrix, array1)
    return row

class ClustersGraph(object):
    """description of class"""

    def __init__(self, wordListFilePath, outputDirPath):
        #with open(wordListFilePath) as wordsListFile:
        with codecs.open(wordListFilePath, 'r', 'utf-8') as wordsListFile:
            self.wordList = wordsListFile.read().split()
        self.graph = None
        self.outputDirPath = outputDirPath
        self.adjacencyMatrix = numpy.array([])
        self.fileNamesFilePath = os.path.join(self.outputDirPath, FILE_NAMES_FILE_NAME)
        pass

    def InitFromAdjacencyGraph(self, graphFilePath):
        self.adjacencyMatrix = numpy.loadtxt(graphFilePath)
        pass

    def InitFromBooleanWordExistanceGraph(self, wordExistanceGraphFilePath, directroyPath):
        self.graph = numpy.loadtxt(wordExistanceGraphFilePath)
        with open(self.fileNamesFilePath,'w') as fileNamesFile:
            for root, subFolders, files in os.walk(directroyPath):
                for filename in files:
                    filePath = os.path.join(root, filename)
                    fileNamesFile.write(filePath + '\n')
        pass

    def addRecursiveDirectoriesToGraph(self, directroyPath):
        with open(self.fileNamesFilePath,'w') as fileNamesFile:
            for root, subFolders, files in os.walk(directroyPath):
                for filename in files:
                    filePath = os.path.join(root, filename)
                    fileNamesFile.write(filePath + '\n')
                    self.addFileToGraph(filePath)
        vectorsFilePath = os.path.join(self.outputDirPath , FILE_VECTORS_FILE_NAME)
        numpy.savetxt(vectorsFilePath,self.graph, delimiter = ' ')
        pass

    def addFileToGraph(self, filePath):
        # make the next 3 lines as a template function.
        wordFreq = WordFrequencies.WordFrequencies(r'')
        wordFreq.addFileToDictionary(filePath)
        fileWordsList = map(lambda word: int(wordFreq.hasWordInDictionary(word)) , self.wordList)
        if (self.graph == None):
            self.graph = numpy.array(fileWordsList)
        else:
            self.graph = numpy.vstack((self.graph, numpy.array(fileWordsList)))
        pass

    def calculateAdjacencyMatrix(self, distanceMetric):
        if distanceMetric == 'cosine':
            metric = cosine
        if distanceMetric == 'euclidean':
            metric = euclidean
        #self.adjacencyMatrix = scipy.spatial.distance.pdist(self.graph, 'euclidean')
        self.adjacencyMatrix = numpy.apply_along_axis(alongAxis, 1, self.graph, self.graph, metric)
        pass

    def toFile(self, roundToIntegers, graphFormat = 'graclus' ):
        filePath = os.path.join(self.outputDirPath , ADJENCY_GRAPH_FILE_NAME)
        if roundToIntegers:
            self.adjacencyMatrix = self.adjacencyMatrix * 1000
        #numpy.savetxt(filePath, self.adjacencyMatrix, fmt='%1d', delimiter = ' ')

        with open(filePath, 'w') as graphFile:
            matrixLen = self.adjacencyMatrix.shape
            header = "%d %d 1\n" % (matrixLen[0], (matrixLen[0]) * (matrixLen[1] - 1) /2)
            graphFile.write(header)
            line = ""
            for x in range(0, matrixLen[0] ):
                for y in range(0, matrixLen[1] ):
                    if (x != y ):
                            line = line + "%d %d " % (y + 1, self.adjacencyMatrix[x, y])
                graphFile.write(line + "\n")
                line =""
        return filePath

    def dumpClustersToFile(self, outputDirPath):
        if (outputDirPath == None):
            outputDirPath = self.outputDirPath
        with open(os.path.join(outputDirPath, ADJENCY_GRAPH_FILE_NAME + GRACLUS_EXTENSION), 'r') as clusteringFile:
            with open(os.path.join(outputDirPath, FILE_NAMES_FILE_NAME), 'r') as fileNamesFile:
                clusteringList = clusteringFile.readlines()
                fileNamesList = fileNamesFile.readlines()
        with open(os.path.join(outputDirPath, '0.txt'), 'w') as firstClusterFile:
            with open(os.path.join(outputDirPath, '1.txt'), 'w') as secondClusterFile:
                for index in range(0,len(clusteringList)):
                   if int(clusteringList[index]) == 0:
                       firstClusterFile.write(fileNamesList[index])
                   else:
                       secondClusterFile.write(fileNamesList[index])

        pass

    def calculateGraphCentorid(self, matrix):
        matrixLen = matrix.shape
        average = numpy.sum(matrix, axis=0) * 1 / matrixLen[0]
        return average

    def calculateAnglesVector(self, matrix):
        average = calculateAnglesVector(matrix)
        anglesVector = numpy.apply_along_axis(angle, 1, matrix, average)
        return anglesVector

    def calculateCoreMatrix(self, matrix):
        coreMatrix = None
        matrixLen = matrix.shape
        anglesVector = calculateAnglesVector(matrix)
        a = (angleIsInRange(i, matrix, angleVector, coreMatrix) for i in xrange(matrixLen[0]))
