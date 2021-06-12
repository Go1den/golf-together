from tkinter import Toplevel, Frame, Label, Entry, E, W, NSEW, Button, SE, messagebox, DISABLED

from client import Client

class JoinLobbyWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.withdraw()
        self.window.resizable(False, False)
        self.window.title("Join")
        self.window.geometry('+{x}+{y}'.format(x=parent.winfo_x(), y=parent.winfo_y()))
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
        self.buttonOk = Button(self.buttonFrame, text="OK", width=8, command=lambda: self.connectToLobby())
        self.buttonOk.grid(row=0, column=0, padx=4, pady=4, sticky=SE)
        self.buttonCancel = Button(self.buttonFrame, text="Cancel", width=8, command=lambda: self.window.destroy())
        self.buttonCancel.grid(row=0, column=1, padx=4, pady=4, sticky=SE)
        self.buttonFrame.grid(row=1, padx=4, pady=4, sticky=SE)

        self.window.deiconify()
        self.window.mainloop()

    def connectToLobby(self):
        try:
            self.parent.client = Client(self.entryAddress.get(), int(self.entryPort.get()), 1024, self.parent)
            self.parent.client.send(self.parent.entryUsername.get())
            self.parent.entryUsername.configure(state=DISABLED)
        except TimeoutError:
            messagebox.showerror("Error", "Attempt to connect timed out. Did you enter the right info?", parent=self.window)
            self.parent.client = None
            return
        self.parent.isHost = False
        self.parent.toggleChat()
        self.parent.toggleLobby()
        self.window.destroy()
