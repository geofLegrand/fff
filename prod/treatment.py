import pandas as pd
import os
from datetime import datetime
from file_treat.yaml_treat import YamlFile


class Treatment(object):
    conf = YamlFile().red_yaml_file(os.getenv('CONFIG_PATH'))

    def __init__(self):

        self.dict_lbl =  Treatment.conf['content']['point_vente'] 
        #  { 
            
        #     '4000':'AGENT MANDATAIRE',
        #     '2003':'BUREAU DIRECT SIEGE',
        #     '2005':'BUREAU DIRECT PETIT PARIS',
        #     '2004':'BUREAU DIRECT POG',
        #     '2000':'BUREAU DIRECT FRANGIPANIER',
        #     '2006':'BUREAU DIRECT MOUILA',
        #     '2007':'BUREAU DIRECT CAMPAGNE',
        #     '2008':'BUREAU DIRECT AKANDA',
        #     '2009':'BUREAU DIRECT MAKOKOU',
        #     '5001':'ECOBANK',
        #     '5004':'BICIG',
        #     '5007':'EDG'
        # }


    def libelle_point_vente(self,code:str):

        return self.dict_lbl.get(code)
    
    
    def code_point_vente(self,police:str):
        
        if(police[0:2] == 'GB'):
            return self.dict_lbl.get(police[2:6])
        else:
            return self.dict_lbl.get(police[0:4])
    
    def export_to_excel(self,df,filename):
        f = f"{filename}_{str(datetime.now()).replace('.','_').replace(':','_')}.xlsx"
        with pd.ExcelWriter(f) as writer:
            df.to_excel(writer)
        return f
        
    def get_encaissement(self,police,quittance,dff):

        for col,row in dff.iterrows():
            if str(row[0]) == police and str(row[1]) == quittance:
                return row[2]  
        
