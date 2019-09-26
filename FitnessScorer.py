
import time
from math import log10
from random import randint
from multiprocessing import Pool
from multiprocessing import cpu_count

def lowerAlphaOnly(text):
    alphaOnlyText = ''
    for i in range(len(text)):
        if text[i].isalpha():
            alphaOnlyText += text[i]
    return alphaOnlyText.lower()

# generates a random key given an alphabet
def generateRandomKey(alphabet):
    randomKey = ''
    listOfLettersLeft = alphabet
    for i in range(len(alphabet)):
        # generate a random index from 0 to the length of the list of letters left:
        # minus 1 is to make the max range exclusive to prevent out of bound errors
        index = randint(0, len(listOfLettersLeft)-1) 
        # add letter onto random key string:
        randomKey += listOfLettersLeft[index]
        # remove the letter to avoid it being picked again
        listOfLettersLeft = listOfLettersLeft.replace(listOfLettersLeft[index], '')
    return randomKey

def isValidKey(key, alphabet):
    if len(key) != len(alphabet):
        return False
    
    mapOfKey = dict()
    for letter in alphabet:
        mapOfKey[letter] = 0
    
    for letter in key:
        mapOfKey[letter] = mapOfKey[letter] + 1

    for value in mapOfKey.values():
        if value != 1:
            return False
    return True

# return a list of the quadgrams with a text
def getNgramInText(text, n):
    quadgramsInText = list()
    for i in range(len(text)-(n-1)):
        quadgramsInText.append(text[i:i+n]) # incrementally takes slices of the text until all quadgrams are accounted for
    return quadgramsInText


# sums up the log probabilities of all the quadgrams within a text
def fitness(fitnessMap, text, zeroFrequencyFitness, n):
    fitness = 0
    quadgrams = getNgramInText(text, n)
    for qg in quadgrams:
        fitness += fitnessMap.get(qg, zeroFrequencyFitness)
    return fitness

# swaps two letters in a key
def swapTwoLettersInKey(key):
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
def getWorseCaseFitness(text, zeroFrequencyFitness, n):
    # determines how many quadgrams are within the text
    numOfQuadgrams = len(text) - (n-1) 
    # since each quadgram is assumed to have a frequency of 0
    # the sum of all the log probabilities of is the product of the number of quadgrams and the zero frequency fitness
    # and making sure that product is negative(since the sum of a bunch of negative numbers is negative)
    return - abs(numOfQuadgrams * zeroFrequencyFitness)


def determineAbsoluteMax(results, zeroFrequencyFitness, n):
    absoluteMax = '', getWorseCaseFitness(results[0][2], zeroFrequencyFitness, n), ''
    for i in range(len(results)):
        if absoluteMax[1] < results[i][1]:
            absoluteMax = results[i]
    return absoluteMax

def encrypt(alphabet, key, plaintext):
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
def decrypt(alphabet, key, ciphertext):
    plaintext = ''
    for i in range(len(ciphertext)):
        plaintext += alphabet[key.find(ciphertext[i])]
    return plaintext


# climbs towards a local maximum given a parent key
def climbHill(fitnessMap, alphabet, n, zeroFrequencyFitness, text):

    # overview of algorithm:
    # 1. calcule fitness of a text decrypted by the a random key (parent/root) key
    # 2. alter the parent/root key (by swapping letters) and calculate the fitness of a text decrypted by this altered key
    # 3. compare them, the local max key is the higher of the two fitness values
    # 4. repeat above until the local max key has not been beat in 1000 iterations

    # calculate fitness of the parent key(which is renamed to local max key for brevity):
    localMaxKey = generateRandomKey(alphabet)
    lmkPlaintext = decrypt(alphabet, localMaxKey, text)
    lmkFitness = fitness(fitnessMap, lmkPlaintext, zeroFrequencyFitness, n)

    # calculate fitness of the alteredKey:
    alteredKey = swapTwoLettersInKey(localMaxKey)
    akPlaintext = decrypt(alphabet, alteredKey, text)
    akFitness = fitness(fitnessMap, akPlaintext, zeroFrequencyFitness, n)

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
        alteredKey = swapTwoLettersInKey(localMaxKey)
        akPlaintext = decrypt(alphabet, alteredKey, text)
        akFitness = fitness(fitnessMap, akPlaintext, zeroFrequencyFitness, n)

    return localMaxKey, lmkFitness, lmkPlaintext

def climbHillWrapper(args):
    return climbHill(*args)
    # return climbHill(args[0][0], args[1][0], args[2][0], args[3][0], args[4][0])
    

def multiprocess_climb_hill(fitnessMap, alphabet, n, zeroFrequencyFitness, text, num_threads=cpu_count(), num_processes=100, length_limit=140):

    print(f"{cpu_count()} {num_threads} {num_processes} {length_limit}")
    # print(f"CPU threads: {cpu_count()}")
    # cuts down the length of the ciphertext to 120
    # 120 characters is enough information to get an accurate answer
    if(len(text) > length_limit):
        text = text[:length_limit]

    tupleArgs = fitnessMap, alphabet, n, zeroFrequencyFitness, text
    args = [tupleArgs] * num_processes

    # creates multiple processes:
    p = Pool(num_threads)
    results = p.map(climbHillWrapper, args)
    # p.close()
    # p.join()

    return results
