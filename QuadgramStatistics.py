#################################################################################################################################
# Author: Sam Alhaqab
# This program uses the hill climbing algorithm in conjunction with quadgram statistics to decrypt any simple substitution cipher
# Please note that given the same piece of text the hill climbing algorithm may and usually returns different results
#################################################################################################################################

from math import log10
from random import randint

class QuadgramStatistics:
    # can't take the log of 0 so 'ZERO' is my 0 value when calculating fitness of quadgrams with frequency of zero
    ZERO =  0.00000000000001
    def __init__(self, dataFilePath):
        self.DATA_FILE_PATH = dataFilePath
        self.TOTAL_QUADGRAMS = 0
        self.ZERO_FREQUENCY_FITNESS = 0
        self.QUADGRAM_FREQUENCY_MAP = dict()
        self.QUADGRAM_FITNESS_MAP = dict()
        self.initMaps()
        
    def printStatistics(self):
        print("----------------------------------------------------------------------------------------------------------")
        print(f"data file path:    {self.DATA_FILE_PATH}")
        print(f"total quadgrams:   {self.TOTAL_QUADGRAMS}")
        print(f"zero fitness freq: {self.ZERO_FREQUENCY_FITNESS}")
        # print(f"{self.QUADGRAM_FREQUENCY_MAP}")
        # print(f"{self.QUADGRAM_FITNESS_MAP}")
        print("----------------------------------------------------------------------------------------------------------")


    # the log probability of a text is its fitness (how similar it is to English texts)
    # this function calculates the log probability of a SINGLE quadgram (four letters)
    # the probability of a quadgram is define as:
    # p(quadgram) = frequency(quadgram) / total quadgrams
    # taking the log is neccessary because multiplying together small probabilities, numerical underflow can occur in floating point numbers
    # p(apieceoftext) = p(apie) x p(piec) x p(iece) x ... x p(ftex) x p(text) <-- numerical underflow can occur
    # log(p(apieceoftext)) = log(p(apie)) + log(p(piec)) + log(p(iece)) + ... + log(p(ftex)) + log(p(text)) <-- problem solved
    def logProbability(self, qm, totalQM, text):
        frequency = qm.get(text, QuadgramStatistics.ZERO) # if the quadgram does not exist in our data set then its frequency will be ZERO = 0.00000000000001
        fitness = log10(frequency/totalQM)
        return fitness

    # used to determine the number of total quadgrams within my data set
    def totalQuadgrams(self, frequency):
        totalQuadgrams = 0
        for value in frequency:
            totalQuadgrams += value
        return totalQuadgrams
    
    def initMaps(self):
        print("----------------------------------------------------------------------------------------------------------")
        print(">>> INITIALIZING MAP WITH DATA FILE...")

        # places each quadgram and its frequency in a dictionary/map data structure:
        quadgramsFile = open(self.DATA_FILE_PATH, "r")
        for line in quadgramsFile:
            # content[0] is the quadgram
            # content[1] is the frequency of that quadgram
            # {key = quadgram : value = frequency}
            content = line.split()
            self.QUADGRAM_FREQUENCY_MAP[content[0]] = int(content[1])
        quadgramsFile.close()

        # calculates all the frequencies added together
        # (the totalQuadgrams of the frequencies of each quadgram)
        self.TOTAL_QUADGRAMS = self.totalQuadgrams(self.QUADGRAM_FREQUENCY_MAP.values()) 

        # calculates the fitness for a quadgram with a frequency of 0 (the worse possible fitness for a quadgram)
        self.ZERO_FREQUENCY_FITNESS = log10(self.ZERO/self.TOTAL_QUADGRAMS)

        # calculates and places the fitness of each quadgram in a dictionary data structure:
        quadgramList = self.QUADGRAM_FREQUENCY_MAP.keys()
        for qg in quadgramList:
            # {key = quadgram : value = fitness score}
            quadgramFitness = self.logProbability(self.QUADGRAM_FREQUENCY_MAP, self.TOTAL_QUADGRAMS, qg)
            self.QUADGRAM_FITNESS_MAP[qg] = quadgramFitness
        print(">>> Initialization of statistics completed. Program is now ready to decrypt ANY simple subsitution cipher.")
        print("----------------------------------------------------------------------------------------------------------")
