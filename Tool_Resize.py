from PIL import Image

def ResizeToSimplePic(PicFile):
    im = Image.open(PicFile)
    imResize = im.resize ((200, 200))

    imResize.save ('Resize.png')



ResizeToSimplePic ('CD_ImageNotFound.png')
