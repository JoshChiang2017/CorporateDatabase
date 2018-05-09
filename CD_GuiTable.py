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
            text = '代碼',
            borderwidth = 1,
            relief=tk.GROOVE,
            )
        self.Column2 = tk.Label(
            self,
            text = '品名',
            borderwidth = 1,
            relief=tk.GROOVE,
            )
        self.Column3 = tk.Label(
            self,
            text = '單價',
            borderwidth = 1,
            relief=tk.GROOVE,
            )
        
        self.pack (side = 'top', fill = 'x')
        self.Column1.pack(side = 'left', fill = 'x', expand = True)
        self.Column2.pack(side = 'left', fill = 'x', expand = True)
        self.Column3.pack(side = 'left', fill = 'x', expand = True)

class TableOfData(tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)
        self.config(
            borderwidth = 1,
            relief=tk.GROOVE,
            bg = '#D8E5f3'
            )
        
        self.Column1 = tk.Entry(
            self,
            borderwidth = 1,
            relief=tk.GROOVE,
            )
        self.Column2 = tk.Entry(
            self,
            borderwidth = 1,
            relief=tk.GROOVE,
            )
        self.Column3 = tk.Entry(
            self,
            borderwidth = 1,
            relief=tk.GROOVE,
            )

       

        self.pack (side = 'top', fill = 'x')
        self.Column1.pack(side = 'left', fill = 'x', expand = True)
        self.Column2.pack(side = 'left', fill = 'x', expand = True)
        self.Column3.pack(side = 'left', fill = 'x', expand = True)

        self.Column1.bind ('<Return>', self.Calkback1)
        self.Column2.bind ('<Return>', self.Calkback2)
        self.Column3.bind ('<Return>', self.Calkback3) 
        
    def Calkback1(self, event):
        print ('Calkback : Column1')
        self.Column2.focus_set()
    def Calkback2(self, event):
        print ('Calkback : Column2')
        self.Column3.focus_set()
    def Calkback3(self, event):
        print ('Calkback : Column3')
        self.Column3.focus_set()

class TableOfAll(tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)
        self.config(
            borderwidth = 5,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        self.a = TableOfTitle(self)
        self.b = TableOfData(self)
        self.c = TableOfData(self)
        self.d = TableOfData(self)
        
        self.pack (side = 'top', fill = 'both', expand = True)


    

#
# Simple test of this module.
#
if __name__ == '__main__':

    M = tk.Tk()
    M.geometry ('600x400')
    a = TableOfAll(M)
    tk.Button (
            M,
            text = '離開',
            font = ('Arial', 12),
            bg = '#6899CA'
            ).pack()

    a1 = tk.Entry(
        M
        )
    a1.pack()
    
    a2 = tk.Entry(
        M
        )
    a2.pack()
    
    a3 = tk.Entry(
        M
        )
    a3.pack()
    



    def qqq(self):
        print ('Press Enter')
        a2.focus_set()
    
    a1.bind ('<Return>', qqq)




    
    tk.mainloop()
