from gui import GUI
from FitnessScorer import FitnessScorer
from QuadgramStatistics import QuadgramStatistics

# '_PROCESSES' is the number of _PROCESSES we are trying to run in parallel
# the MORE processes mean the time taken to find an answer is longer which also means a more accurate answer
# the LESS processes mean the time taken to find an answer is shorter but also less accurate
_PROCESSES = 150

# the alphabet that the decryption and encryption will be based on
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

if __name__ == "__main__":
    QS = QuadgramStatistics("quadgrams-data.txt")
    QS.printStatistics()
    FS = FitnessScorer(QS.QUADGRAM_FITNESS_MAP, QS.ZERO_FREQUENCY_FITNESS, ALPHABET)

    myGui = GUI(FS)
    myGui.root.mainloop()