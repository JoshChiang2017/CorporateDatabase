import tkinter as tk

#
# The Image module provides a class with the same name which is used to represent a PIL image.
#   The module also provides a number of factory functions, including functions to load images from files, and to create new images.
# The ImageTk module contains support to create and modify Tkinter BitmapImage and PhotoImage objects from PIL images.
#
from PIL import Image,ImageTk


######################################################################################################################

#
# Draw GUI root window 
#
class RootWindow:

    def __init__(self, Name):   
        self.Window = tk.Tk()
        self.Window.title (Name)
        self.Window.geometry ('600x400')
        
        self.Window.update_idletasks()
        print (self.Window.winfo_width())
        print (self.Window.winfo_height())
        
        #
        # Frame
        #
        self.FrameMainTop = tk.Frame(
            self.Window,
            borderwidth = 5,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        
        self.FrameMainBottom = tk.Frame(
            self.Window,
            borderwidth = 5,
            relief=tk.SUNKEN,
            bg = '#D8E5f3'
            )
        
        self.FrameMainTop.bind ('<Configure>', self.TopFrameResize)
        self.FrameMainTop.pack (side = 'top', fill = 'both', expand = True)
        self.FrameMainBottom.pack(side = 'top', fill = tk.X)

        #
        # Button
        #
        self.ButtonNew = tk.Button (
            self.FrameMainBottom,
            text = '新增',
            font = ('Arial', 12),
            bg = '#6899CA'
            )
        
        self.ButtonSearch = tk.Button (
            self.FrameMainBottom,
            text = '搜尋',
            font = ('Arial', 12),
            bg = '#6899CA'
            )
        
        self.ButtonExit = tk.Button (
            self.FrameMainBottom,
            text = '離開',
            font = ('Arial', 12),
            bg = '#6899CA'
            )

        self.ButtonNew.pack (side = 'left', fill = 'both', expand = True, padx = 5, pady = 3)
        self.ButtonSearch.pack (side = 'left', fill = 'both', expand = True, padx = 5, pady = 3)
        self.ButtonExit.pack (side = 'left', fill = 'both', expand = True, padx = 5, pady = 3)

        #
        # Get FrameMainTop size
        #
        # Calls all pending idle tasks, without processing any other events.
        # This can be used to carry out geometry management and redraw widgets if necessary, without calling any callbacks.
        #
        # Image label should be create after create button, because FrameMainBottom.winfo_height() is modified after creating button.
        #
        self.Window.update_idletasks()
        print ('---------')
        print (self.Window.winfo_width())
        print (self.Window.winfo_height())
        print (self.FrameMainTop.winfo_width())
        print (self.FrameMainTop.winfo_height())
        print (self.FrameMainBottom.winfo_width())
        print (self.FrameMainBottom.winfo_height())

        #
        # Entry image
        #
        # EntryPhoto = tk.PhotoImage (file = 'CompanyImage.PNG') #only available for .gif
        self.EntryPhotoOriginal = Image.open ('CompanyImage.PNG')
        self.EntryPhotoResize = self.EntryPhotoOriginal.resize ((self.FrameMainTop.winfo_width(), self.FrameMainTop.winfo_height()), Image.ANTIALIAS)
        self.EntryPhotoTkImage = ImageTk.PhotoImage (self.EntryPhotoResize)
        
        self.LabelEntryImage = tk.Label (
            self.FrameMainTop,
            bg = '#123456',
            image = self.EntryPhotoTkImage,
            width = self.FrameMainTop.winfo_width(),
            height = self.FrameMainTop.winfo_height()
            )
        
        # When you add a PhotoImage or other Image object to a Tkinter widget, you must keep your own reference to the image object. If you don’t, the image won’t always show up.
        # The problem is that the Tkinter/Tk interface doesn’t handle references to Image objects properly; the Tk widget will hold a reference to the internal object, but Tkinter does not.
        # When Python’s garbage collector discards the Tkinter object, Tkinter tells Tk to release the image. But since the image is in use by a widget, Tk doesn’t destroy it.
        # Not completely. It just blanks the image, making it completely transparent…
        # The solution is to make sure to keep a reference to the Tkinter object, for example by attaching it to a widget attribute:
        self.LabelEntryImage.image = self.EntryPhotoTkImage  # keep a reference!
        self.LabelEntryImage.pack()
        print ('CCC')

    def TopFrameResize (self, event):
        ModifySize = (event.width, event.height)
        print (self.Window.winfo_width())
        print (self.Window.winfo_height())
        print ('ABC')
        
    def DrawEntryImage (self, event):
        ModifySize = (event.width, event.height)
        size = EntryPhotoOriginal.resize (ModifySize, Image.ANTIALIAS)
        self.EntryPhotoTkImage = ImageTk.PhotoImage (self.EntryPhotoResize)
        self.LabelEntryImage = tk.Label (
            FrameMainTop,
            bg = '#123456',
            image = EntryPhotoTkImage
            #width = FrameMainTop.winfo_width(),
            #height = FrameMainTop.winfo_height()
            )
        



        
#
# Entry point
#
def EntryPoint (Name):
    RootWin = RootWindow(Name)
    tk.mainloop()

#
# Simple test of this module.
#
if __name__ == '__main__':
    EntryPoint ('Company')

