# import main
import time
from os import path
from random import randint
from tkinter import *
from tkinter import scrolledtext as st
from tkinter import filedialog
from QuadgramStatistics import QuadgramStatistics as QS
import FitnessScorer as FS

# ASSIGNMENT CIPHERTEXTS:
CIPHERTEXT_1 = "fqjcb rwjwj vnjax bnkhj whxcq nawjv nfxdu mbvnu ujbbf nnc"
CIPHERTEXT_2 = "oczmz vmzor jocdi bnojv dhvod igdaz admno ojbzo rcvot jprvi oviyv aozmo cvooj ziejt dojig toczr dnzno jahvi fdiyv xcdzq zocznzxjiy"
CIPHERTEXT_3 = "ejitp spawa qleji taiul rtwll rflrl laoat wsqqj atgac kthls iraoa twlpl qjatw jufrh lhuts qataq itats aittk stqfj cae"
CIPHERTEXT_4 = "iyhqz ewqin azqej shayz niqbe aheum hnmnj jaqii yuexq ayqkn jbeuq iihed yzhni ifnun sayiz yudhe sqshu qesqa iluym qkque aqaqm oejjs hqzyu jdzqa diesh niznj jayzy uiqhq vayzq shsnj jejjz nshna hnmyt isnae sqfun dqzew qiead zevqi zhnjq shqze udqai jrmtq uishq ifnun siiqa suoij qqfni syyle iszhn bhmei squih nimnx hsead shqmr udquq uaqeu iisqe jshnj oihyy snaxs hqihe lsilu ymhni tyz"

# ASSIGNMENT PLAINTEXT TO BE ENCRYPTED:
PHRASE_1 = "He who fights with monsters should look to it that he himself does not become a monster. And if you gaze long into an abyss, the abyss also gazes into you."

PHRASE_2 = "There is a theory which states that if ever anybody discovers exactly what the Universe is for and why it is here, it will instantly disappear and be replaced by something even more bizarre and inexplicable. There is another theory which states that this has already happened."

PHRASE_3 = "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people's hats off - then, I account it high time to get to sea as soon as I can."

