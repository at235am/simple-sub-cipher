import time
from random import randint
from FitnessScorer import FitnessScorer
from QuadgramStatistics import QuadgramStatistics


# '_PROCESSES' is the number of _PROCESSES we are trying to run in parallel
# the MORE processes mean the time taken to find an answer is longer which also means a more accurate answer
# the LESS processes mean the time taken to find an answer is shorter but also less accurate
_PROCESSES = 150 

# the alphabet that the decryption and encryption will be based on
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# ASSIGNMENT CIPHERTEXTS:
CIPHERTEXT1 = "fqjcb rwjwj vnjax bnkhj whxcq nawjv nfxdu mbvnu ujbbf nnc"
CIPHERTEXT2 = "oczmz vmzor jocdi bnojv dhvod igdaz admno ojbzo rcvot jprvi oviyv aozmo cvooj ziejt dojig toczr dnzno jahvi fdiyv xcdzq zocznzxjiy"
CIPHERTEXT3 = "ejitp spawa qleji taiul rtwll rflrl laoat wsqqj atgac kthls iraoa twlpl qjatw jufrh lhuts qataq itats aittk stqfj cae"
CIPHERTEXT4 = "iyhqz ewqin azqej shayz niqbe aheum hnmnj jaqii yuexq ayqkn jbeuq iihed yzhni ifnun sayiz yudhe sqshu qesqa iluym qkque aqaqm oejjs hqzyu jdzqa diesh niznj jayzy uiqhq vayzq shsnj jejjz nshna hnmyt isnae sqfun dqzew qiead zevqi zhnjq shqze udqai jrmtq uishq ifnun siiqa suoij qqfni syyle iszhn bhmei squih nimnx hsead shqmr udquq uaqeu iisqe jshnj oihyy snaxs hqihe lsilu ymhni tyz"

# ASSIGNMENT PLAINTEXT TO BE ENCRYPTED:
PHRASE_1 = "He who fights with monsters should look to it that he himself does not become a monster. And if you gaze long into an abyss, the abyss also gazes into you."

PHRASE_2 = "There is a theory which states that if ever anybody discovers exactly what the Universe is for and why it is here, it will instantly disappear and be replaced by something even more bizarre and inexplicable. There is another theory which states that this has already happened."

PHRASE_3 = "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people's hats off - then, I account it high time to get to sea as soon as I can."

# ensures that only lower letters are accepted
# ignores all other characters like capitals, symbols, numbers, etc
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
        index = randint(0, len(listOfLettersLeft)-1) # generate a random index from 0 to the length of the list of letters left; minus 1 is to make the max range exclusive to prevent out of bound errors
        randomKey += listOfLettersLeft[index] # add letter onto random key string
        listOfLettersLeft = listOfLettersLeft.replace(listOfLettersLeft[index], '') # remove the letter to avoid it being picked again
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


