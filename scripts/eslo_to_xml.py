import ast
import xml.etree.ElementTree as ET
import xml.dom.minidom

# Lire le contenu du fichier TXT
with open('../data/annote/eslo_annotation.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# Convertir le contenu du fichier en dictionnaire Python
data_dict = ast.literal_eval(data)

# Créer l'élément racine
root = ET.Element('data')

# Traiter chaque entrée dans le dictionnaire
for key, value in data_dict.items():
    eslo_id = value.get('source', 'unknown')
    nv_etudes = value.get('nv_etudes', 'unknown')

    # Créer un élément 'eslo' avec les attributs 'id' et 'nvetudes'
    eslo_element = ET.SubElement(root, 'eslo', id=eslo_id, niveau=nv_etudes)
    
    # Ajouter les tokens et leurs pos en tant qu'éléments 'w'
    tokens = value.get('tokens', [])
    pos = value.get('pos', [])
    neg_comp = value.get('neg_comp', [])
    y_absent = value.get('y_absent', [])
    
    for i in range(len(tokens)):
        token = tokens[i]
        pos_tag = pos[i]
        
        # Créer l'élément 'w' avec l'attribut 'pos'
        w_element = ET.SubElement(eslo_element, 'w', pos=pos_tag)
        w_element.text = token
        
        # Ajouter les attributs neg_comp et y_absent si présents
        if i < len(neg_comp) and neg_comp[i] is not None:
            w_element.set('neg_comp', str(neg_comp[i]))
        if i < len(y_absent) and y_absent[i] is not None:
            w_element.set('y_absent', str(y_absent[i]))

xml_str = ET.tostring(root, encoding='unicode')

# Utiliser minidom pour prettifier le XML
dom = xml.dom.minidom.parseString(xml_str)
pretty_xml_str = dom.toprettyxml(indent="    ")

# Écrire le contenu XML dans un fichier avec une mise en page correcte
with open('../data/annote/eslo_annotation.xml', 'w', encoding='utf-8') as file:
    file.write(pretty_xml_str)

print("Annotation XML terminée.")
