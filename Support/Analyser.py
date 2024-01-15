import re
import matplotlib.pyplot as plt
from datetime import datetime

def tradpseudocsv(fichier):
    csv_data_list = []
    with open(fichier, 'r') as file:
        lines = file.read()

    # Expression régulière pour matcher les lignes contenant les informations IP
    pattern = r'(\d{2}:\d{2}:\d{2}\.\d+) IP (.+?) > ([\d\.]+)\.(\d+): Flags \[(.+?)\], seq (\d+):(\d+), ack (\d+), win (\d+), options \[(.*?)\], length (\d+)'

    # Trouver toutes les correspondances dans les données
    matches = re.findall(pattern, lines)

    # Traiter chaque match
    for match in matches:
        timestamp, src, dst, port, flags, seq_start, seq_end, ack, win, options, length = match
        csv_data = f'Heure = {timestamp};\n   Source = {src};\n   Destination = {dst};\n   Port = {port};\n   Flags = {flags};\n   début de séquence = {seq_start};\n   Fin de séquence = {seq_end};\n   Accusé = {ack};\n   Win = {win};\n   options = {options};\n   taillee = {length};'
        timestamp, src, dst, port, flags, seq_start, seq_end, ack, win, options, length = match
        csv_data_list.append(csv_data)
    return '\n\n'.join(csv_data_list)



    # Exemple d'utilisation
fichier = input("Donnez le nom du fichier :\n")
pseudocsv =tradpseudocsv(fichier)
print(pseudocsv)
