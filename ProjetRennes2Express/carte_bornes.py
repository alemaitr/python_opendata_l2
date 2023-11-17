

import csv
import pprint
from bokeh.plotting import figure, show
from bokeh.tile_providers import get_provider, Vendors
import numpy as np


#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


def creer_carte(Titre):
    #Création de la figure avec arrière plan
    TOOLTIPS = [("", "$name")]
    p = figure(x_axis_type="mercator", y_axis_type="mercator",tooltips=TOOLTIPS, title=Titre,)
    tile_provider = get_provider(Vendors.CARTODBPOSITRON)
    p.add_tile(tile_provider)

    return p

def tracer_point(carte,long,lat,label,couleur="red"):
    x,y = coor_wgs84_to_web_mercator(long,lat)
    carte.diamond(x,y,color=couleur,size=10,name=label)


def afficher_carte(carte):
    show(carte)

def tracer_ligne(carte, lst_long, lst_lat, label, couleur="red"):
    x = []
    y = []
    for i in range(0,len(lst_lat)):
        cx,cy = coor_wgs84_to_web_mercator(lst_long[i],lst_lat[i])
        x.append(cx)
        y.append(cy)

    carte.line(x=x,y=y,color = couleur,width=2,name=label)




with open("ProjetRennes2Express/bornes.csv") as fp:
    reader = csv.DictReader(fp,delimiter=";")
    etapes = {}
    for dico in reader :
        jour = dico["jour"]
        dicojour = etapes.get(jour,{})
        dicoetape = dicojour.get(dico["num_etape"],{})
        if dico["type"]=="depart":
            dicoetape["depart"]= {"lat":float(dico["lat"]),"long":float(dico["long"]),"nom":dico["nom"]}
        else :
            dicoetape["arrivee"]= {"lat":float(dico["lat"]),"long":float(dico["long"]),"nom":dico["nom"]}
        dicojour[dico["num_etape"]]=dicoetape
        etapes[dico["jour"]]=dicojour

pprint.pprint(etapes)


carte = creer_carte("Rennes2 Express")
for jour,es in etapes.items():
    for num,e in es.items():
        tracer_point(carte,e["depart"]["long"],e["depart"]["lat"],e["depart"]["nom"],'green')
        tracer_point(carte,e["arrivee"]["long"],e["arrivee"]["lat"],e["arrivee"]["nom"],'red')
        label = f"Jour {jour} étape {num}"
        tracer_ligne(carte,[e["depart"]["long"],e["arrivee"]["long"]],[e["depart"]["lat"],e["arrivee"]["lat"]],label,'blue')

afficher_carte(carte)


