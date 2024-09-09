import json


def noms_compteurs(d):
    noms = []
    for elem in d:
        if elem["name"] not in noms:
            noms.append(elem["name"])
    return noms


def nombre_passages(d, noms):
    for nom in noms:
        n_avril = 0
        for elem in d:
            if elem["name"] == nom:
                n_avril += elem["counts"]
        print(f"Compteur '{nom}': {n_avril} passages durant le mois d'avril")


def nombre_passages_9_avril(d, noms):
    for nom in noms:
        n_9_avril = 0
        for elem in d:
            if elem["name"] == nom:
                if (elem["date"]["year"], elem["date"]["month"], elem["date"]["day"]) == (2024, 4, 9):
                    n_9_avril += elem["counts"]
        print(f"Compteur '{nom}': {n_9_avril} passages le 9 avril")


def passages_par_creneau(d):
    passages_par_heure = {}
    for elem in d:
        heure = elem["date"]["hour"]
        passages_par_heure[heure] = passages_par_heure.get(heure, 0) + elem["counts"]
    return passages_par_heure


def recode_gps(d):
    for elem in d:
        lat, lon = elem["gps_coord"]
        del elem["gps_coord"]
        elem["latitude"] = lat
        elem["longitude"] = lon
    return d


def recode_date(d):
    for elem in d:
        year, month, day, hour = (elem["date"]["year"], 
                                  elem["date"]["month"], 
                                  elem["date"]["day"], 
                                  elem["date"]["hour"])
        elem["date"] = f"{day:02d}/{month:02d}/{year} {hour:02d}h-{hour+1:02d}h"
    return d


# Extraction d'informations élémentaires
# 1.
nom_fichier = "TD3/Corrige/eco-counter-data_clean.json"
fp = open(nom_fichier, "r")
donnees = json.load(fp)

# 2.
noms_c = noms_compteurs(donnees)
print(f"Noms des compteurs dans le jeu de données: {noms_c}")

# 3.
nombre_passages(donnees, noms_c)

# 4. 
nombre_passages_9_avril(donnees, noms_c)

# 5.
passages = passages_par_creneau(donnees)
print(f"Nombre de passages heure par heure:")
for heure in range(24):
    print(f"* {heure}h-{heure+1}h : {passages.get(heure, 0)}")

# 6.
heure_max = -1
n_max = -1
for heure, nb in passages.items():
    if nb > n_max:
        n_max = nb
        heure_max = heure
print(f"L'heure la plus fréquentée est {heure_max}h-{heure_max+1}h")

# Export au format JSON

# 1.
donnees = recode_gps(donnees)

# 2.
donnees = recode_date(donnees)

# 3.
nom_fichier = "eco-counter-data_out.json"
fp = open(nom_fichier, "w")
json.dump(donnees, fp, indent=2)
fp.close()
