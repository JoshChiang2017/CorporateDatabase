import os
import shutil
import CD_LinkingList as link

def CreateCompanyFolder (companyName):
    folder = 'database/' + companyName
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
    folder = 'database/' + companyName
    shutil.rmtree (floder)

def ExportProduct (companyName, productList):
    assert isinstance(productList, link.ProductList)
    
    file = open ('database/' + companyName + '/' + companyName + '.txt', 'w')
        
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
    
    file = open ('database/TotalCompanyList.txt', 'w')
        
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
    
if __name__ == '__main__':
    a = link.ProductList()
    ExportProduct ('HappyCompany', a)
