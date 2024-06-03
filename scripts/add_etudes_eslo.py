import csv

# Fichiers d'entrée
id_file = '../data/transformes/xml-ESLO_id/concat_id.txt'
level_file = '../data/transformes/tsv/eslo_id_etudes.csv'
output_file = '../eslo_nvetudes.txt'

# Lecture du fichier des niveaux d'études
levels = {}
with open(level_file, mode='r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        if len(row) >= 2:
            levels[row[0]] = row[1]  # ID est la première colonne, niveau d'études est la deuxième colonne

# Lecture du fichier des IDs et ajout des niveaux d'études
with open(id_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8') as outfile:
    for line in infile:
        id_ = line.strip()
        level = levels.get(id_, 'Unknown')  # En cas d'ID non trouvé dans le fichier CSV
        outfile.write(f"{level}\n")

print("Traitement terminé. Vérifiez le fichier 'eslo_nvetudes.txt'.")