def part1decryption(FS):
    done = False
    while not done:
        print("----------------------------------------------------------------------------------------------------------")
        print(f"Ciphertext 1: \n{CIPHERTEXT1}\n")
        print(f"Ciphertext 2: \n{CIPHERTEXT2}\n")
        print(f"Ciphertext 3: \n{CIPHERTEXT3}\n")
        print(f"Ciphertext 4: \n{CIPHERTEXT4}\n")
        print("----------------------------------------------------------------------------------------------------------")
        ciphertext = lowerAlphaOnly(input(">>> Above are the ciphertexts from the lab assignment for your convenience. \n>>> Please type or copy-paste a TEXT to decrypt\n    {be wary of newlines from copy-paste}:\n>>> "))
        inputKey = lowerAlphaOnly(input(">>> Please type or copy-paste a KEY to use for decryption\n    {press [ENTER] if you have no key, the program will attempt to find the correct key}:\n>>> "))

        print(">>> Decryption has started. Please wait..")

        if(inputKey == ''): # if the user does not provide a key the program will attempt to find one
            startTime = time.perf_counter()

            randomKeyArray = list()
            for i in range(_PROCESSES):
                randomKeyArray.append(generateRandomKey(ALPHABET))

            results = FS.multiprocess_climb_hill(randomKeyArray, ciphertext)
            absoluteMax = FS.determineAbsoluteMax(results)
            # since the FS object cuts down the original ciphertext to the first 120 characters
            # we must decrypt an extra time using the orignal ciphertext:
            absoluteMax = absoluteMax[0], absoluteMax[1], FS.decrypt(ALPHABET, absoluteMax[0], ciphertext)

            endTime = time.perf_counter()
            timeElapsed = endTime - startTime

            print("----------------------------------------------------------------------------------------------------------")
            print(f"<<< R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S")
            print("----------------------------------------------------------------------------------------------------------")
            print(f"<<<                 Time Elapsed: {timeElapsed} seconds")
            print(f"<<<                      Fitness: [{absoluteMax[1]}]")
            print(f"<<< Generated 'Optimal' Key Used: [{absoluteMax[0]}]")
            print(f"<<<         Ciphertext Decrypted:\n+++ {absoluteMax[2]}")
            print("<<< If the phrase above looks like gibberish just decrypt the phrase once again. See main menu for explanation.")
            print("----------------------------------------------------------------------------------------------------------")
        elif(isValidKey(inputKey, ALPHABET)):
            plaintext = FS.decrypt(ALPHABET, inputKey, ciphertext)
            print("----------------------------------------------------------------------------------------------------------")
            print(f"<<< R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S")
            print("----------------------------------------------------------------------------------------------------------")
            print(f"<<< Ciphertext Decrypted:\n+++ {plaintext}")
            print("----------------------------------------------------------------------------------------------------------")
        else:
            print( "!!! INVALID KEY")
            print(f'    The key should be a string of 26 unique letters if using the english alphabet.')
            print(f'    example: {generateRandomKey(ALPHABET)}')

        choice = input(">>> Would you like to continue with another decryption? [y/n]: ").lower()
        if choice == 'y': 
            done = False
        elif choice == 'n':
            done = True

def part2encryption(FS):
    # encryption of the 3 phrases:
    done = False
    while not done:
        print("-------------------------------------------------------------------------------------------------------------")
        print("PHRASES TO BE ENCRYPTED:")
        print("-------------------------------------------------------------------------------------------------------------")
        print(f"Phrase 1: \n{ PHRASE_1}\n")
        print(f"Phrase 2: \n{ PHRASE_2}\n")
        print(f"Phrase 3: \n{ PHRASE_3}\n")
        print("-------------------------------------------------------------------------------------------------------------")
        inputPhrase = lowerAlphaOnly(input(">>> Above are the plaintexts from the lab assignment for your convenience. \n>>> Please type or copy-paste a TEXT to decrypt:\n>>> "))
        print(f'>>> Please type or copy-paste the KEY to be used for this encryption:')
        print(f'    The key should be a string of 26 unique letters if using the english alphabet.')
        print(f'    example: {generateRandomKey(ALPHABET)}')
        print(f'    (press [ENTER] if you have no key, the program will generate a random key):')
        inputKey = input('>>> ')

        if(inputKey == ''): # if the user does not provide a key the program will generate a randomOne
            inputKey = generateRandomKey(ALPHABET)

        if(isValidKey(inputKey, ALPHABET)):
            ciphertext = FS.encrypt(ALPHABET, inputKey, inputPhrase)
            print("----------------------------------------------------------------------------------------------------------")
            print(f"<<< R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S   R E S U L T S")
            print(f"<<< Encryption Key: [{inputKey}]")
            print(f"<<< Plaintext Encrypted:\n+++ {ciphertext}")
            print("----------------------------------------------------------------------------------------------------------")
        else:
            print( "!!! INVALID KEY")
            print(f'    The key should be a string of 26 unique letters if using the english alphabet.')
            print(f'    example: {generateRandomKey(ALPHABET)}')

        choice = input(">>> Would you like to continue with another encryption? [y/n]: ")
        if choice == 'y': 
            done = False
        elif choice == 'n':
            done = True

