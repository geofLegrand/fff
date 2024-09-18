import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path
from prod.treatment import Treatment
from prod.emailbody import BuildBodyEmail 
from prod.separatevalue import SeparateValue
from file_treat.yaml_treat import YamlFile

load_dotenv()

#print(Path(__file__).parent / ".env")


class Rapport():

    conf = YamlFile().red_yaml_file(os.getenv('CONFIG_PATH'))

    def __init__(self,periode:str):
            self.filename = ""
            self.periode = periode
        

    def broullard_de_caisse(self):

        self.filename = os.path.join(Rapport.conf['mod']['readDir'],'Brouillard de Caisse.xlsx')

        if os.path.exists(self.filename):
            df0 = pd.read_excel(self.filename,sheet_name='Brouillard de Caisse')

            df0 = df0.iloc[7:]
            #print(df0.shape)
            if df0.shape[0] == 4:
                return 'no'
            else: 

                df0 = df0[['Unnamed: 0','Unnamed: 1','Unnamed: 4','Unnamed: 5','Unnamed: 6','Unnamed: 7'
                        ,'Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 17']]
                
                df0.columns = ['Numero_Client','Nom_et_Prénoms','Police','Avenant','Quittance','Prime_TTC'
                            ,'Encaissé','Date_encaiss','Mode_Paiement','Numero_Recu','Référence','Numéro_Cheque','Banque','Utilisateur']
                
                df0 = df0.pivot_table(index = ['Police','Quittance'],values=['Encaissé'], aggfunc=['sum','count']).reset_index()

                df0.columns = ['Police','Quittance','Encaissé','Nbre_enc']

                df0 = df0.fillna(0)

        return df0


    def journal_de_production(self):

        self.filename =  os.path.join(Rapport.conf['mod']['readDir'],'Journal de Production.xlsx')

        if os.path.exists(self.filename):
            df = pd.read_excel(self.filename,sheet_name="Journal de Production")
            df = df.iloc[8:-1]
            
            #print(df.shape) 

            if df.shape[0] == 0 :
                return 'no'
            else :
                df = df[['Unnamed: 1','Unnamed: 2','Unnamed: 6','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11',
                        'Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 15','Unnamed: 16','Unnamed: 17','Unnamed: 18',
                        'Unnamed: 19','Unnamed: 20','Unnamed: 21','Unnamed: 22','Unnamed: 23','Unnamed: 24','Unnamed: 26']]
                
                df.columns =['Produit','Client','Police','Avenant','Quittance','Mvt','Emission','Effet',
                            'Expiration','Prime_Nette','Prime_Cedee','Acc_comp','Acc_app','Taxes','Carte_Rose',
                            'Css','Tvl','Cstat_Amiable','Prime_TTC','Com_Aperiteur','Com_Conseiller','Redacteur']
                
                df['Point Vente'] = [Treatment().code_point_vente(e) for e in df['Police']]

                df['Mouvement'] = [ Rapport.conf['content']['mouvement'].get(e.lower()) for e in df['Mvt'] ]

        return df 
    
    
    def join_data(self,df_prod : pd.DataFrame,df_enc: pd.DataFrame):

        df_prod['Encaissement'] = [Treatment().get_encaissement(e[0],e[1],df_enc) for _,e in df_prod[['Police','Quittance']].iterrows()]

        df_prod = df_prod.fillna(0).reset_index()

        file = os.path.join(Rapport.conf['mod']['backupDir'],"Production vs Encaissement") #  os.getenv('SAVE_FILES_DIRECTORY')

        file +=" "+ self.periode

        file = Treatment().export_to_excel(df_prod,file)

        return {
            'filename':file,
            'data':df_prod
        } 
    

    def stat_par_points(self,df_prod:pd.DataFrame,pivot):
        
        if pivot == 'Client':
            p1 = df_prod.pivot_table(index = [pivot],values=['Prime_TTC','Encaissement'], aggfunc='sum').reset_index()\
            .sort_values(by='Prime_TTC',ascending=False).head(10)
            
        else: 
            p1 = df_prod.pivot_table(index = [pivot],values=['Prime_TTC','Encaissement'], aggfunc='sum').reset_index()

        p2 = df_prod.pivot_table(index = [pivot], values='Police', aggfunc='count').reset_index()


        p1['Taux_En'] = [ str(int(round((e[1]/e[0])*100,0)))+"%" if e[0] != 0 else  '0%' for _,e in p1[['Prime_TTC','Encaissement']].iterrows()]

        p1['Impayé'] = [ SeparateValue(int(e[0] - e[1])).generate_value()  for _,e in p1[['Prime_TTC','Encaissement']].iterrows()]

        p1['Taux_Impayé'] = [ str(int(round(((e[0] - e[1])/e[0])*100,0)))+"%" if e[0] != 0 else '0%' for _,e in p1[['Prime_TTC','Encaissement']].iterrows()]


        p1.insert(0,'Nbr_contrat',p2['Police'])
        p1 = p1.reindex(columns=[pivot,'Nbr_contrat','Prime_TTC','Encaissement','Taux_En','Impayé','Taux_Impayé'])
        p1['Prime_TTC'] = [SeparateValue(e).generate_value() for e in p1['Prime_TTC']]
        p1['Encaissement'] = [SeparateValue(int(e)).generate_value() for e in p1['Encaissement']]
        #print("p1",p1)
        return p1
  

    def split_file(self,df_prod):

        df_bd_siege = df_prod[df_prod['Point Vente']=="BUREAU DIRECT SIEGE"]
        

        df_mandataire = df_prod[df_prod['Point Vente']=="AGENT MANDATAIRE"]
        

        df_bd_petit_paris = df_prod[df_prod['Point Vente']=="BUREAU DIRECT PETIT PARIS"]
        

        df_bd_pog = df_prod[df_prod['Point Vente']=="BUREAU DIRECT POG"]
        

