import logging

## Linking list
#
# pre  = previous
# peri = period
#
# Company
#     Column     : Name | Code |
#     MaxSize    :   20 |   10 |
#
# Product
#     Colomn     : Name | Code | Price|
#     MaxSize    :   20 |   10 |     5|

class ListNode (object):
    def __init__ (self):
        self.NextNode = None
        self.NodeData = 0
        
    def GetNextNode(self):
        return self.NextNode
    
    def SetNextNode (self, NextNode):
        self.NextNode = NextNode

    def GetData(self):
        return self.NodeData
    
    def SetData (self, NodeData):
        self.NodeData = NodeData
        
class ProductNode (object):
    def __init__(self, Name = 'NULL', Code = 'NULL', Price = 0, Image = None, comment = 'NULL'):
        
        self.Name = ListNode()
        self.Code = ListNode()
        self.Price = ListNode()
        self.Image = Image
        self.comment = comment

        self.Name.SetData (Name)
        self.Code.SetData (Code)
        self.Price.SetData (Price)

    def SetProductNodeData(self, NewData):
        self.Name.SetData (NewData.Name.GetData())
        self.Code.SetData (NewData.Code.GetData())
        self.Price.SetData (NewData.Price.GetData())
        self.Image = NewData.Image
        self.comment = NewData.comment

    def GetNext (self):
        return self.Name.GetNextNode()
    
    def GetName (self):
        return self.Name.GetData()
        
class ProductList (object):
    def __init__(self, companyName = None):
        self.Header = ProductNode()
        self.companyName = companyName
        self.TotalNodeNumber = 0

    def IsEmpty (self):
        return self.Header.Name.NextNode == None
    
    def GetFirst(self):
        return self.Header.Name.GetNextNode()

    def AddNode(self, NewNodeInput):
        assert isinstance(NewNodeInput, ProductNode)
        
        self.TotalNodeNumber += 1
        NewNode = ProductNode()
        NewNode.SetProductNodeData(NewNodeInput)
    
        #
        # Add Name List
        #
        PreNode = self.Header
        CurrentNode = self.Header.Name.GetNextNode()
        
        while CurrentNode != None:
            
            if CurrentNode.Name.GetData() > NewNode.Name.GetData():
                break
            else:
                PreNode = CurrentNode
                CurrentNode = CurrentNode.Name.GetNextNode()
        
        NewNode.Name.SetNextNode (CurrentNode)
        PreNode.Name.SetNextNode (NewNode)
    
        #
        # Add Code List
        #
        PreNode = self.Header
        CurrentNode = self.Header.Code.GetNextNode()
        
        while CurrentNode != None:
            
            if CurrentNode.Code.GetData() > NewNode.Code.GetData():
                break
            else:
                PreNode = CurrentNode
                CurrentNode = CurrentNode.Code.GetNextNode()
        
        NewNode.Code.SetNextNode (CurrentNode)
        PreNode.Code.SetNextNode (NewNode)
    
        #
        # Add Price List
        #
        PreNode = self.Header
        CurrentNode = self.Header.Price.GetNextNode()
        
        while CurrentNode != None:
            if CurrentNode.Price.GetData() > NewNode.Price.GetData():
                break
            else:
                PreNode = CurrentNode
                CurrentNode = CurrentNode.Price.GetNextNode()
        
        NewNode.Price.SetNextNode (CurrentNode)
        PreNode.Price.SetNextNode (NewNode)

    #
    # @removeNodeNmae the remove node product name
    #
    # @return  True   Node remove successfully
    # @return  False  Node remove failed.
    #
    def RemoveNode (self, removeNodeNmae):
        assert isinstance(removeNodeNmae, str)

        preNode = self.Header
        periNode = preNode.GetNext()

        while periNode != None:
            if periNode.Name.GetData() == removeNodeNmae:
                preNode.Name.SetNextNode (periNode.Name.GetNextNode ())
                preNode.Code.SetNextNode (periNode.Code.GetNextNode ())
                preNode.Price.SetNextNode (periNode.Price.GetNextNode ())
                break

            preNode = periNode
            periNode = periNode.GetNext()

        logging.warning('RemoveNode:')
        logging.warning('  Company : %s' %self.companyName)
        logging.warning('  Product : %s' %removeNodeNmae)
        #
        # If specific node is not found.
        #
        if periNode == None:
            logging.warning('The node want to remove is not exist.')
            return False
        else:
            logging.info('The node remove successfully.')
            return True

    #
    # Note! This function will not modify picture in the database.
    # It must to consider that modify picture name when modify product name.
    #
    # @oriProductName  Product name of modify node
    # @modifyNode         
    #
    def ModifyNode (self, oriProductName, modifyNode):
        assert isinstance(oriProductName, str)
        assert isinstance(modifyNode, ProductNode)

        #
        # Remove original node and add modify node.
        #
        if self.RemoveNode (oriProductName) == True:
                    
            logging.info('AddNode:')
            logging.info('  Company : %s' %self.companyName)
            logging.info('  Product : %s' %modifyNode.GetName())
            self.AddNode (modifyNode)
        
    #
    # Find specific ProductNode by product name.
    #
    def Find (self, searchName):
        assert isinstance(searchName, str)
        currentNode = self.GetFirst()

        while currentNode != None:
            if currentNode.Name.GetData() > searchName:
                #
                # No fit
                #
                return None
            
            elif currentNode.Name.GetData() == searchName:
                return currentNode
            else:
                currentNode = currentNode.GetNext()

    def Print (self):
        CurrentNode = self.Header.Name.GetNextNode()
        Index = 0
        print ('====================Linking List Content Start====================')
        print ('Total product in this company is ' + str(self.TotalNodeNumber))
        
        while CurrentNode != None:
            Index += 1
            print ('Node (%3s) :' %  Index, end = '')
            print ('%-20s' % CurrentNode.Name.GetData(), end = '')
            print ('%-10s' % CurrentNode.Code.GetData(), end = '')
            print ('%10s' % CurrentNode.Price.GetData())
            
            CurrentNode = CurrentNode.Name.GetNextNode()
            
        print ('====================Linking List Content End====================')

