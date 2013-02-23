import ConfigParser
import os
import datetime

BASE_DIR = r"c:\Thesis"
CODE_BASE_DIR = r"Code\AuthorshipClassifier\AuthorshipClassifier"
RESULTS_PATH ="results"
WORDS_LIST_FOLDER = "WordLists"
STAMA_WORDS_LIST_FILE = r'stama-words.txt'
STAMA_FULL_WORDS_LIST_FILE = r'full-stama-words.txt'
MEMRA_WORDS_LIST_FILE = r'memra-words.txt'
RABBANICAL_WORDS_LIST_FILE_PATH = r'Code\AuthorshipClassifier\AuthorshipClassifier\stama-words2.txt'
FREQUENT_WORDS_LIST_FILE = r'c:\Thesis\Code\AuthorshipClassifier\AuthorshipClassifier\frequent.txt'
TALMUD_BY_PEREK = 'TalmudByPerek'
TALMUD_BY_MASECHET = 'Talmud'
TALMUD_BY_MISHNA = 'TalmudByMishna1'
TEMP_COLLECTION_PATH = r'C:\Thesis\Temp\results3'
FINAL_CLUSTERS_FILE_NAME = 'finalCluster'
WORD_BY_FREQ_FILE_NAME = "-dict.txt"
MISHNA_SEPERATOR_FILE_NAME = "seperator.txt"
GRACLUS_PROGRAM_FILE = "graclus.exe"
STAMA_COLLECTION_FILE = 'stama-collection2.txt'
MEMRA_FILE_SUFFIX = "-mem.txt"
STAMA_FILE_SUFFIX =  "-stm.txt"
MEMRA_SUBDIR = "mem"
STAMA_SUBDIR = "stama"
WORD_FREQ_SUBDIR = "word-freq"
MEMRA_FILE_PATH = "memrot.txt"
STAMA_FILE_PATH = "stamaot.txt"
STAMA_VECTOR_COLLECTION_FILE_PATH = "stama_vec_collection.txt"
FREQ_VECTOR_COLLECTION_FILE_PATH = "freq_vec_collection.txt"
VECTOR_COV_FILE_PATH = "vec_cov.txt"
NUM_CLUSTERS = 2

def getConfigIniFilePath():
    return os.path.join(os.path.join(BASE_DIR, CODE_BASE_DIR), "config.ini")

class Config(object):
    """This class parses the ini file """
    parser = ConfigParser.RawConfigParser()

    def __init__(self, iniFilePath):
        self.parser.read(iniFilePath)
        pass

    def __get_config__(self,section, option):
        return self.parser.get(section, option)

    def __get_int_config__(self, section, option):
        return self.parser.getint(section, option)


    def __get_float_config__(self, section, option):
        return self.parser.getfloat(section, option)

    def getResultsPath(self, subDir):
        today = datetime.date.today().strftime("%B %d, %Y")
        resultsPath = os.path.join(BASE_DIR, RESULTS_PATH)
        resultsPath = os.path.join(resultsPath, today, subDir)
        if not os.path.exists(resultsPath):
            os.makedirs(resultsPath)
        return resultsPath

    def getStamaWordListFile(self):
        return os.path.join(BASE_DIR, WORDS_LIST_FOLDER, STAMA_WORDS_LIST_FILE)

    def getStamaFullWordListFile(self):
        return os.path.join(BASE_DIR, WORDS_LIST_FOLDER, STAMA_FULL_WORDS_LIST_FILE)

    def getMemraWordListFile(self):
        return os.path.join(BASE_DIR, WORDS_LIST_FOLDER, MEMRA_WORDS_LIST_FILE)

    def getFrequentWordsListFile(self):
        return os.path.join(BASE_DIR, FREQUENT_WORDS_LIST_FILE)

    def getTalmudByPerekDir(self):
        return os.path.join(BASE_DIR, TALMUD_BY_PEREK)

    def getTalmudByMasechetDir(self):
        return os.path.join(BASE_DIR, TALMUD_BY_MASECHET)

    def getTalmudByMishnaDir(self):
        return os.path.join(BASE_DIR, TALMUD_BY_MISHNA)

    def getWordsByFrequenctListFile(self, wordFreqPrefix):
        return os.path.join(self.getResultsPath(WORD_FREQ_SUBDIR), wordFreqPrefix + WORD_BY_FREQ_FILE_NAME)

    def getMishnaSeperatorFileName(self):
        return os.path.join(BASE_DIR, MISHNA_SEPERATOR_FILE_NAME)

    def getGraclusProgramFilePath(self):
        return os.path.join(os.path.join(BASE_DIR, CODE_BASE_DIR), GRACLUS_PROGRAM_FILE)

    def getMemraFilePath(self, originalFilePath):
        (base, sep, last) = originalFilePath.partition(BASE_DIR)
        fileName = last.replace('\\', '-').replace('/', '-')
        return os.path.join(self.getMemraResultSubDir(), fileName + MEMRA_FILE_SUFFIX)

    def getStamaResultSubDir(self):
        return self.getResultsPath(STAMA_SUBDIR)

    def getMemraResultSubDir(self):
        return self.getResultsPath(MEMRA_SUBDIR)

    def getStamaFilePath(self, originalFilePath):
        (base, sep, last) = originalFilePath.partition(BASE_DIR)
        fileName = last.replace('\\', '-').replace('/', '-')
        return os.path.join(self.getStamaResultSubDir(), fileName + STAMA_FILE_SUFFIX)

    def getMemraFile(self):
        return os.path.join(self.getMemraResultSubDir(), MEMRA_FILE_PATH)

    def getStamaFile(self):
        return os.path.join(self.getStamaResultSubDir(), STAMA_FILE_PATH)

    def getStamaVectorCollectionFile(self):
        return os.path.join(self.getResultsPath(), STAMA_VECTOR_COLLECTION_FILE_PATH)

    def getFreqVectorCollectionFile(self):
        return os.path.join(self.getResultsPath(), FREQ_VECTOR_COLLECTION_FILE_PATH)

    def getCovarianceFile(self):
        return os.path.join(self.getResultsPath(), VECTOR_COV_FILE_PATH)

    def getNumClusters(self):
        return NUM_CLUSTERS