import tkinter as tk
import CorporateDatabaseMain

#
# @Title                     List of string display on each top of column.
# @AdvanceEntryCallback      Advance entry callback.
#
class Table (tk.Frame):
    def __init__(self, Parent, Title, AdvanceEntryCallback = None):
        
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
        self.MaxX = -1 + len (Title)
        self.MaxY = -1
        self.ColumnNumber = len (Title)

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
        self.DataCanvas.bind ('<MouseWheel>', self.MouseWheelCallback)
        self.FrameInDataCanvas.bind ('<Configure>', self.ScrollbarCallback)

        #
        # Initialize one row assume that no data exist.
        #
        #self.AddNewRow()
        #self.EntryArray[self.Y][self.X].focus_set()
        #self.EntryArray[self.Y][self.X].select_range(0, 'end')
        
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

    def AddNewRow (self, Data=None):
        #
        # Data is list of each content of row.
        #
        if Data == None:
            Data = []
            for Index in range(self.ColumnNumber):
                Data.append('N/A')
        else:
            assert isinstance (Data, list)
            assert len (Data) == self.ColumnNumber
        
        ItemX = []
        frame = tk.Frame (self.FrameInDataCanvas)
        frame.pack(side='top', fill='x', expand=True, padx=1)
        
        for Index in range(self.ColumnNumber):
            TitleString = tk.StringVar()
            TitleString.set (Data[Index])
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
    # Foucs at last row.
    #
    def FocusAtLastRow (self):
        self.EntryArray[self.MaxY][0].focus_set()
        self.EntryArray[self.MaxY][0].select_range(0, 'end')
        

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

    def MouseWheelCallback (self):
         self.DataCanvas.yview_scroll(-1*(event.delta/120), "units")

#
# GUI of add data to database
#
class GuiAddToDatabase (tk.Frame):
    def __init__(self, Parent, Database):
        tk.Frame.__init__(self, Parent)
        
        Title = ('產品名稱', '產品代碼', '單價', '圖片(Y/N)')
        self.Database = Database
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 10)
        self.columnconfigure(0, weight = 1)
        
        self.OperationRegion = tk.Frame(
            self,
            borderwidth = 3
            )
        
        self.ObserveRegion = Table (self, Title)
            
        self.OperationRegion.grid(row=0, column=0, sticky='news', padx=1, pady=5)
        self.ObserveRegion.grid(row=1, column=0, sticky='news', padx=1, pady=5)
        
        for i in range (3):
          self.OperationRegion.rowconfigure(i, weight = 1)
        for i in range (8):
          self.OperationRegion.columnconfigure(i, weight = 1)
        
        #
        # Operation Region - Button
        #
        self.ExitButton = tk.Button (
            self.OperationRegion, 
            text = '儲存:',
            bg = '#AA88AA'
            )
        self.ExitButton.grid(row=0, column=7, sticky='news', padx=1, pady=5)
        
        self.SaveButton = tk.Button (
            self.OperationRegion, 
            text = '刪除已選取:',
            bg = '#AA88AA'
            )
        self.SaveButton.grid(row=1, column=7, sticky='news', padx=1, pady=5)

        self.ExitButton = tk.Button (
            self.OperationRegion, 
            text = '回主畫面:',
            bg = '#AA88AA'
            )
        self.ExitButton.grid(row=0, column=6, sticky='news', padx=1, pady=5)
        
        #
        # Operation Region - Entry
        #
        self.CompanyCodeText = tk.Label (
            self.OperationRegion, 
            text = '公司代碼:'
            )
        self.CompanyCodeText.grid(row=0, column=0, sticky='news', padx=1, pady=5)
        
        self.CompanyCodeEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            relief=tk.RIDGE
            )
        self.CompanyCodeEntry.grid(row=0, column=1, sticky='news', padx=1, pady=5)
        
        self.CompanyCodeWarningText = tk.Label (
            self.OperationRegion,
            width = 10,
            #text = 'Code Incorrect!!',
            foreground = '#FF0000',
            font= ("Times New Roman", 12, "bold")
            )
        self.CompanyCodeWarningText.grid(row=0, column=2, sticky='news')
        
        self.CompanyNameText = tk.Label (
            self.OperationRegion, 
            text = '公司名稱:'
            )
        self.CompanyNameText.grid(row=1, column=0, sticky='news', padx=1, pady=5)
        
        self.CompanyNameEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            relief=tk.RIDGE
            )
        self.CompanyNameEntry.grid(row=1, column=1, sticky='news', padx=1, pady=5)

        self.CompanyCodeEntry.focus_set()

        self.CompanyCodeEntry.bind ('<Return>', self.CompanyCodeCallback)
        self.CompanyNameEntry.bind ('<Return>', self.CompanyNameCallback)
        
    def CompanyCodeCallback (self, event):
        CompanyCode = self.CompanyCodeEntry.get()
        if CompanyCode != '':
            CompanyName = self.Database.IsCompanyCodeExist(CompanyCode)
            
            if CompanyName ==None:
                self.CompanyCodeWarningText.config (text = 'Code not Exist!!')
                self.CompanyCodeEntry.select_range(0, 'end')
                return
            else:
                self.CompanyCodeWarningText.config (text = '')
                self.CompanyNameEntry.delete (0, 'end')
                self.CompanyNameEntry.insert (0, CompanyName)
                
        self.CompanyNameEntry.focus_set()
        self.CompanyNameEntry.select_range(0, 'end')
        
    def CompanyNameCallback (self, event):
        CompanyName = self.CompanyNameEntry.get()
        if CompanyName != '':
            CompanyData = self.Database.FindCompany (CompanyName)

            if CompanyData == None:
                print('No')
            else:
                print('Yes')
                self.CompanyCodeEntry.config (state = 'readonly')
                self.CompanyNameEntry.config (state = 'readonly')
                self.AddDataToTable (CompanyData)

    def AddDataToTable (self, CompanyData):

        CurrentProduct = CompanyData.Header.Name.GetNextNode ()

        while CurrentProduct != None:
            Data = []

            Data.append (CurrentProduct.Name.GetData())
            Data.append (CurrentProduct.Code.GetData())
            Data.append (CurrentProduct.Price.GetData())

            if (CurrentProduct.Image == None):
                Data.append ('N')
            else:
                Data.append ('Y')

            CurrentProduct = CurrentProduct.Name.GetNextNode()
            self.ObserveRegion.AddNewRow(Data)

        self.ObserveRegion.AddNewRow()
        self.ObserveRegion.FocusAtLastRow ()
            
        

    

#
# Simple test of this module.
#
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry ('800x600+10+10')
    Database = CorporateDatabaseMain.LoadDatabase()
    a = GuiAddToDatabase(root, Database)
    a.pack (side = 'top', fill = 'both', expand = True)

    b=tk.Button (
            root,
            text = '儲存:',
            bg = '#AA88AA'
            ).pack()
    
    root.mainloop()
