import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image,ImageTk


##########################################

#
#
# @ColumnNumber      Number of column of table will be created.
# @Title             List of string display on each top of column.
#
class Table (tk.Frame):
    def __init__(self, Parent, ColumnNumber, Title):
        tk.Frame.__init__(self, Parent, 
            borderwidth = 3,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        
        #
        # In this frame, contain two sub frame
        #
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 100)
        self.columnconfigure(0, weight = 1)
        
        self.TitleFrame = tk.Frame(
            self,
            borderwidth = 1
            )
        self.DataFrame = tk.Frame(
            self,
            borderwidth = 1,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        
        self.TitleFrame.grid(row=0, column=0, sticky='news', padx=1, pady=1)
        self.DataFrame.grid(row=1, column=0, sticky='news', padx=1, pady=1)
        
        self.TitleFrame.rowconfigure(0, weight = 1)
        for Index in range(ColumnNumber):
            self.TitleFrame.columnconfigure(Index, weight = 1)
            self.DataFrame.columnconfigure(Index, weight = 1)
        
        #
        # Initialize title of table.
        #
        for Index in range(ColumnNumber):
            TitleString = tk.StringVar()
            TitleString.set(Title[Index])
            entry = tk.Entry (
                self.TitleFrame,
                borderwidth = 1,
                relief=tk.GROOVE,
                state = 'disabled',
                justify = 'center',
                textvariable = TitleString
                )
            entry.grid(row=0, column=Index, sticky='news', padx=1, pady=1)
        
        #
        # Initilize table first row.
        #
        self.ItemY = []
        for Index in range(ColumnNumber):
            ItemX = []
            TitleString = tk.StringVar()
            TitleString.set('N/A')
            entry = tk.Entry (
                self.DataFrame,
                borderwidth = 1,
                relief=tk.GROOVE,
                textvariable = TitleString
                )
            entry.grid(row=0, column=Index, sticky='news', padx=1, pady=1)
            ItemX.append (entry)
        self.ItemY.append (ItemX)
            
i = 0.01

def aaa():
    global i
    print (i, 0.1+i)
    Scrollbar1.set(i,0.1+i)

    if i<1:
        i+=0.1






if __name__ == '__main__':
    root = tk.Tk()
    root.geometry ('600x400+10+10')
    
    Title = ('Name', 'Code', 'Price')
    table = Table (root, 3, Title)
    table.pack(side='left', fill='both', expand=True)
    
    
    
    
    root.mainloop()


        
