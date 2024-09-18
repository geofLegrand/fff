
from prod.paramrapport import ParamRapport  
from prod.paramrapport_sin import ParamRapportSinitre
from prod.rapport import Rapport
from prod.sys import kill_current_process
from prod.emailbody import BuildBodyEmail
from prod.sendmail import send_message
from file_treat.yaml_treat import YamlFile 
from file_treat.yaml_mod import YamlModify
from datetime import date,datetime,timedelta
from file_treat.db_treat import ExecuteDate
import shutil
import time
from multiprocessing import Process
import os,sys

# _path = sys.argv[1] # config file path
# field = sys.argv[2] # yaml field at modify
# field_value = sys.argv[3] # yaml field value

def init():
        
    DATE_DEBUT = str(date.today()) #
    DATE_FIN = str(date.today()) #'2023-12-26'  
    if datetime.today().isoweekday() == 7: # si l'on est dimanche
        DATE_DEBUT = str(datetime.today() + timedelta(days=-6)).split(" ")[0]
        DATE_FIN = str(date.today())

    return [DATE_DEBUT,DATE_FIN]
################################################################
def extract_data_from_repport(dt,para):
   
    for e in para['content']['url']:
        print(f"BEGIN {e['name']}")
        ParamRapport(e['link'],e['bureau'],e['name'],dt['date_start'],dt['date_end']).rapport_generer(e['type'])
        kill_current_process()
        print(f"FINISHED {e['name']}")
    time.sleep(30)
################################################################
def create_dataframe(dt,para): 
    df = Rapport(dt['date_start']+" du "+dt['date_end'])
    df_prod = df.journal_de_production() 
    if  isinstance(df_prod,str):
        print("=============== Etat journal de production vide...\n")
        extract_data_from_repport(dt,para)
    df_en = df.broullard_de_caisse()
    if isinstance(df_en,str) :
        print("=============== Etat encaissement vide...\n")
        extract_data_from_repport(dt,para)       
    prd = df.join_data(df_prod,df_en)
    df_prod_joined = prd['data']  
    print("=============== Sauvegarde du Journal vs Encaissement \n")
    time.sleep(10)
    return [df_prod_joined,prd]
################################################################
def create_html_body_email(df_prod_joined,prd,dt,para):
    print("=============== Edition du corps du mail\n")
    df = Rapport(dt['date_start']+" du "+dt['date_end']) #Rapport(init()[0]+" du "+init()[1])
    html_table = ''
    ebuild_body_Email = BuildBodyEmail(prd['filename'])
    for p in para['content']['pivot']:
        re = df.stat_par_points(df_prod_joined,p)
        html_table += ebuild_body_Email.create_html_table_body(re) + '\n'

    email_html = ebuild_body_Email.create_html_email(html_table)
    return email_html
################################################################
def read_config():
    db_dt = ExecuteDate(init()[0],init()[1])
    db_dt.create_record()
    config = YamlFile().red_yaml_file(os.getenv('CONFIG_PATH'))
    db = db_dt.read_items()
    #print(config)
    for item in db:
        extract_data_from_repport(dt=item,para=config)
        r = create_dataframe(dt=item,para=config)
        email_html = create_html_body_email(r[0],r[1],item,config)
        #print(email_html)
        send_message("Journal de production vs Encaissement",email_html,r[1]['filename'])
        ExecuteDate(item['date_start'],item['date_end']).delete_record()
        #time.sleep(10)
################################################################
# def update_yaml_file(field,value_field):
#     json_file = YamlFile().red_yaml_file(_path)
#     funct = {
#         "label" : YamlModify(json_file).modif_label(str(value_field))
#     }

#     json_file = funct[str(field)]

#     YamlFile().write_yaml_file('config.yaml',json_file)


if __name__ == '__main__':
    print(f"=============== !!!! Début du processus de traitement !!! =============== {datetime.now()}\n")
    #update_yaml_file(field,field_value)
    read_config()


   
    












