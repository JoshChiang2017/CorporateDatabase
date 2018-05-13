import tkinter as tk
from PIL import Image,ImageTk

#
# GUI of application entry menu.
#
class EntryMenu (tk.Frame):
    def __init__(self, Parent):
        tk.Frame.__init__(self, Parent)
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
        
        #
        # Button
        #
        self.ButtonNew = tk.Button (
            self.FrameMainBottom,
            text = '新增',
            font = ('標楷體', 14),
            bg = '#6899CA'
            )
        
        self.ButtonSearch = tk.Button (
            self.FrameMainBottom,
            text = '查詢',
            font = ('標楷體', 14),
            bg = '#6899CA'
            )
        
        self.ButtonExit = tk.Button (
            self.FrameMainBottom,
            text = '離開',
            font = ('標楷體', 14),
            bg = '#6899CA',
            command=lambda: Parent.destroy ()
            )

        self.ButtonNew.grid (row=0, column=0, sticky='news', padx=1, pady=1)
        self.ButtonSearch.grid (row=0, column=1, sticky='news', padx=1, pady=1)
        self.ButtonExit.grid (row=0, column=2, sticky='news', padx=1, pady=1)
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
# Simple test of this module.
#
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry ('600x400')
    root.rowconfigure(0, weight = 1)
    root.columnconfigure(0, weight = 1)
    
    EntryMenu(root).grid (row=0, column=0, sticky='w'+'e'+'n'+'s')
    root.mainloop()

