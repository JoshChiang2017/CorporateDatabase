import os
import time
import logging
import CD_LinkingList as link
import CD_Configuration as CONF

class HistoryLog(object):
    def __init__(self, company):
        assert isinstance (company, str)
        
        self.fileName = CONF.GLOBAL_CONFIG_LOG_PATH
        self.company = company
        self.addFile = '\n'
        self.removeFile = '\n'
        self.modifyFile = '\n'
        
        if not os.path.isdir(CONF.GLOBAL_CONFIG_DB_FOLDER):
            os.mkdir(CONF.GLOBAL_CONFIG_DB_FOLDER)

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
class CompanyHistoryLog(object):
    def __init__(self):
        
        self.fileName = CONF.GLOBAL_CONFIG_LOG_PATH
        self.company = CONF.GLOBAL_CONFIG_DB_FOLDER
        self.addFile = '\n'
        self.removeFile = '\n'
        self.modifyFile = '\n'
        
        if not os.path.isdir(CONF.GLOBAL_CONFIG_DB_FOLDER):
            os.mkdir(CONF.GLOBAL_CONFIG_DB_FOLDER)

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
        
    def SetAddFile (self, companyNode):
        assert isinstance (companyNode, link.CompanyNode)
        self.addFile += self.ObjectToString (companyNode)
        
    def SetRemoveFile (self, companyNode):
        assert isinstance (companyNode, link.CompanyNode)
        self.removeFile += self.ObjectToString (companyNode)
        
    def SetModifyFile (self, preNode, postNode):
        assert isinstance (preNode, link.CompanyNode)
        assert isinstance (postNode, link.CompanyNode)

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

    def ObjectToString(self, companyNode):
        string = '    '
        string += '%-20s' %companyNode.Name.GetData() + '| '
        string += '%-10s' %companyNode.Code.GetData() + '| '
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
    


        