DEFAULT_DATA_FILE_PATH = "quadgrams-data.txt"
class GUI():
    TEXT_FIELD_INPUT_FONT = ("fixedsys 8")
    TEXT_LABEL_FONT = ("TkDefaultFont 8 bold")
    ROOT_WINDOW_WIDTH = 600
    ROOT_WINDOW_HEIGHT = 400
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, length_limit=120):
        self.qs = QS(DEFAULT_DATA_FILE_PATH)
        self.num_processes = 100
        self.cpu_count = (FS.cpu_count(), FS.cpu_count()/2)[FS.cpu_count() > 8]
        self.length_limit = length_limit

        def listenerInfo():
            print('x')

        def listenerTexts():
            settingbgcolor = "gray"
            newheight = GUI.ROOT_WINDOW_HEIGHT - 100
            newwidth = GUI.ROOT_WINDOW_WIDTH - 100

            window = Toplevel(self.root)
            window.focus_set()
            window.configure(background=settingbgcolor)
            window.title("Settings")
            x_position = int(self.root.winfo_screenwidth()/2 - newwidth/2)
            y_position = int(self.root.winfo_screenheight()/2 - newheight/2)
            window.geometry(f'{newwidth}x{newheight}+{x_position}+{y_position}')

            window.grid_rowconfigure(0, minsize=30)
            window.grid_columnconfigure(0, minsize=30)


            textinput.delete("1.0", END)
            res = "HAVENT DONE YET"
            textinput.insert(INSERT, res)

        def listenerEncrypt():
            resultoutput.config(state="normal")
            keyusedoutput.config(state="normal")

            inputText = FS.lowerAlphaOnly(textinput.get("1.0", END).strip("\n"))
            inputKey = keyinput.get()

            if(inputText == ''):
                resultoutput.delete("1.0", END)
                resultoutput.insert(INSERT, "NO TEXT SO NO RESULTS")
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
            timevalueplaceholder.config(text=f'{timeElapsed:.10f}')

            keyusedoutput.delete(0, END)
            keyusedoutput.insert(0, inputKey)

            resultoutput.delete("1.0", END)
            resultoutput.insert(INSERT, encryptionresult)

            resultoutput.config(state="disabled")
            keyusedoutput.config(state="readonly")

        def listenerDecrypt():
            resultoutput.config(state="normal")
            keyusedoutput.config(state="normal")

            inputText = FS.lowerAlphaOnly(textinput.get("1.0", END).strip("\n"))
            inputKey = keyinput.get()

            if(inputText == ''):
                resultoutput.delete("1.0", END)
                resultoutput.insert(INSERT, "NO TEXT SO NO RESULTS")
                return ''

            startTime = time.perf_counter()
            result = ''
            if(inputKey == ''):
                
                results = FS.multiprocess_climb_hill(self.qs.QUADGRAM_FITNESS_MAP, GUI.ALPHABET, 4, self.qs.ZERO_FREQUENCY_FITNESS, inputText, num_threads=self.cpu_count)
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
            timevalueplaceholder.config(text=f'{timeElapsed:.10f}')

            keyusedoutput.delete(0, END)
            keyusedoutput.insert(0, result[0])

            resultoutput.delete("1.0", END)
            resultoutput.insert(INSERT, result[2])

            resultoutput.config(state="disabled")
            keyusedoutput.config(state="readonly")
        
        # color and dimension values:
        bgcolor          = "#515358"
        maincolor        = "#09BA7C"
        maintextcolor    = "white"
        inputfieldcolor1 = "white"
        inputfieldcolor2 = "#C6C6C6"
        buttonwidth      = 7
        buttonheight     = 1
        btngapwidth      = 4

        # style arguments for various widgets:
        btnStyleArgs     = {'width':buttonwidth, 'height':buttonheight, 'bg':maincolor, 'relief':FLAT, 'font':GUI.TEXT_LABEL_FONT, 'fg':maintextcolor, 'borderwidth':0}
        labelStyleArgs   = {'font':GUI.TEXT_LABEL_FONT, 'bg':maincolor, 'fg':maintextcolor}
        inputFieldActiveStyleArgs = {'font':GUI.TEXT_FIELD_INPUT_FONT, 'bg':inputfieldcolor1, 'relief':FLAT}
        inputFriendDisabledStyleArgs = {'font':GUI.TEXT_FIELD_INPUT_FONT, 'bg':inputfieldcolor2, 'relief':FLAT}

        # creates and sets the root window:
        root = Tk()
        root.configure(background=bgcolor)
        root.title("Simple Substitution Encryption and Decryption")

        # determines the dimensions and initial position of the window (center):
        x_position = int(root.winfo_screenwidth()/2 - GUI.ROOT_WINDOW_WIDTH/2)
        y_position = int(root.winfo_screenheight()/2 - GUI.ROOT_WINDOW_HEIGHT/2)
        root.geometry(f'{GUI.ROOT_WINDOW_WIDTH}x{GUI.ROOT_WINDOW_HEIGHT}+{x_position}+{y_position}')
        
        # creates the two bottom frames:
        button_frame     = Frame(root, bg=bgcolor)
        time_stat_frame  = Frame(root, bg=maincolor)

        # creates the labels and text box widgets:
        keyinputlabel     =           Label(root, **labelStyleArgs,               text="KEY (leave blank to find/generate one):")
        keyusedlabel      =           Label(root, **labelStyleArgs,               text="KEY USED:")   
        textinputlabel    =           Label(root, **labelStyleArgs,               text="TEXT:")
        resultoutputlabel =           Label(root, **labelStyleArgs,               text="RESULT:")
        keyinput          =           Entry(root, **inputFieldActiveStyleArgs,    width=30)
        keyusedoutput     =           Entry(root, **inputFriendDisabledStyleArgs, width=30, state="readonly", readonlybackground=inputfieldcolor2) 
        textinput         = st.ScrolledText(root, **inputFieldActiveStyleArgs,    width=28, height=15)
        resultoutput      = st.ScrolledText(root, **inputFriendDisabledStyleArgs, width=28, height=15, state="disabled")

        # creates the buttons:
        textsbtn    = Button(button_frame, text="Info",    command=listenerInfo,     **btnStyleArgs)
        examplesbtn = Button(button_frame, text="Texts",   command=listenerTexts, **btnStyleArgs)
        encryptbtn  = Button(button_frame, text="Encrypt", command=listenerEncrypt,  **btnStyleArgs)
        decryptbtn  = Button(button_frame, text="Decrypt", command=listenerDecrypt,  **btnStyleArgs)

        # creates the time elapsed widgets:
        timeelapsedlabel     = Label(time_stat_frame, text="Time Elapsed:", **labelStyleArgs)
        timevalueplaceholder = Label(time_stat_frame, text="0.0000000000",  **labelStyleArgs)
        timeunitlabel        = Label(time_stat_frame, text="seconds",       **labelStyleArgs)
        
        # creates spacing in the gui layout without setting paddings:
        root.grid_columnconfigure(0, minsize=30)
        root.grid_rowconfigure(0, minsize=30)
        root.grid_columnconfigure(2, minsize=50)
        root.grid_rowconfigure(3, minsize=15)

        # layouts the labels and text box widgets:
        keyinputlabel.       grid(column=1, row=1, sticky="we")
        keyinput.            grid(column=1, row=2, sticky="we")
        keyusedlabel.        grid(column=3, row=1, sticky="we")
        keyusedoutput.       grid(column=3, row=2, sticky="we")
        textinputlabel.      grid(column=1, row=4, sticky="we")
        textinput.           grid(column=1, row=5, sticky="we")
        resultoutputlabel.   grid(column=3, row=4, sticky="we")
        resultoutput.        grid(column=3, row=5, sticky="we")

        # layouts the button frame and the buttons that go into the frame:
        button_frame.        grid(column=1, row=6, sticky='we')
        textsbtn.            grid(column=0, row=0, pady=5, padx=(1, btngapwidth))
        examplesbtn.         grid(column=1, row=0, pady=5, padx=btngapwidth)
        encryptbtn.          grid(column=2, row=0, pady=5, padx=btngapwidth)
        decryptbtn.          grid(column=3, row=0, pady=5, padx=(btngapwidth, 0))

        # layouts the time frame and the time-related widgets that belong in the frame:
        time_stat_frame.     grid(column=3, row=6, sticky='we')
        timeelapsedlabel.    grid(column=0, row=0, pady=5, padx=(5,0))
        timevalueplaceholder.grid(column=1, row=0, pady=5, padx=(22,0))
        timeunitlabel.       grid(column=2, row=0, pady=5, padx=(0,5))

        # assigns all the the work above to a variable:
        self.root = root

if __name__ == "__main__":
    myGui = GUI()
    myGui.qs.printStatistics()
    myGui.root.mainloop()