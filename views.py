from tkinter import Button, Tk, Frame, Label, LabelFrame, Checkbutton, IntVar, Toplevel
import tkmacosx
from models import WindowMgr, Mouse

class StartApp:
    def __init__(self):
        self.mainWin = Tk()
        self.mainWin.geometry("420x30")
        self.title = "Olho mágico"
        self.mainWin.title(self.title)
        self.totalButtons = 6
        self.assignedList = []
        self.listClear()
        self.buttonCollapsedH = 5
        self.buttonH = 20
        self.contextMenuWin = None
        self.appsList = []
        self.labelHighlightColor = "#AAAABB"
        self.labelColor = "#FFFFFF"
        self.topmostIntvar = IntVar()

        self.mainWin.bind("<Enter>",self.focusMainWindow)

        self.mainWin.bind("<Key>",self.shortcut)
    
        self.draw()

    def shortcut(self,event):
        key = ""
        try:
            key = int(event.char)
        except:
            pass

        if key > 0 and key <= 6:
            self.buttonClick(key-1)

    def focusMainWindow(self,event):
        # self.mainWin.wm_attributes("-topmost",True)
        # self.mainWin.grab_set()
        # self.mainWin.lift()
        # self.mainWin.wm_attributes("-topmost", False)
        self.mainWin.focus_force()
        # self.mainWin.wm_attributes("-topmost", True)
        # self.mainWin.focus()
        # self.mainWin.grab_release()
        # WindowMgr().show_window(self.hwnd)
        # WindowMgr().set_foreground(self.hwnd)
        # self.mainWin.focus_set()
        pass

    def labelHover(self,labelIndex,highlight):
        if highlight:
            self.labelList[labelIndex].configure(background=self.labelHighlightColor)
        else:
            self.labelList[labelIndex].configure(background=self.labelColor)

    def showContextMenu(self,event,buttonIndex):
        self.contextMenuWin = Tk()
        self.contextMenuWin.title(self.title)
        self.contextMenuWin.overrideredirect(1)
        self.contextMenuWin.bind("<FocusOut>", self.hideContextMenu)
        self.contextMenuWin.lift()
        self.contextMenuWin.wm_attributes("-topmost",True)
        self.contextMenuWin.focus_force()
        x = Mouse().get_x()
        y = Mouse().get_y()
        self.contextMenuWin.geometry('+%d+%d' % (x, y))

        frame1 = Frame(self.contextMenuWin, background="#AFFFFF")
        frame1.pack(side="left", expand=1, fill="both", anchor="n")
        frame1.bind("<Leave>", self.hideContextMenu)

        w = WindowMgr()
        appList = w.get_app_list(self.title)
        self.appsList.clear()
        self.labelList = []

        for window in appList:
            currentApp = [window[0], window[1], Label(frame1, text=window[1], anchor="w", bg="white")] # [0]: HWND [1]: Title [2]: Label
            self.labelList.append(currentApp[2])
            self.appsList.append(currentApp)

        for labelIndex, label in enumerate(self.appsList):
            label[2].pack(side="top", expand=1, fill="x", anchor="n")
            label[2].bind("<Enter>", lambda event, labelIndex=labelIndex, highlight=True: self.labelHover(labelIndex,highlight))
            label[2].bind("<Leave>", lambda event, labelIndex=labelIndex, highlight=False: self.labelHover(labelIndex,highlight))
            label[2].bind("<Button-1>", lambda event, index=buttonIndex, appHwnd=label[0]: self.assignButton(buttonIndex, appHwnd))

        clearLabel = Label(frame1,text="Desabilitar botão", fg="red", bg="white")
        self.labelList.append(clearLabel)
        clearLabel.pack(side="top", expand=1, fill="x", anchor="n")
        clearLabel.bind("<Enter>", lambda event, labelIndex=len(self.labelList) - 1, highlight=True: self.labelHover(labelIndex,highlight))
        clearLabel.bind("<Leave>", lambda event, labelIndex=len(self.labelList) - 1, highlight=False: self.labelHover(labelIndex,highlight))
        clearLabel.bind("<Button-1>", lambda event, index=buttonIndex, appHwnd="": self.assignButton(buttonIndex, appHwnd))

        self.contextMenuWin.mainloop()

    def hideContextMenu(self,event=""):
        self.contextMenuWin.destroy()

    def listClear(self):
        self.assignedList.clear()
        for i in range(self.totalButtons):
            self.assignedList.append("")

    def assignButton(self,buttonIndex,app):
        self.hideContextMenu()
        self.assignedList[buttonIndex] = app
        if app != "":
            self.toggleButton(buttonIndex,True)
        else:
            self.toggleButton(buttonIndex,False)

    def toggleButton(self,index,expand):
        if expand:
            self.buttonList[index].configure(height=self.buttonH)
        elif not expand and self.assignedList[index] == "":
            self.buttonList[index].configure(height=self.buttonCollapsedH)

    def topmost(self):
        self.mainWin.wm_attributes("-topmost", self.topmostIntvar.get())

    def draw(self):
        frame1 = Frame(self.mainWin)
        frame1.pack(side="left", expand=1, fill="x")

        self.button1 = tkmacosx.Button(frame1, text="A", bg="#FFFFFF")
        self.button1.pack(side="left", padx=3)
        self.button1.bind("<Button-1>", lambda event, index=0: self.buttonClick(index))
        self.button1.bind("<Button-3>", lambda event, index=0: self.showContextMenu(event,index))
        self.button1.bind("<Enter>", lambda event, index=0, expand=True: self.toggleButton(index, expand))
        self.button1.bind("<Leave>", lambda event, index=0, expand=False: self.toggleButton(index, expand))

        self.button2 = tkmacosx.Button(frame1, text="B", bg="#FFFFAA")
        self.button2.pack(side="left", padx=3)
        self.button2.bind("<Button-1>", lambda event, index=1: self.buttonClick(index))
        self.button2.bind("<Button-3>", lambda event, index=1: self.showContextMenu(event,index))
        self.button2.bind("<Enter>", lambda event, index=1, expand=True: self.toggleButton(index, expand))
        self.button2.bind("<Leave>", lambda event, index=1, expand=False: self.toggleButton(index, expand))

        self.button3 = tkmacosx.Button(frame1, text="C", bg="#AAFFAA")
        self.button3.pack(side="left", padx=3)
        self.button3.bind("<Button-1>", lambda event, index=2: self.buttonClick(index))
        self.button3.bind("<Button-3>", lambda event, index=2: self.showContextMenu(event,index))
        self.button3.bind("<Enter>", lambda event, index=2, expand=True: self.toggleButton(index, expand))
        self.button3.bind("<Leave>", lambda event, index=2, expand=False: self.toggleButton(index, expand))

        self.button4 = tkmacosx.Button(frame1, text="D", bg="#AAAAFF")
        self.button4.pack(side="left", padx=3)
        self.button4.bind("<Button-1>", lambda event, index=3: self.buttonClick(index))
        self.button4.bind("<Button-3>", lambda event, index=3: self.showContextMenu(event,index))
        self.button4.bind("<Enter>", lambda event, index=3, expand=True: self.toggleButton(index, expand))
        self.button4.bind("<Leave>", lambda event, index=3, expand=False: self.toggleButton(index, expand))

        self.button5 = tkmacosx.Button(frame1, text="E", bg="#AA55FF")
        self.button5.pack(side="left", padx=3)
        self.button5.bind("<Button-1>", lambda event, index=4: self.buttonClick(index))
        self.button5.bind("<Button-3>", lambda event, index=4: self.showContextMenu(event,index))
        self.button5.bind("<Enter>", lambda event, index=4, expand=True: self.toggleButton(index, expand))
        self.button5.bind("<Leave>", lambda event, index=4, expand=False: self.toggleButton(index, expand))

        self.button6 = tkmacosx.Button(frame1, text="F", bg="#AAAAAA")
        self.button6.pack(side="left", padx=3)
        self.button6.bind("<Button-1>", lambda event, index=5: self.buttonClick(index))
        self.button6.bind("<Button-3>", lambda event, index=5: self.showContextMenu(event,index))
        self.button6.bind("<Enter>", lambda event, index=5, expand=True: self.toggleButton(index, expand))
        self.button6.bind("<Leave>", lambda event, index=5, expand=False: self.toggleButton(index, expand))

        self.buttonList = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6]

        topmostCheckbutton = Checkbutton(frame1, text="Manter no topo", variable=self.topmostIntvar, command=self.topmost)
        topmostCheckbutton.pack(side="right", padx=10)

        for btn in self.buttonList:
            btn.configure(height=self.buttonCollapsedH, borderless=1, width=40)

    def buttonClick(self,buttonIndex):
        if self.assignedList[buttonIndex] == "":
            return 0
        WindowMgr().set_foreground(self.assignedList[buttonIndex])


if __name__ == "__main__":
    app = StartApp()
    app.mainWin.mainloop()
    