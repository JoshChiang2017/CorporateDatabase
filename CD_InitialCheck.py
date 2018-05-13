import os

## Linking list
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
    def __init__(self, Name = 'NULL', Code = 'NULL', Price = 0, Image = None):
        
        self.Name = ListNode()
        self.Code = ListNode()
        self.Price = ListNode()
        self.Image = Image

        self.Name.SetData (Name)
        self.Code.SetData (Code)
        self.Price.SetData (Price)

    def SetProductNodeData(self, NewData):
        self.Name.SetData (NewData.Name.GetData())
        self.Code.SetData (NewData.Code.GetData())
        self.Price.SetData (NewData.Price.GetData())
        self.Image = NewData.Image
        
class ProductList (object):
    def __init__(self):
        self.Header = ProductNode()
        self.TotalNodeNumber = 0

    def IsEmpty (self):
        return self.Header.Name.NextNode == None
    
    def GetHeader(self):
        return self.Header
    
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
    # Find specific ProductNode by product name.
    #
    def Find (self, SearchName):
        assert isinstance(SearchName, str)
        CurrentNode = self.Header.Name.GetNextNode()

        while CurrentNode != None:
            if CurrentNode.Name.GetData() > SearchName:
                #
                # No fit
                #
                return None
            
            elif CurrentNode.Name.GetData() == SearchName:
                return CurrentNode
            else:
                CurrentNode = CurrentNode.Name.GetNextNode()

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
        self.ProductListHeader = ProductList ()
        
        self.Name.SetData (Name)
        self.Code.SetData (Code)

class CompanyList (object):
    def __init__(self):
        self.Header = CompanyNode ()
        self.TotalNodeNumber = 0

    def IsEmpty (self):
        return self.Header.CompanyName.NextNode == None
    
    def GetHeader(self):
        return self.Header
    
    def NewCompanyNode(self, Name = 'NULL', Code = 'NULL'):
        assert isinstance(Name, str)
        assert isinstance(Code, str)
        
        self.TotalNodeNumber += 1
        NewNode = CompanyNode (Name, Code)
    
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
    # Find specific ProductNode by product name.
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
    
    def FindProduct (self, CompanyName, ProductName):
        assert isinstance(CompanyName, str)
        assert isinstance(ProductName, str)
        
        CurrentCompany = self.FindCompany (CompanyName)
        CurrentProducr = CurrentCompany.ProductListHeader.Header.Name.GetNextNode ()

        while CurrentProducr != None:
            if CurrentProducr.Name.GetData() > ProductName:
                #
                # No fit
                #
                return None
            
            elif CurrentProducr.Name.GetData() == ProductName:
                return CurrentProducr
            else:
                CurrentProducr = CurrentProducr.Name.GetNextNode()

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
    L1.NewCompanyNode('CompanyA', 'aaa')
    L1.NewCompanyNode('CompanyC', 'ccc')
    L1.NewCompanyNode('CompanyE', 'eee')
    L1.Print()
    
    L1.NewCompanyNode('CompanyB', 'bbb')
    L1.NewCompanyNode('CompanyD', 'ddd')
    L1.Print()
    
    print ('--------- CA_LinkingList.py  End ---------')

