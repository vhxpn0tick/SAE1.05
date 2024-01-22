import re
import markdown
import matplotlib.pyplot as plt
# Définition du patern de l'entête
Ip_pattern = re.compile(r'IP (\S+)')
Ip_pattern4 = re.compile(r'IP (\S+)')
IP_pattern3 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
IP_pattern5 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
port_pattern = re.compile(r'\.\d+$')


def Analyser(log_contents):
#ouverture du fichier de log"
    with open(log_contents, "r") as f:
        infect_compteur = http = moyenne = https =drap= http_final = domaine = ssh = icmp = icmp_req = icmp_rep = ipa = flags_connexion = flags_SynAcK = flags_deco = flags_push = flags_nokonnexion = compteur = 0
        pseudo_csv_fin = pseudo_csv_début=pseudo_csv=[]
        suspect = {}
        occurence ={} 
        allip ={}

        for line in f:

            if '.domain' in line:
                domaine += 1
            if 'ssh' in line:
                ssh += 1
            if 'https' in line:
                https += 1
            if 'http' in line:
                http += 1
            if 'ICMP echo request' in line:
                icmp_req += 1
            if 'ICMP echo reply' in line:
                icmp_rep += 1
            if '192.168' in line:
                ipa += 1
            if 'Flags [S]' in line:
                flags_connexion += 1
            if 'Flags [S.]' in line:
                drap = 1
                flags_SynAcK += 1
            if 'Flags [F.]' in line:
                flags_deco += 1
            if 'Flags [P.]' in line:
                drap = 1
                flags_push += 1
            if 'Flags [.]' in line:
                drap = 1
                flags_nokonnexion += 1



            for ip2 in Ip_pattern4.findall(line):
                clean_ip2 = port_pattern.sub('', ip2)

                if clean_ip2 not in allip :


                    allip[clean_ip2]=1
                        

                if clean_ip2 in allip:
                    allip[clean_ip2]=allip[clean_ip2]+1
            
            for ip2  in IP_pattern5.findall(line):
                clean_ip2 = port_pattern.sub('', ip2)
                if clean_ip2 not in allip:
                    allip[clean_ip2]=1
                        
                if clean_ip2 in allip :
                    allip[clean_ip2]=allip[clean_ip2]+1



                    
            
            for ip in Ip_pattern.findall(line):
                clean_ip = port_pattern.sub('', ip)
                compteur += 1
                

                if clean_ip not in occurence and 'https' not in clean_ip:

                    occurence[clean_ip]=1
                        

                if clean_ip in occurence and 'https' not in clean_ip:
                    occurence[clean_ip]=occurence[clean_ip]+1


            for ip in IP_pattern3.findall(line):
                clean_ip = port_pattern.sub('', ip)
                if clean_ip not in occurence  and 'https' not in clean_ip:
                    if drap == 0 :
                        for lien in line :
                            if 'https' in lien:
                                occurence[clean_ip]=1
                        
                if clean_ip in occurence and 'https' not in clean_ip:
                    if drap == 0   :
                        for lien in line :
                            if 'https' in lien:
                                occurence[clean_ip]=occurence[clean_ip]+1



        drap = 0

    moyenne = sum(occurence.values()) /len(occurence) 

    suspect = {cle: valeur for cle, valeur in occurence.items() if valeur > moyenne}
    for cle, valeur in suspect.items():
        print(f"{cle}: {valeur}\n")

    http_final = http - https
    icmp = icmp_req + icmp_rep
    
    return http, https, http_final, domaine, ssh, icmp, icmp_req, icmp_rep, ip, flags_connexion, flags_SynAcK, flags_deco, flags_push, flags_nokonnexion, compteur, suspect, allip

fichier = input("Donnez le nom du fichier :\n")
http, https, http_final, domaine, ssh, icmp, icmp_req, icmp_rep, ip, flags_connexion, flags_SynAcK, flags_deco, flags_push, flags_nokonnexion, compteur, suspect, addresse =Analyser(fichier)

pseudo_csv_content = "IP;Nombre de requêtes\n"
for ip, count in addresse.items():
    pseudo_csv_content += f"{ip};{count}\n"


with open("adresses.csv", "w") as csv_file:
    csv_file.write(pseudo_csv_content)


cles = list(suspect.keys())
valeurs = list(suspect.values())

colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','red','blue','yellow']
plt.figure(figsize=(10, 7))
plt.pie(valeurs, labels=cles, colors=colors,autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.savefig('Activité-suspect.png', transparent=True)

markdown_text = f'''
#___Résultats Brut analyse du trafic___

___Nombre de trames :___ {compteur}

##___adresses IP :___
''' +'\n'.join(f'- {ip} : {addresses} requêtes' for ip, addresses in addresse.items()) +f'''

##___Activité Suspecte :___
''' +'\n'.join(f'- {ip} : {occurrences} requêtes' for ip, occurrences in suspect.items()) +f'''





<img src="Activité-suspect.png" class="merge" />
##___Protocol + Stats :___ 
- SSH: {ssh}
- HTTP: {http_final}
- HTTPS: {https}
- DNS: {domaine}
- ICMP: {icmp}
- ICMP Requests: {icmp_req}
- ICMP Replies: {icmp_rep}


##___Flags :___
- Connexion Demande: {flags_connexion}
- SynAcK: {flags_SynAcK}
- Déconnexion: {flags_deco}
- Push: {flags_push}
- No Connexion: {flags_nokonnexion}
'''

html_output = markdown.markdown(markdown_text)

with open("rapport.html", "w") as file:
    file.write(html_output)

print("Done.")
