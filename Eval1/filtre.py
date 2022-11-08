import json
import os
os.chdir("Eval1")
with open("SanFrancisco_restaurants.json") as fp:
    restos = json.load(fp)


nv_liste = []

#Au nord de 37.70, au sud de 37.83
#A l'est de 122.36

for r in restos:
    lat, long = (r['gps']['latitude'],r['gps']['longitude'] )
    if lat > 37.79 and lat < 37.83 and long < -122.36 and long > -122.41:
        nv_liste.append(r)

print(len(restos))

print(len(nv_liste))