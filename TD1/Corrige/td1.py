import json


def noms_compteurs(d):
    noms = []
    for elem in d:
        if elem["name"] not in noms:
            noms.append(elem["name"])
    return noms


def compte_passages_compteurs(d, noms):
    dico = {}
    for compteur in noms:
        n_avril = 0
        for elem in d:
            if elem["name"] == compteur:
                n_avril += elem["counts"]
        dico[compteur]=n_avril
    return dico


def compte_passages_horaire(d):
    passages_par_heure = {}
    for elem in d:
        heure = elem["date"]["hour"]
        passages_par_heure[heure] = passages_par_heure.get(heure, 0) + elem["counts"]
    return passages_par_heure

def compte_passages_jour(d, jour):
    total = 0
    for elem in d:
        if jour == elem["date"]["day"] :
            total = total + elem["counts"]
    return total

def compare_tous_les_jours(d24,d26):
    dico = {}
    for jour in range(1,31): #30 jours en avril
        val_2024 = compte_passages_jour(d24,jour)
        val_2026 = compte_passages_jour(d26,jour)
        dico[jour]={2024: val_2024,2026:val_2026}
    return dico

def exporte_comparaison(d24, d26):
    comparaison = compare_tous_les_jours(d24,d26)
    file = "TD1/Corrige/nb_passages_avril-2024_2026.json"
    with open(file,"w") as fp :
        json.dump(comparaison, fp,indent=2)
    

############################################
# Exercice 2 - Extraction d'informations élémentaires
############################################
# 1.Chargement
nom_fichier = "TD1/Donnees/counter_avril2026.json"
fp = open(nom_fichier, "r")
donnees_2026 = json.load(fp)

# 2.Nombre d'enregistrements
print(f"Il y a {len(donnees_2026)} enregistrements")

# 3. Premier enregistrement
print(donnees_2026[0])

# 4. Nom des compteurs
noms_c = noms_compteurs(donnees_2026)
print(f"Noms des compteurs dans le jeu de données: {noms_c}")

############################################
# Exercice 3 - Comptage des vélos
############################################

# 1. Passage par compteurs
passage_compteur = compte_passages_compteurs(donnees_2026, noms_c)
print("Passage par compteurs :\n",passage_compteur)

# 2. Passages par horaire
passages = compte_passages_horaire(donnees_2026)
print(f"Nombre de passages heure par heure:")
for heure in range(24):
    print(f"* {heure}h-{heure+1}h : {passages.get(heure, 0)}")

# 3. Heure fréquentée
heure_max = -1
n_max = -1
for heure, nb in passages.items():
    if nb > n_max:
        n_max = nb
        heure_max = heure
print(f"L'heure la plus fréquentée est {heure_max}h-{heure_max+1}h")

############################################
# Exercice 4 - Comparaison 2024-2026
############################################

# 2.Chargement
nom_fichier = "TD1/Donnees/counter_avril2024.json"
fp = open(nom_fichier, "r")
donnees_2024 = json.load(fp)

# 4. Comptage pour un jour le 9 avril
passages_9avril2024 = compte_passages_jour(donnees_2024,9)
passages_9avril2026 = compte_passages_jour(donnees_2026,9)

print(f"Le 9 avril, on a compté {passages_9avril2024} passages en 2024 et {passages_9avril2026} en 2026.")

# 5. Comparaison de tous les jours
comparaison = compare_tous_les_jours(donnees_2024,donnees_2026)
print(comparaison)


############################################
# Exercice 5. Export json
############################################
exporte_comparaison(donnees_2024,donnees_2026)