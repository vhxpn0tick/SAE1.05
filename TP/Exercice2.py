import re
from datetime import datetime

def tradpseudocsv(fichier):
    evenements = []
    evenement = {}
    with open(fichier, 'r') as file:
        lines = file.readlines()
        
    for line in lines:
        if line.startswith('BEGIN:VEVENT'):
            evenement = {}
            continue
        if line.startswith('END:VEVENT'):
            evenements.append(evenement)
            continue
        if ':' in line :
            key, value = line.strip().split(':', 1)
            evenement[key] = value

    csv_data_list = []

    for evenement in evenements:
        dtstart = datetime.strptime(evenement['DTSTART'], '%Y%m%dT%H%M%SZ')
        dtend = datetime.strptime(evenement['DTEND'], '%Y%m%dT%H%M%SZ')
        duration = dtend - dtstart

        ID = evenement['UID']
        date = dtstart.strftime('%d-%m-%Y')
        heure = dtstart.strftime('%H:%M')
        duree = '{:02}:{:02}'.format(duration.seconds // 3600, (duration.seconds // 60) % 60)
        intitule = evenement.get('SUMMARY', '')
        salle = evenement.get('LOCATION', '')
        description_raw = evenement.get('DESCRIPTION', '')
        description_parts = re.split(r'\\n', description_raw)

        groupe = description_parts[2] if len(description_parts) > 2 else ''
        if description_parts[3].startswith('(') :
            prof =  'Pas de professeur'
        else :
            prof = description_parts[3]
        salles = salle.split(',') if salle != "vide" else ["vide"]
        professeurs = prof.split(',') if prof != "vide" else ["vide"]

        csv_data = f'"UID = {ID}";\n"Date = {date}"; "Heure = {heure}"; "Durée = {duree}";\n"Ressource = {intitule}";\n"Salle = {", ".join(salles)}";\n"Professeur = {", ".join(professeurs)}";\n"Groupe = {groupe}";'
        csv_data_list.append(csv_data)

    return '\n\n'.join(csv_data_list)


# Exemple d'utilisation
fichier = input("Donnez le nom du fichier :\n")
pseudocsv = tradpseudocsv(fichier)
print(pseudocsv)