import os
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image,ImageTk
import logging

#
# GUI of data display table
#
class DataTable (tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)

        #
        # Initialize Treeview
        #
        self.AllColumn = ('CompanyName','ProductName','ProductCode', 'ProductPrice', 'ProductComment')
        self.A_Column = self.AllColumn

        self.tree = ttk.Treeview(
                self,
                columns = self.AllColumn,
                displaycolumns = self.A_Column,
                show = 'headings',
                selectmode = 'browse'
                )
        self.tree.pack(side='left', fill='both', expand=True)

        self.tree.column ('CompanyName', anchor = 'w', width = 100)
        self.tree.column ('ProductName', anchor = 'w', width = 100)
        self.tree.column ('ProductCode', anchor = 'w', width = 50)
        self.tree.column ('ProductPrice', anchor = 'e', width = 50)
        self.tree.column ('ProductComment', anchor = 'w', width = 200)

        
        self.tree.heading ('CompanyName', text = '公司')
        self.tree.heading ('ProductName', text = '品名')
        self.tree.heading ('ProductCode', text = '代碼')
        self.tree.heading ('ProductPrice', text = '單價')
        self.tree.heading ('ProductComment', text = '附註')

        #
        # Initialize scrollbar
        #
        Scrollbar1 = tk.Scrollbar(self)
        Scrollbar1.pack (side='left', fill='y')
        Scrollbar1.config (command = self.tree.yview)
        self.tree.config (yscrollcommand = Scrollbar1.set)
        