class CompanyNode (object):
    def __init__(self, Name = 'NULL', Code = 'NULL'):
        
        self.Name = ListNode ()
        self.Code = ListNode ()
        self.ProductListHeader = ProductList (Name)
        
        self.Name.SetData (Name)
        self.Code.SetData (Code)
        
    def GetNext(self):
        return self.Name.GetNextNode ()
        
    def GetName(self):
        return self.Name.GetData ()

class CompanyList (object):
    def __init__(self):
        self.Header = CompanyNode ()
        self.TotalNodeNumber = 0

    def IsEmpty (self):
        return self.Header.Name.GetNextNode() == None
    
    #
    # Check whether all company have no product.
    #
    def HaveAnyPoduct (self):
        company = self.GetFirst()
        while company != None:
            if not company.ProductListHeader.IsEmpty():
                return True
            company = company.GetNext()
            
        return False
    
    def GetFirst (self):
        return self.Header.Name.GetNextNode()
    
    def AddNode (self, newNode):
        assert isinstance(newNode, CompanyNode)
        
        self.TotalNodeNumber += 1
    
        #
        # Add Name List
        #
        preNode = self.Header
        periNode = self.Header.Name.GetNextNode()
        
        while periNode != None:
            
            if periNode.GetName() > newNode.GetName():
                break
            else:
                preNode = periNode
                periNode = periNode.GetNext()
        
        newNode.Name.SetNextNode (periNode)
        preNode.Name.SetNextNode (newNode)
    
        #
        # Add Code List
        #
        preNode = self.Header
        periNode = self.Header.Code.GetNextNode()
        
        while periNode != None:
            
            if periNode.Code.GetData() > newNode.Code.GetData():
                break
            else:
                preNode = periNode
                periNode = periNode.Code.GetNextNode()
        
        newNode.Code.SetNextNode (periNode)
        preNode.Code.SetNextNode (newNode)
    
    #
    # @removeNodeName the remove node product name
    #
    # @return  True   Node remove successfully
    # @return  False  Node remove failed.
    #
    def RemoveNode (self, removeNodeName):
        assert isinstance(removeNodeName, str)

        preNode = self.Header
        periNode = preNode.GetNext()

        while periNode != None:
            if periNode.Name.GetData() == removeNodeName:
                preNode.Name.SetNextNode (periNode.Name.GetNextNode ())
                preNode.Code.SetNextNode (periNode.Code.GetNextNode ())
                break

            preNode = periNode
            periNode = periNode.GetNext()

        logging.info('RemoveNode:')
        logging.info('  Company : %s' %removeNodeName)
        #
        # If specific node is not found.
        #
        if periNode == None:
            logging.warning('The node want to remove is not exist.')
            return False
        else:
            logging.info('The node remove successfully.')
            return True

    #
    # Note! This function will not modify picture in the database.
    # It must to consider that modify picture name when modify product name.
    #
    # @oriProductName  Product name of modify node
    # @modifyNode         
    #
    def ModifyNode (self, oriCompanyName, modifyNode):
        assert isinstance(oriCompanyName, str)
        assert isinstance(modifyNode, CompanyNode)
        
        node = self.FindCompany (oriCompanyName)
        
        if node != None:
            node.Name.SetData (modifyNode.Name.GetData())
            node.Code.SetData (modifyNode.Code.GetData())
            
            logging.info('Modify Company Node:')
            logging.info('    %s => %s' %(node.Name.GetData(), modifyNode.Name.GetData()))
            logging.info('    %s => %s' %(node.Code.GetData(), modifyNode.Code.GetData()))

    #
    # If company code exist return company name, else return None
    #
    def IsCompanyCodeExist (self, CompanyCode):
        assert isinstance(CompanyCode, str)
        
        CurrentCompany = self.Header.Code.GetNextNode()
        
        while CurrentCompany != None:
            if CurrentCompany.Code.GetData() > CompanyCode:
                #
                # No fit
                #
                return None
            
            elif CurrentCompany.Code.GetData() == CompanyCode:
                return CurrentCompany.Name.GetData()
            else:
                CurrentCompany = CurrentCompany.Code.GetNextNode()
        
    #
    # Find specific CompanyNode by company name.
    #
    def FindCompany (self, CompanyName):
        assert isinstance(CompanyName, str)
        
        CurrentCompany = self.Header.Name.GetNextNode()

        while CurrentCompany != None:
            if CurrentCompany.Name.GetData() > CompanyName:
                #
                # No fit
                #
                return None
            
            elif CurrentCompany.Name.GetData() == CompanyName:
                return CurrentCompany
            else:
                CurrentCompany = CurrentCompany.Name.GetNextNode()
                
    #
    # Find specific CompanyNode by company name.
    #
    def FindCompanyData (self, CompanyName):
        if self.FindCompany(CompanyName) != None:
            return self.FindCompany(CompanyName).ProductListHeader
        else:
            return None
    
    #
    # Find specific ProductNode by product name.
    #
    def FindProduct (self, CompanyName, ProductName):
        assert isinstance(CompanyName, str)
        assert isinstance(ProductName, str)
        
        CurrentCompany = self.FindCompanyData (CompanyName)
        CurrentProduct = CurrentCompany.Header.Name.GetNextNode ()

        while CurrentProduct != None:
            if CurrentProduct.Name.GetData() > ProductName:
                #
                # No fit
                #
                return None
            
            elif CurrentProduct.Name.GetData() == ProductName:
                return CurrentProduct
            else:
                CurrentProduct = CurrentProduct.Name.GetNextNode()

    def Print (self):
        CurrentNode = self.Header.Name.GetNextNode()
        Index = 0
        print ('====================Linking List Content Start====================')
        print ('Total company in this database is ' + str(self.TotalNodeNumber))

        while CurrentNode != None:
            Index += 1
            print ('Node (%3s) :' %  Index, end = '')
            print ('%-20s' % CurrentNode.Name.GetData(), end = '')
            print ('%-10s' % CurrentNode.Code.GetData())
            
            CurrentNode = CurrentNode.Name.GetNextNode()
            
        print ('====================Linking List Content End====================')

