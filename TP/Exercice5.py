import re
import matplotlib.pyplot as plt
from datetime import datetime
import markdown
import html

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
    sept=oct=nov=dec=0

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
        if dtstart.strftime('%m')== '09' or dtstart.strftime('%m')=='10' or dtstart.strftime('%m')=='11' or dtstart.strftime('%m')=='12'  :
            if groupe=="RT1-TP B2"  : 
                csv_data = f'"UID = {ID}";\n"Date = {date}"; "Heure = {heure}"; "Durée = {duree}";\n"Ressource = {intitule}";\n"Salle = {", ".join(salles)}";\n"Professeur = {", ".join(professeurs)}";\n"Groupe = {groupe}";'
                csv_data_list.append(csv_data)
                if dtstart.strftime('%m')== '09' : 
                    sept += 1
                elif dtstart.strftime('%m')== '10' : 
                    oct += 1
                elif dtstart.strftime('%m')== '11' : 
                    nov += 1
                elif dtstart.strftime('%m')== '12' : 
                    dec += 1



    return '\n\n'.join(csv_data_list) , sept, oct , nov , dec 




# Exemple d'utilisation
fichier = input("Donnez le nom du fichier :\n")
pseudocsv, sept ,oct ,nov ,dec= tradpseudocsv(fichier)
print (sept ,",",oct,",",nov,",",dec)
print(pseudocsv)
labels = 'Septembre', 'Octobre' ,'Novembre', 'Décembre'
sizes = [sept, oct, nov, dec]
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
plt.pie(sizes, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.savefig('Camembert1.png')
with open("testtt.md",'r') as f:
    text=f.read()
    html=markdown.markdown(pseudocsv,extensions=['tables'])
with open('Picnic.html','w') as f:
    f.write(html)