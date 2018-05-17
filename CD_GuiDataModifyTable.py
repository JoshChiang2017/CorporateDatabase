import tkinter as tk

class TableOfTitle(tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)
        self.config(
            borderwidth = 3,
            relief=tk.GROOVE,
            bg = '#D8E5f3'
            )
        
        self.Column1 = tk.Label(
            self,
            text = '產品名稱',
            borderwidth = 1,
            relief=tk.GROOVE,
            width=10
            )
        self.Column2 = tk.Label(
            self,
            text = '產品代碼',
            borderwidth = 1,
            relief=tk.GROOVE,
            width=10
            )
        self.Column3 = tk.Label(
            self,
            text = '單價',
            borderwidth = 1,
            relief=tk.GROOVE,
            width=10
            )
        self.Column4 = tk.Label(
            self,
            text = '圖片',
            borderwidth = 1,
            relief=tk.GROOVE,
            width=10
            )
        
        self.pack (side = 'top', fill = 'x')
        self.Column1.pack(side = 'left', fill = 'x', expand = True)
        self.Column2.pack(side = 'left', fill = 'x', expand = True)
        self.Column3.pack(side = 'left', fill = 'x', expand = True)
        self.Column4.pack(side = 'left', fill = 'x', expand = True)

class TableOfData(tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)
        
        String1 = tk.StringVar()
        String2 = tk.StringVar()
        String3 = tk.StringVar()
        String4 = tk.StringVar()

        String1.set ('由此輸入新資料')
        
        self.config(
            borderwidth = 1,
            relief=tk.GROOVE,
            bg = '#D8E5f3'
            )
        
        self.Column1 = tk.Entry(
            self,
            borderwidth = 1,
            relief=tk.GROOVE,
            textvariable = String1
            )
        self.Column2 = tk.Entry(
            self,
            borderwidth = 1,
            relief=tk.GROOVE,
            textvariable = String2
            )
        self.Column3 = tk.Entry(
            self,
            borderwidth = 1,
            relief=tk.GROOVE,
            textvariable = String4
            )
        self.Column4 = tk.Entry(
            self,
            borderwidth = 1,
            relief=tk.GROOVE,
            textvariable = String4
            )

        self.pack (side = 'top', fill = 'x')
        self.Column1.pack(side = 'left', fill = 'x', expand = True)
        self.Column2.pack(side = 'left', fill = 'x', expand = True)
        self.Column3.pack(side = 'left', fill = 'x', expand = True)
        self.Column4.pack(side = 'left', fill = 'x', expand = True)

        self.Column1.bind ('<Return>', self.Calkback1)
        self.Column2.bind ('<Return>', self.Calkback2)
        self.Column3.bind ('<Return>', self.Calkback3) 
        self.Column4.bind ('<Return>', self.Calkback4) 
        
    def Calkback1(self, event):
        print ('Calkback : Column1')
        self.Column2.focus_set()
    def Calkback2(self, event):
        print ('Calkback : Column2')
        self.Column3.focus_set()
    def Calkback3(self, event):
        print ('Calkback : Column3')
        self.Column4.focus_set()
    def Calkback4(self, event):
        print ('Calkback : Column4')
        self.Column1.focus_set()

class TableOfModify(tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)
        self.config(
            borderwidth = 5,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        self.a = TableOfTitle(self)
        self.b = TableOfData(self)
        
        self.DataTableSize = 0
        self.DataTableBuffer = []

    def AddDataTable (self):
        
        self.DataTableSize += 1
        NewDataTable = TableOfData(self)

        self.DataTableBuffer.append (NewDataTable)
    

#
# Simple test of this module.
#
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry ('800x600+10+10')
    a = TableOfModify(root)
    a.pack (side = 'top', fill = 'both', expand = True)

    b=tk.Button (
            root,
            text = '儲存:',
            bg = '#AA88AA',
            command = a.AddDataTable
            ).pack()
    
    root.mainloop()
