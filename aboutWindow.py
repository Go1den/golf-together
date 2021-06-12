import webbrowser
from tkinter import W, Toplevel, Label, LEFT, PhotoImage, Frame, SE, GROOVE, Button

class AboutWindow:
    def __init__(self, parent):
        self.aboutWindow = Toplevel(parent)
        self.aboutWindow.withdraw()
        self.aboutWindow.geometry('+{x}+{y}'.format(x=parent.winfo_x(), y=parent.winfo_y()))
        self.aboutWindow.wm_attributes("-topmost", 1)
        self.aboutWindow.focus_force()
        self.aboutWindow.iconbitmap("golfTogether.ico")
        self.aboutWindow.title("About")
        self.aboutWindow.resizable(False, False)
        self.aboutWindow.grab_set()

        self.frameTop = Frame(self.aboutWindow)

        self.aboutImage = PhotoImage(file="images/golf64.png")
        self.aboutImageLabel = Label(self.frameTop, image=self.aboutImage)
        self.aboutImageLabel.grid(row=0, column=0, padx=4, pady=4)

        self.aboutLabel = Label(self.frameTop, text="Golf Together\n\nVersion 1.0\n\nReleased: 6/24/2021", justify=LEFT)
        self.aboutLabel.grid(row=0, column=1, sticky=W, pady=4)

        self.frameTop.grid(row=0, column=0, sticky=W)

        self.aboutSupportLabel = Label(self.aboutWindow,
                                       text="Hello. I'm Go1den. I developed Golf Together.\nThis program is available to use for free.\nPlease support my project if you like it:",
                                       justify=LEFT)
        self.aboutSupportLabel.grid(row=1, column=0, sticky=W, padx=4, columnspan=2)

        self.myPaypalImage = PhotoImage(file="images/donate.png")
        self.myPaypalButton = Label(self.aboutWindow, image=self.myPaypalImage, cursor="hand2")
        self.myPaypalButton.bind("<Button-1>", lambda x: webbrowser.open('https://www.paypal.com/donate?hosted_button_id=V9YAA55ZKDYLL', new=2))
        self.myPaypalButton.grid(row=2, column=0, columnspan=2, pady=4, padx=4)

        self.aboutThanksLabel = Label(self.aboutWindow, text="Thank you so much for trying my program!\nIf you enjoy it, please tell others about it.", justify=LEFT)
        self.aboutThanksLabel.grid(row=3, column=0, sticky=W, pady=4, padx=4)

        self.okButton = Button(self.aboutWindow, text="OK", width=10, bd=2, relief=GROOVE, command=lambda: self.aboutWindow.destroy())
        self.okButton.grid(row=4, column=0, sticky=SE, pady=4)

        self.aboutWindow.deiconify()
        self.aboutWindow.mainloop()
