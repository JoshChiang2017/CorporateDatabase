import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image,ImageTk

a=tk.Tk()
a.geometry ('800x600+10+10')
a.rowconfigure(0, weight = 1)
a.columnconfigure(0, weight = 1)

EntryPhotoOriginal = Image.open ('image/EntryImage.png')

EntryPhotoResize = EntryPhotoOriginal.resize ((
            200,
            100),
            Image.ANTIALIAS
            )
EntryPhotoTkImage = ImageTk.PhotoImage (EntryPhotoResize)


LabelEntryImage = tk.Label (
            a,
            bg = '#123456',
            text = 'ABBC'
            #image = EntryPhotoTkImage,
            #width = 400,
            #height = 400
            )
LabelEntryImage.pack()#grid(row=0, column=0, sticky='news', padx=5, pady=5)

print (a.winfo_height())
print (a.winfo_width())
print (a.winfo_reqheight())
print (a.winfo_reqwidth())
print()

print (LabelEntryImage.winfo_height())
print (LabelEntryImage.winfo_width())
print (LabelEntryImage.winfo_reqheight())
print (LabelEntryImage.winfo_reqwidth())
print('-------')

a.update_idletasks()
LabelEntryImage.update_idletasks()

print (a.winfo_height())
print (a.winfo_width())
print (a.winfo_reqheight())
print (a.winfo_reqwidth())
print()

print (LabelEntryImage.winfo_height())
print (LabelEntryImage.winfo_width())
print (LabelEntryImage.winfo_reqheight())
print (LabelEntryImage.winfo_reqwidth())
print('-------')
a.mainloop()
