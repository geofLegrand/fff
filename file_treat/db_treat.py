import json
import os 
from datetime import datetime,date
from file_treat.yaml_treat import YamlFile 



class ExecuteDate:

    conf = YamlFile().red_yaml_file(os.getenv('CONFIG_PATH'))
    db_path = conf['mod']['dbPath']  #os.getenv("DB_PATH")

    def __init__(self,date_start,date_end,log = ""):
        self.date_start = date_start
        self.date_end = date_end
        self.date_create = str(datetime.now())
        self.log = log 


    
    def __write_json(self,data):
        try :
            with open(ExecuteDate.db_path, 'w') as file :
                json.dump(data, file, indent=4)
            return True
        except:
            return False


    def __read_json(self):

        try:
            
            with open(ExecuteDate.db_path, 'r') as file:

                return json.load(file)

        except json.decoder.JSONDecodeError  :
            return []
        except FileNotFoundError:
            print("""The database file is not find""")



    def create_record(self):
        if self.read_item() != 0 :
            return True 
            
        data = self.__read_json()
         

        data.append(
            {
                'date_start': self.date_start,
                'date_end' : self.date_end,
                'date_create': self.date_create,
                'log' : self.log  
            })

        return self.__write_json(data)


    def read_items(self):
        return self.__read_json()



    def read_item(self):
    
        return len(list(filter(lambda x : x['date_start'] == self.date_start and
                             x['date_end'] == self.date_end, self.__read_json())))


    def delete_record(self):
        data = self.__read_json()
        data = [record for record in data 
               if record['date_start'] != self.date_start and record['date_end'] != self.date_end ]
        return self.__write_json(data)



if __name__ == '__main__':
    print(f"=============== !!!! Début du processus !!! =============== {str(date.today())}\n")
    #print(os.getenv("DB_PATH"))
    execData = ExecuteDate(str(date.today()),str(date.today()))
    
    print(execData.read_items())
    
    print(execData.read_item())