#
# Simple test of this module.
#
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    print ('--------- CA_LinkingList.py  Start ---------')
    
    a = ProductNode ('ProductA', 'Aaa', 10)
    b = ProductNode ('ProductB', 'Bbb', 20)
    c = ProductNode ('ProductC', 'Ccc', 30)
    d = ProductNode ('ProductD', 'Ddd', 40)
    e = ProductNode ('ProductE', 'Eee', 50)
    
    L = ProductList()
    L.AddNode(a)
    L.AddNode(c)
    L.AddNode(e)
    L.Print()
    
    L.AddNode(b)
    L.AddNode(d)
    L.Print()
    
    L1 = CompanyList()
    LL1 = CompanyNode ('CompanyA', 'aaa')
    L1.AddNode(LL1)
    LL1 = CompanyNode ('CompanyC', 'ccc')
    L1.AddNode(LL1)
    LL1 = CompanyNode ('CompanyE', 'eee')
    L1.AddNode(LL1)
    L1.Print()
    
    LL1 = CompanyNode ('CompanyB', 'bbb')
    L1.AddNode(LL1)
    LL1 = CompanyNode ('CompanyD', 'ddd')
    L1.AddNode(LL1)
    L1.Print()
    
    print ('--------- CA_LinkingList.py  End ---------')

