import numpy
import math
import scipy.spatial.distance

TOP_ANGLE = 1.0 / math.sqrt(2)
BOTOM_ANGLE = 0.1
CLOSEST_VECTORS_RATIO = 0.3

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

class FileVectorCluster(object):
    """description of class"""

    def __init__(self, vectorList):
        self.vectorList = vectorList
        self.center = self.calculateCenter()
        pass

    def vectorIsInCore(self, vector, clustersCenterList):
        vectorToCenterAngle = angle(vector, self.center)
        #if vectorToCenterAngle < TOP_ANGLE:
        #    return False
        for clusterCenter in clustersCenterList:
            if (numpy.alltrue(clusterCenter == self.center)):
                continue
            else:
                otherCenterVectorAngle = angle(vector, clusterCenter)
                if(vectorToCenterAngle -  otherCenterVectorAngle < BOTOM_ANGLE):
                    return False
        return True

    def calculateCenter(self):
        clusterVectors = [vector.featureVector for vector in self.vectorList]
        average = numpy.sum(clusterVectors, axis=0) * 1.0 / len(self.vectorList)
        return average

    # retruns a list of vectors in this core cluster
    def calculateCoreVectors(self, clustersCenterList):
        coreVectors = [vector for vector in self.vectorList if self.vectorIsInCore(vector.featureVector, clustersCenterList )]
        return coreVectors

    def getClosestToCenter(self):
        vectorsList = [vector.featureVector for vector in self.vectorList]
        vectorArray = numpy.array(vectorsList)
        #distanceVector = numpy.linalg.norm(numpy.subtract(vectorArray, self.center))
        distanceVector = numpy.apply_along_axis(numpy.linalg.norm, 1, numpy.subtract(vectorArray, self.center))
        distanceList = distanceVector.tolist()
        distanceZipped = zip(self.vectorList, distanceList)
        distanceResult = sorted(distanceZipped, key=lambda distance: distance[1])
        listSize = int( len(distanceList) * CLOSEST_VECTORS_RATIO)
        distanceResultVectors, distances  = zip(*distanceResult)
        result = distanceResultVectors[:listSize]
        return result

    def getFurthestFromCenters(self, clustersCenterList):
        vectorsList = [vector.featureVector for vector in self.vectorList]
        vectorArray = numpy.array(vectorsList)
        result = None
        for center in clustersCenterList:
            if numpy.array_equal(center, self.center):
                continue
            distanceVector = numpy.sum(numpy.abs(numpy.subtract(vectorArray, center))**2,axis=-1)**(1./2)
            #distanceVector = numpy.linalg.norm(numpy.subtract(vectorArray, self.center))
            distanceList = distanceVector.tolist()
            distanceZipped = zip(self.vectorList, distanceList)
            distanceResult = sorted(distanceZipped, key=lambda distance: distance[1], reverse = True)
            listSize = int( len(distanceList) * CLOSEST_VECTORS_RATIO)
            distanceResultVectors, distances  = zip(*distanceResult)
            result = [vector for vector in distanceResultVectors[:listSize] if (result == None or vector in result) ]
        return result

    def calculateCoreVectors2(self, clustersCenterList):
        closestToCenterList = self.getClosestToCenter()
        furthestFromOtherList = self.getFurthestFromCenters(clustersCenterList)
        coreVectors = [vector for vector in self.vectorList if vector in closestToCenterList and vector in furthestFromOtherList]
        return coreVectors