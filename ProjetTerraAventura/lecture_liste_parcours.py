from bs4 import BeautifulSoup, Tag, NavigableString
from multiprocessing import Pool, cpu_count
import json
from urllib import request, parse
import os 

def get_liste_caches(bsobj):
    lst = {}
    articles = bsobj.findAll("article",class_="gc-caches-liste")
    for art in articles : 
        titre = art.find("span",class_="gc-caches-liste-title").get_text()

        if art.find("a"):
            lst[titre]=art.find("a").attrs["href"]

    return lst

def get_script(bsobj):
    lst = []

    articles = bsobj.findAll("script")
    for art in articles : 
        # Selon la version de bs4, cela pourrait etre art.gettext
        code = art.contents
        
        if(code)!=[]:
            lst.append(code[0])
            

    return lst

def construit_dico(bsobj):
    print("Debut de la construction de la liste des caches")
    malst = []
    lst = json.loads(get_script(bsobj)[0])["geocaching_map"]['markers']
    # print(lst[0].keys())
    for cache in lst :
        if cache["type"]  == "geocaching_cache" : #Pour éviter les partner sites et adventures
            dico={}
            dico["nid"]=cache['nid']
            dico["lat"]= cache["lat"]
            dico["lng"]= cache["lng"]
            dico["nom"]= cache["title"]
            dico["terrain"]=cache["field_ground"]
            dico["departement"]=cache["field_department"]
            dico["difficulte"]=cache["field_difficulty"]
            dico["ville"]= cache["field_city"]

            poiz = cache["icon"]
            poiz = poiz.split("/")[-1][:-4]
            if "_" in poiz : 
                poiz = poiz.split("_")[1]
            if "-" in poiz : 
                poiz = poiz.split("-")[0]
            poiz = poiz.capitalize()   
            dico["type"] = poiz

            malst.append(dico)
        # else :
        #     print("Cache non retenue car de types ",cache["type"])
    return malst





def construction_liste_parcours(fichier_parcours, fichier_produit):
    with open(fichier_parcours,'r',encoding="utf-8") as fp:
        bsobj = BeautifulSoup(fp.read(),features='lxml')
        lescaches = construit_dico(bsobj)
        print(f"Nombre de caches chargées dans la liste : {len(lescaches)}")
                


    with open(fichier_produit,'w',encoding="utf-8") as fp:
        json.dump(lescaches,fp,ensure_ascii=False,indent=4)

if __name__ == "__main__":
    #Définition des variables si nécessaire : 
    os.chdir("ProjetTerraAventura")
    fichier_parcours = "parcours2024.html"

    fichier_caches = "tresors.json"

    ###### 1. Analyse du fichier parcours pour faire la liste des caches, et celle déjà trouvées
    construction_liste_parcours(fichier_parcours,fichier_caches)