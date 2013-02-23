import numpy
import os

SVM_LEARN_PATH = r'c:\Thesis\Code\AuthorshipClassifier\AuthorshipClassifier\svm_multiclass_learn.exe'
SVM_CLASSIFY_PATH = r'c:\Thesis\Code\AuthorshipClassifier\AuthorshipClassifier\svm_multiclass_classify.exe'
SVM_CLUSTERING_DIRECTORY = r'C:\Thesis\Temp\svm'
TRAINING_FILE_NAME = 'training'
MODEL_FILE_NAME = 'model'
TEST_FILE_NAME = 'tests'
CLUSTERS_FILE_NAME = 'clusters'

class SVMClustering(object):
    """ description of the class"""

    def __init__(self, testVectorList, trainingVectorList):
        self.testVectorList = testVectorList
        self.trainingVectorList = trainingVectorList

    def __vectorToFile(self, vectorList, filePath, graphFormat = 'svmlight' ):

        #numpy.savetxt(filePath, self.adjacencyMatrix, fmt='%1d', delimiter = ' ')

        with open(filePath, 'w') as graphFile:
            line = ""
            for vector  in vectorList:
                line = "%d " % (vector.cluster)
                for i in range(1, len(vector.featureVector)):
                    line = line + "%d:%d " % (i, vector.featureVector[i])
                line = line + '#%s\n' % (vector.filePath)
                graphFile.write(line)
        return filePath

    def getClusters(self, numberOfClusters):
        trainingFilePath = os.path.join(SVM_CLUSTERING_DIRECTORY , TRAINING_FILE_NAME)
        self.__vectorToFile(self.trainingVectorList, trainingFilePath)
        errorTradeOff = 0.001
        modelFilePath = os.path.join(SVM_CLUSTERING_DIRECTORY , MODEL_FILE_NAME)
        commandLine =  '%s -c %f %s %s' % (SVM_LEARN_PATH, errorTradeOff, trainingFilePath, modelFilePath)
        os.chdir(SVM_CLUSTERING_DIRECTORY)
        os.system(commandLine)
        testFilePath = os.path.join(SVM_CLUSTERING_DIRECTORY , TEST_FILE_NAME)
        self.__vectorToFile(self.testVectorList, testFilePath)
        clustersFilePath = os.path.join(SVM_CLUSTERING_DIRECTORY , CLUSTERS_FILE_NAME)
        commandLine = '%s %s %s %s' % (SVM_CLASSIFY_PATH, testFilePath, modelFilePath, clustersFilePath)
        os.system(commandLine)
        with open(clustersFilePath) as clustersFile:
             clusterFileLines = clustersFile.readlines()
             zippedList = zip(clusterFileLines, self.testVectorList)
             for zipTuple in zippedList:
                cluster = zipTuple[0].split()[0]
                zipTuple[1].cluster = int(cluster)

        clusters = [None] * numberOfClusters
        allVectorsList = []
        allVectorsList.extend(self.testVectorList)
        allVectorsList.extend(self.trainingVectorList)
        for vector in allVectorsList:
            i = vector.cluster - 1
            if (clusters[i] == None):
                clusters[i] = [vector]
            else:
                clusters[i].append(vector)
        i = 0
        for cluster in clusters:
            clusterFilePath = clustersFilePath + "-%d" % (i)
            with open(clusterFilePath, "w") as clusterFile:
                for vector in cluster:
                    clusterFile.writelines(vector.clusterString())
            i = i + 1

        return clusters

