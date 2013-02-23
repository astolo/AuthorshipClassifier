"""Module docstring.

This serves as a long usage message.
"""
import sys
import os
import getopt
import WordFrequencies
import ClustersGraph
import shutil
import codecs

import Config
import FileVector
import FileVectorCollection
import FileVectorCluster
import GraclusClustering
import SVMClustering
import WordListSelector

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def mergeDirectoriesToFiles(sourceDirPath, destDirPath):
    for root, subFolders, files in os.walk(sourceDirPath):
        for folderName in subFolders:
            destFilePath = os.path.join(destDirPath, folderName + '.txt')
            dirPath = os.path.join(root, folderName)
            mergeDirectoryFilesToOneFile(destFilePath, dirPath)
        return

def mergeDirectoryFilesToOneFile(outputFilePath, directoryPath):
    outputFile = open(outputFilePath,"a")
    for root, subFolders, files in os.walk(directoryPath):
        for fileName in files:
            if fileName.endswith(".txt"):
                fileObj = open(os.path.join(root, fileName))
                shutil.copyfileobj(fileObj, outputFile)
                fileObj.close()
    outputFile.close()

def splitFileByString(sourceFilePath, destDirPath, stringToSplit):
    with open(sourceFilePath) as perekFile:
        perekText = perekFile.read().decode('utf-8')
        mishnaList = perekText.split(stringToSplit)
        mishnaDir = os.path.join(destDirPath, os.path.basename(sourceFilePath).replace(".txt",""))
        try:
            os.makedirs(mishnaDir)
        except OSError:
            pass
        index = 0
        for mishna in mishnaList:
            index = index + 1
            fileName = "mishna%d.txt" % (index)
            mishnaFilePath = os.path.join(mishnaDir, fileName)
            with open(mishnaFilePath, 'w') as mishnaFile:
                mishnaFile.write(mishna.encode('utf-8'))
    pass

def recursivelySplitFilesInDirectory(sourceDirPath, destDirPath, stringToSplit):
    for root, subFolders, files in os.walk(sourceDirPath):
         for folderName in subFolders:
            outputDirPath = os.path.join(destDirPath, folderName)
            perekDirPath = os.path.join(root, folderName)
            for sourceRoot, folders, fileNames in os.walk(perekDirPath):
                for perekFile in fileNames:
                    sourceFilePath = os.path.join(sourceRoot, perekFile)
                    splitFileByString(sourceFilePath, outputDirPath, stringToSplit)
    pass

def getWordFrequencies(wordFilesDir, resultFilePath):
    wordFreq =  WordFrequencies.WordFrequencies("")
    wordFreq.addRecursiveDirectoriesToDictionary(wordFilesDir )
    freqDict = wordFreq.getFequencyDictionary()
    wordFreq.printFreqencyDictionaryToFileSorted(freqDict, resultFilePath )
    #wordFreq.printFreqencyDictionaryToFileSorted(freqDict, r'c:\Thesis\py-dict.txt', False)
    print 'Finished parsing files'

def mainWordFreq(argv = None):
    config = Config.Config(Config.getConfigIniFilePath())
    #getWordFrequencies(config.getTalmudByPerekDir(), config.getWordsByFrequenctListFile())
    getWordFrequencies(config.getStamaResultSubDir(), config.getWordsByFrequenctListFile("stama"))
    getWordFrequencies(config.getMemraResultSubDir(), config.getWordsByFrequenctListFile("mem"))

