import xml.etree.ElementTree as ET

# Lecture à partir du fichier d'entrée
# Ici c'est les résultats du script annotation.py
with open("results.txt", "r") as file:
    input_data = file.read()

# Lecture du fichier contenant les identifiants
with open("./data/transformes/xml-ESLO_id/concat_id.txt", "r") as id_file:
    identifiers = id_file.read().splitlines()

# Conversion du contenu du fichier en dictionnaire
data = eval(input_data)

# Initialisation du XML de sortie
xml_output = "<data> \n"


# Génération de la sortie XML pour chaque entrée
for line_number, (key, value) in enumerate(data.items(), start=1):
    # Utilisation de l'identifiant au lieu du numéro de ligne dans la balise
    identifier = identifiers[line_number - 1] if line_number <= len(identifiers) else str(line_number)
    xml_output += f"    <eslo id='{identifier}'>\n"
    for token, pos in zip(value['tokens'], value['pos']):
        xml_output += f'        <w pos="{pos}">{token}</w>\n'
    xml_output += f"    </eslo>\n"

xml_output += "</data>"

# Écriture de la sortie XML dans un fichier
with open("output.xml", "w") as file:
    file.write(xml_output)
