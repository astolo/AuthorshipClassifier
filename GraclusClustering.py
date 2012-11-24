import numpy
import os

GRACLUS_PATH = r'c:\Thesis\Code\AuthorshipClassifier\AuthorshipClassifier\graclus.exe'
TEMPORARY_PATH = r'C:\Thesis\Temp\results1'
TEMPORARY_FILE_NAME = 'results1'
ADJENCY_GRAPH_FILE_NAME = 'graph.txt'
GRACLUS_EXTENSION = '.part.'

class GraclusClustering(object):
    """ description of the class"""

    def __init__(self, distanceMatrix, vectorList):
        self.distanceMatrix = distanceMatrix
        self.vectorList = vectorList

    def __distanceMatrixToFile(self, filePath, roundToIntegers, graphFormat = 'graclus' ):
        if roundToIntegers:
            self.distanceMatrix = self.distanceMatrix * 10000
        #numpy.savetxt(filePath, self.adjacencyMatrix, fmt='%1d', delimiter = ' ')

        with open(filePath, 'w') as graphFile:
            matrixLen = self.distanceMatrix.shape
            header = "%d %d 1\n" % (matrixLen[0], (matrixLen[0]) * (matrixLen[1] - 1) /2)
            graphFile.write(header)
            line = ""
            for x in range(0, matrixLen[0] ):
                for y in range(0, matrixLen[1] ):
                    if (x != y ):
                            line = line + "%d %d " % (y + 1, self.distanceMatrix[x, y])
                graphFile.write(line + "\n")
                line =""
        return filePath

    def getClusters(self, numberOfClusters):
        graphFilePath = os.path.join(TEMPORARY_PATH , ADJENCY_GRAPH_FILE_NAME)
        self.__distanceMatrixToFile(graphFilePath, True)
        commandLine =  '%s %s %d' % (GRACLUS_PATH, graphFilePath, numberOfClusters)
        os.chdir(TEMPORARY_PATH)
        os.system(commandLine)
        clustersFilePath = graphFilePath + GRACLUS_EXTENSION + "%d" % (numberOfClusters)
        with open(clustersFilePath) as clustersFile:
            clusterFileLines = clustersFile.readlines()
            zippedList = zip(clusterFileLines, self.vectorList)
            for zipTuple in zippedList:
                zipTuple[1].cluster = int(zipTuple[0])

        clusters = [None] * numberOfClusters
        for vector in self.vectorList:
            i = vector.cluster
            if (clusters[i] == None):
                clusters[i] = [vector]
            else:
                clusters[i].append(vector)
        i = 0
        for cluster in clusters:
            clusterFilePath = graphFilePath + "-%d" % (i)
            with open(clusterFilePath, "w") as clusterFile:
                for fileVector in cluster:
                    clusterFile.write(fileVector.__str__())
                #clusterFile.writelines(cluster)
            i = i + 1
        return clusters

