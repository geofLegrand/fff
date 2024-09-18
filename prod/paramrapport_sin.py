from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.common.keys import Keys
from datetime import date
from prod.download import Download
from dotenv import load_dotenv
from file_treat.yaml_treat import YamlFile
from prod.paramrapport import ParamRapport

load_dotenv()


class ParamRapportSinitre(ParamRapport):


    def __init__(self,url:str, reseau : str,name :str,date_arrete : str):
        super().__init__(url, reseau,name,date_arrete,"")
        self.date_arrete = date_arrete





    def select_statut_dossier(self):
        # if self.reseau == super().conf["content"]["reseau"][0] :
        self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl17_ddDropDownButton").click() 
        time.sleep(3)
        self.DRIVER.find_element(By.ID, f"ReportViewer1_ctl04_ctl17_divDropDown_ctl00").click()
        time.sleep(2)
        for i in [3,5]:
            self.DRIVER.find_element(By.ID, f"ReportViewer1_ctl04_ctl17_divDropDown_ctl0{i}").click() # selection du réseau
            time.sleep(0)
     
        time.sleep(5)
        
        self.DRIVER.find_element(By.ID, "ReportViewer1").click()  # slectionner le rapport
        
        time.sleep(5)

        self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl15_txtValue").send_keys(self.date_arrete)

        time.sleep(5)

        self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl00").click() # Lancer le rapport

        time.sleep(5)

        self.DRIVER.find_element(By.ID, "ReportViewer1").click()  # slectionner le rapport
        
        #time.sleep(20)

        download = Download(self.DRIVER)

        download.export(60)

        #self.DRIVER.close()


    def rapport_generer(self,type_etat):

        self.DRIVER.find_element(By.ID,"ReportViewer1_ctl04_ctl05").click() # cliquer sur list réseau
        
        time.sleep(5)
        #DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl05_divDropDown_ctl00").click() # deselection de tous les réseaux

        self.select_reseau()
        
        try:
            self.point_de_vente()
        except:
            self.point_de_vente()

        time.sleep(27)
        if type_etat == "1":
            
            self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl17_txtValue").send_keys(self.date_debut)
            
            self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl19_txtValue").send_keys(self.date_fin)
        elif type_etat == "2":

            self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl19_txtValue").send_keys(self.date_debut)

            self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl21_txtValue").send_keys(self.date_fin)

        time.sleep(2)

        self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04_ctl00").click() # Lancer le rapport
        time.sleep(10)
        self.DRIVER.find_element(By.ID, "ReportViewer1").click()  # slectionner le rapport
        
        download = Download(self.DRIVER)

        try:
            download.export()
        except Exception:
            print("Error exporting")
            download.export()

    def point_de_vente(self):
        if not (self.looping()):
                self.DRIVER.find_element(By.ID,"ReportViewer1_ctl04_ctl07").click() # cliquer sur list réseau
                for i in range(1,10):
                    if i not in [1,2,3,4,5,6,7,8,9,10,11] :
                        self.DRIVER.find_element(By.ID, f"ReportViewer1_ctl04_ctl07_divDropDown_ctl0{i}").click() # selection Bureau Direct
                        time.sleep(3)
                self.DRIVER.find_element(By.ID, "ReportViewer1_ctl04").click()  # clicking ReportViewer

    def looping(self):
        while True:
            print('Chargement point de vente...')
            time.sleep(5)
            self.DRIVER.find_element(By.ID, "ReportViewer1").click()  # slectionner le rapport
            if not self.DRIVER.find_element(By.ID, "ReportViewer1_AsyncWait_Wait").is_displayed():
                break
        print('Chargement point de vente terminé...')    
        return False
   
# BUREAU DIRECT SIEGE

if __name__ == '__main__':

    URL_PROD="https://ixperta-gb.groupensia.com/Views/PageControls/Vie/Reports/frmBaseReport.aspx?rapport=%2fRapports%2fRapports%2fEmissions%2fJournal+de+Production&_dc=1695511494495"
    URL="https://ixperta-gb.groupensia.com/Views/PageControls/Vie/Reports/frmBaseReport.aspx?rapport=%2fRapports%2fRapports%2fSinistres%2fSinistres+SAP+avec+Date+Arretee&_dc=1725213716663"
    
    emission = ParamRapport(URL,1,'BUREAUX DIRECTS',str(date.today()),str(date.today()))
    
    emission.rapport_generer("brouillar_caisse")

    print("FINISHED")