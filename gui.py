############################################################################################
# PLEASE READ THE 'README.txt' for instructions on how to RUN this program
############################################################################################
# Author: Sam Alhaqab
# This is the GUI applying the FitnessScorer and QuadgramStatistics modules I made.
# The GUI is made using the tkinter library.
# I've provided information on this program within the GUI.
# There is also the assignment ciphertexts and plaintexts for your testing convenience.
# WARNING: this program may claim that its "NOT RESPONDING" when you decrypt 
#          but that is not true, just be patient (less than 20 secs on even a bad laptop)
############################################################################################

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

# !!!!!!!!!!!!!!! Program Information variables:
INTRO_TEXT = "This program was developed using a [HILL CLIMBING ALGORITHM] that measures the fitness of a text using [QUADGRAM STATISTICS]. The methodology of this program can be divided two parts:"

SECTION_1_CONTENT_PART_1 = """1.  Get a lot of books.

2.  Record the frequency of each quadgram within each book.
        Note a quadgram is a string of four letters.
        Thank fully, I found a public data set on http://practicalcryptography.com/
        Which is advantageous since it'll have more data than I could gather myself.
        This file is called 'quadgrams-data.txt'

3.  Once we have the frequencies of the quadgrams we have to calculate the fitness of a text.
        The fitness of a text is defined as:"""

FORMULA_1 = "fitness('apieceoftext') = p('apieceoftext') = p('apie') x p('piec') x p('iece') x ... x p('ftex') x p('text'))"

SECTION_1_CONTENT_PART_2 = """        where p(quadgram) = frequency(quadgram) / total quadgrams
        example: p('apie') = frequency('apie') / total quadgrams

4.  However, due to numerical underflow caused by multiplying many small probabilities, 
    we will take the log of the probability.
        *Recall the log identity: log(a * b) = log(a) + log(b)
        Therefore fitness can also be defined as:"""

FORMULA_2 = "log(p('apieceoftext')) = log(p('apie')) + log(p('piec')) + log(p('iece')) + ... + log(p('ftex')) + log(p('text')))"

SECTION_2_CONTENT = """1.  Generate a random parent key.
    Calculate the fitness of the text decrypted by this key.

2.  Swap two letters in the parent key which will be called the altered key.
    Calculate the fitness of the text decrypted by this key.

3.  Compare the fitness measure:
    If the altered key has a higher fitness, then it becomes the new parent key.
    Other wise the parent key remains the key with the 'local maximum'.

4.  Repeat steps 2-3 until there is no change within the last 1000 iterations.
    When there is no change within the last 1000 iterations, the key has reached a 'local maximum'.
    This means no swap can make the key better than the current parent key.
    Therefore to increase the probability of getting a correct decryption, 
    we will have to run this entire algorithm a couple hundred times.
    This also means that there is no GUARANTEE that we get a 100% accurate decryption
    but it should be close."""

