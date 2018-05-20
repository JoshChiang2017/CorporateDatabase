import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image,ImageTk


##########################################

#
# @ColumnNumber      Number of column of table will be created.
# @Title             List of string display on each top of column.
#
class Table (tk.Frame):
    def __init__(self, Parent, ColumnNumber, Title, AdvanceEntryCallback = None):

        if (ColumnNumber < 1) or (ColumnNumber < len (Title)):
            assert False
        
        tk.Frame.__init__(self, Parent, 
            borderwidth = 3,
            relief=tk.SUNKEN
            )
        
        #
        # Manage group of one row entry by Frame.
        # Collect all entry object into the array 'EntryArray'.
        # Collect all frame object into the array 'EntryRowArrray'.
        #
        # EntryArray start from [0][0] to [MaY][MaxX]
        # EntryRowArrray start from [0] to [MaxY]
        # Current input cursor will focus at [Y][X]
        #
        self.EntryArray = []
        self.EntryRowArrray = []
        self.X = 0
        self.Y = 0
        self.MaxX = -1 + ColumnNumber
        self.MaxY = -1
        self.ColumnNumber = ColumnNumber

        #
        # AdvanceEntryCallback allow parent provide advance callback of keyboard enter key.
        # Default is none.
        # Parent declare like Table.AdvanceEntryCallback = FunctionName
        #
        self.AdvanceEntryCallback = None
        
        #
        # In this frame, contain two sub frame and scrollbar.
        #
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 100)
        
        self.TitleFrame = tk.Frame(
            self,
            borderwidth = 1
            )
        self.DataCanvas = tk.Canvas(
            self
            )
        self.Scrollbar = tk.Scrollbar(
            self,
            command = self.DataCanvas.yview
            )
        
        self.TitleFrame.grid(row=0, column=0, sticky='news')
        self.DataCanvas.grid(row=1, column=0, sticky='news')
        self.Scrollbar.grid(row=0, column=1, rowspan = 2, sticky='news')
        
        #
        # Initialize title of table.
        #
        for Index in range(self.ColumnNumber):
            TitleString = tk.StringVar()
            TitleString.set(Title[Index])
            entry = tk.Entry (
                self.TitleFrame,
                borderwidth = 1,
                relief=tk.GROOVE,
                state = 'disabled',
                justify = 'center',
                textvariable = TitleString
                )
            entry.pack(side='left', fill='both', expand=True)
        
        #
        # Initialize data of table.
        #
        self.FrameInDataCanvas = tk.Frame(self.DataCanvas)
        self.WindowInCanvas = self.DataCanvas.create_window(
            (0, 0), window=self.FrameInDataCanvas, anchor="nw")
        self.DataCanvas.configure(yscrollcommand=self.Scrollbar.set)

        #
        # Callback event.
        #
        self.DataCanvas.bind ('<Configure>', self.CanvasResize)
        self.FrameInDataCanvas.bind ('<Configure>', self.ScrollbarCallback)

        #
        # Initialize one row assume that no data exist.
        #
        self.AddNewRow()
        self.EntryArray[self.Y][self.X].focus_set()
        self.EntryArray[self.Y][self.X].select_range(0, 'end')
        
    #
    # Use to make frame in the canvas can be resized with canvas.
    #
    def CanvasResize (self, event):
        self.DataCanvas.itemconfig (self.WindowInCanvas, width = event.width)

    #
    # Control canvaas with scrollbar.
    #
    def ScrollbarCallback (self, event):
        self.DataCanvas.configure(scrollregion=self.DataCanvas.bbox("all"))

    def AddNewRow (self):
        ItemX = []
        frame = tk.Frame (self.FrameInDataCanvas)
        frame.pack(side='top', fill='x', expand=True, padx=1)
        
        for Index in range(self.ColumnNumber):
            TitleString = tk.StringVar()
            TitleString.set('N/A')
            entry = tk.Entry (
                frame,
                borderwidth = 1,
                relief=tk.GROOVE,
                textvariable = TitleString
                )
            
            entry.bind ('<Return>', self.EnterKeyCallback)
            entry.bind ('<Button-1>', self.LeftMouseCallback)
            entry.bind ('<Tab>', self.TabKeyCallback)
            entry.bind ('<Shift-Tab>', self.ShiftTabKeyCallback)
            
            entry.pack(side='left', fill='x', expand=True)
            ItemX.append (entry)

        self.MaxY += 1
        self.EntryArray.append (ItemX)
        self.EntryRowArrray.append (frame)

    #
    # Callback when keyboard TAB key press.
    #
    def TabKeyCallback (self, event):
        #
        # There are two feature have not implemented.
        # 1. Action tab when cursor at last row and column.
        #    And use tab to focus fist enter after circle around.
        #    It will focus at wrong location with enter key when last row with valid data.
        # 2. Scrollbar are not linked with cursor.
        #
        if self.X < self.MaxX:
            self.X += 1
            
        else:
            if self.Y < self.MaxY:
                self.X = 0
                self.Y += 1                
        self.EntryArray[self.Y][self.X].focus_set()
        self.EntryArray[self.Y][self.X].select_range(0, 'end')
    
    #
    # Callback when keyboard shift-TAB key press.
    #
    def ShiftTabKeyCallback (self, event):
        if self.X > 0:
            self.X -= 1
            
        else:
            if self.Y > 0:
                self.X = self.MaxX
                self.Y -= 1
                
        self.EntryArray[self.Y][self.X].focus_set()
        self.EntryArray[self.Y][self.X].select_range(0, 'end')
    
    #
    # Callback when keyboard return key press.
    #
    def EnterKeyCallback (self, event):
        if self.AdvanceEntryCallback != None:
            self.AdvanceEntryCallback ()
        if (self.X ==self.MaxX) and (self.Y ==self.MaxY):
            #
            # If current cursor focus at last row and last column.
            # And if all of entry string of last row is 'N/A'.
            # Create a new row when keyboard enter key press.
            #
            DataWithinRow = False
            for i in range (self.MaxX + 1):
                if self.EntryArray[self.MaxY][i].get() != 'N/A':
                    DataWithinRow = True
                    break
            if DataWithinRow:
                self.AddNewRow()
        
        #
        # Callback of enter is similar with tab.
        #
        self.TabKeyCallback(None)

    #
    # Callback when mouse left button press.
    #
    def LeftMouseCallback (self, event):
        for i in range (self.MaxX + 1):
            for j in range (self.MaxY + 1):
                if self.EntryArray[j][i] == event.widget:
                    self.Y = j
                    self.X = i
                    self.EntryArray[self.Y][self.X].focus_set()
                    self.EntryArray[self.Y][self.X].select_range(0, 'end')
                    return   


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry ('600x400+200+100')
    
    Title = ('Name', 'Code', 'Price')
    table = Table (root, 3, Title)
    table.pack(side='top', fill='both', expand=True)
    root.focus_force()
    
    def handleReturn(event):
      print('return：event.widget is',event.widget)
      print('focus is：',root.focus_get())
      print('focus is：',root.focus_get().get())

    def aaa():
        print('aaa--------------')

    def bbb():
        print('bbb--------------')
        for i in range(1):
            for j in range(3):
                print (table.Item[i][j])
                print(root.focus_get())
                print('X=', i, ',Y=', j)
                if table.Item[i][j] == root.focus_get():
                    print ('    FIND')
                    break
                else:
                    print ('    NO')
        print('bbb--------------')

    def ddd(event):
        print (event.widget)
        
    def ccc():
        print('ccc--------------')
        table.AddNewRow()
        print('ccc--------------')
    
    for i in range(3):
        table.AddNewRow()

    
    #root.bind ('<Button-1>', ddd)
    table.AdvanceEntryCallback = aaa
        
    aa=tk.Button(root, command=aaa, text='delete')
    aa.pack()
    bb=tk.Button(root, command=bbb, text='get')
    bb.pack()
    cc=tk.Button(root, command=ccc, text='Add')
    cc.pack()
    
    root.mainloop


        
