import smtplib, ssl
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime
from file_treat.yaml_treat import YamlFile 

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bootstrap.vault import SecManager
#print(Path(__file__).parent / ".env")
load_dotenv()

def send_message(subject,mail_html,fichier=""):
    #print(mail_html)
    ################################################################
    conf = YamlFile().red_yaml_file(os.getenv('CONFIG_PATH'))
    smtp_server = conf["mod"]["smtpserver"]
    sender_email = conf["mod"]["sender"]
    cc = []
    ################################################################
    print(f'"""""""""""""" MODE {conf["mod"]["label"]} """"""""""""""\n')
    to = []
    if 'PROD' == conf["mod"]["label"] :
        to = conf["content"]["mailprod"]["to"] #"juste.moumbangou@nsiaassurances.com"
        cc = conf["content"]["mailprod"]["cc"]
            
    elif 'DEV' == conf["mod"]["label"]:
        to = conf["content"]["maildev"]["to"]
        cc = conf["content"]["maildev"]["cc"]
        subject = "Test Journal de production vs Encaissement"

    # Create a multipart message and set headers
    message = MIMEMultipart('alternative')
    message["From"] = os.getenv("EMAIL_SENDER") 
    message["To"] = ",".join(to)
    message["Subject"] = subject
    message['Cc'] = ",".join(cc) 
    #message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    part = MIMEText(mail_html, "html")

    message.attach(part)

    if fichier:
            
            #print(fichier.split("SAVE_TEST/")[1])
            filename = os.path.join(conf['mod']['readDir'],fichier)  # In same directory as script

            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            fichier = fichier.split("SAVE_TEST/")[1]
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {fichier}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)

    
    message = message.as_string()

    context = ssl.create_default_context()
    #print(context.get_ca_certs())
    with smtplib.SMTP(smtp_server,os.getenv("PORT")) as server:
        print("=============== Send the email =================\n")
        server.ehlo()  # Can be omitted
        server.starttls(context = context)
        server.ehlo()  # Can be omitted
        server.login(user=sender_email, password=SecManager(os.getenv("VSERVER")).my_secret('key-dev')[os.getenv("KEY_SECRET")])
        #print(message,cc)
        result = server.sendmail(sender_email, cc, message)

    if result == {}:
        print(f"=============== !!!! Process done !!!!\n\n=============== {datetime.now()}")
    else:
        print("=============== Erreur !!!!! Mail non transmis au destinataire")