DEFAULT_DATA_FILE_PATH = "quadgrams-data.txt"
class GUI():
    TEXT_FIELD_INPUT_FONT = ("fixedsys 8")
    TEXT_LABEL_FONT = ("TkDefaultFont 8 bold")
    TEXT_LABEL_FONT_BIGGER = ("TkDefaultFont 10 bold")
    TEXT_CONTENT_FONT = ("TkDefaultFont 10")

    ROOT_WINDOW_WIDTH = 600
    ROOT_WINDOW_HEIGHT = 400
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, length_limit=120):
        self.qs = QS(DEFAULT_DATA_FILE_PATH)
        self.num_processes = 100
        self.cpu_count = (FS.cpu_count(), FS.cpu_count()/2)[FS.cpu_count() > 8]
        self.length_limit = length_limit

        def listenerInfo():
            # colors and dimensions for 'Texts' window:
            settingbgcolor = "gray"
            newheight      = GUI.ROOT_WINDOW_HEIGHT + 390
            newwidth       = GUI.ROOT_WINDOW_WIDTH + 265
            textboxwidth   = 100

            # creates the 'Texts' window:
            window = Toplevel(self.root)
            window.focus_set() # focuses on this window
            window.configure(background=settingbgcolor)
            window.title("Program Information")
            x_position = int(self.root.winfo_screenwidth()/2 - newwidth/2)
            y_position = int(self.root.winfo_screenheight()/2 - newheight/2)
            window.geometry(f'{newwidth}x{newheight}+{x_position}+{y_position}') 

            # creates spacing in the gui layout without setting paddings:
            window.grid_rowconfigure(0, minsize=20)
            window.grid_columnconfigure(0, minsize=30)

            # creates the label and text box widgets:
            introlabel    = Label(window, **labelbiggerStyleArgs, text="Introduction")
            section1label = Label(window, **labelbiggerStyleArgs, text="I. Quadgram Statistics as a fitness measure")
            section2label = Label(window, **labelbiggerStyleArgs, text="II. Hill Climbing Algorithm")
            introtextbox      = Text(window, **programinfotextboxStyleArgs, width=textboxwidth, height=2)
            section1p1textbox = Text(window, **programinfotextboxStyleArgs, width=textboxwidth, height=10)
            section1p2textbox = Text(window, **programinfotextboxStyleArgs, width=textboxwidth, height=7)
            formula1textbox   = Text(window, **formulatextboxStyleArgs,     width=textboxwidth, height=1)
            formula2textbox   = Text(window, **formulatextboxStyleArgs,     width=textboxwidth, height=1)
            section2textbox   = Text(window, **programinfotextboxStyleArgs, width=textboxwidth, height=17)

            # sets the content for the text boxes:
            introtextbox.insert(INSERT, INTRO_TEXT)
            section1p1textbox.insert(INSERT, SECTION_1_CONTENT_PART_1)
            section1p2textbox.insert(INSERT, SECTION_1_CONTENT_PART_2)
            formula1textbox.insert(INSERT, FORMULA_1)
            formula2textbox.insert(INSERT, FORMULA_2)
            section2textbox.insert(INSERT, SECTION_2_CONTENT)

            # disables all the text boxes so that the user cannot change the contents:
            introtextbox.configure(state=DISABLED)
            section1p1textbox.configure(state=DISABLED)
            section1p2textbox.configure(state=DISABLED)
            formula1textbox.configure(state=DISABLED)
            formula2textbox.configure(state=DISABLED)
            section2textbox.configure(state=DISABLED)

            # lays out the all widgets:
            introlabel.       grid(column=1, row=1, pady=5, sticky="we")
            introtextbox.     grid(column=1, row=2, pady=5, sticky="we")
            section1label.    grid(column=1, row=3, pady=5, sticky="we")
            section1p1textbox.grid(column=1, row=4, pady=5, sticky="we")
            formula1textbox.  grid(column=1, row=5, pady=5)
            section1p2textbox.grid(column=1, row=6, pady=5, sticky="we")
            formula2textbox.  grid(column=1, row=7, pady=5)
            section2label.    grid(column=1, row=8, pady=5, sticky="we")
            section2textbox.  grid(column=1, row=9, pady=5, sticky="we")
            
        def listenerTexts():
            def setInputText(event):
                # sets each text boxs' bg to be its default color:
                ct1.config(background=inputfieldcolor2)
                ct2.config(background=inputfieldcolor2)
                ct3.config(background=inputfieldcolor2)
                ct4.config(background=inputfieldcolor2)
                pt1.config(background=inputfieldcolor2)
                pt2.config(background=inputfieldcolor2)
                pt3.config(background=inputfieldcolor2)

                # changes the bg color of the text box that was clicked: 
                event.widget.config(background="white")

                # sets the contents of input text field on the main window:
                text = event.widget.get("1.0", END)
                textinput.delete("1.0", END)
                textinput.insert(INSERT, text)

            # colors and dimensions for 'Texts' window:
            settingbgcolor = "gray"
            newheight = GUI.ROOT_WINDOW_HEIGHT + 320
            newwidth = GUI.ROOT_WINDOW_WIDTH - 100
            textboxwidth = 54
            cursorvalue = "plus"

            # creates the 'Texts' window:
            window = Toplevel(self.root)
            window.focus_set() # focuses on this window
            window.configure(background=settingbgcolor)
            window.title("Sample ciphertexts and plaintexts (click to use a text):")
            x_position = int(self.root.winfo_screenwidth()/2 - newwidth/2)
            y_position = int(self.root.winfo_screenheight()/2 - newheight/2)
            # an offset of 250 was given for the x position so that the user can see their selection:
            window.geometry(f'{newwidth}x{newheight}+{x_position+250}+{y_position}') 

            # creates spacing in the gui layout without setting paddings:
            window.grid_rowconfigure(0, minsize=20)
            window.grid_columnconfigure(0, minsize=30)

            # creates label and text box widgets:
            ciphertextlabel = Label(window, text="Ciphertexts", **labelStyleArgs)
            plaintextlabel = Label(window, text="Plaintexts", **labelStyleArgs)
            ct1 = Text(window, **inputFieldDisabledStyleArgs, cursor=cursorvalue, wrap=WORD, width=textboxwidth, height=2)
            ct2 = Text(window, **inputFieldDisabledStyleArgs, cursor=cursorvalue, wrap=WORD, width=textboxwidth, height=3)
            ct3 = Text(window, **inputFieldDisabledStyleArgs, cursor=cursorvalue, wrap=WORD, width=textboxwidth, height=3)
            ct4 = Text(window, **inputFieldDisabledStyleArgs, cursor=cursorvalue, wrap=WORD, width=textboxwidth, height=8)
            pt1 = Text(window, **inputFieldDisabledStyleArgs, cursor=cursorvalue, wrap=WORD, width=textboxwidth, height=3)
            pt2 = Text(window, **inputFieldDisabledStyleArgs, cursor=cursorvalue, wrap=WORD, width=textboxwidth, height=6)
            pt3 = Text(window, **inputFieldDisabledStyleArgs, cursor=cursorvalue, wrap=WORD, width=textboxwidth, height=10)

            # sets the context for each text box:
            ct1.insert(INSERT, CIPHERTEXT_1)
            ct2.insert(INSERT, CIPHERTEXT_2)
            ct3.insert(INSERT, CIPHERTEXT_3)
            ct4.insert(INSERT, CIPHERTEXT_4)
            pt1.insert(INSERT, PHRASE_1)
            pt2.insert(INSERT, PHRASE_2)
            pt3.insert(INSERT, PHRASE_3)

            # binds a function to the left click for each text box:
            ct1.bind("<Button-1>", setInputText)
            ct2.bind("<Button-1>", setInputText)
            ct3.bind("<Button-1>", setInputText)
            ct4.bind("<Button-1>", setInputText)
            pt1.bind("<Button-1>", setInputText)
            pt2.bind("<Button-1>", setInputText)
            pt3.bind("<Button-1>", setInputText)

            # disables all the text boxes so that the user cannot change the contents:
            ct1.configure(state=DISABLED)
            ct2.configure(state=DISABLED)
            ct3.configure(state=DISABLED)
            ct4.configure(state=DISABLED)
            pt1.configure(state=DISABLED)
            pt2.configure(state=DISABLED)
            pt3.configure(state=DISABLED)

            # lays out all the label and text box widgets:
            ciphertextlabel.grid(column=1, row=1, pady=5, sticky="we")
            plaintextlabel.grid(column=1, row=6, pady=5, sticky="we")
            ct1.grid(column=1, row=2, pady=5)
            ct2.grid(column=1, row=3, pady=5)
            ct3.grid(column=1, row=4, pady=5)
            ct4.grid(column=1, row=5, pady=5)
            pt1.grid(column=1, row=7, pady=5)
            pt2.grid(column=1, row=8, pady=5)
            pt3.grid(column=1, row=9, pady=5)

        # this function runs when the 'Encrypt' button is clicked
        # it uses the FitnessScorer utility module I made to encrypt the ciphertext (variable is FS)
        # most of code in the this function is just input validation and gui control flow
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

            endTime = time.perf_counter()
            timeElapsed = endTime - startTime
            timevalueplaceholder.config(text=f'{timeElapsed:.10f}')

            keyusedoutput.delete(0, END)
            keyusedoutput.insert(0, inputKey)

            resultoutput.delete("1.0", END)
            resultoutput.insert(INSERT, encryptionresult)

            resultoutput.config(state="disabled")
            keyusedoutput.config(state="readonly")

        # this function runs when the 'Encrypt' button is clicked
        # it uses the FitnessScorer utility module I made to encrypt the ciphertext (variable is FS)
        # most of code in the this function is just input validation and gui control flow
        # note FS.multiprocess_climb_hill() is used here
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
        btnStyleArgs                = {'width':buttonwidth, 'height':buttonheight, 'bg':maincolor, 'relief':FLAT, 'font':GUI.TEXT_LABEL_FONT, 'fg':maintextcolor, 'borderwidth':0}
        labelStyleArgs              = {'font':GUI.TEXT_LABEL_FONT,        'bg':maincolor, 'fg':maintextcolor}
        labelbiggerStyleArgs        = {'font':GUI.TEXT_LABEL_FONT_BIGGER, 'bg':maincolor, 'fg':maintextcolor}
        programinfotextboxStyleArgs = {'font':GUI.TEXT_FIELD_INPUT_FONT,  'bg':inputfieldcolor1, 'relief':FLAT, 'wrap':WORD}
        formulatextboxStyleArgs     = {'font':GUI.TEXT_LABEL_FONT,        'bg':inputfieldcolor1, 'relief':FLAT}
        inputFieldActiveStyleArgs   = {'font':GUI.TEXT_FIELD_INPUT_FONT,  'bg':inputfieldcolor1, 'relief':FLAT}
        inputFieldDisabledStyleArgs = {'font':GUI.TEXT_FIELD_INPUT_FONT,  'bg':inputfieldcolor2, 'relief':FLAT}

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
        keyinputlabel     =           Label(root, **labelStyleArgs,              text="KEY (leave blank to find/generate one):")
        keyusedlabel      =           Label(root, **labelStyleArgs,              text="KEY USED:")   
        textinputlabel    =           Label(root, **labelStyleArgs,              text="TEXT:")
        resultoutputlabel =           Label(root, **labelStyleArgs,              text="RESULT:")
        keyinput          =           Entry(root, **inputFieldActiveStyleArgs,   width=30)
        keyusedoutput     =           Entry(root, **inputFieldDisabledStyleArgs, width=30, state="readonly", readonlybackground=inputfieldcolor2) 
        textinput         = st.ScrolledText(root, **inputFieldActiveStyleArgs,   width=28, height=15, wrap=WORD)
        resultoutput      = st.ScrolledText(root, **inputFieldDisabledStyleArgs, width=28, height=15, state="disabled", wrap=WORD)

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