import tkinter as tk
import os
import logging
from PIL import Image,ImageTk
from tkinter import messagebox

import CD_GuiDataDisplayTable
import CD_GuiProductModify
import CD_GuiCompanyModify
import CD_FileAccess
import CD_LinkingList

#
# Begin a new database.
#
def InitDatabase():
    dataBaseName = 'database'
    if not os.path.isdir(dataBaseName):
        logging.info ('Create New Database.')
        os.mkdir(dataBaseName)
        
        file = open (dataBaseName + '/TotalCompanyList.txt', 'w')
        file.write ('%1s' % '' + '| ' + '%-20s' % 'CompanyName' + '| ' + '%-20s' % 'CompanyCode' +'|\n')
        for i in range (50):
            file.write ('=')
        file.write ('\n')
        file.close()

#
# Check if nesseary file is prepared.
# If missing display warning message box.
#
# @RETRUN True   All file is prepared.
# @RETRUN False  Missing some file.
#
def InitialCheck():

    #
    # Nesseary file:
    #     Database path
    #     GUI entry image
    #     Product image not found image
    #
    NecessaryFile = (
        'database/TotalCompanyList.txt',
        'image/EntryImage.png',
        'image/ImageNotFound.png'
        )

    #
    # Each warning message correspond one path in NecessaryFile
    #
    WarningMessage = (
        '-> Database Missing\n',
        '-> GUI entry image missing\n',
        '-> ImageNotFound image misssing\n'
        )

    NecessaryFileCount = len (NecessaryFile)
    MessageDisplay = ''
    Check = True

    for i in range (NecessaryFileCount):
        if not os.path.exists (NecessaryFile[i]):
            print ('WARNING!!', NecessaryFile[i], WarningMessage[i])
            MessageDisplay += WarningMessage[i]
            Check = False

    if Check == False:
        messagebox.showinfo('WARNING', MessageDisplay)

    return Check

def SwitchToModify (root, database):
    if database.IsEmpty() is False:
        menu = CD_GuiProductModify.GuiProductModify (root, database)
        menu.grid (row=0, column=0, sticky='news', padx=5, pady=5)
        menu.tkraise ()
    else:
        messagebox.showinfo('INFO', 'There are no data in database.')
    
def SwitchToModifyCompany (root, database):
    menu = CD_GuiCompanyModify.GuiCompanyModify (root, database)
    menu.grid (row=0, column=0, sticky='news', padx=5, pady=5)
    menu.tkraise ()
    
def SwitchToSearch (root, database):
    if database.IsEmpty() is False:
        menu = CD_GuiDataDisplayTable.DataDisplayMenu (root, database)
        menu.grid (row=0, column=0, sticky='news', padx=5, pady=5)
        menu.tkraise ()
    else:
        messagebox.showinfo('INFO', 'There are no data in database.')
 
#
# GUI of application entry menu.
#
class EntryMenu (tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)
        InitDatabase()
        
        #
        # Check necessary file before app application start.
        #
        if InitialCheck () == False:
            raise
        
        #
        # Load data from database as linking list.
        # Insert data to display table
        #
        Database = CD_FileAccess.LoadDatabase()
        if Database == None:
            raise
        
        self.rowconfigure(0, weight = 50)
        self.rowconfigure(1, weight = 1)
        self.columnconfigure(0, weight = 1)
        #
        # Frame
        #
        self.FrameMainTop = tk.Frame(
            self,
            borderwidth = 3,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        
        self.FrameMainBottom = tk.Frame(
            self,
            borderwidth = 3,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        
        self.FrameMainTop.grid (row=0, column=0, rowspan=1, sticky='news')
        self.FrameMainBottom.grid (row=1, column=0, rowspan=1, sticky='news')
        self.update()
        
        #
        # Layout grid configure
        #
        self.FrameMainTop.rowconfigure(0, weight = 1)
        self.FrameMainTop.columnconfigure(0, weight = 1)
        self.FrameMainBottom.rowconfigure(0, weight = 1)
        self.FrameMainBottom.columnconfigure(0, weight = 1)
        self.FrameMainBottom.columnconfigure(1, weight = 1)
        self.FrameMainBottom.columnconfigure(2, weight = 1)
        self.FrameMainBottom.columnconfigure(3, weight = 1)
        
        #
        # Button
        #
        self.ButtonModifyCompany = tk.Button (
            self.FrameMainBottom,
            text = '修改(公司)',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command = lambda: SwitchToModifyCompany (root, Database)
            )
        self.ButtonModifyProduct = tk.Button (
            self.FrameMainBottom,
            text = '修改(產品)',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command = lambda: SwitchToModify (root, Database)
            )
        
        self.ButtonSearch = tk.Button (
            self.FrameMainBottom,
            text = '查詢',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command = lambda: SwitchToSearch (root, Database)
            )
        
        self.ButtonExit = tk.Button (
            self.FrameMainBottom,
            text = '離開',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command=lambda: Parent.destroy ()
            )    

        self.ButtonModifyCompany.grid (row=0, column=0, sticky='news', padx=1, pady=1)
        self.ButtonModifyProduct.grid (row=0, column=1, sticky='news', padx=1, pady=1)
        self.ButtonSearch.grid (row=0, column=2, sticky='news', padx=1, pady=1)
        self.ButtonExit.grid (row=0, column=3, sticky='news', padx=1, pady=1)
        self.update()

        #
        # Entry image
        #
        ModifySize = (600, 400)
        self.EntryPhotoOriginal = Image.open ('image/EntryImage.png')
        self.EntryPhotoResize = self.EntryPhotoOriginal.resize (
            ModifySize,
            Image.ANTIALIAS
            )
        self.EntryPhotoTkImage = ImageTk.PhotoImage (self.EntryPhotoResize)

        self.LabelEntryImage = tk.Label (
            self.FrameMainTop,
            bg = '#FFFFFF',
            image = self.EntryPhotoTkImage
            )
        self.LabelEntryImage.grid (row=0, column=0, sticky='news', padx=5, pady=5)
        

#
# Run main
#
if __name__ == '__main__':
    print ("==== GUI Start ====")
    
    #
    # Debug message level=
    #   CRITICAL
    #   ERROR
    #   WARNING
    #   INFO
    #   DEBUG
    #   NOTSET
    #
    logging.basicConfig(level=logging.INFO)
    
    #
    # Initalize root window
    #
    root = tk.Tk ()
    root.minsize (width = 800, height = 600)
    root.geometry ('800x600+10+10')
    root.title ('Corporate Database')
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 1)

    MenuMain = EntryMenu (root)

    #
    # Draw Main menu GUI
    #
    MenuMain.grid (row=0, column=0, sticky='news', padx=5, pady=5)
    MenuMain.tkraise ()

    root.mainloop()

    print ("==== GUI  End  ====")
