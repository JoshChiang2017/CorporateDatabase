"""
Create several company database with dummy data to simulate.

    MaryCompany:
        Data : ProductA0 ~ ProductA100
        Price : 1s
        Image : None

    MelodyCompany:
        Data : ProductB0 ~ ProductB100
        Price : 1000s
        Image : ProductB00 ~ ProductB100
        
    ZoeCompany:
        Data : ProductA0 ~ ProductA49
        Price : 2000s
        Image : ProductA00 ~ ProductA50
        
    JannyCompany:
        Data : ProductA1 ~ ProductA(n+2) ~ ProductA49
        Price : 3000s
        Image : ProductA39 ~ ProductA49
"""
import os
from CD_LinkingList import *
from PIL import Image
import random

print ('--------- Tool_CreateDummyDatabase.py  Start ---------')

#
# Initialize Database
#
DataBaseName = 'database-dummy'
if not os.path.isdir(DataBaseName):
    os.mkdir(DataBaseName)
    
#
# Initialize image 
#
img = Image.new( 'RGB', (1000, 1000), "black") # create a new black image
pixels = img.load() # create the pixel map

#
# Initialize total company list
#
file = open (DataBaseName + '/' + 'TotalCompanyList.txt', 'w')
file.write ('%1s' % '' + '| ' + '%-20s' % 'CompanyName' + '| ' + '%-20s' % 'CompanyCode' +'|\n')
for i in range (50):
    file.write ('=')
file.write ('\n')

file.write ('%1s' % '@' + '| ')
file.write ('%-20s' % 'MaryCompany' + '| ')
file.write ('%-20s' % 'Mary' + '| ')
file.write ('\n')
file.write ('%1s' % '@' + '| ')
file.write ('%-20s' % 'MelodyCompany' + '| ')
file.write ('%-20s' % 'Melody' + '| ')
file.write ('\n')
file.write ('%1s' % '@' + '| ')
file.write ('%-20s' % 'ZoeCompany' + '| ')
file.write ('%-20s' % 'Zoe' + '| ')
file.write ('\n')
file.write ('%1s' % '@' + '| ')
file.write ('%-20s' % 'JannyCompany' + '| ')
file.write ('%-20s' % 'Janny' + '| ')
file.write ('\n')

file.close()

##############################################################################
#
# Company 1
#
Company = 'MaryCompany'
if not os.path.isdir(DataBaseName + '/' + Company):
    os.mkdir(DataBaseName + '/' + Company)
file = open (DataBaseName + '/' + Company + '/' + Company + '.txt', 'w')

#
# Header of company.
#
file.write ('%1s' % '' + '| ' + '%-20s' % 'Name' + '| ' + '%-10s' % 'Code' + '| ' + '%5s' % 'Price' + '| ' + '%5s' % 'Comment' + '|\n')
for i in range (50):
    file.write ('=')
file.write ('\n')

#
# Data of company
#
for i in range (101):
    file.write ('%1s' % '@' + '| ')
    file.write ('%-20s' % ('ProductA' + str(i)) + '| ')
    file.write ('%-10s' % ('A' + str(i)) + '| ')
    file.write ('%5s' % '' + '|')
    file.write ('%5s' % str(i) + '|')
    file.write ('\n')

file.close()
##############################################################################
#
# Company 2
#
Company = 'MelodyCompany'
if not os.path.isdir(DataBaseName + '/' + Company):
    os.mkdir(DataBaseName + '/' + Company)
file = open (DataBaseName + '/' + Company + '/' + Company + '.txt', 'w')

#
# Header of company.
#
file.write ('%1s' % '' + '| ' + '%-20s' % 'Name' + '| ' + '%-10s' % 'Code' + '| ' + '%5s' % 'Price' + '| ' + '%5s' % 'Comment' + '|\n')
for i in range (50):
    file.write ('=')
file.write ('\n')

