import os
from xml.etree import ElementTree as ET

# Chemin du dossier contenant les fichiers XML
input_folder = '../data/xml-ESLO_nettoye/'
# Dossiers de sortie pour les fichiers d'ids et de contenus
output_folder_who = './data/xml-ESLO_id/'
output_folder_content = './data/xml-ESLO_contenu/'

# Vérifie si les dossiers de sortie existent, sinon les crée
os.makedirs(output_folder_who, exist_ok=True)
os.makedirs(output_folder_content, exist_ok=True)

# Parcours des fichiers dans le dossier d'entrée
for filename in os.listdir(input_folder):
    if filename.endswith('.xml'):
        # Chemin complet du fichier XML d'entrée
        input_file_path = os.path.join(input_folder, filename)
        tree = ET.parse(input_file_path)
        root = tree.getroot()

        # Chemins de sortie pour les fichiers who_values.txt et content_values.txt
        who_output_path = os.path.join(output_folder_who, filename.replace('.xml', '_who.txt'))
        content_output_path = os.path.join(output_folder_content, filename.replace('.xml', '_contenu.txt'))

        # Ouvre les fichiers de sortie
        with open(who_output_path, 'w') as who_file, open(content_output_path, 'w') as content_file:
            # Parcours des enfants de la racine
            for child in root:
                # Vérifie si l'élément est une balise <u>
                if child.tag == 'u':
                    # Récupère la valeur de l'attribut "who"
                    who_value = child.attrib.get('who', '')
                    # Récupère le contenu de la balise <u>, vérifie si c'est None avant d'appeler strip()
                    content_value = child.text.strip() if child.text is not None else ''
                    # Écrit les valeurs dans les fichiers de sortie
                    who_file.write(who_value + '\n')
                    content_file.write(content_value + '\n')

print("Traitement terminé.")
