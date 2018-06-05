import tkinter as tk
import CorporateDatabaseMain
import logging
import tkinter.filedialog as Dialog
import CD_LinkingList as link
import CD_FileAccess
import CD_LogHistotry as logger
from tkinter import messagebox

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
        # EntryArray start from [0][0] to [MaY][MaxX]
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
                disabledforeground = '#000000',
                width = 5
                )
            entry.pack(side='left', fill='x')
            entry.bind ('<Button-1>', self.IndexCallback)
        
        for Index in range(self.ColumnNumber):
            TitleString = tk.StringVar()
            TitleString.set (Data[Index])
            entry = tk.Entry (
                frame,
                borderwidth = 1,
                relief=tk.GROOVE,
                textvariable = TitleString,
                bg = Background
                )
            entry.pack(side='left', fill='x', expand=True)
            
            ItemX.append ([entry, Status, Data[Index]])
            
            entry.bind ('<Return>', self.EnterKeyCallback)
            entry.bind ('<Button-1>', self.LeftMouseCallback)

        self.EntryArray.append (ItemX)

        #
        # Move and focus at last row.
        #
        self.X = 0
        self.Y = self.MaxY
        self.EntryObjectGet(self.X, self.Y).focus_set()
        self.EntryObjectGet(self.X, self.Y).select_range(0, 'end')
        self.DataCanvas.update_idletasks()
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

        else:
            #################################
            # Particular table feature start#
            #################################


            ################################
            # Particular table feature end #
            ################################
            
            #
            # Callback of enter is similar with tab.
            #
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
                parent = self.EntryObjectGet(0, y).winfo_parent()
                parentObject = self.EntryObjectGet(0, y)._nametowidget(parent)
                parentObject.destroy()

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
        else self.EntryStatusGet(0, y) != 'new':
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
            if (self.EntryStatusGet(self.X, self.Y) == 'exist') or (self.EntryStatusGet(self.X, self.Y) == 'modify'):
                if self.EntryDefaultGet(self.X, self.Y) != self.EntryTextGet (self.X, self.Y):
                    self.EntryStatusSet (self.X, self.Y, 'modify')
                    self.EntryObjectGet(self.X, self.Y).config (bg = '#FFFFBB')
                else:
                    self.EntryStatusSet (self.X, self.Y, 'exist')
                    self.EntryObjectGet(self.X, self.Y).config (bg = '#DDFFDD')

            if self.EntryStatusGet(self.X, self.Y) == 'new':
                self.EntryObjectGet(self.X, self.Y).config (bg = '#FFFFFF')
            
            self.Y = y
            self.X = x
            self.EntryObjectGet(self.X, self.Y).focus_set()
            self.EntryObjectGet(self.X, self.Y).select_range(0, 'end')

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
# GUI of add data to database
#
class GuiCompanyModify (tk.Frame):
    def __init__(self, Parent, Database):
        tk.Frame.__init__(self, Parent)
        
        self.title = ('公司名稱', '公司代號')
        self.database = Database
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 100)
        self.columnconfigure(0, weight = 1)
        
        self.controlFrame = tk.Frame(
            self,
            borderwidth = 3
            )
        
        self.table = Table (self, self.title, ShowRowIndex = True)
            
        self.controlFrame.grid(row=0, column=0, sticky='news')
        self.table.grid(row=1, column=0, sticky='news')
        
        #
        # Operation Region - Button
        #
        self.SaveButton = tk.Button (
            self.controlFrame, 
            text = '儲存(S):',
            bg = '#AA88AA',
            width=20,
            command = self.ButtonSaveCallback
            )
        self.SaveButton.pack (side = 'left', fill = 'y', padx=5)
        
        self.ExitButton = tk.Button (
            self.controlFrame, 
            text = '放棄變更(Q):',
            bg = '#AA88AA',
            width=20,
            command = self.ButtonBackCallback
            )
        self.ExitButton.pack (side = 'left', fill = 'y', padx=5)
        
        self.bind_all ('<Control-Key-S>', lambda event: self.ButtonSaveCallback())
        self.bind_all ('<Control-Key-s>', lambda event: self.ButtonSaveCallback())
        self.bind_all ('<Control-Key-Q>', lambda event: self.ButtonBackCallback())
        self.bind_all ('<Control-Key-q>', lambda event: self.ButtonBackCallback())
        
        self.TableInit()

    def TableInit (self):

        periCompany = self.database.GetFirst()
        while periCompany != None:
            data = []
            
            data.append (periCompany.Name.GetData())
            data.append (periCompany.Code.GetData())
            
            periCompany = periCompany.GetNext()
            self.table.AddNewRow (data)

        self.table.AddNewRow()

    def DataValidCheck(self):
        logging.info ('DataValidCheck() Start...')

        msg = 'Invalid:\n'
        def LogWarning(rowNumber, message):
            nonlocal msg
            msgFormat = 'Row(%d). ' %rowNumber + message
            logging.info (msgFormat)
            msg += msgFormat + '\n'

        nameValid = True
        codeValid = True
        lastRowValid = True
        rowNumber = self.table.GetMaxRow()# Don't compare last row.
        
        for currentRow in range (rowNumber):
            #
            # Name column (0)
            # Code column (1)
            #
            name = self.table.EntryTextGet(0, currentRow)
            code = self.table.EntryTextGet(1, currentRow)
            
            #
            # Should not have two same Product name, empty is illegal.
            # Company name with '/' is illegal. 
            # Because it cause error when create a new folder with path.
            #
            if (name == '') or (name == 'N/A'):
                self.table.EntryObjectGet(0, currentRow).config (bg = '#FF3333')
                nameValid = False
                LogWarning (currentRow, 'Name invalid (empty).')
                
            elif name.find('/') != -1:
                self.table.EntryObjectGet(0, currentRow).config (bg = '#FF3333')
                nameValid = False
                LogWarning (currentRow, 'Name invalid (should not contain \'/\' ).')

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
        # Last row should be all 'N/A'
        #
        for column in range (len(self.title)):
            if self.table.EntryTextGet(column, rowNumber) != 'N/A':
                self.table.EntryObjectGet(column, rowNumber).config (bg = '#FF3333')
                lastRowValid = False
                LogWarning (rowNumber, 'Lase row should be N/A')

        logging.info ('DataValidCheck() End...\n')

        if nameValid and codeValid and lastRowValid:
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
                # 3.Call api save to database.
                #
                log = logger.CompanyHistoryLog ()
                for y in range (self.table.GetMaxRow()):
                    if self.table.EntryStatusGet (0, y) == 'new':
                        node = self.TransferRowToNode(y)
                        
                        self.database.AddNode(node)
                        log.SetAddFile (node)
                        CD_FileAccess.CreateCompanyFolder (node.GetName())
                        
                    elif self.table.EntryStatusGet (0, y) == 'remove':
                        node = self.TransferRowDefaultToNode(y)
                        name = node.GetName ()
                        
                        self.database.RemoveNode (name)
                        log.SetRemoveFile (node)
                        CD_FileAccess.RemoveCompanyFolder (nmae)
                        
                    else:
                        for x in range (self.table.GetColumnNumber()):
                            if self.table.EntryStatusGet (x, y) == 'modify':
                                preNode = self.TransferRowDefaultToNode(y)
                                postNode = self.TransferRowToNode(y)
                                name = preNode.GetName()

                                self.database.ModifyNode (name, postNode)
                                log.SetModifyFile (preNode, postNode)
                                os.rename ('database/' + preNode.GetName(), 'database/' + postNode.GetName(), )
                                break

                #
                # 4. Save database to hard drive
                #
                CD_FileAccess.ExportCompany(self.database)
                log.AddLog()
                logging.info ('Modify product file success!\n')
                self.Exit()

    #
    # Transfer specific node into class ProductNode
    #
    def TransferRowToNode(self, row):
        node = link.CompanyNode()

        node.Name.SetData (self.table.EntryTextGet (0, row))
        node.Code.SetData (self.table.EntryTextGet (1, row))

        return node
    
    def TransferRowDefaultToNode(self, row):
        node = link.CompanyNode()

        node.Name.SetData (self.table.EntryDefaultGet (0, row))
        node.Code.SetData (self.table.EntryDefaultGet (1, row))

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
    a = GuiCompanyModify(root, Database)
    a.pack (side = 'top', fill = 'both', expand = True)

    for i in range (0):
        a.table.AddNewRow()
    
    root.mainloop()
