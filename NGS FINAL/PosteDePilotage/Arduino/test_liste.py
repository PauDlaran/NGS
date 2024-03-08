liste = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

resultat = ""
for i in range(0, len(liste), 3):
    resultat += ",".join(liste[i:i+3]) + ";"

resultat = resultat.rstrip(";")  # Pour enlever le dernier point-virgule

print(resultat)