def main(argv=None):
    if argv is None:
        argv = sys.argv

    config = Config.Config(Config.getConfigIniFilePath())
    filesDirPath = r'C:\Thesis\TalmudByPerek\Shabbos'
    talmudByPerekDirPath = config.getTalmudByPerekDir()
    talmudDirPath = config.getTalmudByMasechetDir()
    talmudByMishnaDirPath = config.getTalmudByMishnaDir()
    seperatorFilePath = config.getMishnaSeperatorFileName()
    #mergeDirectoriesToFiles(talmudByPerekDirPath, talmudDirPath)
    with open(seperatorFilePath) as seperatorFile:
        seperatorString = unicode(seperatorFile.read(),'utf-8')
    #recursivelySplitFilesInDirectory(talmudByPerekDirPath,talmudByMishnaDirPath, seperatorString)
    graphDirPath = r'c:\Thesis\Code\AuthorshipClassifier\AuthorshipClassifier\out3'
    graphFileName = 'graph.txt'
    wordsListFilePath = config.getStamaWordListFile()
    cGraph = ClustersGraph.ClustersGraph(wordsListFilePath, graphDirPath)
    #cGraph.addRecursiveDirectoriesToGraph(talmudDirPath)
    cGraph.InitFromBooleanWordExistanceGraph(graphDirPath + '\\' + ClustersGraph.FILE_VECTORS_FILE_NAME, talmudDirPath)
    cGraph.calculateAdjacencyMatrix('cosine')
    graphFilePath = cGraph.toFile(True)
    commandLine = config.getGraclusProgramFilePath + ' %s 2' % (graphFilePath)
    os.chdir(graphDirPath)
    os.system(commandLine)
    cGraph.dumpClustersToFile(graphDirPath)
    #raw_input()
    #try:
    #    try:
    #        opts, args = getopt.getopt(argv[1:], "h", ["help"])
    #    except getopt.error, msg:
    #         raise Usage(msg)
    #
    #


    #except Usage, err:
    #    print >>sys.stderr, err.msg
    #    print >>sys.stderr, "for help use --help"
    #    return 2


TEMP_COLLECTION_PATH = r'C:\Thesis\Temp\results3'
FINAL_CLUSTERS_FILE_NAME = 'finalCluster'

def splitFiles(argv = None):
    config = Config.Config(Config.getConfigIniFilePath())
    selector = WordListSelector.WordListSelector()
    selector.addRecursiveDirectories(config.getTalmudByPerekDir())
    mainWordFreq()

def mainAlgorithm(argv=None):
    if argv is None:
        argv = sys.argv

    config = Config.Config(Config.getConfigIniFilePath())
    # get files as vector by first word list file  and compute distance matrix
    vectorCollection = FileVectorCollection.FileVectorCollection(config.getStamaWordListFile() , config.getTalmudByPerekDir())
    vectorCollection.saveCollectionToFile(config.getStamaVectorCollectionFile())
    distanceMatrix = vectorCollection.calculateDistanceMatrix('cosine')

    (maxVector, minVector) = vectorCollection.getVectorsProperties()
    cov = vectorCollection.getCovMatrix(config.getCovarianceFile())


    # cluster the vectors using kernel kmeans
    clustering = GraclusClustering.GraclusClustering(distanceMatrix, vectorCollection.vectorsList)
    clusters = clustering.getClusters(config.getNumClusters())

    # count how many ones in each vector, what is the max. for both mishna and perek
    # what is the dense vector and the sparse
    # what is the range of pairwise similarity values?

    # calculate new vectors by a differnet word list file
    newVectorCollection = FileVectorCollection.FileVectorCollection(config.getFrequentWordsListFile(),config.getTalmudByPerekDir())
    vectorCollection.saveCollectionToFile(config.getFreqVectorCollectionFile())
    #distanceMatrix = vectorCollection.calculateDistanceMatrix('cosine')

    trainingVectorsList = []
    testVectorList = []
    allVectorslist = []

    clustersCenter = []
    for cluster in clusters:
        clustersCenter.append(FileVectorCluster.FileVectorCluster(cluster).center)

    with codecs.open(config.getFrequentWordsListFile(), 'r', 'utf-8') as wordsListFile:
            wordList = wordsListFile.read().split()
    i = 1
    for cluster in clusters:
        oldCluster = FileVectorCluster.FileVectorCluster(cluster)
        coreVectorsInCluster = oldCluster.calculateCoreVectors2(clustersCenter)
        newCoreVectors = [FileVector.FileVector(vector.filePath, wordList, None, i) for vector in coreVectorsInCluster]
        tempSet = set(coreVectorsInCluster)
        otherVectors = [FileVector.FileVector(vector.filePath, wordList, None, i) for vector in cluster if vector not in tempSet]
        trainingVectorsList = trainingVectorsList + newCoreVectors
        testVectorList = testVectorList + otherVectors
        i = i + 1

    # svm classifier
    svmclustering = SVMClustering.SVMClustering(testVectorList, trainingVectorsList)
    newClusters = svmclustering.getClusters(config.getNumClusters())

if __name__ == "__main__":
    #sys.exit(mainAlgorithm())
    #sys.exit(main())
    sys.exit(splitFiles())