import os
import shutil
import logging
from PIL import Image,ImageTk
import CD_LinkingList as link
from CD_Configuration import *

def CreateCompanyFolder (companyName):
    folder = GLOBAL_CONFIG_DB_FOLDER + '/' + companyName
    fileName = folder + '/' + companyName + '.txt'
    
    os.mkdir (folder)
    file = open (fileName, 'w')
    
    #
    # Header of product list file.
    #
    file.write ('%1s' %'' + '| ')
    file.write ('%-20s' %'Name' + '| ')
    file.write ('%-10s' %'Code' + '| ')
    file.write ('%5s' %'Price' + '| ')
    file.write ('%-90s' %'Comment' + '| ')
    file.write ('\n')
    
    for i in range (140):
        file.write ('=')
    file.write ('\n')
    
    file.close()
    
def RemoveCompanyFolder (companyName):
    folder = GLOBAL_CONFIG_DB_FOLDER + '/' + companyName
    shutil.rmtree (folder)
    
#
# The function is used to modify picture name or add or modify picture.
#
# Only below parameters group can be entered at the same time.
#     Input : oriName              => Delete picture.
#     Input : oriName  + modName   => Modify picture name.        => return Tk resized image .
#     Input : oriName  + picPath   => Add picture of product.
#
# @company      Company name of product belong.
# @oriName      The name before modified product name.
# @modName      The name of modified product name.
# @picPath      New picture path.
#
def ProductImageModify (company, oriName=None, modName=None, picPath=None):
    if oriName != None:
        oriFileName = GLOBAL_CONFIG_DB_FOLDER + '/' + company + '/' + oriName + '.png'
        oriFileSimpleName = GLOBAL_CONFIG_DB_FOLDER + '/' + company + '/' + oriName + '_Simple.png'
    if modName != None:
        modFileName = GLOBAL_CONFIG_DB_FOLDER + '/' + company + '/' + modName + '.png'
        modFileSimpleName = GLOBAL_CONFIG_DB_FOLDER + '/' + company + '/' + modName + '_Simple.png'
    
    #
    # Modify picture name.
    #
    if (oriName!=None) and (modName!=None) and (picPath==None):
        if os.path.exists(oriFileName):
            os.rename (oriFileName, modFileName)
            os.rename (oriFileSimpleName, modFileSimpleName)

    #
    # Add picture of product.
    #
    elif (oriName!=None) and (modName==None) and (picPath!=None):
        im = Image.open (picPath)
        imResize = im.resize ((200, 200))
        imTk = ImageTk.PhotoImage(imResize)
        
        if os.path.exists(oriFileName):
            os.remove (oriFileName)
            os.remove (oriFileSimpleName)
        
        im.save (oriFileName)
        imResize.save (oriFileSimpleName)
        return imTk
        
    #
    # Delete picture.
    #
    elif (oriName!=None) and (modName==None) and (picPath==None):
        if os.path.exists(oriFileName):
            os.remove (oriFileName)
            os.remove (oriFileSimpleName)
    else:
        logging.warning ('Parameter Error!!')
        assert False

def ExportProduct (companyName, productList):
    assert isinstance(productList, link.ProductList)
    
    file = open (GLOBAL_CONFIG_DB_FOLDER + '/' + companyName + '/' + companyName + '.txt', 'w')
        
    #
    # Header of product list file.
    #
    file.write ('%1s' %'' + '| ')
    file.write ('%-20s' %'Name' + '| ')
    file.write ('%-10s' %'Code' + '| ')
    file.write ('%5s' %'Price' + '| ')
    file.write ('%-90s' %'Comment' + '| ')
    file.write ('\n')
    
    for i in range (140):
        file.write ('=')
    file.write ('\n')
    
    currentProduct = productList.GetFirst()
    while currentProduct != None:
        name = currentProduct.Name.GetData()
        code = currentProduct.Code.GetData()
        price = currentProduct.Price.GetData()
        comment = currentProduct.comment
        
        file.write ('%1s' %'@' + '| ')
        file.write ('%-20s' %name + '| ')
        file.write ('%-10s' %code + '| ')
        file.write ('%5s' %price + '| ')
        file.write ('%-90s' %comment + '| ')
        file.write ('\n')

        currentProduct = currentProduct.GetNext()
        
    file.close()

def ExportCompany (companyList):
    assert isinstance(companyList, link.CompanyList)
    
    file = open (GLOBAL_CONFIG_DB_PATH, 'w')
        
    #
    # Header of product list file.
    #
    file.write ('%1s' %'' + '| ')
    file.write ('%-20s' %'Name' + '| ')
    file.write ('%-10s' %'Code' + '| ')
    file.write ('\n')
    
    for i in range (140):
        file.write ('=')
    file.write ('\n')
    
    currentNode = companyList.GetFirst()
    while currentNode != None:
        name = currentNode.Name.GetData()
        code = currentNode.Code.GetData()
        
        file.write ('%1s' %'@' + '| ')
        file.write ('%-20s' %name + '| ')
        file.write ('%-10s' %code + '| ')
        file.write ('\n')

        currentNode = currentNode.GetNext()
        
    file.close()

# 
# Load database and record to linking list
#
# @RETURN Database linking list.
#
def LoadDatabase():

    #
    # First, load all company list.
    #
    try:
        rootFile = open (GLOBAL_CONFIG_DB_PATH, 'r')
    except FileNotFoundError:
        print ('WARNING! No database exist!!!!!')
        raise

    database = link.CompanyList()
    for eachLine in rootFile:
        strList = eachLine.split ('|')
        
        if strList[0] == '@':

            #
            # StrList[1].strip() : Company name
            # StrList[2].strip() : Company code
            #
            companyNode = link.CompanyNode(strList[1].strip(), strList[2].strip())
            database.AddNode (companyNode)

    rootFile.close()

    #
    # Second, load all company data according to company list.
    #
    CurrentCompany = database.Header.Name.GetNextNode()

    while CurrentCompany != None:
        CompanyPath = GLOBAL_CONFIG_DB_FOLDER + '/' + CurrentCompany.Name.GetData() + '/'
        CompanyProductFile = CompanyPath + CurrentCompany.Name.GetData() + '.txt'

        if not os.path.exists(CompanyProductFile):
            print ('WARNING! No company data exist!!!!! (%s)' % CompanyProductFile)
            
        else:
            logging.info (CompanyProductFile)
            File = open (CompanyProductFile, 'r')

            ProductList1 = CurrentCompany.ProductListHeader

            for EachLine in File:
                StrList = EachLine.split ('|')
                
                if StrList[0] == '@':
                    ProductNode1 = link.ProductNode()
                    ProductNode1.Name.SetData (StrList[1].strip())
                    ProductNode1.Code.SetData (StrList[2].strip())
                    ProductNode1.Price.SetData (StrList[3].strip())

                    #
                    # Open simple picture according to product name.
                    #
                    PicName = CompanyPath + ProductNode1.Name.GetData() + '_Simple.png'
                    
                    if os.path.exists(PicName):
                        im = Image.open(PicName)
                        imTk = ImageTk.PhotoImage(im)
                        im.close()
                    else:
                        imTk = None
                        
                    ProductNode1.Image = imTk
                    ProductNode1.comment = (StrList[4].strip())
                    
                    ProductList1.AddNode(ProductNode1)
            File.close()

        CurrentCompany = CurrentCompany.Name.GetNextNode()
    
    return database
    
if __name__ == '__main__':
    a = link.ProductList()
    ExportProduct ('HappyCompany', a)