#
# GUI of data display table
#
# @Database  Database linking list.
#
class DataDisplayMenu (tk.Frame):
    def __init__(self, Parent, Database):
        tk.Frame.__init__(self, Parent)

        #
        # Initalize table of data display.
        #
        self.DisplayTable = DataTable(self)
        self.DisplayTable.grid (row=0, column=0, columnspan=3, rowspan=2, sticky='news', padx=5, pady=5)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.Database = Database
        CurrentCompany = Database.Header.Name.GetNextNode()
        
        #
        # Load image not found image.
        #
        im = Image.open ('image/ImageNotFound.png')
        self.NotFoundImage = ImageTk.PhotoImage(im)
        im.close()

        while CurrentCompany != None:
            CurrentProduct = CurrentCompany.ProductListHeader.Header.Name.GetNextNode()
            
            while CurrentProduct != None:
                self.DisplayTable.tree.insert('', -1,
                    values=(
                        CurrentCompany.Name.GetData(),
                        CurrentProduct.Name.GetData(),
                        CurrentProduct.Code.GetData(),
                        CurrentProduct.Price.GetData(),
                        CurrentProduct.comment
                        ))
                CurrentProduct = CurrentProduct.Name.GetNextNode()
            CurrentCompany = CurrentCompany.Name.GetNextNode()

        #
        # Initial canvas to display simple picture of product.
        #
        self.ProductSimpleImage = tk.Label (
            self,
            bg = '#DDDDDD',
            height = 100,
            width = 100,
            image = None
            )
        self.ProductSimpleImage.grid(row=2, column=2, columnspan=1, rowspan=1, sticky='news', padx = 5, pady = 5)


        #
        # Configure operation calkback in treeview
        #
        self.DisplayTable.tree.bind("<KeyRelease-Down>", self.TreeviewSimplePictureCalkback)
        self.DisplayTable.tree.bind("<KeyRelease-Up>", self.TreeviewSimplePictureCalkback)
        self.DisplayTable.tree.bind("<ButtonRelease-1>", self.TreeviewSimplePictureCalkback)
        self.DisplayTable.tree.bind("<Return>", self.TreeviewReturnCalkback)
        self.bind_all ('<Control-Key-Q>', lambda event: self.Exit())
        self.bind_all ('<Control-Key-q>', lambda event: self.Exit())

        #
        # Search relate control
        #
        self.SearchFrame = tk.Frame (
            self,
            borderwidth = 5,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        self.SearchFrame.grid (row=2, column=0, columnspan=2, rowspan=1, sticky='news', padx = 5, pady = 5)

        #
        # Search item
        #
        self.ButtonBackToMain = tk.Button (
            self.SearchFrame,
            text = '回主畫面(Q)',
            bg = '#6899CA',
            command = lambda: self.Exit ()
            )
        self.ButtonBackToMain.grid()

        if self.Database.IsEmpty() is False:
            #
            # Focus on first item in the treeview.
            #
            self.DisplayTable.tree.selection_set (self.DisplayTable.tree.get_children()[0]) # highlight first item in treeview
            
            self.DisplayTable.tree.focus_set() # set focus to treeview
            self.DisplayTable.tree.focus(self.DisplayTable.tree.get_children()[0]) #set focus to item
            
            self.TreeviewSimplePictureDisplay()
    
    #
    # Clakback function of display simple picture from treeview selected item.
    #
    def TreeviewSimplePictureDisplay(self):
        self.CurrentSelectItem = self.DisplayTable.tree.focus ()
        self.CurrentSelectValue = self.DisplayTable.tree.item(self.CurrentSelectItem, "values")

        #
        # CurrentSelectValue[0] is company name
        # CurrentSelectValue[1] is product name
        #
        self.CurrentProductNode = self.Database.FindProduct (self.CurrentSelectValue[0], self.CurrentSelectValue[1])
        if self.CurrentProductNode.Image != None:
            self.ProductSimpleImage.config (image = self.CurrentProductNode.Image)
        else:
            self.ProductSimpleImage.config (image = self.NotFoundImage)
        
    #
    # Treeview callback of arrow up/down key, left mouse button.
    #
    def TreeviewSimplePictureCalkback(self, event):
        logging.debug ('Callback - Arrow Up/Down, or left mouse botton.')
        self.TreeviewSimplePictureDisplay()
    
    #
    # Treeview callback of Enter key.
    #
    def TreeviewReturnCalkback(self, event):
        logging.debug ('Callback - key of Enter.')
        CurrentSelectItem = self.DisplayTable.tree.focus ()
        CurrentSelectValue = self.DisplayTable.tree.item(CurrentSelectItem, "values")

        #
        # CurrentSelectValue[0] is company name
        # CurrentSelectValue[1] is product name
        #
        CurrentProductNode = self.Database.FindProduct (CurrentSelectValue[0], CurrentSelectValue[1])
        if CurrentProductNode.Image != None:
            os.startfile(os.getcwd() + '/database/' + CurrentSelectValue[0] + '/' + CurrentSelectValue[1] + '.png')
            
    def Exit(self):
        self.destroy()
        self.unbind_all ('<Control-Key-Q>')
        self.unbind_all ('<Control-Key-q>')


if __name__ == '__main__':

    #
    # Draw GUI
    #
    root=tk.Tk()
    a = DataTable (root)
    a.grid(row=0, column=0, columnspan=2, rowspan=2, sticky='w'+'e', padx=5, pady=5)
    
    def onDBClick(event):
        item = a.tree.selection()[0]
        print ("you clicked on ", a.tree.item(item, "values"))
        print (a.tree.focus ())
        print (a.tree.selection())
    
    a.tree.bind("<Double-1>", onDBClick)

    a1=a.tree.insert('',0,text='AAA', values=(5,6,'aa666aaa'))
    a2=a.tree.insert('',0,text='BBB', values=(5,6,'bbb'))
    a3=a.tree.insert('',0,text='BBB', values=(5,6,'ccccccc'))
    a.tree.insert(a1,-1,text='CCC', values=(5,6,'Q|||||'))
    a.tree.insert(a1,'end',text='CCC', values=(5,6,'sdsadssa'))
    a.tree.insert(a1,'end',text='CCC', values=(5,6,'sdsadssa'))
    a.tree.insert(a1,'end',text='CCC', values=(5,6,'sdsadssa'))
    a.tree.insert(a1,'end',text='CCC', values=(5,6,'sdsadssa'))

    for i in range(50):
        a.tree.insert('',-1,text='BBB', values=(i,i*2,'aaaaa'))

    #
    # Focus
    #
    a.tree.selection_set (a.tree.get_children()[0]) # highlight first item in treeview
    
    a.tree.focus_set() # set focus to treeview
    a.tree.focus(a.tree.get_children()[0]) #set focus to item
            
    root.mainloop ()
    
 
