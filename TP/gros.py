import re
from datetime import datetime

def tradpseudocsv(fichier):
    i = 0
    evenement = {}
    with open(fichier, 'r') as file:
        for line in file:
            if line.startswith('BEGIN') : 
                i += 1
        print("Le nombre de ligne est ", i)
        for line in file:
            if line.startswith('BEGIN:VEVENT'):
                continue
            if line.startswith('END:VEVENT'):
                break
            key, value = line.strip().split(':', 1)
            evenement[key] = value


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
    prof = description_parts[3] if len(description_parts) > 3 else ''

    csv_data = f'"ID = {ID}"\n"Date = {date}", "Heure = {heure}", "Durée = {duree}"\n"Ressource = {intitule}"\n"Salle = {salle}"\n"Professeur = {prof}"\n"Groupe = {groupe}"'
    return csv_data

# Exemple d'utilisation
fichier = input("donnez le nom du fichier :\n")
pseudocsv = tradpseudocsv(fichier)
print(pseudocsv)
