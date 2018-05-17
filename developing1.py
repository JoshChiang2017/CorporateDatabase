import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image,ImageTk


##########################################
class GuiAddToDatabaseInternal (tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent, 
            borderwidth = 3,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        
        v0 = tk.StringVar()
        e0 = tk.Entry(self, textvariable = v0, state = 'readonly')
        v0.set('aaaa')
        e0.grid(row = 1, column = 0 )
        e0.delete(0, tk.END)
        e0.insert(0, "a default value")

        v1 = tk.StringVar()
        e1 = tk.Entry(self, textvariable = v1, state = 'readonly')
        v1.set('Col1')
        e1.grid(row = 1, column = 1 )

        v2 = tk.StringVar()
        e2 = tk.Entry(self, textvariable = v2, state = 'readonly')
        v2.set('Col2')
        e2.grid(row = 1, column = 2)

        v3 = tk.StringVar()
        e3 = tk.Entry(self, textvariable = v3, state = 'readonly')
        v3.set('Col3')
        e3.grid(row = 1, column = 3 )

        v4 = tk.StringVar()
        e4 = tk.Entry(self, textvariable = v4, state = 'readonly')
        v4.set('Col4')
        e4.grid(row = 1, column = 4 )
        

#
# GUI of add data to database
#
class GuiAddToDatabase (tk.Frame):
    def __init__(self, Parent, Database):
        tk.Frame.__init__(self, Parent)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 10)
        self.columnconfigure(0, weight = 1)
        
        self.OperationRegion = tk.Frame(
            self,
            borderwidth = 3
            )
        self.OperationRegion2 = tk.Frame(
            self,
            borderwidth = 3,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        self.ObserveRegion = GuiAddToDatabaseInternal (self)
            
        self.OperationRegion.grid(row=0, column=0, sticky='news', padx=1, pady=5)
        self.ObserveRegion.grid(row=1, column=0, sticky='news', padx=1, pady=5)
        
        for i in range (3):
          self.OperationRegion.rowconfigure(i, weight = 1)
        for i in range (8):
          self.OperationRegion.columnconfigure(i, weight = 1)
        
        #
        # Operation Region - Button
        #
        self.ExitButton = tk.Button (
            self.OperationRegion, 
            text = '儲存:',
            bg = '#AA88AA'
            )
        self.ExitButton.grid(row=0, column=7, sticky='news', padx=1, pady=5)
        
        self.SaveButton = tk.Button (
            self.OperationRegion, 
            text = '刪除已選取:',
            bg = '#AA88AA'
            )
        self.SaveButton.grid(row=1, column=7, sticky='news', padx=1, pady=5)

        self.ExitButton = tk.Button (
            self.OperationRegion, 
            text = '回主畫面:',
            bg = '#AA88AA'
            )
        self.ExitButton.grid(row=0, column=6, sticky='news', padx=1, pady=5)
        
        #
        # Operation Region - Entry
        #
        self.CompanyCodeText = tk.Label (
            self.OperationRegion, 
            text = '公司代碼:'
            )
        self.CompanyCodeText.grid(row=0, column=0, sticky='news', padx=1, pady=5)
        self.CompanyCodeEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            relief=tk.RIDGE
            )
        self.CompanyCodeEntry.grid(row=0, column=1, sticky='news', padx=1, pady=5)
        
        self.CompanyNameText = tk.Label (
            self.OperationRegion, 
            text = '公司名稱:'
            )
        self.CompanyNameText.grid(row=1, column=0, sticky='news', padx=1, pady=5)
        self.CompanyNameEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            relief=tk.RIDGE
            )
        self.CompanyNameEntry.grid(row=1, column=1, sticky='news', padx=1, pady=5)
        
        self.ProductNameText = tk.Label (
            self.OperationRegion, 
            text = '產品名稱:'
            )
        self.ProductNameText.grid(row=2, column=0, sticky='news', padx=1, pady=5)
        self.ProductNameEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3,
            relief=tk.RIDGE
            )
        self.ProductNameEntry.grid(row=2, column=1, sticky='news', padx=1, pady=5)
        
        self.ProductCodeText = tk.Label (
            self.OperationRegion, 
            text = '產品代碼:'
            )
        self.ProductCodeText.grid(row=2, column=2, sticky='news', padx=1, pady=5)
        self.ProductCodeEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            relief=tk.RIDGE,
            width = 10
            )
        self.ProductCodeEntry.grid(row=2, column=3, sticky='news', padx=1, pady=5)
        
        self.ProductPriceText = tk.Label (
            self.OperationRegion, 
            text = '價錢:'
            )
        self.ProductPriceText.grid(row=2, column=4, sticky='news', padx=1, pady=5)
        self.ProductPriceEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            relief=tk.RIDGE,
            width = 10
            )
        self.ProductPriceEntry.grid(row=2, column=5, sticky='news', padx=1, pady=5)
        
        self.ProductPictureText = tk.Label (
            self.OperationRegion, 
            text = '圖片(Y/N):'
            )
        self.ProductPictureText.grid(row=2, column=6, sticky='news', padx=1, pady=5)
        self.ProductPictureEntry = tk.Entry (
            self.OperationRegion,
            borderwidth = 3, 
            relief=tk.RIDGE,
            width = 3
            )
        self.ProductPictureEntry.grid(row=2, column=7, sticky='news', padx=1, pady=5)
        
        

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry ('800x600+10+10')
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 1)
    
    Database = 0
    
    GuiAddToDatabase(root, Database).grid (row=0, column=0, sticky='w'+'e'+'n'+'s')
    root.mainloop()


        
