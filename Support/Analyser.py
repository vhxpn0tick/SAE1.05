import re
import matplotlib.pyplot as plt
from datetime import datetime

def tradpseudocsv(fichier):
    evenements = []
    evenement = {}
    with open(fichier, 'r') as file:
        lines = file.readlines()
        
    for line in lines:
        if line.startswith('11:42'):
            evenement = {}
            continue
        if line.endswith('546f'):
            evenements.append(evenement)
            continue
        if ' ' in line :
            key, value = line.strip().split(' ', 1)
            evenement[key] = value

    csv_data_list = []
    print(evenement)
    print(evenements)
    for evenement in evenements:
        description_parts = re.split(r'\\n', evenement)
        print(description_parts)
        heure = description_parts[0]
        print(heure)
        ID = evenement['IP']
        csv_data = f'"UID = {ID}";\n"Date = {heure}"";'
        csv_data_list.append(csv_data)
        for line2 in evenement :
            description_parts = re.split(r'\\n', evenement)
            heure = evenement('11:42','')
            print(heure)
            ID = evenement['IP']
            csv_data = f'"UID = {ID}";\n"Date = {heure}"";'
            csv_data_list.append(csv_data)
            if line2.startswith('	0x') :
                protocol = evenement.get('	0x', '')
                csv_data = f'"Protocol = {", ".join(protocol)}";'
                csv_data_list.append(csv_data)
 #       description_raw = evenement.get('DESCRIPTION', '')
 #       description_parts = re.split(r'\\n', description_raw)
#
 #       groupe = description_parts[2] if len(description_parts) > 2 else ''
 #       if description_parts[3].startswith('(') :
 #           prof =  'Pas de professeur'
 #       else :
 #           prof = description_parts[3]
 #       salles = salle.split(',') if salle != "vide" else ["vide"]
 #       professeurs = prof.split(',') if prof != "vide" else ["vide"]

        csv_data = f'"UID = {ID}";\n"Date = {heure}";\n"Protocol = {", ".join(protocol)}";'
        csv_data_list.append(csv_data)




    return '\n\n'.join(csv_data_list)



# Exemple d'utilisation
fichier = input("Donnez le nom du fichier :\n")
pseudocsv= tradpseudocsv(fichier)

print(pseudocsv)
