import yaml
import pprint
import sys, os
from datetime import date,datetime,timedelta
from file_treat.yaml_mod import YamlModify


class YamlFile:

    
    def red_yaml_file(self,yaml_file_path):
        _yaml_file = {}
        print(yaml_file_path)
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

    



def update_yaml_file(field,value_field):
    json_file = YamlFile().red_yaml_file(_path)
    funct = {
        "label" : YamlModify(json_file).modif_label(value_field)
    }

    json_file = funct[field]
    
    YamlFile().write_yaml_file('config.yaml',json_file)


if __name__ == '__main__':
    print(f"=============== !!!! Début du processus de modification !!! =============== {datetime.now()}\n")
    #update_yaml_file(field,field_value)

    

    # r = YamlFile().red_yaml_file(_path)

    # pprint.pprint(r)