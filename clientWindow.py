import json
import os
import sys
import time
import uuid
import webbrowser
from copy import deepcopy
from socket import gethostbyname, gethostname
from threading import Thread
from tkinter import Tk, Frame, Text, NSEW, DISABLED, Label, EW, Button, GROOVE, CENTER, W, E, IntVar, Scrollbar, WORD, Entry, END, StringVar, NORMAL, Menu, Canvas, HIDDEN, Listbox
from tkinter.ttk import Combobox

from PIL.ImageTk import PhotoImage

from aboutWindow import AboutWindow
from client import Client
from course import Course
from courseSelectWindow import CourseSelectWindow
from game import Game
from hostWindow import HostWindow
from joinLobbyWindow import JoinLobbyWindow
from player import Player
from server import Server
from validateUsername import validateUsername

class ClientWindow(Tk):
    def __init__(self):
        Tk.__init__(self, None)
        self.withdraw()
        self.resizable(False, False)
        self.title("Golf Together")
        self.iconbitmap('golfTogether.ico')
        self.protocol("WM_DELETE_WINDOW", lambda: self.exit())

        self.games = self.getGames()
        self.gamesList = [x.name for x in self.games]
        self.courseList = []

        self.server = None
        self.client = None
        self.isHost = False
        self.myUUID = str(uuid.uuid4())
        self.players = []

        self.menubar = Menu(self)
        self.fileMenu = Menu(self.menubar, tearoff=0, takefocus=0)
        self.fileMenu.add_command(label="Quit", command=lambda: self.exit())
        self.courseMenu = Menu(self.menubar, tearoff=0, takefocus=0)
        self.courseMenu.add_command(label="Download Course Data", command=lambda: webbrowser.open('https://github.com/Go1den/golf-together/discussions/categories/course-data', new=2))
        self.courseMenu.add_command(label="Upload Course Data", command=lambda: webbrowser.open('https://github.com/Go1den/golf-together/discussions/6', new=2))
        self.helpMenu = Menu(self.menubar, tearoff=0, takefocus=0)
        self.helpMenu.add_command(label="Report Issue", command=lambda: webbrowser.open('https://github.com/Go1den/golf-together/issues', new=2))
        self.helpMenu.add_command(label="About", command=lambda: AboutWindow(self))
        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.menubar.add_cascade(label="Course Data", menu=self.courseMenu)
        self.menubar.add_cascade(label="Help", menu=self.helpMenu)
        self.config(menu=self.menubar)

        self.myChatLine = StringVar()

        self.wholeWindowFrame = Frame()

        self.chatFrame = Frame(self.wholeWindowFrame)
        self.chatboxFrame = Frame(self.chatFrame)
        self.scrollBar = Scrollbar(self.chatboxFrame)
        self.leaderboardSlots = IntVar()
        self.leaderboardSlots.set(16)

        self.chatUsernameFrame = Frame(self.chatFrame)
        self.labelUsername = Label(self.chatUsernameFrame, text="Username:")
        self.labelUsername.grid(row=0, column=0, padx=4, pady=4, sticky=W)
        self.entryUsername = Entry(self.chatUsernameFrame, width=20)
        self.entryUsername.grid(row=0, column=1, padx=4, pady=4, sticky=W)
        self.labelLeaderboardSlots = Label(self.chatUsernameFrame, text="Leaderboard Slots:")
        self.labelLeaderboardSlots.grid(row=0, column=2, padx=(20, 4), pady=4, sticky=W)
        self.comboboxLeaderboardSlots = Combobox(self.chatUsernameFrame, width=3, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                                                 textvariable=self.leaderboardSlots, state="readonly")
        self.comboboxLeaderboardSlots.grid(row=0, column=3, padx=4, pady=4, sticky=W)
        self.comboboxLeaderboardSlots.bind("<<ComboboxSelected>>", self.onLeaderboardSlotsSelect)
        self.chatUsernameFrame.grid(row=0, padx=4, pady=(4, 0), sticky=NSEW)

        self.textChat = Text(self.chatboxFrame, width=50, height=24, state=DISABLED, yscrollcommand=self.scrollBar.set, wrap=WORD)
        self.textChat.bindtags((str(self.textChat), str(self), "all"))
        self.textChat.grid(row=1, column=0, padx=(4, 0), pady=4, sticky=NSEW)
        self.scrollBar.configure(command=self.textChat.yview)
        self.scrollBar.grid(row=1, column=1, padx=(0, 4), pady=4, sticky='nsw')  # TODO this is broken not scrolling trash lul
        self.chatboxFrame.grid(row=1, padx=4, pady=(4, 0), sticky=NSEW)
        self.chatEntryFrame = Frame(self.chatFrame)
        self.entryChat = Entry(self.chatEntryFrame, width=60, textvariable=self.myChatLine, state=DISABLED)
        self.entryChat.grid(row=0, column=0, padx=4, pady=4, sticky=NSEW)
        self.entryChat.bind("<Return>", self.sendChatMessageOnEnter)
        self.buttonChat = Button(self.chatEntryFrame, text="Chat", command=lambda: self.sendChatMessage(), state=DISABLED)
        self.buttonChat.grid(row=0, column=1, padx=4, pady=4, sticky=NSEW)
        self.chatEntryFrame.grid(row=2, padx=4, pady=(0, 4), sticky=NSEW)
        self.chatFrame.grid(row=0, column=0, rowspan=2)

        self.par1 = IntVar()
        self.par2 = IntVar()
        self.par3 = IntVar()
        self.par4 = IntVar()
        self.par5 = IntVar()
        self.par6 = IntVar()
        self.par7 = IntVar()
        self.par8 = IntVar()
        self.par9 = IntVar()
        self.par10 = IntVar()
        self.par11 = IntVar()
        self.par12 = IntVar()
        self.par13 = IntVar()
        self.par14 = IntVar()
        self.par15 = IntVar()
        self.par16 = IntVar()
        self.par17 = IntVar()
        self.par18 = IntVar()
        self.pars = [self.par1, self.par2, self.par3, self.par4, self.par5, self.par6, self.par7, self.par8, self.par9,
                     self.par10, self.par11, self.par12, self.par13, self.par14, self.par15, self.par16, self.par17, self.par18]

        self.score1 = IntVar()
        self.score2 = IntVar()
        self.score3 = IntVar()
        self.score4 = IntVar()
        self.score5 = IntVar()
        self.score6 = IntVar()
        self.score7 = IntVar()
        self.score8 = IntVar()
        self.score9 = IntVar()
        self.score10 = IntVar()
        self.score11 = IntVar()
        self.score12 = IntVar()
        self.score13 = IntVar()
        self.score14 = IntVar()
        self.score15 = IntVar()
        self.score16 = IntVar()
        self.score17 = IntVar()
        self.score18 = IntVar()
        self.scores = [self.score1, self.score2, self.score3, self.score4, self.score5, self.score6, self.score7, self.score8, self.score9,
                       self.score10, self.score11, self.score12, self.score13, self.score14, self.score15, self.score16, self.score17, self.score18]

        self.currentHole = 1
        self.totalPar = IntVar()
        self.totalScore = StringVar()
        self.totalScore.set("0")

        self.sidebarFrame = Frame(self.wholeWindowFrame, bd=2, relief=GROOVE)
        self.labelLobbyOptions = Label(self.sidebarFrame, text="Lobby Options")
        self.labelLobbyOptions.grid(row=0, column=0, columnspan=2, padx=4, pady=4, sticky=W)
        self.buttonHost = Button(self.sidebarFrame, text="Host Lobby", command=self.onHostLobby)
        self.buttonHost.grid(row=1, column=0, columnspan=2, padx=4, pady=4, sticky=EW)
        self.buttonJoin = Button(self.sidebarFrame, text="Join Lobby", command=lambda: self.joinLobby())
        self.buttonJoin.grid(row=2, column=0, columnspan=2, padx=4, pady=4, sticky=EW)
        self.buttonLeave = Button(self.sidebarFrame, text="Leave Lobby", state=DISABLED, command=lambda: self.client.send("!quit"))
        self.buttonLeave.grid(row=3, column=0, columnspan=2, padx=4, pady=4, sticky=EW)
        self.buttonStartGame = Button(self.sidebarFrame, text="Start Game", state=DISABLED, command=self.onStartGame)
        self.buttonStartGame.grid(row=4, column=0, columnspan=2, padx=4, pady=4, sticky=EW)
        self.buttonEndGame = Button(self.sidebarFrame, text="End Game", state=DISABLED, command=self.onEndGame)
        self.buttonEndGame.grid(row=5, column=0, columnspan=2, padx=4, pady=4, sticky=EW)
        self.labelPlayers = Label(self.sidebarFrame, text="Players")
        self.labelPlayers.grid(row=6, column=0, columnspan=2, padx=4, pady=(4,0), sticky=W)
        self.scrollBarPlayers = Scrollbar(self.sidebarFrame)
        self.listboxPlayers = Listbox(self.sidebarFrame, height=15, yscrollcommand=self.scrollBarPlayers.set)
        self.listboxPlayers.grid(row=7, column=0, padx=(4,0), pady=(0,4), sticky=EW)
        self.scrollBarPlayers.configure(command=self.listboxPlayers.yview)
        self.scrollBarPlayers.grid(row=7, column=1, padx=(0, 4), pady=4, sticky='nsw')
        self.sidebarFrame.grid(row=0, column=1, padx=4, pady=4, sticky=NSEW)

        self.scoreFrame = Frame(self.wholeWindowFrame, bd=2, relief=GROOVE)
        self.labelHole = Label(self.scoreFrame, text="Hole:")
        self.labelHole.grid(row=0, column=0, padx=4, pady=4, sticky=E)
        self.label1 = Label(self.scoreFrame, text="1", width=2)
        self.label1.grid(row=0, column=1, padx=2, pady=4, sticky=NSEW)
        self.label2 = Label(self.scoreFrame, text="2", width=2)
        self.label2.grid(row=0, column=2, padx=2, pady=4, sticky=NSEW)
        self.label3 = Label(self.scoreFrame, text="3", width=2)
        self.label3.grid(row=0, column=3, padx=2, pady=4, sticky=NSEW)
        self.label4 = Label(self.scoreFrame, text="4", width=2)
        self.label4.grid(row=0, column=4, padx=2, pady=4, sticky=NSEW)
        self.label5 = Label(self.scoreFrame, text="5", width=2)
        self.label5.grid(row=0, column=5, padx=2, pady=4, sticky=NSEW)
        self.label6 = Label(self.scoreFrame, text="6", width=2)
        self.label6.grid(row=0, column=6, padx=2, pady=4, sticky=NSEW)
        self.label7 = Label(self.scoreFrame, text="7", width=2)
        self.label7.grid(row=0, column=7, padx=2, pady=4, sticky=NSEW)
        self.label8 = Label(self.scoreFrame, text="8", width=2)
        self.label8.grid(row=0, column=8, padx=2, pady=4, sticky=NSEW)
        self.label9 = Label(self.scoreFrame, text="9", width=2)
        self.label9.grid(row=0, column=9, padx=2, pady=4, sticky=NSEW)
        self.label10 = Label(self.scoreFrame, text="10", width=2)
        self.label10.grid(row=0, column=10, padx=2, pady=4, sticky=NSEW)
        self.label11 = Label(self.scoreFrame, text="11", width=2)
        self.label11.grid(row=0, column=11, padx=2, pady=4, sticky=NSEW)
        self.label12 = Label(self.scoreFrame, text="12", width=2)
        self.label12.grid(row=0, column=12, padx=2, pady=4, sticky=NSEW)
        self.label13 = Label(self.scoreFrame, text="13", width=2)
        self.label13.grid(row=0, column=13, padx=2, pady=4, sticky=NSEW)
        self.label14 = Label(self.scoreFrame, text="14", width=2)
        self.label14.grid(row=0, column=14, padx=2, pady=4, sticky=NSEW)
        self.label15 = Label(self.scoreFrame, text="15", width=2)
        self.label15.grid(row=0, column=15, padx=2, pady=4, sticky=NSEW)
        self.label16 = Label(self.scoreFrame, text="16", width=2)
        self.label16.grid(row=0, column=16, padx=2, pady=4, sticky=NSEW)
        self.label17 = Label(self.scoreFrame, text="17", width=2)
        self.label17.grid(row=0, column=17, padx=2, pady=4, sticky=NSEW)
        self.label18 = Label(self.scoreFrame, text="18", width=2)
        self.label18.grid(row=0, column=18, padx=2, pady=4, sticky=NSEW)

        self.holeLabels = [self.label1, self.label2, self.label3, self.label4, self.label5, self.label6, self.label7, self.label8, self.label9,
                           self.label10, self.label11, self.label12, self.label13, self.label14, self.label15, self.label16, self.label17, self.label18]

        self.labelPar = Label(self.scoreFrame, text="Par:")
        self.labelPar.grid(row=1, column=0, padx=4, pady=4, sticky=E)
        self.labelPar1 = Label(self.scoreFrame, textvariable=self.par1, width=2, bd=2, relief=GROOVE, anchor=CENTER)
        self.labelPar1.grid(row=1, column=1, padx=2, pady=4, sticky=NSEW)
        self.labelPar2 = Label(self.scoreFrame, textvariable=self.par2, width=2, bd=2, relief=GROOVE)
        self.labelPar2.grid(row=1, column=2, padx=2, pady=4, sticky=NSEW)
        self.labelPar3 = Label(self.scoreFrame, textvariable=self.par3, width=2, bd=2, relief=GROOVE)
        self.labelPar3.grid(row=1, column=3, padx=2, pady=4, sticky=NSEW)
        self.labelPar4 = Label(self.scoreFrame, textvariable=self.par4, width=2, bd=2, relief=GROOVE)
        self.labelPar4.grid(row=1, column=4, padx=2, pady=4, sticky=NSEW)
        self.labelPar5 = Label(self.scoreFrame, textvariable=self.par5, width=2, bd=2, relief=GROOVE)
        self.labelPar5.grid(row=1, column=5, padx=2, pady=4, sticky=NSEW)
        self.labelPar6 = Label(self.scoreFrame, textvariable=self.par6, width=2, bd=2, relief=GROOVE)
        self.labelPar6.grid(row=1, column=6, padx=2, pady=4, sticky=NSEW)
        self.labelPar7 = Label(self.scoreFrame, textvariable=self.par7, width=2, bd=2, relief=GROOVE)
        self.labelPar7.grid(row=1, column=7, padx=2, pady=4, sticky=NSEW)
        self.labelPar8 = Label(self.scoreFrame, textvariable=self.par8, width=2, bd=2, relief=GROOVE)
        self.labelPar8.grid(row=1, column=8, padx=2, pady=4, sticky=NSEW)
        self.labelPar9 = Label(self.scoreFrame, textvariable=self.par9, width=2, bd=2, relief=GROOVE)
        self.labelPar9.grid(row=1, column=9, padx=2, pady=4, sticky=NSEW)
        self.labelPar10 = Label(self.scoreFrame, textvariable=self.par10, width=2, bd=2, relief=GROOVE)
        self.labelPar10.grid(row=1, column=10, padx=2, pady=4, sticky=NSEW)
        self.labelPar11 = Label(self.scoreFrame, textvariable=self.par11, width=2, bd=2, relief=GROOVE)
        self.labelPar11.grid(row=1, column=11, padx=2, pady=4, sticky=NSEW)
        self.labelPar12 = Label(self.scoreFrame, textvariable=self.par12, width=2, bd=2, relief=GROOVE)
        self.labelPar12.grid(row=1, column=12, padx=2, pady=4, sticky=NSEW)
        self.labelPar13 = Label(self.scoreFrame, textvariable=self.par13, width=2, bd=2, relief=GROOVE)
        self.labelPar13.grid(row=1, column=13, padx=2, pady=4, sticky=NSEW)
        self.labelPar14 = Label(self.scoreFrame, textvariable=self.par14, width=2, bd=2, relief=GROOVE)
        self.labelPar14.grid(row=1, column=14, padx=2, pady=4, sticky=NSEW)
        self.labelPar15 = Label(self.scoreFrame, textvariable=self.par15, width=2, bd=2, relief=GROOVE)
        self.labelPar15.grid(row=1, column=15, padx=2, pady=4, sticky=NSEW)
        self.labelPar16 = Label(self.scoreFrame, textvariable=self.par16, width=2, bd=2, relief=GROOVE)
        self.labelPar16.grid(row=1, column=16, padx=2, pady=4, sticky=NSEW)
        self.labelPar17 = Label(self.scoreFrame, textvariable=self.par17, width=2, bd=2, relief=GROOVE)
        self.labelPar17.grid(row=1, column=17, padx=2, pady=4, sticky=NSEW)
        self.labelPar18 = Label(self.scoreFrame, textvariable=self.par18, width=2, bd=2, relief=GROOVE)
        self.labelPar18.grid(row=1, column=18, padx=2, pady=4, sticky=NSEW)
        self.labelParTotal = Label(self.scoreFrame, textvariable=self.totalPar, width=5, anchor=W)
        self.labelParTotal.grid(row=1, column=19, padx=2, pady=4, sticky=NSEW)

        self.labelScore = Label(self.scoreFrame, text="Score:")
        self.labelScore.grid(row=2, column=0, padx=4, pady=4, sticky=E)
        self.labelScore1 = Label(self.scoreFrame, textvariable=self.score1, width=2, bd=2, relief=GROOVE, anchor=CENTER)
        self.labelScore1.grid(row=2, column=1, padx=2, pady=4, sticky=NSEW)
        self.labelScore2 = Label(self.scoreFrame, textvariable=self.score2, width=2, bd=2, relief=GROOVE)
        self.labelScore2.grid(row=2, column=2, padx=2, pady=4, sticky=NSEW)
        self.labelScore3 = Label(self.scoreFrame, textvariable=self.score3, width=2, bd=2, relief=GROOVE)
        self.labelScore3.grid(row=2, column=3, padx=2, pady=4, sticky=NSEW)
        self.labelScore4 = Label(self.scoreFrame, textvariable=self.score4, width=2, bd=2, relief=GROOVE)
        self.labelScore4.grid(row=2, column=4, padx=2, pady=4, sticky=NSEW)
        self.labelScore5 = Label(self.scoreFrame, textvariable=self.score5, width=2, bd=2, relief=GROOVE)
        self.labelScore5.grid(row=2, column=5, padx=2, pady=4, sticky=NSEW)
        self.labelScore6 = Label(self.scoreFrame, textvariable=self.score6, width=2, bd=2, relief=GROOVE)
        self.labelScore6.grid(row=2, column=6, padx=2, pady=4, sticky=NSEW)
        self.labelScore7 = Label(self.scoreFrame, textvariable=self.score7, width=2, bd=2, relief=GROOVE)
        self.labelScore7.grid(row=2, column=7, padx=2, pady=4, sticky=NSEW)
        self.labelScore8 = Label(self.scoreFrame, textvariable=self.score8, width=2, bd=2, relief=GROOVE)
        self.labelScore8.grid(row=2, column=8, padx=2, pady=4, sticky=NSEW)
        self.labelScore9 = Label(self.scoreFrame, textvariable=self.score9, width=2, bd=2, relief=GROOVE)
        self.labelScore9.grid(row=2, column=9, padx=2, pady=4, sticky=NSEW)
        self.labelScore10 = Label(self.scoreFrame, textvariable=self.score10, width=2, bd=2, relief=GROOVE)
        self.labelScore10.grid(row=2, column=10, padx=2, pady=4, sticky=NSEW)
        self.labelScore11 = Label(self.scoreFrame, textvariable=self.score11, width=2, bd=2, relief=GROOVE)
        self.labelScore11.grid(row=2, column=11, padx=2, pady=4, sticky=NSEW)
        self.labelScore12 = Label(self.scoreFrame, textvariable=self.score12, width=2, bd=2, relief=GROOVE)
        self.labelScore12.grid(row=2, column=12, padx=2, pady=4, sticky=NSEW)
        self.labelScore13 = Label(self.scoreFrame, textvariable=self.score13, width=2, bd=2, relief=GROOVE)
        self.labelScore13.grid(row=2, column=13, padx=2, pady=4, sticky=NSEW)
        self.labelScore14 = Label(self.scoreFrame, textvariable=self.score14, width=2, bd=2, relief=GROOVE)
        self.labelScore14.grid(row=2, column=14, padx=2, pady=4, sticky=NSEW)
        self.labelScore15 = Label(self.scoreFrame, textvariable=self.score15, width=2, bd=2, relief=GROOVE)
        self.labelScore15.grid(row=2, column=15, padx=2, pady=4, sticky=NSEW)
        self.labelScore16 = Label(self.scoreFrame, textvariable=self.score16, width=2, bd=2, relief=GROOVE)
        self.labelScore16.grid(row=2, column=16, padx=2, pady=4, sticky=NSEW)
        self.labelScore17 = Label(self.scoreFrame, textvariable=self.score17, width=2, bd=2, relief=GROOVE)
        self.labelScore17.grid(row=2, column=17, padx=2, pady=4, sticky=NSEW)
        self.labelScore18 = Label(self.scoreFrame, textvariable=self.score18, width=2, bd=2, relief=GROOVE)
        self.labelScore18.grid(row=2, column=18, padx=2, pady=4, sticky=NSEW)
        self.labelScoreTotal = Label(self.scoreFrame, textvariable=self.totalScore, width=9, anchor=W)
        self.labelScoreTotal.grid(row=2, column=19, padx=2, pady=4, sticky=NSEW)

        self.scoreFrame.grid(row=2, column=0, columnspan=2, padx=4, pady=4, sticky=NSEW)

        self.scoreInputFrame = Frame(self.wholeWindowFrame, bd=2, relief=GROOVE)
        self.buttonHoleInOne = Button(self.scoreInputFrame, text="Hole in One", width=18, command=lambda: self.recordScore(1), state=DISABLED)
        self.buttonHoleInOne.grid(row=0, column=0, padx=4, pady=4, sticky=NSEW)
        self.buttonAlbatross = Button(self.scoreInputFrame, text="Albatross (-3)", command=lambda: self.recordScore(self.getCurrentHolePar() - 3), state=DISABLED)
        self.buttonAlbatross.grid(row=1, column=0, padx=4, pady=4, sticky=NSEW)
        self.buttonEagle = Button(self.scoreInputFrame, text="Eagle (-2)", command=lambda: self.recordScore(self.getCurrentHolePar() - 2), state=DISABLED)
        self.buttonEagle.grid(row=2, column=0, padx=4, pady=4, sticky=NSEW)
        self.buttonBirdie = Button(self.scoreInputFrame, text="Birdie (-1)", command=lambda: self.recordScore(self.getCurrentHolePar() - 1), state=DISABLED)
        self.buttonBirdie.grid(row=3, column=0, padx=4, pady=4, sticky=NSEW)
        self.buttonPar = Button(self.scoreInputFrame, text="Par (0)", command=lambda: self.recordScore(self.getCurrentHolePar()), state=DISABLED)
        self.buttonPar.grid(row=0, column=1, padx=4, pady=4, sticky=NSEW)
        self.buttonBogey = Button(self.scoreInputFrame, text="Bogey (+1)", width=18, command=lambda: self.recordScore(self.getCurrentHolePar() + 1), state=DISABLED)
        self.buttonBogey.grid(row=1, column=1, padx=4, pady=4, sticky=NSEW)
        self.buttonDoubleBogey = Button(self.scoreInputFrame, text="Double Bogey (+2)", command=lambda: self.recordScore(self.getCurrentHolePar() + 2), state=DISABLED)
        self.buttonDoubleBogey.grid(row=2, column=1, padx=4, pady=4, sticky=NSEW)
        self.buttonTripleBogey = Button(self.scoreInputFrame, text="Triple Bogey (+3)", command=lambda: self.recordScore(self.getCurrentHolePar() + 3), state=DISABLED)
        self.buttonTripleBogey.grid(row=3, column=1, padx=4, pady=4, sticky=NSEW)
        self.button4OverPar = Button(self.scoreInputFrame, text="Four Over Par (+4)", command=lambda: self.recordScore(self.getCurrentHolePar() + 4), state=DISABLED)
        self.button4OverPar.grid(row=0, column=2, padx=4, pady=4, sticky=NSEW)
        self.button5OverPar = Button(self.scoreInputFrame, text="Five Over Par (+5)", command=lambda: self.recordScore(self.getCurrentHolePar() + 5), state=DISABLED)
        self.button5OverPar.grid(row=1, column=2, padx=4, pady=4, sticky=NSEW)
        self.button6OverPar = Button(self.scoreInputFrame, text="Six Over Par (+6)", width=18, command=lambda: self.recordScore(self.getCurrentHolePar() + 6), state=DISABLED)
        self.button6OverPar.grid(row=2, column=2, padx=4, pady=4, sticky=NSEW)
        self.button7OverPar = Button(self.scoreInputFrame, text="Seven Over Par (+7)", command=lambda: self.recordScore(self.getCurrentHolePar() + 7), state=DISABLED)
        self.button7OverPar.grid(row=3, column=2, padx=4, pady=4, sticky=NSEW)
        self.button8OverPar = Button(self.scoreInputFrame, text="Eight Over Par (+8)", command=lambda: self.recordScore(self.getCurrentHolePar() + 8), state=DISABLED)
        self.button8OverPar.grid(row=0, column=3, padx=4, pady=4, sticky=NSEW)
        self.button9OverPar = Button(self.scoreInputFrame, text="Nine Over Par (+9)", command=lambda: self.recordScore(self.getCurrentHolePar() + 9), state=DISABLED)
        self.button9OverPar.grid(row=1, column=3, padx=4, pady=4, sticky=NSEW)
        self.button10OverPar = Button(self.scoreInputFrame, text="Ten Over Par (+10)", command=lambda: self.recordScore(self.getCurrentHolePar() + 10), state=DISABLED)
        self.button10OverPar.grid(row=2, column=3, padx=4, pady=4, sticky=NSEW)
        self.buttonClearMostRecentHole = Button(self.scoreInputFrame, text="Clear Most Recent", width=18, command=lambda: self.clearMostRecentScore(), state=DISABLED)
        self.buttonClearMostRecentHole.grid(row=3, column=3, padx=4, pady=4, sticky=NSEW)
        self.scoreInputFrame.grid(row=3, column=0, columnspan=2, padx=4, pady=4, sticky=NSEW)

        self.canvasFrame = Frame(self.wholeWindowFrame)
        self.canvas = Canvas(self.canvasFrame, bg="#00ff00", width=361, height=717)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        self.topOfLeaderboardImage = PhotoImage(file="images/leaderboard.png")
        self.canvas.create_image(182, 24, image=self.topOfLeaderboardImage, tags="topOfLeaderboardImage")
        self.img2 = PhotoImage(file="images/leaderboard2.png")

        y = 66
        for x in range(16):
            self.canvas.create_image(182, y, image=self.img2, tags="rectangle")
            y += 42

        self.canvasFrame.grid(row=0, rowspan=4, column=2, padx=4, pady=4, sticky=NSEW)
        self.wholeWindowFrame.grid()

        self.addText("<System> Welcome to Golf Together! To start, host or join a lobby.")
        self.thread = Thread(target=self.leaderboardLoop, daemon=True).start()
        self.deiconify()
        self.mainloop()

    def leaderboardLoop(self):
        while True:
            self.drawLeaderboard()

    def drawLeaderboard(self):
        sortedPlayerList = sorted(deepcopy(self.players), key=lambda x: (x.score - x.parThroughCurrentHole, x.currentHole))
        sortedPlayerListChunks = self.splitListIntoChunks(sortedPlayerList, self.leaderboardSlots.get())
        place = 1
        idx = 1
        previousPlayer = None
        for chunk in sortedPlayerListChunks:
            y = 66
            for player in chunk:
                if not previousPlayer or previousPlayer.scoreAsString != player.scoreAsString:
                    place = idx
                self.canvas.create_text(38, y, text=place, fill="white", font=("Franklin Gothic Medium", 18), anchor=E, tags="text")
                self.canvas.create_text(72, y, text=player.name, fill="white", font=("Franklin Gothic Medium", 18), anchor=W, tags="text")
                self.canvas.create_text(270, y, text=player.scoreAsString, font=("Franklin Gothic Medium", 18), tags="text")
                self.canvas.create_text(336, y, text=player.currentHole, fill="white", font=("Franklin Gothic Medium", 18), tags="text")
                y += 42
                idx += 1
                previousPlayer = player
            time.sleep(5)
            self.canvas.delete("text")
        if not sortedPlayerListChunks:
            time.sleep(5)

    def setPlayerListbox(self, playerList):
        self.listboxPlayers.delete(0, END)
        for player in sorted(playerList, key=lambda x: x.upper()):
            self.listboxPlayers.insert(END, player + "\n")

    def splitListIntoChunks(self, lst, chunkSize):
        result = []
        for i in range(0, len(lst), chunkSize):
            result.append(lst[i:i + chunkSize])
        return result

    def addText(self, text):
        self.textChat.configure(state=NORMAL)
        self.textChat.insert(END, text + "\n")
        self.textChat.configure(state=DISABLED)
        self.textChat.see(END)

    def hostLobby(self, port):
        if not self.client:
            self.server = Server('', port, 1024, 128, self)
            self.client = Client(gethostbyname(gethostname()), port, 1024, self)
            self.client.send(self.entryUsername.get())
            self.entryUsername.configure(state=DISABLED)
            self.isHost = True
            self.buttonStartGame.configure(state=NORMAL)
            self.toggleChat()
            self.toggleLobby()

    def joinLobby(self):
        if validateUsername(self.entryUsername.get(), self):
            JoinLobbyWindow(self)
            self.client.send(self.entryUsername.get())
            self.entryUsername.configure(state=DISABLED)

    def sendChatMessageOnEnter(self, e):
        self.sendChatMessage()

    def sendChatMessage(self):
        if self.client and self.myChatLine.get():
            if not self.myChatLine.get().startswith("!startgame") and not self.myChatLine.get().startswith("!endgame") \
                    and not self.myChatLine.get().startswith("!setcourse") and not self.myChatLine.get().startswith("!setgame"):
                self.client.send(self.myChatLine.get())
            self.myChatLine.set("")
            self.entryChat.focus_set()

    def toggleLobby(self):
        if self.client:
            self.buttonHost.configure(state=DISABLED)
            self.buttonJoin.configure(state=DISABLED)
            self.buttonLeave.configure(state=NORMAL)
        else:
            self.buttonHost.configure(state=NORMAL)
            self.buttonJoin.configure(state=NORMAL)
            self.buttonLeave.configure(state=DISABLED)

    def toggleChat(self):
        if self.client:
            self.entryChat.configure(state=NORMAL)
            self.buttonChat.configure(state=NORMAL)
        else:
            self.entryChat.configure(state=DISABLED)
            self.buttonChat.configure(state=DISABLED)

    def recordScore(self, score):
        if self.currentHole < 19:
            self.scores[self.currentHole - 1].set(score)
            self.currentHole += 1
            self.updateTotalScore()
            self.highlightCurrentHole()
            msg = "!setscore " + self.entryUsername.get() + " " + self.myUUID + " " + str(self.getTotalScore()) + " " + str(self.getPartialParScore()) + " " \
                  + str(self.currentHole - 1) + " " + str(self.scores[self.currentHole - 2].get())
            self.client.send(msg)

    def clearMostRecentScore(self):
        if self.currentHole > 1:
            self.scores[self.currentHole - 2].set(0)
            self.currentHole -= 1
            self.updateTotalScore()
            self.highlightCurrentHole()
            msg = "!setscore " + self.entryUsername.get() + " " + self.myUUID + " " + str(self.getTotalScore()) + " " + str(self.getPartialParScore()) + " " \
                  + str(self.currentHole - 1)
            self.client.send(msg)

    def updatePlayerScore(self, msg):
        splitMsg = msg.split()
        player = next((x for x in self.players if x.uuid == splitMsg[2]), None)
        if not player:
            self.players.append(Player(splitMsg[1], splitMsg[2], int(splitMsg[3]), int(splitMsg[4]), int(splitMsg[5])))
        else:
            player.score = int(splitMsg[3])
            player.parThroughCurrentHole = int(splitMsg[4])
            player.currentHole = int(splitMsg[5])
            player.setRelativeScore()
        if len(splitMsg) == 7:
            self.addText("<System> " + splitMsg[1] + " scored " + splitMsg[6] + " on hole " + splitMsg[5])
        self.printAllPlayerInfo()

    def printAllPlayerInfo(self):
        for p in self.players:
            p.print()

    def setPars(self, pars):
        idx = 0
        parsAsList = pars.split(",")
        for par in self.pars:
            par.set(int(parsAsList[idx]))
            idx += 1
        self.totalPar.set(sum([int(x) for x in parsAsList]))

    def getCurrentHolePar(self) -> int:
        try:
            result = self.pars[self.currentHole - 1].get()
            return result
        except IndexError:
            return 0

    def getPartialParScore(self) -> int:
        if self.currentHole == 1:
            return 0
        return sum([x.get() for x in self.pars[0:self.currentHole - 1]])

    def getTotalScore(self) -> int:
        return sum([x.get() for x in self.scores])

    def updateTotalScore(self):
        if self.currentHole == 1:
            self.totalScore.set("0")
        else:
            self.totalScore.set(str(sum(x.get() for x in self.scores)) + " (" + self.getCurrentRelativeScore() + ")")

    def getCurrentRelativeScore(self) -> str:
        relScore = sum(x.get() for x in self.scores[0:self.currentHole - 1]) - sum(x.get() for x in self.pars[0:self.currentHole - 1])
        if relScore == 0:
            return "E"
        elif relScore > 0:
            return str("+") + str(relScore)
        return str(relScore)

    def onHostLobby(self):
        if validateUsername(self.entryUsername.get(), self):
            HostWindow(self)

    def onStartGame(self):
        CourseSelectWindow(self)

    def onLeaderboardSlotsSelect(self, e):
        for x in range(2, 2 + self.leaderboardSlots.get()):
            self.canvas.itemconfig(x, state=NORMAL)
        for x in range(2 + self.leaderboardSlots.get(), 18):
            self.canvas.itemconfig(x, state=HIDDEN)

    def onEndGame(self):
        self.server.broadcast(bytes("!endgame", "utf8"))
        self.buttonStartGame.configure(state=NORMAL)
        self.buttonEndGame.configure(state=DISABLED)

    def getGames(self) -> list[Game]:
        games = []
        try:
            for filePath in os.listdir(os.getcwd() + '/courses'):
                courses = []
                with open('courses/' + filePath, encoding="utf8") as f:
                    thisJson = json.load(f)
                    for course in thisJson.get("courses", []):
                        courses.append(Course(course.get("name"), course.get("parList")))
                    games.append(Game(thisJson.get("game", "Unknown Course"), courses))
            return games
        except:
            return []

    def resetGame(self):
        self.currentHole = 1
        for x in self.pars:
            x.set(0)
        for y in self.scores:
            y.set(0)
        self.updateTotalScore()
        self.totalPar.set(0)
        self.setStateOfAllScoreButtons(DISABLED)

    def resetOnLogoff(self):
        if self.server:
            self.server.closeAllConnections()
            self.server.server.close()
        self.server = None
        self.isHost = False
        self.client = None
        self.buttonHost.configure(state=NORMAL)
        self.buttonJoin.configure(state=NORMAL)
        self.buttonLeave.configure(state=DISABLED)
        self.buttonStartGame.configure(state=DISABLED)
        self.buttonEndGame.configure(state=DISABLED)
        self.entryChat.configure(state=DISABLED)
        self.buttonChat.configure(state=DISABLED)
        self.entryUsername.configure(state=NORMAL)
        self.players = []
        self.setPlayerListbox([])
        self.removeAllHoleHighlights()

    def setStateOfAllScoreButtons(self, newState):
        self.buttonHoleInOne.configure(state=newState)
        self.buttonAlbatross.configure(state=newState)
        self.buttonEagle.configure(state=newState)
        self.buttonBirdie.configure(state=newState)
        self.buttonPar.configure(state=newState)
        self.buttonBogey.configure(state=newState)
        self.buttonDoubleBogey.configure(state=newState)
        self.buttonTripleBogey.configure(state=newState)
        self.button4OverPar.configure(state=newState)
        self.button5OverPar.configure(state=newState)
        self.button6OverPar.configure(state=newState)
        self.button7OverPar.configure(state=newState)
        self.button8OverPar.configure(state=newState)
        self.button9OverPar.configure(state=newState)
        self.button10OverPar.configure(state=newState)
        self.buttonClearMostRecentHole.configure(state=newState)

    def highlightCurrentHole(self):
        self.removeAllHoleHighlights()
        if 0 < self.currentHole < 19:
            self.holeLabels[self.currentHole - 1].configure(background="#00ff00")

    def removeAllHoleHighlights(self):
        for hole in self.holeLabels:
            hole.configure(background="SystemButtonFace")

    def exit(self):
        if self.client:
            self.client.closeConnection()
        sys.exit(0)
