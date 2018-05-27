import os
import time
import logging
import CD_LinkingList as link

class HistoryLog(object):
    def __init__(self, company):
        assert isinstance (company, str)
        
        self.fileName = 'database/History.log'
        self.company = company
        self.addFile = '\n'
        self.removeFile = '\n'
        self.modifyFile = '\n'
        
        if not os.path.isdir('database'):
            os.mkdir('database')

        if not os.path.exists (self.fileName):
            logging.info ('New %s create.' %self.fileName)
            file = open (self.fileName, 'w')
            timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            file.write ('Time : %s\n' %timeNow)
            file.write ('Company : \n')
            file.write ('Add : %s\n' %self.fileName)
            file.write ('Remove : \n')
            file.write ('Modify : \n')
            file.close()
        
    def SetAddFile (self, productNode):
        assert isinstance (productNode, link.ProductNode)
        self.addFile += self.ObjectToString (productNode)
        
    def SetRemoveFile (self, productNode):
        assert isinstance (productNode, link.ProductNode)
        self.removeFile += self.ObjectToString (productNode)
        
    def SetModifyFile (self, preNode, postNode):
        assert isinstance (preNode, link.ProductNode)
        assert isinstance (postNode, link.ProductNode)

        preString = self.ObjectToString (preNode)
        postString = self.ObjectToString (postNode)
        self.modifyFile += preString + '  =>' + postString
        
    def AddLog (self):
        file = open (self.fileName, 'a')
        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        for i in range(50):
            file.write ('*')
        file.write ('\nTime : %s\n' %timeNow)
        file.write ('Company : %s\n' %self.company)
        file.write ('Add :')
        file.write ('%s' %self.addFile)
        file.write ('Remove :')
        file.write ('%s' %self.removeFile)
        file.write ('Modify :')
        file.write ('%s' %self.modifyFile)
        file.write ('\n')
        file.close()

    def ObjectToString(self, productNode):
        string = '    '
        string += '%-20s' %productNode.Name.GetData() + '| '
        string += '%-10s' %productNode.Code.GetData() + '| '
        string += '%5s' %productNode.Price.GetData() + '| '
        string += '\n'

        return string

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    for k in range(6):
        a = HistoryLog()
        a.SetCompany('Company%d' %k)
        
        for i in range(3):
            a.SetAddFile('Add%d' %i)
        for i in range(2):
            a.SetRemoveFile('Bbb%d' %i)
        for i in range(2):
            a.SetModifyFile('Ccc%02d' %i, '666')

        a.AddLog()
    


        
