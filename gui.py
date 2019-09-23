# import main
import time
from random import randint
from tkinter import *
from tkinter import scrolledtext
from QuadgramStatistics import QuadgramStatistics as QS
import FitnessScorer as FS

DEFAULT_DATA_FILE_PATH = "quadgrams-data.txt"
class GUI():
    TEXT_FIELD_INPUT_FONT = ("TkFixedFont")
    ROOT_WINDOW_WIDTH = 595
    ROOT_WINDOW_HEIGHT = 400
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    def __init__(self):
        self.qs = QS(DEFAULT_DATA_FILE_PATH)
        self.num_processes = 100

        def btn_init_data():
            print("nothing")

        def generateRandomKeyBtn():
            textinput.delete("1.0", END)
            res = "HAVENT DONE YET"
            textinput.insert(INSERT, res)

        def encryptbtn():
            
            inputText = FS.lowerAlphaOnly(textinput.get("1.0", END).strip("\n"))
            inputKey = keyinput.get()

            if(inputText == ''):
                resulttext.delete("1.0", END)
                resulttext.insert(INSERT, "NO TEXT SO NO RESULTS")
                return ''

            startTime = time.perf_counter()
            if(inputKey == ''):
                inputKey = FS.generateRandomKey(GUI.ALPHABET)
            
            if(FS.isValidKey(inputKey, GUI.ALPHABET)):
                encryptionresult = FS.encrypt(GUI.ALPHABET, inputKey, inputText)
            else:
                encryptionresult = f"INVALID KEY!!!!!!\n\nThe key should be a string of 26 unique letters if using the english alphabet.\n\nExample:\n[{FS.generateRandomKey(GUI.ALPHABET)}]"

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
            inputText = FS.lowerAlphaOnly(textinput.get("1.0", END).strip("\n"))
            inputKey = keyinput.get()

            if(inputText == ''):
                resulttext.delete("1.0", END)
                resulttext.insert(INSERT, "NO TEXT SO NO RESULTS")
                return ''

            startTime = time.perf_counter()
            result = ''
            if(inputKey == ''):
                results = FS.multiprocess_climb_hill(self.qs.QUADGRAM_FITNESS_MAP, GUI.ALPHABET, 4, self.qs.ZERO_FREQUENCY_FITNESS, inputText, self.num_processes)
                absoluteMax = FS.determineAbsoluteMax(results, self.qs.ZERO_FREQUENCY_FITNESS, 4)
                # since the FS object cuts down the original ciphertext to the first 120 characters
                # we must decrypt an extra time using the orignal ciphertext:
                result = absoluteMax[0], absoluteMax[1], FS.decrypt(GUI.ALPHABET, absoluteMax[0], inputText)
            
            elif(FS.isValidKey(inputKey, GUI.ALPHABET)):
                result = inputKey, inputText, FS.decrypt(GUI.ALPHABET, inputKey, inputText)
            else:
                result = inputKey, inputText, f"INVALID KEY!!!!!!\n\nThe key should be a string of 26 unique letters if using the english alphabet.\n\nExample:\n[{FS.generateRandomKey(GUI.ALPHABET)}]"
            
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

if __name__ == "__main__":
    myGui = GUI()
    myGui.qs.printStatistics()
    myGui.root.mainloop()