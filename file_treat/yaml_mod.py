
class YamlModify:

    def __init__(self, file):
        self.file = file


    def modif_label(self,value):

        if self.file: 
            self.file['mod']['label'] = value
        return self.file

    def modif_readDir(self,value):
        if self.file: 
            self.file['mod']['readDir'] =  value 
        return self.file

    def modif_readDir(self,value):
        if self.file: 
            self.file['mod']['backupDir'] =  value 
        return self.file
    
    def modif_readDir(self,value):
        if self.file: 
            self.file['mod']['dbPath'] =  value 
        return self.file

    def modif_sender(self,value):
        if self.file: 
            self.file['mod']['sender'] =  value 
        return self.file

    def modif_smtpserver(self,value):
        if self.file: 
            self.file['mod']['smtpserver'] =  value 
        return self.file



