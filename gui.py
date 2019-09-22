# import main
import time
from random import randint
from tkinter import *
from tkinter import scrolledtext

class GUI():
    TEXT_FIELD_INPUT_FONT = ("TkFixedFont")
    ROOT_WINDOW_WIDTH = 595
    ROOT_WINDOW_HEIGHT = 400
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    def __init__(self, FS):
        self.FS = FS
        def generateRandomKeyBtn():
            textinput.delete("1.0", END)
            res = "HAVENT DONE YET"
            textinput.insert(INSERT, res)

        def encryptbtn():

            inputText = GUI.lowerAlphaOnly(textinput.get("1.0", END).strip("\n"))
            inputKey = keyinput.get()

            if(inputText == ''):
                resulttext.delete("1.0", END)
                resulttext.insert(INSERT, "NO TEXT SO NO RESULTS")
                return ''

            startTime = time.perf_counter()
            if(inputKey == ''):
                inputKey = GUI.generateRandomKey(GUI.ALPHABET)
            
            if(GUI.isValidKey(inputKey, GUI.ALPHABET)):
                encryptionresult = self.FS.encrypt(GUI.ALPHABET, inputKey, inputText)
            else:
                encryptionresult = f"INVALID KEY!!!!!!\n\nThe key should be a string of 26 unique letters if using the english alphabet.\n\nExample:\n[{GUI.generateRandomKey(GUI.ALPHABET)}]"

            # print(f"{FS.fitness("whatsinanamearosebyanyothernamewouldsmellassweet",)}")
            endTime = time.perf_counter()
            timeElapsed = endTime - startTime
            timevaluelbl.config(text=f'{timeElapsed:.10f}')

            keyusedoutput.delete(0, END)
            keyusedoutput.insert(0, inputKey)

            resulttext.delete("1.0", END)
            resulttext.insert(INSERT, encryptionresult)

            print()

        def decryptbtn():
            inputText = GUI.lowerAlphaOnly(textinput.get("1.0", END).strip("\n"))
            inputKey = keyinput.get()

           
            if(inputText == ''):
                resulttext.delete("1.0", END)
                resulttext.insert(INSERT, "NO TEXT SO NO RESULTS")
                return ''

            startTime = time.perf_counter()
            result = ''
            if(inputKey == ''):
                randomKeyArray = list()
                # for i in range(_PROCESSES):
                for i in range(100):
                    randomKeyArray.append(GUI.generateRandomKey(GUI.ALPHABET))

                results = self.FS.multiprocess_climb_hill(randomKeyArray, inputText)
                absoluteMax = self.FS.determineAbsoluteMax(results)
                # since the FS object cuts down the original ciphertext to the first 120 characters
                # we must decrypt an extra time using the orignal ciphertext:
                result = absoluteMax[0], absoluteMax[1], self.FS.decrypt(GUI.ALPHABET, absoluteMax[0], inputText)
            
            elif(GUI.isValidKey(inputKey, GUI.ALPHABET)):
                result = inputKey, inputText, self.FS.decrypt(GUI.ALPHABET, inputKey, inputText)
            else:
                result = inputKey, inputText, f"INVALID KEY!!!!!!\n\nThe key should be a string of 26 unique letters if using the english alphabet.\n\nExample:\n[{GUI.generateRandomKey(GUI.ALPHABET)}]"
            
            print(f"fitness: {result[1]}")
            endTime = time.perf_counter()
            timeElapsed = endTime - startTime
            timevaluelbl.config(text=f'{timeElapsed:.10f}')

            keyusedoutput.delete(0, END)
            keyusedoutput.insert(0, result[0])

            resulttext.delete("1.0", END)
            resulttext.insert(INSERT, result[2])

        root = Tk()
        root.title("Simple Substitution Encryption and Decryption")
        x_position = int(root.winfo_screenwidth()/2 - GUI.ROOT_WINDOW_WIDTH/2)
        y_position = int(root.winfo_screenheight()/2 - GUI.ROOT_WINDOW_HEIGHT/2)

        root.geometry(f'{GUI.ROOT_WINDOW_WIDTH}x{GUI.ROOT_WINDOW_HEIGHT}+{x_position}+{y_position}')
        root.grid_rowconfigure(0, minsize=15)

        keylbl = Label(root, text="KEY (leave blank to find/generate one):")
        keylbl.grid(column=0, row=1, padx=5, sticky="W")
        
        keyinput = Entry(root,width=30, font=GUI.TEXT_FIELD_INPUT_FONT)
        keyinput.grid(column=0, row=2, padx=5, sticky="W")

        keyusedlbl = Label(root, text="KEY USED:")
        keyusedlbl.grid(column=2, row=1, padx=5, sticky="W")
        
        keyusedoutput = Entry(root,width=30, font=GUI.TEXT_FIELD_INPUT_FONT, bg="lightgray")
        keyusedoutput.grid(column=2, row=2, padx=5, sticky="W")

        root.grid_rowconfigure(3, minsize=15)

        textlbl = Label(root, text="TEXT:")
        textlbl.grid(column=0, row=4, padx=5, sticky="W")

        textinput = scrolledtext.ScrolledText(root, width=30, height=15, font=GUI.TEXT_FIELD_INPUT_FONT)
        textinput.grid(column=0, row=5, padx=5, sticky="W")

        root.grid_columnconfigure(1, minsize=50)

        textlbl = Label(root, text="RESULT:")
        textlbl.grid(column=2, row=4, padx=5, sticky="W")

        resulttext = scrolledtext.ScrolledText(root, width=30, height=15, font=GUI.TEXT_FIELD_INPUT_FONT, bg="lightgray")
        resulttext.grid(column=2, row=5, padx=5, sticky="W")

        # button section:
        encrypt_decrypt_btn_frame = Frame(root)
        encrypt_decrypt_btn_frame.grid(column=0, row=6, sticky='we')
        encrypt_decrypt_btn_frame.grid_columnconfigure(0, weight=1)
        encrypt_decrypt_btn_frame.grid_columnconfigure(1, weight=1)
        encrypt_decrypt_btn_frame.grid_columnconfigure(2, weight=1)

        programinfobtn = Button(encrypt_decrypt_btn_frame, text="Program Information", command=generateRandomKeyBtn)
        programinfobtn.grid(column=0, row=0, padx=(5,0), pady=5, sticky="W")

        encryptbtn = Button(encrypt_decrypt_btn_frame, text="encrypt".capitalize(), command=encryptbtn)
        encryptbtn.grid(column=1, row=0, padx=(0,0), pady=5, sticky="W")

        decryptbtn = Button(encrypt_decrypt_btn_frame, text="decrypt".capitalize(), command=decryptbtn)
        decryptbtn.grid(column=2, row=0, padx=(0,12), pady=5, sticky="W")

        # time elapsed section:
        time_stat_frame = Frame(root)
        time_stat_frame.grid(column=2, row=6, sticky='we')
        time_stat_frame.grid_columnconfigure(0, weight=1)
        time_stat_frame.grid_columnconfigure(1, weight=1)

        timeelapsedlbl = Label(time_stat_frame, text="Time Elapsed:")
        timeelapsedlbl.grid(column=0, row=0, padx=(5,0), pady=5, sticky="W")

        timevaluelbl = Label(time_stat_frame, text="0.0000000000")
        timevaluelbl.grid(column=1, row=0, pady=5, sticky="E")

        secondstextlbl = Label(time_stat_frame, text="seconds")
        secondstextlbl.grid(column=2, row=0, padx= (0,20), pady=5, sticky="E")

        self.root = root

    @staticmethod
    def lowerAlphaOnly(text):
        alphaOnlyText = ''
        for i in range(len(text)):
            if text[i].isalpha():
                alphaOnlyText += text[i]
        return alphaOnlyText.lower()

    # generates a random key given an alphabet
    @staticmethod
    def generateRandomKey(alphabet):
        randomKey = ''
        listOfLettersLeft = alphabet
        for i in range(len(alphabet)):
            index = randint(0, len(listOfLettersLeft)-1) # generate a random index from 0 to the length of the list of letters left; minus 1 is to make the max range exclusive to prevent out of bound errors
            randomKey += listOfLettersLeft[index] # add letter onto random key string
            listOfLettersLeft = listOfLettersLeft.replace(listOfLettersLeft[index], '') # remove the letter to avoid it being picked again
        return randomKey

    @staticmethod
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