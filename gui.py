# import main
import time
from random import randint
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from os import path
from QuadgramStatistics import QuadgramStatistics as QS
import FitnessScorer as FS

DEFAULT_DATA_FILE_PATH = "quadgrams-data.txt"
class GUI():
    TEXT_FIELD_INPUT_FONT = ("fixedsys 8")
    TEXT_LABEL_FONT = ("TkDefaultFont 8 bold")

    ROOT_WINDOW_WIDTH = 600
    ROOT_WINDOW_HEIGHT = 400
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"
    def __init__(self):
        self.qs = QS(DEFAULT_DATA_FILE_PATH)
        self.num_processes = 100

        # self.datafilepathinput = ''
        def listenerfileexplorer():
            currentDirectory =path.dirname(path.abspath(__file__))
            file = filedialog.askopenfilename(initialdir=currentDirectory)
            
            self.datafilepathinput.delete(0, END)
            self.datafilepathinput.insert(0, file)
            self.window.focus_set()

        def listenerSettings():
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

            inputframe = Frame(window, bg=settingbgcolor, width=200, height=300)
            fileframe = Frame(inputframe, bg=settingbgcolor, width=50)

            settingslabelwidth = 13
            cpucountlabel = Label(inputframe, text= "CPU Cores: ", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, anchor="e", width = settingslabelwidth)
            numofprocesseslabel = Label(inputframe, text="# of processes: ", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, anchor="e", width = settingslabelwidth)
            lenghtlimitlabel = Label(inputframe, text="Length Limit: ", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, anchor="e", width = settingslabelwidth)
            alphabetlabel = Label(inputframe, text="Alphabet: ", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, anchor="e", width = settingslabelwidth)
            datafilepathlabel = Label(inputframe, text="Data File Path: ", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, anchor="e", width = settingslabelwidth)

            cpucountinput = Entry(inputframe,width=4, font=GUI.TEXT_FIELD_INPUT_FONT, relief=FLAT, bg=inputfieldcolor1)
            numofprocessesinput = Entry(inputframe,width=4, font=GUI.TEXT_FIELD_INPUT_FONT, relief=FLAT, bg=inputfieldcolor1)
            lengthlimitinput = Entry(inputframe,width=4, font=GUI.TEXT_FIELD_INPUT_FONT, relief=FLAT, bg=inputfieldcolor1)
            alphabetinput = Entry(inputframe,width=30, font=GUI.TEXT_FIELD_INPUT_FONT, relief=FLAT, bg=inputfieldcolor1)
            self.datafilepathinput = Entry(fileframe,width=23, font=GUI.TEXT_FIELD_INPUT_FONT, relief=FLAT, bg=inputfieldcolor1)
            browseforfilebtn = Button(fileframe, text="Browse", command=listenerfileexplorer, width=buttonwidth, height=buttonheight, bg=buttoncolor, relief=FLAT, font=GUI.TEXT_LABEL_FONT, fg=labelfgcolor, overrelief=FLAT, borderwidth=0)
            

            inputframe.grid(column=1, row=1, pady=(5,5))
            fileframe.grid(column=1, row=4, pady=(0,5), sticky="we")
            cpucountlabel.grid(column=0,row=0, pady=(0,5), padx=(0,2))
            cpucountinput.grid(column=1,row=0, pady=(0,5), sticky="w")
            numofprocesseslabel.grid(column=0,row=1, pady=(0,5), padx=(0,2))
            numofprocessesinput.grid(column=1,row=1, pady=(0,5), sticky="w")
            lenghtlimitlabel.grid(column=0,row=2, pady=(0,5), padx=(0,2))
            lengthlimitinput.grid(column=1,row=2, pady=(0,5), sticky="w")
            alphabetlabel.grid(column=0,row=3, pady=(0,5), padx=(0,2))
            alphabetinput.grid(column=1,row=3, pady=(0,5))
            datafilepathlabel.grid(column=0,row=4, pady=(0,5), padx=(0,2))
            self.datafilepathinput.grid(column=1,row=0, pady=(0,0), sticky="w")
            browseforfilebtn.grid(column=2,row=0, pady=(0,0), padx=(2,0), sticky="e")

            # test = Label(window, text="KEY (leave blank to find/generate one):", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, width=labelbgwidth)
            # test.grid(column=0, row=0)
            self.window = window


        def listenerHelp():
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
                
                results = FS.multiprocess_climb_hill(self.qs.QUADGRAM_FITNESS_MAP, GUI.ALPHABET, 4, self.qs.ZERO_FREQUENCY_FITNESS, inputText, num_threads=8)
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
        
        bgcolor = "#515358"
        labelbgcolor = "#09BA7C"
        labelfgcolor = "white"
        labelbgwidth = 34
        buttoncolor = labelbgcolor
        buttonwidth = 7
        buttonheight = 1
        btngapwidth = 1
        inputfieldcolor1 = "white"
        inputfieldcolor2 = "#C6C6C6"

        root = Tk()
        root.configure(background=bgcolor)
        root.title("Simple Substitution Encryption and Decryption")
        x_position = int(root.winfo_screenwidth()/2 - GUI.ROOT_WINDOW_WIDTH/2)
        y_position = int(root.winfo_screenheight()/2 - GUI.ROOT_WINDOW_HEIGHT/2)
        root.geometry(f'{GUI.ROOT_WINDOW_WIDTH}x{GUI.ROOT_WINDOW_HEIGHT}+{x_position}+{y_position}')
        
        # create the two bottom frames:
        encrypt_decrypt_btn_frame = Frame(root, bg=bgcolor)
        time_stat_frame = Frame(root, bg=labelbgcolor)
        textlabelframe = Frame(root, bg=labelbgcolor)
        textlabelframe.grid(column=1, row=4, sticky='we')
        resultlabelframe = Frame(root, bg=labelbgcolor)
        resultlabelframe.grid(column=3, row=4, sticky='we')


        # create the labels and text boxes:
        keyinputlabel = Label(root, text="KEY (leave blank to find/generate one):", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, width=labelbgwidth)
        keyinput = Entry(root,width=30, font=GUI.TEXT_FIELD_INPUT_FONT, relief=FLAT, bg=inputfieldcolor1)
        keyusedlabel = Label(root, text="KEY USED:", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, width=labelbgwidth)     
        keyusedoutput = Entry(root,width=30, font=GUI.TEXT_FIELD_INPUT_FONT, bg=inputfieldcolor2, relief=FLAT, state="readonly", readonlybackground=inputfieldcolor2) 
        textinputlabel = Label(textlabelframe, text="TEXT:", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, width=labelbgwidth)
        textinput = scrolledtext.ScrolledText(root, width=28, height=15, font=GUI.TEXT_FIELD_INPUT_FONT, relief=FLAT, bg=inputfieldcolor1)
        resultoutputlabel = Label(resultlabelframe, text="RESULT:", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor, width=labelbgwidth)
        resultoutput = scrolledtext.ScrolledText(root, width=28, height=15, font=GUI.TEXT_FIELD_INPUT_FONT, bg=inputfieldcolor2, relief=FLAT, state="disabled")

        # create the buttons:
        settingsbtn = Button(encrypt_decrypt_btn_frame, text="Settings", command=listenerSettings, width=buttonwidth, height=buttonheight, bg=buttoncolor, relief=FLAT, font=GUI.TEXT_LABEL_FONT, fg=labelfgcolor, overrelief=FLAT, borderwidth=0)
        helpbtn = Button(encrypt_decrypt_btn_frame, text="Help", command=listenerHelp, width=buttonwidth , height=buttonheight,bg=buttoncolor, relief=FLAT, font=GUI.TEXT_LABEL_FONT, fg=labelfgcolor, borderwidth=0)
        encryptbtn = Button(encrypt_decrypt_btn_frame, text="Encrypt", command=listenerEncrypt, width=buttonwidth+1 , height=buttonheight,bg=buttoncolor, relief=FLAT, font=GUI.TEXT_LABEL_FONT, fg=labelfgcolor, borderwidth=0)
        decryptbtn = Button(encrypt_decrypt_btn_frame, text="Decrypt", command=listenerDecrypt, width=buttonwidth+1 , height=buttonheight,bg=buttoncolor, relief=FLAT, font=GUI.TEXT_LABEL_FONT, fg=labelfgcolor, borderwidth=0)

        # create the time elapsed widgets:
        timeelapsedlabel = Label(time_stat_frame, text="Time Elapsed:", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor)
        timevalueplaceholder = Label(time_stat_frame, text="0.0000000000", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor)
        timeunitlabel = Label(time_stat_frame, text="seconds", font=GUI.TEXT_LABEL_FONT, bg=labelbgcolor, fg=labelfgcolor)
        
        root.grid_columnconfigure(0, minsize=30)
        root.grid_columnconfigure(2, minsize=50)
        root.grid_rowconfigure(0, minsize=30)
        root.grid_rowconfigure(3, minsize=15)

        keyinputlabel.grid(column=1, row=1, sticky="W")
        keyinput.grid(column=1, row=2, sticky="W")
        keyusedlabel.grid(column=3, row=1, sticky="W")
        keyusedoutput.grid(column=3, row=2, sticky="W")
        textinputlabel.grid(column=0, row=0, sticky="W")
        textinput.grid(column=1, row=5, sticky="W")
        resultoutputlabel.grid(column=0, row=0, sticky="W")
        resultoutput.grid(column=3, row=5, sticky="W")
        encrypt_decrypt_btn_frame.grid(column=1, row=6, sticky='we')

        settingsbtn.grid(column=0, row=0, pady=5, padx=(2,btngapwidth))
        helpbtn.grid(column=1, row=0, pady=5, padx=btngapwidth)
        encryptbtn.grid(column=2, row=0, pady=5, padx=btngapwidth)
        decryptbtn.grid(column=3, row=0, pady=5, padx=(btngapwidth, 0))

        
        time_stat_frame.grid(column=3, row=6, sticky='we')
        time_stat_frame.grid_columnconfigure(0, weight=1)
        time_stat_frame.grid_columnconfigure(1, weight=1)

        timeelapsedlabel.grid(column=0, row=0, padx=(5,0), pady=5, sticky="W")
        timevalueplaceholder.grid(column=1, row=0, pady=5, sticky="E")
        timeunitlabel.grid(column=2, row=0, padx= (0,20), pady=5, sticky="E")

        self.root = root

if __name__ == "__main__":
    myGui = GUI()
    myGui.qs.printStatistics()
    myGui.root.mainloop()