def programInformation():
    print(">>> This program was developed using a [HILL CLIMBING ALGORITHM]")
    print(">>> that measures the fitness of a text using [QUADGRAM STATISTICS].")
    print(">>> The methodology of this program can be divided two parts: ")
    print()
    print(">>> [I. Quadgram Statistics as a fitness measure]".upper())
    print(">>> >>> Get a lot of books.")
    print(">>> >>> Record the frequency of each quadgram within each book.")
    print("        Note a quadgram is a string of four letters.")
    print("        Thank fully, I found a public data set on http://practicalcryptography.com/")
    print("        Which is advantageous since it'll have more data than I could gather myself.")
    print("        This file is called 'quadgrams-data.txt'")
    print(">>> >>> Once we have the frequencies of the quadgrams we have to calculate the fitness of a text.")
    print(">>> >>> The fitness of a text is defined as:")
    print("        fitness('apieceoftext') = p('apieceoftext') = p('apie') x p('piec') x p('iece') x ... x p('ftex') x p('text')")
    print("        where p(quadgram) = frequency(quadgram) / total quadgrams")
    print("        example: p('apie') = frequency('apie') / total quadgrams")
    print(">>> >>> However, due to numerical underflow caused by multiplying many small probabilities,")
    print("        we will take the log of the probability.")
    print("        Recall the log identity: log(a * b) = log(a) + log(b)")
    print(">>> >>> Therefore fitness can also be defined as: ")
    print("        log(p('apieceoftext')) = log(p('apie')) + log(p('piec')) + log(p('iece')) + ... + log(p('ftex')) + log(p('text'))")
    print()    
    print(">>> [II. Hill Climbing Algorithm]".upper())
    print(">>> >>> 1. Generate a random parent key.")
    print("        Calculate the fitness of the text decrypted by this key.")
    print(">>> >>> 2. Swap two letters in the parent key which will be called the altered key.")
    print("        Calculate the fitness of the text decrypted by this key")
    print(">>> >>> 3. Compare the fitness measure: ")
    print("        If the altered key has a higher fitness, then it becomes the new parent key.")
    print("        Other wise the parent key remains the key with the 'local maximum'.")
    print(">>> >>> 4. Repeat steps 2-3 until there is no change within the last 1000 iterations.")
    print(">>> >>> When there is no change within the last 1000 iterations, the key has reached a 'local maximum'.")
    print(">>> >>> This means no swap can make the key better than the current parent key.")
    print(">>> >>> Therefore to increase the probability of getting a correct decryption,")
    print("        we will have to run this entire algorithm a couple hundred times.")
    print(">>> >>> This also means that there is no GUARANTEE that we get a 100% accurate decryption")
    print("        but it should be close.")

    input("\n>>> Press [ENTER] to go back to the MAIN MENU: ")

def menu(FS):
    done = False
    while not done:
        print("----------------------------------------------------------------------------------------------------------")
        print("   MENU")
        print("----------------------------------------------------------------------------------------------------------")
        print("0. Program Information (weaknesses)")
        print("1. Decrypt (Lab Part 1)")
        print("2. Encrypt (Lab Part 2)")
        print("3. Exit")
        print("----------------------------------------------------------------------------------------------------------")

        choice = input(">>> Enter number corresponding to your choice[0-3]: ")
        print("----------------------------------------------------------------------------------------------------------")

        if   choice == '0':
            programInformation()
        elif choice == '1':
            part1decryption(FS) # the decryption part of the lab
        elif choice == '2':
            part2encryption(FS) # the encryption part of the lab
        elif choice == '3':
            done = True
            print(">>> Bye ~")
        else:
            print(">>> Invalid input, try again.")
    print("-------------------------------------------------------------------------------------------------------------")

if __name__ == '__main__':

    # initializing the statistics needed to calculate fitness of texts
    QS = QuadgramStatistics("quadgrams-data.txt")
    QS.printStatistics()
    FS = FitnessScorer(QS.QUADGRAM_FITNESS_MAP, QS.ZERO_FREQUENCY_FITNESS, ALPHABET)

    menu(FS)
    

    