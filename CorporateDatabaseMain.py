import tkinter as tk
import os
import logging
from PIL import Image,ImageTk
from tkinter import messagebox

import CD_GuiDataDisplayTable
import CD_GuiEntryMenu
import CD_LinkingList

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

# 
# Load database and record to linking list
#
# @RETURN Database linking list.
#
def LoadDatabase():

    #
    # First, load all company list.
    #
    try:
        RootFile = open ('database/TotalCompanyList.txt', 'r')
    except FileNotFoundError:
        print ('WARNING! No database exist!!!!!')
        raise

    CompanyList1 = CD_LinkingList.CompanyList()
    for EachLine in RootFile:
        StrList = EachLine.split ('|')
        
        if StrList[0] == '@':

            #
            # StrList[1].strip() : Company name
            # StrList[2].strip() : Company code
            #
            CompanyList1.NewCompanyNode (StrList[1].strip(), StrList[2].strip())

    #CompanyList1.Print()  ## Test
    RootFile.close()

    #
    # Second, load all company data according to company list.
    #
    CurrentCompany = CompanyList1.Header.Name.GetNextNode()

    while CurrentCompany != None:
        CompanyPath = 'database/' + CurrentCompany.Name.GetData() + '/'
        CompanyProductFile = CompanyPath + CurrentCompany.Name.GetData() + '.txt'

        if not os.path.exists(CompanyProductFile):
            print ('WARNING! No company data exist!!!!! (%s)' % CompanyProductFile)
            
        else:
            logging.info (CompanyProductFile)
            File = open (CompanyProductFile, 'r')

            ProductList1 = CurrentCompany.ProductListHeader
            ProductNode1 = CD_LinkingList.ProductNode()

            for EachLine in File:
                StrList = EachLine.split ('|')
                
                if StrList[0] == '@':
                    ProductNode1.Name.SetData (StrList[1].strip())
                    ProductNode1.Code.SetData (StrList[2].strip())
                    ProductNode1.Price.SetData (StrList[3].strip())

                    #
                    # Open simple picture according to product name.
                    #
                    PicName = CompanyPath + ProductNode1.Name.GetData() + '_Simple.png'
                    
                    if os.path.exists(PicName):
                        im = Image.open(PicName)
                        imTk = ImageTk.PhotoImage(im)
                        im.close()
                    else:
                        imTk = None
                        
                    ProductNode1.Image = imTk
                    ProductList1.AddNode(ProductNode1)
            File.close()

        CurrentCompany = CurrentCompany.Name.GetNextNode()
    
    return CompanyList1

def SwitchToSearch (root, Database):
    MenuSearch = CD_GuiDataDisplayTable.DataDisplayMenu (root, Database)
    MenuSearch.grid (row=0, column=0, sticky='news', padx=5, pady=5)
    MenuSearch.tkraise ()
    
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
    logging.basicConfig(level=logging.WARNING)
    
    #
    # Initalize root window
    #
    root = tk.Tk ()
    root.minsize (width = 800, height = 600)
    root.geometry ('800x600+10+10')
    root.title ('Corporate Database')
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 1)
    
    #
    # Load data from database as linking list.
    # Insert data to display table
    #
    Database = LoadDatabase()

    MenuMain = CD_GuiEntryMenu.EntryMenu (root)

    #
    # Draw Main menu GUI
    #
    MenuMain.grid (row=0, column=0, sticky='news', padx=5, pady=5)
    MenuMain.tkraise ()

    #
    # Menu switch related callback.
    #
    MenuMain.ButtonSearch .config (command = lambda: SwitchToSearch (root, Database))
    
    root.mainloop()

    print ("==== GUI  End  ====")
