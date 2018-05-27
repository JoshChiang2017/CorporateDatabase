import os
import CD_LinkingList as link

def ExportCompany (companyName, productList):
    assert isinstance(productList, link.ProductList)
    
    file = open ('database/' + companyName + '/' + companyName + '.txt', 'w')
        
    #
    # Header of company.
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

if __name__ == '__main__':
    a = link.ProductList()
    ExportCompany ('HappyCompany', a)
