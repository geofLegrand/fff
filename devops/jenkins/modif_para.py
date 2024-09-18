import yaml
import pprint
import sys, os
from datetime import date,datetime,timedelta



_path = sys.argv[1] # config file path
field = sys.argv[2] # yaml field at modify
field_value = sys.argv[3] # yaml field value

class YamlFile:

    
    def red_yaml_file(self,yaml_file_path):
        _yaml_file = {}
        #print(yaml_file_path)
        try:
            with open(yaml_file_path,'r') as yaml_doc:
                _yaml_file = yaml.load(yaml_doc,Loader=yaml.FullLoader) #,Loader=yaml.FullLoader
            return _yaml_file

        except Exception as e:
            print("Erreur",e)
            return []
            

    def write_yaml_file(self,file_save,_yaml_file):
        try:
            with open(file_save,'w') as yaml_doc:
                g = yaml.dump(_yaml_file)
                yaml_doc.write(g)
                print("file save successfully !")
        except Exception as e:

            print("Erreur",e)

    


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






def update_yaml_file(field,value_field):
    json_file = YamlFile().red_yaml_file(_path)
    funct = {
        "label" : YamlModify(json_file).modif_label(value_field)
    }

    json_file = funct[field]
    
    YamlFile().write_yaml_file('config.yaml',json_file)


if __name__ == '__main__':
    print(f"=============== !!!! Début du processus de modification !!! =============== {datetime.now()}\n")
    update_yaml_file(field,field_value)

