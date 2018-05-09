import tkinter as tk
import os
import logging
from PIL import Image,ImageTk

import CD_DataTable
import CD_LinkingList

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
    

def CorporateDatabaseMain():
    #CA_GuiLayout.EntryPoint('Company')

    #
    # Initalize root window
    #
    root = tk.Tk ()
    root.minsize (width = 600, height = 300)
    root.geometry ('600x300+10+10')

    #
    # Initalize table of data display.
    #
    DisplayTable = CD_DataTable.DataTable(root)
    DisplayTable.grid(row=0, column=0, columnspan=3, rowspan=2, sticky='w'+'e'+'n'+'s', padx=5, pady=5)

    root.rowconfigure(0, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.rowconfigure(2, weight = 1)
    root.columnconfigure(0, weight = 1)
    root.columnconfigure(1, weight = 1)
    root.columnconfigure(2, weight = 1)

    #
    # Load data from database as linking list.
    # Insert data to display table
    #
    DatabaseHeader = LoadDatabase()
    CurrentCompany = DatabaseHeader.Header.Name.GetNextNode()
    
    #
    # Load image not found image.
    #
    im = Image.open ('CD_ImageNotFound.png')
    NotFoundImage = ImageTk.PhotoImage(im)
    im.close()

    while CurrentCompany != None:
        CurrentProduct = CurrentCompany.ProductListHeader.Header.Name.GetNextNode()
        
        while CurrentProduct != None:
            DisplayTable.tree.insert('', -1,
                values=(
                    CurrentCompany.Name.GetData(),
                    CurrentProduct.Name.GetData(),
                    CurrentProduct.Code.GetData(),
                    CurrentProduct.Price.GetData()
                    ))
            CurrentProduct = CurrentProduct.Name.GetNextNode()
        CurrentCompany = CurrentCompany.Name.GetNextNode()

    #
    # Initial canvas to display simple picture of product.
    #
    ProductSimpleImage = tk.Label (
        root,
        bg = '#DDDDDD',
        height = 100,
        width = 100,
        image = None
        )
    ProductSimpleImage.grid(row=2, column=2, columnspan=1, rowspan=1, sticky='w'+'e'+'n'+'s', padx = 5, pady = 5)

    #
    # Clakback function of display simple picture from treeview selected item.
    #
    def TreeviewSimplePictureDisplay():
        CurrentSelectItem = DisplayTable.tree.focus ()
        CurrentSelectValue = DisplayTable.tree.item(CurrentSelectItem, "values")

        #
        # CurrentSelectValue[0] is company name
        # CurrentSelectValue[1] is product name
        #
        CurrentProductNode = DatabaseHeader.FindProduct (CurrentSelectValue[0], CurrentSelectValue[1])
        if CurrentProductNode.Image != None:
            ProductSimpleImage.config (image = CurrentProductNode.Image)
        else:
            ProductSimpleImage.config (image = NotFoundImage)
        
    #
    # Treeview callback of arrow up/down key, left mouse button.
    #
    def TreeviewSimplePictureCalkback(event):
        logging.debug ('Callback - Arrow Up/Down, or left mouse botton.')
        TreeviewSimplePictureDisplay()
    
    #
    # Treeview callback of Enter key.
    #
    def TreeviewReturnCalkback(event):
        logging.debug ('Callback - key of Enter.')
        CurrentSelectItem = DisplayTable.tree.focus ()
        CurrentSelectValue = DisplayTable.tree.item(CurrentSelectItem, "values")

        #
        # CurrentSelectValue[0] is company name
        # CurrentSelectValue[1] is product name
        #
        CurrentProductNode = DatabaseHeader.FindProduct (CurrentSelectValue[0], CurrentSelectValue[1])
        if CurrentProductNode.Image != None:
            os.startfile(os.getcwd() + '/database/' + CurrentSelectValue[0] + '/' + CurrentSelectValue[1] + '.png')

    #
    # Configure operation calkback in treeview
    #
    DisplayTable.tree.bind("<KeyRelease-Down>", TreeviewSimplePictureCalkback)
    DisplayTable.tree.bind("<KeyRelease-Up>", TreeviewSimplePictureCalkback)
    DisplayTable.tree.bind("<ButtonRelease-1>", TreeviewSimplePictureCalkback)
    DisplayTable.tree.bind("<Return>", TreeviewReturnCalkback)

    #
    # Search relate control
    #
    SearchFrame = tk.Frame (
        root,
        borderwidth = 5,
        #height = 100,
        #width = 150,
        relief=tk.SUNKEN,
        bg = '#D8E5f3'
        )
    SearchFrame.grid (row=2, column=0, columnspan=2, rowspan=1, sticky='w'+'e'+'n'+'s', padx = 5, pady = 5)

    #
    # Focus on first item in the treeview.
    #
    DisplayTable.tree.selection_set (DisplayTable.tree.get_children()[0]) # highlight first item in treeview
    
    DisplayTable.tree.focus_set() # set focus to treeview
    DisplayTable.tree.focus(DisplayTable.tree.get_children()[0]) #set focus to item
    TreeviewSimplePictureDisplay()

    root.mainloop()

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
    # Entry point of project
    #
    CorporateDatabaseMain()
    print ("==== GUI  End  ====")
