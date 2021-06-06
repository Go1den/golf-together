from tkinter import Toplevel, Frame, Label, Entry, E, W, NSEW, Button, SE

from client import Client

class JoinLobbyWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.withdraw()
        self.window.resizable(False, False)
        self.window.title("Join")
        self.window.iconbitmap('golfTogether.ico')
        self.window.grab_set()

        self.entryFrame = Frame(self.window)
        self.labelAddress = Label(self.entryFrame, text="IP Address:")
        self.labelAddress.grid(row=0, column=0, padx=4, pady=4, sticky=E)
        self.entryAddress = Entry(self.entryFrame, width=20)
        self.entryAddress.grid(row=0, column=1, padx=4, pady=4, sticky=W)
        self.labelPort = Label(self.entryFrame, text="Port:")
        self.labelPort.grid(row=1, column=0, padx=4, pady=4, sticky=E)
        self.entryPort = Entry(self.entryFrame, width=6)
        self.entryPort.grid(row=1, column=1, padx=4, pady=4, sticky=W)
        self.entryFrame.grid(row=0, padx=4, pady=4, sticky=NSEW)

        self.buttonFrame = Frame(self.window)
        self.buttonOk = Button(self.buttonFrame, text="OK", width=8)
        self.buttonOk.grid(row=0, column=0, padx=4, pady=4, sticky=SE)
        self.buttonCancel = Button(self.buttonFrame, text="Cancel", width=8, command = lambda: self.window.destroy())
        self.buttonCancel.grid(row=0, column=1, padx=4, pady=4, sticky=SE)
        self.buttonFrame.grid(row=1, padx=4, pady=4, sticky=SE)

        self.window.deiconify()
        self.window.mainloop()

    def connectToLobby(self, c):
        self.parent.client = Client(self.entryAddress.get(), self.entryPort.get(), 1024, self.parent)
        self.parent.isHost = False
        self.parent.toggleChat()
        self.parent.toggleGameButtons()
        self.parent.toggleLobby()
        self.parent.toggleCourseButtons()
        self.window.destroy()