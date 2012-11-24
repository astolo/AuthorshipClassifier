import numpy
import WordFrequencies
import FileVector
import os
import codecs

def cosine(vector1, vector2):
    """ related documents j and q are in the concept space by comparing the vectors :
    cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
    if (numpy.linalg.norm(vector1) == 0 or numpy.linalg.norm(vector2) == 0):
        return 0

    cosine = float(numpy.dot(vector1, vector2) / (numpy.linalg.norm(vector1) * numpy.linalg.norm(vector2)))
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

COUNTER = 0

def calculateDistanceFromAllVectorsInList(fileVector, fileVectorList, metric, counter):
    distanceList = [metric(fileVector.featureVector, vector.featureVector) for vector in fileVectorList]
    counter += 1
    return numpy.array(distanceList)

class FileVectorCollection(object):
    """ description of the class"""

    def __init__(self, wordListFilePath, sourceFileDirectory=None):
        with codecs.open(wordListFilePath, 'r', 'utf-8') as wordsListFile:
            self.wordList = wordsListFile.read().split()
        self.vectorsList = []
        if (sourceFileDirectory != None):
            self.addRecursiveDirectoriesToCollection(sourceFileDirectory)
        pass

    def calculateDistanceMatrix(self, distanceMetric):
        if distanceMetric == 'cosine':
            metric = cosine
        if distanceMetric == 'euclidean':
            metric = euclidean
        COUNTER = 0
        distanceVectorList = [calculateDistanceFromAllVectorsInList(fileVector, self.vectorsList, metric, COUNTER) for fileVector in self.vectorsList]
        adjacencyMatrix = numpy.array(distanceVectorList)
        return adjacencyMatrix


    def addRecursiveDirectoriesToCollection(self, directroyPath):
        for root, subFolders, files in os.walk(directroyPath):
            for filename in files:
                filePath = os.path.join(root, filename)
                fileVector = FileVector.FileVector(filePath, self.wordList)
                self.vectorsList.append(fileVector)
        pass


    def saveCollectionToFile(self, outputFilePath):
        with open(outputFilePath, "w") as collectionFile:
            for fileVector in self.vectorsList:
#                collectionFile.write(fileVector)
                collectionFile.write(fileVector.__str__())
            #collectionFile.writelines(self.vectorsList)

    def loadCollectionFromFile(self, inputFilePath):
        with open(inputFilePath) as collectionFile:
            vectors = collectionFile.readlines()
            for vector in vectors:
                array, filePath, cluster = vector.split('\t')
                collectionVector = numpy.fromString(array)
                fileVector = FileVector.FileVector(filePath, None, collectionVector, cluster, False)
                self.vectorsList.append(fileVector)

    def getVectorsProperties(self):
        maxVector = max(self.vectorsList, key=lambda x: x.sum)
        minVector = min(self.vectorsList, key=lambda x: x.sum)
        return (maxVector.sum, minVector.sum)

    def getCovMatrix(self, filePath):
        vectorList = [fileVector.featureVector for fileVector in self.vectorsList]
        cov = numpy.cov(numpy.array(vectorList))
        numpy.savetxt(filePath, cov)
        return cov