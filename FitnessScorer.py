
import time
from math import log10
from random import randint
from multiprocessing import Pool
from multiprocessing import cpu_count

class FitnessScorer:
    def __init__(self, quadgramFitnessMap, zeroFrequencyFitness, alphabet, text=""):
        self.quadgramFitnessMap = quadgramFitnessMap
        self.zeroFrequencyFitness = zeroFrequencyFitness
        self.alphabet = alphabet
        self.originalText = text
        self.text = text
        if len(text) > 120:
            self.text = text[:120]
        
    # return a list of the quadgrams with a text
    def getQuadgramsInText(self, text):
        quadgramsInText = list()
        for i in range(len(text)-3):
            quadgramsInText.append(text[i:i+4]) # incrementally takes slices of the text until all quadgrams are accounted for
        return quadgramsInText

    # sums up the log probabilities of all the quadgrams within a text
    def fitness(self, fitnessMap, text):
        fitness = 0
        quadgrams = self.getQuadgramsInText(text)
        for qg in quadgrams:
            fitness += fitnessMap.get(qg, self.zeroFrequencyFitness)

        return fitness

    # swaps two letters in a key
    def swapTwoLettersInKey(self, key):
        i = randint(0, len(key) - 1) # the 1st index
        j = randint(0, len(key) - 1) # the 2nd index

        # ensures that the two indices generated are not equal
        while j == i:
            j = randint(0, len(key) - 1)

        # ensures that the 1st index is less than the 2nd index
        if i > j:
            t = j
            j = i
            i = t

        # swaps the two indices by cutting the original keys
        return ''.join((key[0:i], key[j], key[i+1:j], key[i], key[j+1:]))

    # the worse case fitness of a text is dependent all of its quadgrams having a frequency of 0 and how long the piece of text is
    def getWorseCaseFitness(self, text):
        numOfQuadgrams = len(text) - 3 # determines how many quadgrams are within the text
        return - abs(numOfQuadgrams * self.zeroFrequencyFitness) # since each quadgram is assumed to have a frequency of 0, the sum of all the log probabilities of is the product of the number of quadgrams and the zero frequency fitness and making sure that product is negative(since the sum of a bunch of negative numbers is negative)

    def determineAbsoluteMax(self, results):
        absoluteMax = '', self.getWorseCaseFitness(results[0][2]), ''
        for i in range(len(results)):
            if absoluteMax[1] < results[i][1]:
                absoluteMax = results[i]
        return absoluteMax

    def encrypt(self, alphabet, key, plaintext):
        ciphertext = ''
        # with each iteration of the for loop the ciphertext is updated with a encrypted letter
        # the encrypted letter is found by finding which index the plaintext letter is located in the 'alphabet' string
        # this index corresponds to the desired encrypted letter in the 'key' string
        for i in range(len(plaintext)):
            ciphertext += key[alphabet.find(plaintext[i])]
        return ciphertext

    # with each iteration of the for loop the plaintext is updated with a decrypted letter
    # the decrypted letter is found by finding which index the ciphertext letter is located in the 'key' string
    # this index corresponds to the "correct" letter in the 'alphabet' string
    def decrypt(self, alphabet, key, ciphertext):
        plaintext = ''
        for i in range(len(ciphertext)):
            plaintext += alphabet[key.find(ciphertext[i])]
        return plaintext

    # climbs towards a local maximum given a parent key
    def climbHill(self, parentKey):

        # overview of algorithm:
        # 1. calcule fitness of a text decrypted by the parent key
        # 2. alter the parent key (by swapping letters) and calculate the fitness of a text decrypted by this altered key
        # 3. compare them, the local max key is the higher of the two fitness values
        # 4. repeat above until the local max key has not been beat in 1000 iterations

        # calculate fitness of the parent key(which is renamed to local max key for brevity):
        localMaxKey = parentKey
        lmkPlaintext = self.decrypt(self.alphabet, localMaxKey, self.text)
        lmkFitness = self.fitness(self.quadgramFitnessMap, lmkPlaintext)

        # calculate fitness of the alteredKey:
        alteredKey = self.swapTwoLettersInKey(localMaxKey)
        akPlaintext = self.decrypt(self.alphabet, alteredKey, self.text)
        akFitness = self.fitness(self.quadgramFitnessMap, akPlaintext)

        iteration = 0
        while iteration < 1000:
            # comparison:
            if akFitness > lmkFitness:
                iteration = 0 # resets the iteration since a new local max has been found
                localMaxKey = alteredKey
                lmkPlaintext = akPlaintext
                lmkFitness = akFitness
            else: 
                iteration += 1 # a new local max has not been found so increment the iteration count
            
            # recalculate fitness of the alteredKey after swapping:
            alteredKey = self.swapTwoLettersInKey(localMaxKey)
            akPlaintext = self.decrypt(self.alphabet, alteredKey, self.text)
            akFitness = self.fitness(self.quadgramFitnessMap, akPlaintext)

        return localMaxKey, lmkFitness, lmkPlaintext

    def multiprocess_climb_hill(self, randomKeyArray, ciphertext):
        # cuts down the length of the ciphertext to 120
        # 120 characters is enough information to get an accurate answer
        if len(ciphertext) > 120:
            self.text = ciphertext[:120]
        else:
            self.text = ciphertext
        # creates multiple processes:
        print(f"CPU threads: {cpu_count()}")
        p = Pool(7)
        results = p.map(self.climbHill, randomKeyArray)
        p.close()
        p.join()

        # what happens NOWWWW????
        # just testing stuff
        x = "whatsinanamearosebyanyothernamewouldsmellassweet"
        y = "whatsinanamearosebyanyothernamewouldsmellassweetwhatsinanamearosebyanyothernamewouldsmellassweet"
        var1 = self.fitness(self.quadgramFitnessMap, x)
        var2 = self.fitness(self.quadgramFitnessMap, y)

        print(f"fitness({len(x)}): {var1}")
        print(f"fitness({len(y)}): {var2}")

        z1 = "tiontiontiontiontiontiontiontiontiontiontiontion"
        z2 = "tiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontiontion"

        print(len(z1))
        z1 = self.fitness(self.quadgramFitnessMap, z1)
        z2 = self.fitness(self.quadgramFitnessMap, z2)

        print(f"fitness({1}): {z1}")
        print(f"fitness({2}): {z2}")

        return results






