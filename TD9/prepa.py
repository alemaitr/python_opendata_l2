from bs4 import BeautifulSoup
import csv

# Charger le code HTML (tu peux aussi lire depuis un fichier)
with open("TD9/aurelfeur.htm", "r", encoding="utf-8") as f:
    html = f.read()

# Analyser le HTML
soup = BeautifulSoup(html, "html.parser")

# Trouver tous les boutons correspondant aux zobjets
buttons = soup.find_all("button", class_="js-profile-quests-button")

# Préparer la liste des données
data = []
for btn in buttons:
    title = btn.get("data-title", "").strip()
    date = btn.get("data-date", "").strip()
    data.append([title, date])

# Écrire le CSV
with open("zobjets.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerow(["data-title", "data-date"])  # en-têtes
    writer.writerows(data)

print("✅ Fichier CSV créé : zobjets.csv")
