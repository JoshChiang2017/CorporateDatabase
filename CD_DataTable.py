import tkinter as tk
import tkinter.ttk as ttk

class DataTable (tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)

        #
        # Initialize Treeview
        #
        self.AllColumn = ('CompanyName','ProductName','ProductCode', 'ProductPrice')
        self.A_Column = self.AllColumn

        self.tree = ttk.Treeview(
                self,
                columns = self.AllColumn,
                displaycolumns = self.A_Column,
                show = 'headings',
                selectmode = 'browse'
                )
        self.tree.pack(side='left', fill='both', expand=True)

        self.tree.column ('CompanyName', anchor = 'w', width = 200)
        self.tree.column ('ProductName', anchor = 'w', width = 200)
        self.tree.column ('ProductCode', anchor = 'w', width = 100)
        self.tree.column ('ProductPrice', anchor = 'e', width = 50)

        
        self.tree.heading ('CompanyName', text = '公司')
        self.tree.heading ('ProductName', text = '品名')
        self.tree.heading ('ProductCode', text = '代碼')
        self.tree.heading ('ProductPrice', text = '單價')

        #
        # Initialize scrollbar
        #
        Scrollbar1 = tk.Scrollbar(self)
        Scrollbar1.pack (side='left', fill='y')
        Scrollbar1.config (command = self.tree.yview)
        self.tree.config (yscrollcommand = Scrollbar1.set)
        
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
            
    root.mainloop
    
 
