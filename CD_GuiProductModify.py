import tkinter as tk
import CorporateDatabaseMain
import logging
import threading
import tkinter.filedialog as Dialog
import CD_LinkingList as link
import CD_FileAccess
import CD_LogHistotry as logger
from tkinter import messagebox
import CD_Configuration as CONF

class PopupMenu(tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent, bg = '#123456')
        self.listBox = tk.Listbox(self, height=1)
        self.button = tk.Button(self, text='v', command=self.Triggle)
        self.HideList = True
        
        for i in range(10):
            self.listBox.insert(i, 'Item%d'%i)
            
        self.listBox.grid(row=1, column=1, sticky='news')
        self.button.grid(row=1, column=2, sticky='news')
        
    def Triggle(self):
        self.HideList ^= 1
        self.listBox.config (height=[self.listBox.size(), 1][self.HideList])

#
# @Title                     List of string display on each top of column.
# @ShowIndex                 Display row index.
#
class Table (tk.Frame):
    def __init__(self, Parent, Title, ShowRowIndex = False):
        
        tk.Frame.__init__(self, Parent, 
            borderwidth = 3,
            relief=tk.SUNKEN
            )
        
        #
        # Manage group of one row entry by Frame.
        # Collect all entry object into the array 'EntryArray'.
        #
        # EntryArray start from [0][0] to [MaxY][MaxX]
        #   In each cell
        #       [0] : object of entry
        #       [1] : record entry status
        #           If self.AddNewRow(None), status is 'new'.
        #           If self.AddNewRow(Data), status is 'exist'.
        #           The other two status is 'modify' and 'remove'.
        #       [2] : This space is used to save default entry text.
        #           It's usually used by status 'exist' of entry.
        #           Used to check whether the entry has been modified.
        #
        #   EX:
        #       Object of (1,2) : [2][1][self.DefineObject]
        #       Status of (1,2) : [2][1][self.DefineStatus]
        #
        
        self.DefineObject      = 0
        self.DefineStatus      = 1
        self.DefineDefaultText = 2
        
        self.EntryArray = []
        self.IndexArray = []
        self.X = 0
        self.Y = 0
        self.MaxX = -1 + len (Title)
        self.MaxY = -1
        self.ColumnNumber = len (Title)

        self.ShowRowIndex = ShowRowIndex
        
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
        
        self.TitleFrame.grid(row=0, column=0, sticky='news', padx=1)
        self.DataCanvas.grid(row=1, column=0, sticky='news')
        self.Scrollbar.grid(row=0, column=1, rowspan = 2, sticky='news')
        
        #
        # Initialize title of table.
        #
        if self.ShowRowIndex == True:
            entry = tk.Label (
                self.TitleFrame,
                borderwidth = 1,
                relief=tk.GROOVE,
                text = 'NO.',
                font = CONF.GLOBAL_CONFIG_FONT,
                width = 5
                )
            entry.pack(side='left', fill='both')
            
        for Index in range(self.ColumnNumber):
            TitleString = tk.StringVar()
            TitleString.set(Title[Index])
            entry = tk.Entry (
                self.TitleFrame,
                borderwidth = 1,
                relief=tk.GROOVE,
                state = 'disabled',
                justify = 'center',
                textvariable = TitleString,
                font = CONF.GLOBAL_CONFIG_FONT,
                disabledforeground = '#000000'
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
        self.DataCanvas.bind ('<Configure>', lambda event: self.DataCanvas.itemconfig (self.WindowInCanvas, width = event.width))
        self.FrameInDataCanvas.bind ('<Configure>', lambda event: self.DataCanvas.configure(scrollregion=self.DataCanvas.bbox("all")))
        
        self.bind_all ('<MouseWheel>', lambda event: self.DataCanvas.yview_scroll(-1 * (event.delta//30), "units"))
        self.bind_all("<Next>",  lambda event: self.DataCanvas.yview_scroll(1, "pages"))
        self.bind_all("<Prior>",  lambda event: self.DataCanvas.yview_scroll(-1, "pages"))
            
        self.bind_all ('<Tab>', self.NextEntryCallback)
        self.bind_all ('<Down>', self.NextEntryCallback)
        self.bind_all ('<Shift-Tab>', self.PreEntryCallback)
        self.bind_all ('<Up>', self.PreEntryCallback)

        #
        # Initialize one row assume that no data exist.
        #
        #self.AddNewRow()
        #self.EntryArray[self.Y][self.X][self.DefineObject].focus_set()
        #self.EntryArray[self.Y][self.X][self.DefineObject].select_range(0, 'end')
        

    def AddNewRow (self, Data=None):
        #
        # Data is list of each content of row.
        #
        if Data == None:
            Data = []
            for Index in range(self.ColumnNumber):
                Data.append('N/A')
            Status = 'new'
            Background = '#FFFFFF'
            
        else:
            assert isinstance (Data, list)
            assert len (Data) == self.ColumnNumber
            Status = 'exist'
            Background = '#DDFFDD'
        
        self.MaxY += 1
        
        ItemX = []
        frame = tk.Frame (self.FrameInDataCanvas)
        frame.pack(side='top', fill='x', expand=True, padx=1)

        #
        # Display row index
        #
        if self.ShowRowIndex == True:
            TitleString = tk.StringVar()
            TitleString.set (self.MaxY)
            entry = tk.Entry (
                frame,
                borderwidth = 1,
                relief=tk.GROOVE,
                state = 'disabled',
                justify = 'center',
                textvariable = TitleString,
                font = CONF.GLOBAL_CONFIG_FONT,
                disabledforeground = '#000000',
                width = 5
                )
            entry.pack(side='left', fill='x')
            entry.bind ('<Button-1>', self.IndexCallback)
            self.IndexArray.append (entry)
        
        for Index in range(self.ColumnNumber):
            TitleString = tk.StringVar()
            TitleString.set (Data[Index])
            entry = tk.Entry (
                frame,
                borderwidth = 1,
                relief=tk.GROOVE,
                textvariable = TitleString,
                font = CONF.GLOBAL_CONFIG_FONT,
                bg = Background
                )
            entry.pack(side='left', fill='x', expand=True)
            
            #
            # Record default value.
            #
            ItemX.append ([entry, Status, Data[Index]])
            
            entry.bind ('<Return>', self.EnterKeyCallback)
            entry.bind ('<Button-1>', self.LeftMouseCallback)

        self.EntryArray.append (ItemX)
        self.DataCanvas.yview_moveto (1)

    #
    # Callback of go to next entry.
    #
    def NextEntryCallback (self, event):
        if self.X < self.MaxX:
            x = self.X +1
            y = self.Y
            
        else:
            if self.Y < self.MaxY:
                x = 0
                y = self.Y + 1
            else :
                x = self.MaxX
                y = self.MaxY

        self.FocusAtNewEntry (x, y)
    
    #
    # Callback of go to previous entry.
    #
    def PreEntryCallback (self, event):
        if self.X > 0:
            x = self.X -1
            y = self.Y
            
        else:
            if self.Y > 0:
                x = self.MaxX
                y = self.Y - 1
            else :
                x = 0
                y = 0
                
        self.FocusAtNewEntry (x, y)
    
    #
    # Callback when keyboard return key press.
    #
    def EnterKeyCallback (self, event):
        if (self.X ==self.MaxX) and (self.Y ==self.MaxY):
            #
            # If current cursor focus at last row and last column.
            # And if all of entry string of last row is 'N/A'.
            # Create a new row when keyboard enter key press.
            #
            DataWithinRow = False
            for i in range (self.MaxX + 1):
                if self.EntryTextGet (i, self.MaxY) != 'N/A':
                    DataWithinRow = True
                    break
            if DataWithinRow:
                self.AddNewRow()
            
        self.NextEntryCallback(None)

    #
    # Callback when mouse left button press.
    #
    def LeftMouseCallback (self, event):
        for i in range (self.MaxX + 1):
            for j in range (self.MaxY + 1):
                if self.EntryObjectGet(i, j) == event.widget:
                    self.FocusAtNewEntry (i, j)

    def IndexCallback (self, event):
        y = int(event.widget.get())

        #
        # Status : new. Remove whole row.
        #
        if self.EntryStatusGet(0, y) == 'new':
            #
            # Remove by remove parent of each object in the row.
            # Last row should not be removable. Avoid no 'new' row occurrence.
            #
            if y != self.MaxY:
                self.RemoveRow (y)
        
        #
        # Status : remove -> exist
        #
        elif self.EntryStatusGet(0, y) == 'remove':
            for x in range(self.ColumnNumber):
                self.EntryStatusSet(x, y, 'exist')
                self.EntryObjectGet(x, y).config (bg = '#DDFFDD')

                self.EntryTextSet(x, y, self.EntryDefaultGet(x, y))

        #
        # Status : exist/modify -> remove
        # Because modify only transfer from exist.
        #
        else:
            for x in range(self.ColumnNumber):
                self.EntryStatusSet(x, y, 'remove')
                self.EntryObjectGet(x, y).config (bg = '#FFCCCC')

    #
    # If current entry text has been modify, and if current entry status is 
    # 'exist', configure status to 'modify'.
    # Then focus at new entry
    #
    def FocusAtNewEntry (self, x, y):
        #
        # If no row in table, do nothing.
        #
        if self.MaxY != -1:
            
            #
            # 1. Specific process for specific column.
            #
            #################################
            # Particular table feature start#
            #################################

            #
            # Picture column
            #
            if self.X == 3:
                self.ImageEntryInternal()

            ################################
            # Particular table feature end #
            ################################
            #
            # 2. Check content of entry is modified or not.
            #
            if (self.EntryStatusGet(self.X, self.Y) == 'exist') or (self.EntryStatusGet(self.X, self.Y) == 'modify'):
                if self.EntryDefaultGet(self.X, self.Y) != self.EntryTextGet (self.X, self.Y):
                    self.EntryStatusSet (self.X, self.Y, 'modify')
                    self.EntryObjectGet(self.X, self.Y).config (bg = '#FFFFBB')
                else:
                    self.EntryStatusSet (self.X, self.Y, 'exist')
                    self.EntryObjectGet(self.X, self.Y).config (bg = '#DDFFDD')

            if self.EntryStatusGet(self.X, self.Y) == 'new':
                self.EntryObjectGet(self.X, self.Y).config (bg = '#FFFFFF')
            
            #
            # 3. Focus at new entry
            #
            self.Y = y
            self.X = x
            self.EntryObjectGet(self.X, self.Y).focus_set()
            self.EntryObjectGet(self.X, self.Y).select_range(0, 'end')
            

    def RemoveRow (self, y):
        #
        # Remove by remove parent of each object in the row.
        #
        self.FocusAtNewEntry (0, y)
        parent = self.EntryObjectGet(0, y).winfo_parent()
        parentObject = self.EntryObjectGet(0, y)._nametowidget(parent)
        parentObject.destroy()
        
        #
        # Remove recode in array.
        #
        self.EntryArray.pop(y)
        self.IndexArray.pop(y)
        self.MaxY -= 1
        
        #
        # Modify row index of each row below.
        #
        for i in range (y, self.MaxY + 1):
            self.IndexArray[i].config (state = 'normal')
            self.IndexArray[i].delete (0, 'end')
            self.IndexArray[i].insert (0, i)
            self.IndexArray[i].config (state = 'disable')
        self.FocusAtNewEntry (0, y)
        
    def FocusAtLast (self):
        self.FocusAtNewEntry (self.MaxX, self.MaxY)
        
    def EntryObjectGet (self, x, y):
        return self.EntryArray[y][x][self.DefineObject]

    def EntryTextSet (self, x, y, NewString):
        self.EntryObjectGet(x, y).delete(0, 'end')
        self.EntryObjectGet(x, y).insert(0, NewString)
    def EntryTextGet (self, x, y):
        return self.EntryObjectGet(x, y).get()
    
    def EntryStatusSet (self, x, y, NewStatus):
        self.EntryArray[y][x][self.DefineStatus] = NewStatus
    def EntryStatusGet (self, x, y):
        return self.EntryArray[y][x][self.DefineStatus]

    def EntryDefaultGet (self, x, y):
        return self.EntryArray[y][x][self.DefineDefaultText]

    def GetRowNumber(self):
        return (self.MaxY + 1)
    def GetMaxRow(self):
        return (self.MaxY)
    def GetColumnNumber(self):
        return (self.MaxX + 1)
    def GetMaxColumn(self):
        return (self.MaxX)
        
    #
    # Lock table. Transfer all entrys of table to readonly.
    #
    def LockTable(self):
        for x in range (self.GetColumnNumber()):
            for y in range (self.GetRowNumber()):
                self.EntryObjectGet (x, y).config (state = 'readonly')
                
    #
    # Remove empty and cr/lf before and after the text of each entry.
    #
    def RemoveEmpty(self):
        for x in range (self.GetColumnNumber()):
            for y in range (self.GetRowNumber()):
                newText = self.EntryTextGet (x, y).strip()
                self.EntryTextSet (x, y, newText)

    #################################
    # Particular table feature start#
    #################################
    
    #
    # Do not consider which entry of table should call this function.
    # It is control by FocusAtNewEntry()
    #
    def ImageEntryInternal(self):
        if (self.EntryTextGet(self.X, self.Y) == 'Y') or (self.EntryTextGet(self.X, self.Y) == 'y'):
            if ((self.EntryStatusGet(self.X, self.Y) == 'new') or 
                self.EntryStatusGet(self.X, self.Y) == 'modify' or
                ((self.EntryStatusGet(self.X, self.Y) == 'exist') and (self.EntryDefaultGet(self.X, self.Y) == 'N'))
                ):
                
                PicPath = Dialog.askopenfilename ()
                if PicPath=='':
                    self.EntryTextSet (self.X, self.Y, 'N')
                else:
                    self.EntryTextSet (self.X, self.Y, '@'+PicPath)
                    
            else:
                self.EntryTextSet (self.X, self.Y, 'Y')

        elif self.EntryTextGet(self.X, self.Y) == '' or self.EntryTextGet(self.X, self.Y)[0] !='@':
            #
            # If string start with '@', it is valid.
            #
            self.EntryTextSet (self.X, self.Y, 'N')
    
    ################################
    # Particular table feature end #
    ################################

#
# GUI of add data to database
#
class GuiProductModify (tk.Frame):
    def __init__(self, Parent, Database):
        tk.Frame.__init__(self, Parent)
        
        self.title = ('產品名稱', '產品代碼', '單價', '圖片(Y/N)', '備註')
        self.Database = Database
        self.root = Parent
        self.CompanyName =None
        self.companyData = None
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 10)
        self.columnconfigure(0, weight = 1)
        
        self.OperationRegion = tk.Frame(
            self,
            borderwidth = 3
            )
        
        self.table = Table (self, self.title, ShowRowIndex = True)
            
        self.OperationRegion.grid(row=0, column=0, sticky='news', padx=1, pady=5)
        self.table.grid(row=1, column=0, sticky='news', padx=1, pady=5)
        
        for i in range (3):
          self.OperationRegion.rowconfigure(i, weight = 1)
        for i in range (8):
          self.OperationRegion.columnconfigure(i, weight = 1)
        
        #
        # Operation Region - Button
        #
        self.SaveButton = tk.Button (
            self.OperationRegion, 
            text = '儲存(S):',
            bg = '#C7C1D4',
            font = CONF.GLOBAL_CONFIG_FONT,
            command = self.ButtonSaveCallback
            )

        self.ExitButton = tk.Button (
            self.OperationRegion, 
            text = '放棄變更(Q):',
            bg = '#C7C1D4',
            font = CONF.GLOBAL_CONFIG_FONT,
            command = self.ButtonBackCallback
            )
        
        #
        # Operation Region - Entry
        #
        self.CompanyCodeText = tk.Label (
            self.OperationRegion, 
            font = CONF.GLOBAL_CONFIG_FONT,
            text = '公司代碼:'
            )
        
        self.CompanyCodeEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            font = CONF.GLOBAL_CONFIG_FONT,
            relief=tk.RIDGE
            )
        
        self.CompanyCodeWarningText = tk.Label (
            self.OperationRegion,
            width = 10,
            foreground = '#FF0000',
            font = CONF.GLOBAL_CONFIG_FONT
            )
        
        self.CompanyNameText = tk.Label (
            self.OperationRegion, 
            font = CONF.GLOBAL_CONFIG_FONT,
            text = '公司名稱:'
            )
        
        self.CompanyNameEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            font = CONF.GLOBAL_CONFIG_FONT,
            relief=tk.RIDGE
            )
            
        self.CompanyNameWarningText = tk.Label (
            self.OperationRegion,
            width = 20,
            foreground = '#FF0000',
            font = CONF.GLOBAL_CONFIG_FONT
            )
            
        self.SaveButton.grid              (row=0, column=7, sticky='news', padx=1, pady=5)
        self.ExitButton.grid              (row=1, column=7, sticky='news', padx=1, pady=5)
        self.CompanyCodeText.grid         (row=0, column=0, sticky='news', padx=1, pady=5)
        self.CompanyCodeEntry.grid        (row=0, column=1, sticky='news', padx=1, pady=5)
        self.CompanyCodeWarningText.grid  (row=0, column=2, sticky='news')
        self.CompanyNameText.grid         (row=1, column=0, sticky='news', padx=1, pady=5)
        self.CompanyNameEntry.grid        (row=1, column=1, sticky='news', padx=1, pady=5)
        self.CompanyNameWarningText.grid  (row=1, column=2, sticky='news')
        
        self.CompanyCodeEntry.focus_set()

        self.CompanyCodeEntry.bind ('<Return>', self.CompanyCodeCallback)
        self.CompanyNameEntry.bind ('<Return>', self.CompanyNameCallback)
        self.bind_all ('<Control-Key-Q>', lambda event: self.ButtonBackCallback())
        self.bind_all ('<Control-Key-q>', lambda event: self.ButtonBackCallback())
        
        self.bind_all ('<Control-Key-S>', lambda event: self.ButtonSaveCallback())
        self.bind_all ('<Control-Key-s>', lambda event: self.ButtonSaveCallback())
        
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
            company = self.Database.FindCompany (CompanyName)
            companyCode = company.Code.GetData()
            CompanyData = company.ProductListHeader

            if CompanyData == None:
                self.CompanyNameWarningText.config (text = 'Name not Exist!!')
                self.CompanyNameEntry.select_range(0, 'end')
                return
            else:
                self.CompanyCodeEntry.delete (0, 'end')
                self.CompanyCodeEntry.insert (0, companyCode)
                
                self.CompanyCodeWarningText.config (text = '')
                self.CompanyNameWarningText.config (text = '')
                
                self.CompanyCodeEntry.config (state = 'readonly')
                self.CompanyNameEntry.config (state = 'readonly')
                self.CompanyName = CompanyName
                self.OneCompanyToTable (CompanyData)

    def OneCompanyToTable (self, companyData):

        self.companyData = companyData
        CurrentProduct = companyData.Header.Name.GetNextNode ()

        while CurrentProduct != None:
            Data = []
            
            Data.append (CurrentProduct.Name.GetData())
            Data.append (CurrentProduct.Code.GetData())
            Data.append (CurrentProduct.Price.GetData())

            if (CurrentProduct.Image == None):
                Data.append ('N')
            else:
                Data.append ('Y')

            Data.append (CurrentProduct.comment)

            CurrentProduct = CurrentProduct.Name.GetNextNode()
            self.table.AddNewRow(Data)

        #
        # Add empty data row at last.
        # And focus at last row first column.
        #
        self.table.AddNewRow()
        self.table.FocusAtNewEntry (0, self.table.GetMaxRow())

    def DataValidCheck(self):
        logging.info ('DataValidCheck()')

        msg = 'Invalid:\n'
        def LogWarning(rowNumber, message):
            nonlocal msg
            msgFormat = 'Row(%d). ' %rowNumber + message
            logging.info (msgFormat)
            msg += msgFormat + '\n'

        nameValid = True
        codeValid = True
        priceValid = True
        lastRowValid = True
        rowNumber = self.table.GetMaxRow()# Don't compare last row.
        
        for currentRow in range (rowNumber):
            #
            # Name column (0)
            # Code column (1)
            # Price column (2)
            #
            name = self.table.EntryTextGet(0, currentRow)
            code = self.table.EntryTextGet(1, currentRow)
            price = self.table.EntryTextGet(2, currentRow)
            
            #
            # Should not have two same Product name, empty is illegal.
            #
            if (name == '') or (name == 'N/A'):
                self.table.EntryObjectGet(0, currentRow).config (bg = '#FF3333')
                nameValid = False
                LogWarning (currentRow, 'Name invalid (empty).')

            else:
                for compareRow in range (currentRow+1, rowNumber):
                    if name == self.table.EntryTextGet(0, compareRow):
                        self.table.EntryObjectGet(0, currentRow).config (bg = '#FF3333')
                        self.table.EntryObjectGet(0, compareRow).config (bg = '#FF3333')
                        nameValid = False
                        LogWarning (currentRow, 'Name invalid (repeat).')
                        LogWarning (compareRow, 'Code invalid (repeat).')

            #
            # Should not have two same Code name, empty is legal.
            #
            if code == 'N/A':
                self.table.EntryObjectGet(1, currentRow).config (bg = '#FF3333')
                codeValid = False
                LogWarning (currentRow, 'Code invalid (empty).')
            
            elif code != '':
                for compareRow in range (currentRow+1, rowNumber):
                    if code == self.table.EntryTextGet (1, compareRow):
                        self.table.EntryObjectGet(1, currentRow).config (bg = '#FF3333')
                        self.table.EntryObjectGet(1, compareRow).config (bg = '#FF3333')
                        codeValid = False
                        LogWarning (currentRow, 'Code invalid (repeat).')
                        LogWarning (compareRow, 'Code invalid (repeat).')
            
            #
            # Price should be number and not zero. 
            #
            try:
                float (price)
                self.table.EntryTextSet(2, currentRow, price.strip())
            except:
                self.table.EntryObjectGet(2, currentRow).config (bg = '#FF3333')
                priceValid = False
                LogWarning (currentRow, 'Price invalid.')

        #
        # Last row should be all 'N/A'
        #
        for column in range (len(self.title)):
            if self.table.EntryTextGet(column, rowNumber) != 'N/A':
                self.table.EntryObjectGet(column, rowNumber).config (bg = '#FF3333')
                lastRowValid = False
                LogWarning (rowNumber, 'Lase row should be N/A')

        if nameValid and codeValid and priceValid and lastRowValid:
            return True
        else:
            messagebox.showinfo('WARNING', msg)
            return False

    def ButtonBackCallback(self):
        abort = messagebox.askokcancel('WARNING', '確定放棄此次編輯?')
            
        if abort:
            self.Exit()
    
    def ButtonSaveCallback (self):
        #
        # Avoid user input last data without pressing enter key.
        # It is possible to lose last data.
        #
        self.table.FocusAtLast()
        
        #
        # 1.Check data of table valid.
        #
        if self.DataValidCheck() == True:
            #
            # 2. Show message make sure to modify database.
            #
            addNumber = 0
            removeNumber = 0
            modifyNumber = 0

            for y in range (self.table.GetMaxRow()):
                if self.table.EntryStatusGet (0, y) == 'new':
                    addNumber += 1
                elif self.table.EntryStatusGet (0, y) == 'remove':
                    removeNumber += 1
                else:
                    for x in range (self.table.GetColumnNumber()):
                        if self.table.EntryStatusGet (x, y) == 'modify':
                            modifyNumber += 1

            msg = '確定儲存此次編輯?\n\n' +\
                '新增 : %d\n' %addNumber +\
                '移除 : %d\n' %removeNumber +\
                '修改 : %d\n' %modifyNumber
                
            save = messagebox.askokcancel('WARNING', msg)

            if save:
                #
                # 3.Save table to database.
                #
                logging.info ('Start save table to database')
                self.table.RemoveEmpty()
                self.table.LockTable()
                
                loadingImage = CorporateDatabaseMain.LoadingImage(self.root)
                loadingImage.Start()
                
                self.InternalSaveCallback()

                #
                # 4. Save database to hard drive
                #
                self.after (0, self.InternalExitCallback, loadingImage)

    def InternalExitCallback(self, loadingImage):
        if (threading.active_count() > 1):
            self.after (400, self.InternalExitCallback, loadingImage)
        
        else:
            CD_FileAccess.ExportProduct(self.CompanyName, self.companyData)
            loadingImage.End()
            self.Exit()
            logging.info ('Modify product file success!\n')
            
    def InternalSaveCallback(self):
        log = logger.HistoryLog(self.CompanyName)
        for y in range (self.table.GetMaxRow()):
            if self.table.EntryStatusGet (0, y) == 'new':
                node = self.TransferRowToNode(y)
                name = node.GetName()
                picPath = self.table.EntryTextGet (3, y)
                
                #
                # Valid path begin with '@'
                #
                if picPath[0] == '@':
                    picPath = picPath.lstrip ('@')
                    
                    #
                    # Add picture.
                    #
                    tkImage = CD_FileAccess.ProductImageModify (self.CompanyName, oriName=name, picPath=picPath)
                    node.Image = tkImage
                
                self.companyData.AddNode(node)
                log.SetAddFile (node)
                
            elif self.table.EntryStatusGet (0, y) == 'remove':
                node = self.TransferRowDefaultToNode(y)
                name = node.GetName()
                
                self.companyData.RemoveNode (name)
                log.SetRemoveFile (node)
                
                #
                # Remove picture.
                #
                CD_FileAccess.ProductImageModify (self.CompanyName, oriName=name)
                
            else:
                modifyFlag = False
                for x in range (self.table.GetColumnNumber()):
                    if self.table.EntryStatusGet (x, y) == 'modify':
                        modifyFlag = True
                        break
                        
                if modifyFlag == True:
                    preNode = self.TransferRowDefaultToNode(y)
                    postNode = self.TransferRowToNode(y)
                    name = preNode.GetName()
                    modName = postNode.GetName()
                    
                    #
                    # Rename picture if modify product name.
                    #
                    if self.table.EntryStatusGet (0, y) == 'modify':
                        CD_FileAccess.ProductImageModify (self.CompanyName, oriName=name, modName=modName)
                    
                    #
                    # Modify picture of product.
                    #
                    if self.table.EntryStatusGet (3, y) == 'modify':
                        picPath = self.table.EntryTextGet (3, y)
                        
                        #
                        # Remove
                        #
                        if picPath[0] == 'N' or picPath[0] == 'n':
                          tkImage = CD_FileAccess.ProductImageModify (self.CompanyName, oriName=name)
                          postNode.Image = None
                        
                        #
                        # Modify
                        #
                        elif picPath[0] == '@':
                            picPath = picPath.lstrip ('@')
                            tkImage = CD_FileAccess.ProductImageModify (self.CompanyName, oriName=name, picPath=picPath)
                            postNode.Image = tkImage
                        
                    self.companyData.ModifyNode (name, postNode)
                    log.SetModifyFile (preNode, postNode)
                        
        log.AddLog()
    
    #
    # Transfer specific node into class ProductNode
    #
    def TransferRowToNode(self, row):
        node = link.ProductNode()

        node.Name.SetData (self.table.EntryTextGet (0, row))
        node.Code.SetData (self.table.EntryTextGet (1, row))
        node.Price.SetData (self.table.EntryTextGet (2, row))
        node.Image = None
        node.comment = self.table.EntryTextGet (4, row)

        return node
    
    def TransferRowDefaultToNode(self, row):
        node = link.ProductNode()

        node.Name.SetData (self.table.EntryDefaultGet (0, row))
        node.Code.SetData (self.table.EntryDefaultGet (1, row))
        node.Price.SetData (self.table.EntryDefaultGet (2, row))
        node.comment = self.table.EntryDefaultGet (4, row)

        return node

    def Exit(self):
        self.destroy()
        self.unbind_all ('<MouseWheel>')
        self.unbind_all ('<Next>')
        self.unbind_all ('<Prior>')
        self.unbind_all ('<Tab>')
        self.unbind_all ('<Down>')
        self.unbind_all ('<Shift-Tab>')
        self.unbind_all ('<Up>')
        self.unbind_all ('<Control-Key-Q>')
        self.unbind_all ('<Control-Key-q>')
        self.unbind_all ('<Control-Key-S>')
        self.unbind_all ('<Control-Key-s>')
        

#
# Simple test of this module.
#
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    root = tk.Tk()
    root.geometry ('800x600+100+100')
    Database = CD_FileAccess.LoadDatabase()
    a = GuiProductModify(root, Database)
    a.pack (side = 'top', fill = 'both', expand = True)

    for i in range (0):
        a.table.AddNewRow()


    b=tk.Button (
            root,
            text = '儲存:',
            bg = '#AA88AA'
            ).pack()
    
    root.mainloop()
