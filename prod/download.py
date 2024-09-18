import time
import sys
from selenium.webdriver.common.by import By

class Download(object):
    
    def __init__(self,driver):
         self.DRIVER = driver


    def export(self,time_temp=30) :
        
        i = 0
        separate = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚']
        while True:
            
            i += 1
            for symb in separate:
                sys.stdout.write(f'\rChargement des données en cours ......{symb}')
                sys.stdout.flush()
                time.sleep(0.3)
            #print('Chargement des données en cours ...')
            if not self.DRIVER.find_element(By.ID, "ReportViewer1_AsyncWait_Wait").is_displayed():
                # print('Chargement des données terminé ...')
                sys.stdout.write(f'\rChargement des données terminé!  \n')

                self.DRIVER.find_element(By.ID, "ReportViewer1_ctl05_ctl04_ctl00_Button").click()

                time.sleep(3)
                # print('Extraction des données  ...')
                sys.stdout.write(f'\rExtraction des données!  \n')

                self.DRIVER.find_element(By.XPATH,"//*[@id='ReportViewer1_ctl05_ctl04_ctl00_Menu']/div[2]/a").click()  # Exporter vers excel 

                break
            if i == 10 * 60 :
                self.DRIVER.close()
        time.sleep(time_temp)
        self.DRIVER.close()
