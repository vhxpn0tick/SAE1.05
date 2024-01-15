import re
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict


def count_dynamic_ip_occurrences(log_contents):

    ip_pattern = re.compile(r"Source = (\S+);|Destination = (\S+);")
    
    ip_count = defaultdict(int)
    
    matches = ip_pattern.findall(log_contents)
    
    for match in matches:
        for ip in match:
            if ip: 
                ip_count[ip] += 1
    
    return ip_count

def tradpseudocsv(fichier):
    csv_data_list=timestamp= src= dst= port= flags= seq_start= seq_end= ack= win= options= length = []
    evenements = []
    premiere ={}
    evenement = {}
    affichage =[]
    affichage_part = {}
    affichage_split =[]
    ip =[]

    with open(fichier, 'r') as file:
        lines = file.readlines()
        
    for line in lines:
        
        if line.startswith('11:42'):
            premiere = line
            affichage.append(premiere)
            evenements.append(evenement)
            evenement={}            
            continue
        if line.startswith('11:42'):
            evenements.append(evenement)
            continue
        if ' ' in line :
            key, value = line.strip().split(' ', 1)
            evenement[key] = value
    

    csv_data_list = []

    for i in range (len(affichage)) :

        description_raw = affichage[i]
        description_parts = re.split(r'\\n', description_raw)
        
        affichage_part = description_parts
        affichage_split.append(affichage_part)



        pattern = r'(\d{2}:\d{2}:\d{2}\.\d+) IP (.+?) > ([\d\.]+)\.(\d+): Flags \[(.+?)\], seq (\d+):(\d+), ack (\d+), win (\d+), options \[(.*?)\], length (\d+)'

        matches = re.findall(pattern, affichage[i])


        for match in matches:
            timestamp, src, dst, port, flags, seq_start, seq_end, ack, win, options, length = match
            csv_data = f'Heure = {timestamp};\n   Source = {src};\n   Destination = {dst};\n   Port = {port};\n   Flags = {flags};\n   début de séquence = {seq_start};\n   Fin de séquence = {seq_end};\n   Accusé = {ack};\n   Win = {win};\n   options = {options};\n   taille = {length};'
            csv_data_list.append(csv_data)
            print(src,dst)
            



        print(ip)                    
    return '\n\n'.join(csv_data_list)




    # Exemple d'utilisation
fichier = input("Donnez le nom du fichier :\n")
information =tradpseudocsv(fichier)
print(information)
ip_counts = count_dynamic_ip_occurrences(information)
for ip, count in ip_counts.items():
    print(f"L'adresse IP {ip} apparaît {count} fois.")