#
# Data of company
#
for i in range (101):
    file.write ('%1s' % '@' + '| ')
    file.write ('%-20s' % ('ProductB' + str(i)) + '| ')
    file.write ('%-10s' % ('A' + str(i)) + '| ')
    file.write ('%5s' % str(i + 1000) + '|')
    file.write ('%5s' % '' + '|')
    file.write ('\n')
file.close()

#
# Image of company
#
for Index in range (101):
    PicName = 'ProductB' + str(Index)

    Color = (random.randint (0, 255), random.randint (0, 255), 150)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i,j] = Color
    img.save(DataBaseName + '/' + Company + '/' + PicName + '.png')
    
    img_simple = img.resize ((200, 200))
    img_simple.save(DataBaseName + '/' + Company + '/' + PicName + '_Simple' + '.png')
    print (DataBaseName + '/' + Company + '/' + '/' + PicName + '.png' + ' - Create Success')

##############################################################################
#
# Company 3
#
Company = 'ZoeCompany'
if not os.path.isdir(DataBaseName + '/' + Company):
    os.mkdir(DataBaseName + '/' + Company)
file = open (DataBaseName + '/' + Company + '/' + Company + '.txt', 'w')

#
# Header of company.
#
file.write ('%1s' % '' + '| ' + '%-20s' % 'Name' + '| ' + '%-10s' % 'Code' + '| ' + '%5s' % 'Price' + '| ' + '%5s' % 'Comment' + '|\n')
for i in range (50):
    file.write ('=')
file.write ('\n')

#
# Data of company
#
for i in range (50):
    file.write ('%1s' % '@' + '| ')
    file.write ('%-20s' % ('ProductA' + str(i)) + '| ')
    file.write ('%-10s' % ('A' + str(i)) + '| ')
    file.write ('%5s' % str(i + 2000) + '|')
    file.write ('%5s' % '' + '|')
    file.write ('\n')
file.close()

#
# Image of company
#
for Index in range (50):
    PicName = 'ProductA' + str(Index)

    Color = (150, random.randint (0, 255), random.randint (0, 255))
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i,j] = Color
    img.save(DataBaseName + '/' + Company + '/' + PicName + '.png')
    
    img_simple = img.resize ((200, 200))
    img_simple.save(DataBaseName + '/' + Company + '/' + PicName + '_Simple' + '.png')
    print (DataBaseName + '/' + Company + '/' + '/' + PicName + '.png' + ' - Create Success')

##############################################################################
#
# Company 4
#
Company = 'JannyCompany'
if not os.path.isdir(DataBaseName + '/' + Company):
    os.mkdir(DataBaseName + '/' + Company)
file = open (DataBaseName + '/' + Company + '/' + Company + '.txt', 'w')

#
# Header of company.
#
file.write ('%1s' % '' + '| ' + '%-20s' % 'Name' + '| ' + '%-10s' % 'Code' + '| ' + '%5s' % 'Price' + '| ' + '%5s' % 'Comment' + '|\n')
for i in range (50):
    file.write ('=')
file.write ('\n')

#
# Data of company
#
for i in range (1, 49, 2):
    file.write ('%1s' % '@' + '| ')
    file.write ('%-20s' % ('ProductA' + str(i)) + '| ')
    file.write ('%-10s' % ('A' + str(i)) + '| ')
    file.write ('%5s' % str(i + 3000) + '|')
    file.write ('%5s' % '' + '|')
    file.write ('\n')
file.close()

#
# Image of company
#
for Index in range (39, 49, 2):
    PicName = 'ProductA' + str(Index)

    Color = (random.randint (0, 255), 150, random.randint (0, 255))
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixels[i,j] = Color
    img.save(DataBaseName + '/' + Company + '/' + PicName + '.png')
    
    img_simple = img.resize ((200, 200))
    img_simple.save(DataBaseName + '/' + Company + '/' + PicName + '_Simple' + '.png')
    print (DataBaseName + '/' + Company + '/' + '/' + PicName + '.png' + ' - Create Success')

print ('--------- CA_LinkingList.py  End ---------')




