from tkinter import Toplevel, Frame, Label, EW, GROOVE, DISABLED, W, NSEW, Button, SE, NORMAL, messagebox
from tkinter.ttk import Combobox

from messageConstants import MESSAGE_SUFFIX, START_GAME

class CourseSelectWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.withdraw()
        self.window.resizable(False, False)
        self.window.title("Join")
        self.window.geometry('+{x}+{y}'.format(x=parent.winfo_x(), y=parent.winfo_y()))
        self.window.iconbitmap('golfTogether.ico')
        self.window.grab_set()

        self.courseFrame = Frame(self.window, bd=2, relief=GROOVE)
        self.labelCourseOptions = Label(self.courseFrame, text="Course Select")
        self.labelCourseOptions.grid(row=0, padx=4, pady=4, sticky=EW)
        self.labelGame = Label(self.courseFrame, text="Game:")
        self.labelGame.grid(row=1, padx=4, pady=4, sticky=W)
        self.comboboxGame = Combobox(self.courseFrame, values=sorted(self.parent.gamesList, key=lambda x: x.upper()), width=40, state="readonly")
        self.comboboxGame.grid(row=2, padx=4, pady=4, sticky=W)
        self.comboboxGame.bind("<<ComboboxSelected>>", self.onGameSelect)
        self.labelCourse = Label(self.courseFrame, text="Course:")
        self.labelCourse.grid(row=3, padx=4, pady=4, sticky=W)
        self.comboboxCourse = Combobox(self.courseFrame, values=self.parent.courseList, width=40, state="readonly")
        self.comboboxCourse.grid(row=4, padx=4, pady=4, sticky=W)
        self.comboboxCourse.bind("<<ComboboxSelected>>", self.onCourseSelect)
        self.courseFrame.grid(row=0, padx=4, pady=4, sticky=NSEW)

        self.buttonFrame = Frame(self.window)
        self.buttonOk = Button(self.buttonFrame, text="OK", width=8, command=lambda: self.onOk())
        self.buttonOk.grid(row=0, column=0, padx=4, pady=4, sticky=SE)
        self.buttonCancel = Button(self.buttonFrame, text="Cancel", width=8, command=lambda: self.window.destroy())
        self.buttonCancel.grid(row=0, column=1, padx=4, pady=4, sticky=SE)
        self.buttonFrame.grid(row=1, padx=4, pady=4, sticky=SE)

        self.window.deiconify()
        self.window.mainloop()

    def onGameSelect(self, e):
        game = [x for x in self.parent.games if x.name == self.comboboxGame.get()]
        if game:
            self.parent.courseList = [x.name for x in game[0].courses]
            self.comboboxCourse.configure(values=self.parent.courseList)
        self.parent.server.broadcast(bytes("!setgame " + self.comboboxGame.get() + MESSAGE_SUFFIX, "utf8"))
        self.comboboxCourse.set("")

    def onCourseSelect(self, e):
        self.parent.server.broadcast(bytes("!setcourse \"" + self.comboboxCourse.get() + "\" " + self.lookupCoursePars(self.comboboxGame.get(), self.comboboxCourse.get()) + MESSAGE_SUFFIX, "utf8"))

    def onOk(self):
        if self.comboboxCourse.get() and self.comboboxGame.get():
            self.parent.server.broadcast(bytes(START_GAME + MESSAGE_SUFFIX, "utf8"))
            self.parent.buttonStartGame.configure(state=DISABLED)
            self.parent.buttonEndGame.configure(state=NORMAL)
            self.parent.scoreUpdated = True
            self.parent.canvas.delete("primaryText")
            self.parent.canvas.delete("secondaryText")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "You must select a game and course.", parent=self.window)

    def lookupCoursePars(self, selectedGame, selectedCourse):
        game = next(g for g in self.parent.games if g.name == selectedGame)
        course = next(c for c in game.courses if c.name == selectedCourse)
        return course.getParsAsString()
