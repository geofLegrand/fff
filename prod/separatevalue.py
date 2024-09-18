
class SeparateValue(object):

    def __init__(self,value:int,separateur:str = " "):

        self.separateur = separateur
        self.value = value

    def generate_value(self) -> str:
        valeur = []
        n =  len(str(self.value)) // 3
        j = 0 # nombre de caracteres réccuprés
        k = 0 # nombre d'espace à enregistrer
        for i in range(len(str(self.value))):
            c = str(self.value)[len(str(self.value)) - 1 - i]
            valeur.insert(0,c)
            j += 1
            if j == 3:
                if k != n:
                    valeur.insert(0,self.separateur)
                    k += 1
                j = 0
        ",".join(valeur)        

        return (",".join(valeur)).strip().replace(",", "") 