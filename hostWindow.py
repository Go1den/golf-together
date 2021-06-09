from tkinter import Toplevel, Frame, Label, Entry, NSEW, W, E, Button, SE, messagebox, END

class HostWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.withdraw()
        self.window.resizable(False, False)
        self.window.title("Host")
        self.window.geometry('+{x}+{y}'.format(x=parent.winfo_x(), y=parent.winfo_y()))
        self.window.iconbitmap('golfTogether.ico')
        self.window.grab_set()

        self.entryFrame = Frame(self.window)
        self.labelPort = Label(self.entryFrame, text="Port:")
        self.labelPort.grid(row=0, column=0, padx=4, pady=4, sticky=E)
        self.entryPort = Entry(self.entryFrame, width=6)
        self.entryPort.insert(END, "33000")
        self.entryPort.grid(row=0, column=1, padx=4, pady=4, sticky=W)
        self.entryFrame.grid(row=0, padx=4, pady=4, sticky=NSEW)

        self.buttonFrame = Frame(self.window)
        self.buttonOk = Button(self.buttonFrame, text="OK", width=8, command=self.onOk)
        self.buttonOk.grid(row=0, column=0, padx=4, pady=4, sticky=SE)
        self.buttonCancel = Button(self.buttonFrame, text="Cancel", width=8, command=lambda: self.window.destroy())
        self.buttonCancel.grid(row=0, column=1, padx=4, pady=4, sticky=SE)
        self.buttonFrame.grid(row=1, padx=4, pady=4, sticky=SE)

        self.window.deiconify()
        self.window.mainloop()

    def onOk(self):
        if self.entryPort.get().isnumeric():
            self.parent.hostLobby(int(self.entryPort.get()))
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Please enter a valid port number.", parent=self.window)
