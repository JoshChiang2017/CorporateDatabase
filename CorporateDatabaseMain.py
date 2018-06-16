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
import CD_Configuration as CONF

#
# Begin a new database.
#
def InitDatabase():
    dataBaseName = CONF.GLOBAL_CONFIG_DB_FOLDER
    if not os.path.isdir(dataBaseName):
        logging.info ('Create New Database.')
        os.mkdir(dataBaseName)
        
        file = open (CONF.GLOBAL_CONFIG_DB_PATH, 'w')
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
        CONF.GLOBAL_CONFIG_DB_PATH,
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
            logging.warning ('WARNING!!', NecessaryFile[i], WarningMessage[i])
            MessageDisplay += WarningMessage[i]
            Check = False

    if Check == False:
        messagebox.showinfo('WARNING', MessageDisplay)

    return Check
    
def SwitchToModifyProduct (root, database):
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

#
# Entry display GUI only there is company in database, and product in company.
#
def SwitchToSearch (root, database):
    if not database.IsEmpty() and database.HaveAnyPoduct():
            menu = CD_GuiDataDisplayTable.DataDisplayMenu (root, database)
            menu.grid (row=0, column=0, sticky='news', padx=5, pady=5)
            menu.tkraise ()
    else:
        messagebox.showinfo('INFO', 'There are no data in database.')

#def FontConfig (font):
#    global CONF.GLOBAL_CONFIG_FONT
#    CONF.GLOBAL_CONFIG_FONT = font

#
# GUI of application entry menu.
#
class EntryMenu (tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
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
        
        for y in range(2):
            self.FrameMainBottom.rowconfigure(y, weight = 1)
        for x in range(3):
            self.FrameMainBottom.columnconfigure(x, weight = 1)
        
        #
        # Button
        #
        self.buttonList = []
        
        self.ButtonModifyCompany = tk.Button (
            self.FrameMainBottom,
            text = '修改(公司)',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command = lambda: SwitchToModifyCompany (parent, Database)
            )
        self.buttonList.append (self.ButtonModifyCompany)
        
        self.ButtonModifyProduct = tk.Button (
            self.FrameMainBottom,
            text = '修改(產品)',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command = lambda: SwitchToModifyProduct (parent, Database)
            )
        self.buttonList.append (self.ButtonModifyProduct)
        
        self.ButtonSearch = tk.Button (
            self.FrameMainBottom,
            text = '查詢',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command = lambda: SwitchToSearch (parent, Database)
            )
        self.buttonList.append (self.ButtonSearch)
        
        self.ButtonFontConfig = tk.Button (
            self.FrameMainBottom,
            text = 'Assistance',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command=lambda: self.FontConfig ()
            )
        self.buttonList.append (self.ButtonFontConfig)
        
        self.ButtonExit = tk.Button (
            self.FrameMainBottom,
            text = '離開',
            font = ('標楷體', 14),
            bg = '#6899CA',
            width=1,
            command=lambda: parent.destroy ()
            )
        self.buttonList.append (self.ButtonExit)

        self.ButtonModifyCompany.grid (row=0, column=0, sticky='news', padx=1, pady=1)
        self.ButtonModifyProduct.grid (row=1, column=0, sticky='news', padx=1, pady=1)
        self.ButtonSearch.grid        (row=0, column=1, sticky='news', padx=1, pady=1)
        self.ButtonFontConfig.grid    (row=0, column=2, sticky='news', padx=1, pady=1)
        self.ButtonExit.grid          (row=1, column=2, sticky='news', padx=1, pady=1)
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
        
    def FontConfig (self):
        if CONF.GLOBAL_CONFIG_FONT == ('標楷體', 12):
            CONF.GLOBAL_CONFIG_FONT = ('標楷體', 20)
        else:
            CONF.GLOBAL_CONFIG_FONT = ('標楷體', 12)
        
        for button in self.buttonList:
            button.config (font = CONF.GLOBAL_CONFIG_FONT)

class LoadingImage(object):
    def __init__(self, parent):
        self.frameNumber = CONF.GLOBAL_CONFIG_LOADING_PIC_FRAMES
        self.frames = [tk.PhotoImage(file=CONF.GLOBAL_CONFIG_LOADING_PIC, format = 'gif -index %i' %(i)) for i in range(self.frameNumber)]
        self.loadingImageEvent = None
        
        self.loadingLabel = tk.Label (parent)
        self.loadingLabel.grid (row=0, column=0)
    
    #
    # Some file access cost too much time. Use this funciton to display
    # loading animation. User should use LoadingImageEnd() to distroy 
    # animation after access successful.
    #
    def Start(self, frameIndex=0):
        frame = self.frames[frameIndex]
        
        frameIndex += 1
        if frameIndex == self.frameNumber:
            frameIndex = 0
        self.loadingLabel.configure(image=frame)
        
        self.loadingImageEvent = self.loadingLabel.after(100, self.Start, frameIndex)
        self.loadingLabel.tkraise ()

    def End(self):
        self.loadingLabel.after_cancel (self.loadingImageEvent)
        self.loadingLabel.destroy()

#
# Run main
#
if __name__ == '__main__':
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
