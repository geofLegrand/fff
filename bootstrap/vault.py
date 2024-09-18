import hvac  
import logging

class SecManager:

    def __init__(self,_url):
        try:
            self.client = hvac.Client(url=_url)  
        except:
            self.client = {}
   
    #assert client.is_authenticated()

    def my_secret(self,path):
        try:
            myvault = self.client.secrets.kv.v2.read_secret_version(path=path,raise_on_deleted_version=True)  
            return myvault['data']['data']
        except : #ConnectionRefusedError
            print("Erreur server")
            logging.Logger()
            
        


if __name__ == "__main__":
    secmanager = SecManager('http://127.0.0.21:8200')
    print(secmanager.my_secret(path='hello'))  