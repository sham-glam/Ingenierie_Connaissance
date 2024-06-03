import sys
import spacy
import regex
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print("Veuillez fournir le corpus que vous souhaitez traiter: eslo ou sms \
        \nExemple d'exécution : python3 annotation.py eslo\n")
    sys.exit(1)
    
corpus = sys.argv[1]

if corpus == 'eslo':
    texts = open('../data/transformes/xml-ESLO_contenu/concat_contenu.txt', 'r')
    ids = open('../data/transformes/xml-ESLO_id/concat_id.txt', 'r')
    niv = open('../data/transformes/xml-ESLO_niv/eslo-niveaux.txt', 'r')
elif corpus == 'sms':
    texts = open('../data/transformes/xml-SMS_contenu/SMS_contenu.txt', 'r')
    ids = open('../data/transformes/xml-SMS_id/SMS_ids.txt', 'r')
    niv = open('../data/transformes/tsv/SMS_id_education.tsv', 'r')
else:
    print("Corpus non reconnu")
    sys.exit(1)
      
nlp = spacy.load("fr_core_news_md")
print("Modèle spacy chargé...")

# input_file = "../data/transformes/xml-ESLO_contenu/ESLO2_ENT_1001_C_contenu.txt"


source_niveau = {}

for line in niv:
    source, niveau = line.split('\t')
    source_niveau[source] = niveau.rstrip()

# reenitialize the file pointer
niv.seek(0)


annotation = {}

list_neg = ['ne', "n'", 'n']
list_adv_neg = ['pas', 'rien', 'jamais', 'point', 'aucunement', 'aucun', 'aucunement', 'nul', 'nullement', 'nulle', 'plus']
list_neg_tok = list_neg + list_adv_neg

n = 1
for t, i in zip(texts,ids):
    complete_neg = None
    if n % 1000 == 0:
        #break
    #elif n % 100 == 0:
        print(f"working on eslo {n}...")
        
    annotation[f"eslo {n}"] = {}
    annotation[f"eslo {n}"][f"source"] = i.strip()
    
    # récuperer le niveau correspondant à la source 
    niveau = source_niveau.get(i.strip())
    if niveau:
        annotation[f"eslo {n}"][f"niveau"] = niveau
    else:
        annotation[f"eslo {n}"][f"niveau"] = "inconnu"
    
    
    annotation[f"eslo {n}"]["tokens"] = []
    annotation[f"eslo {n}"]["pos"] = []
    annotation[f"eslo {n}"]["neg_comp"] = []
    annotation[f"eslo {n}"]["y_absent"] = []
    annotation[f"eslo {n}"]["schwa_absent"] = []
    # print("\t<eslo>")
    
    complete_negation_in_sent = None
    if regex.findall(r"\b(ne|n')\b.*\b({0})\b".format('|'.join(list_adv_neg)), t):
        complete_negation_in_sent = True
        # in_complete_neg = False
        
    # if complete_negation_in_sent:
    #     annotation[f"eslo {n}"]["neg"] = True
        
    doc = nlp(t)
    for j, token in enumerate(doc):
        if token.pos_ != 'SPACE':
            annotation[f"eslo {n}"]["tokens"].append(token.text)
            # print(f'<w pos="{token.pos_}', end='')
            if token.pos_ == 'VERB':
                # print(':', end='')
                if len(token.morph.get('Tense')) > 0:
                    complete_pos = token.pos_ + ':' + token.morph.get('Tense')[0]
                    # print(token.morph.get('Tense')[0], end='')
                else:
                    complete_pos = token.pos_ + ':' + 'Inf'
                    # print(token.text)
                    # print('Unk', end='')
            else:
                complete_pos = token.pos_
            annotation[f"eslo {n}"]["pos"].append(complete_pos)
            
            if complete_negation_in_sent:
                if token.text in list_neg:
                    position = len(annotation[f"eslo {n}"]["tokens"]) - 1
                    # position_verb = len(annotation[f"eslo {n}"]["neg_comp"]) + 1
                    # position_adv = len(annotation[f"eslo {n}"]["neg_comp"]) + 2
                    complete_neg = True
            #     elif token.text in list_adv_neg and complete_neg:
            #         complete_neg = False

                if complete_neg and token.text in list_adv_neg and regex.match(r"(^VERB.*|AUX)", annotation[f"eslo {n}"]["pos"][position+1]):
                    annotation[f"eslo {n}"]["neg_comp"].append(True)
                    # print(annotation[f"eslo {n}"])
                else:
                    annotation[f"eslo {n}"]["neg_comp"].append(None)
                    
                # if complete_neg and                         annotation[f"eslo {n}"]["pos"][position_verb] == "VERB":
                #     annotation[f"eslo {n}"]["neg_comp"].append(True)
                # else:
                #     annotation[f"eslo {n}"]["neg_comp"].append(None)
                
                # print(annotation[f"eslo {n}"])
                
            # print('">', end='')
            # print(token.text, end='')
            # print('</w>', end=' ')
            if j < len(doc) - 1 and token.dep_ == "nsubj" and regex.match(r't\'', token.text) and regex.match(r'[aeiouy]', doc[j+1].text):
                if token.text == 'tu':
                    annotation[f"eslo {n}"]["y_absent"].append(False)
                    print(token, doc[j+1].text, ' : ypresent')
                else:
                    annotation[f"eslo {n}"]["y_absent"].append(True)
                    print(token, doc[j+1].text, ' : yabsent')

            elif j < len(doc) - 1 and regex.match(r'[cdjlmnqst]\'', token.text) and regex.match(r'^[^aeiouyéèhAEIOUYÉÈH]', doc[j+1].text):
                annotation[f"eslo {n}"]["schwa_absent"].append(True)
                # print(token, doc[j+1].text, ' : schwa')
                
            elif j < len(doc) -1 and regex.match(r'\bj', token.text) and regex.match(r'^[^vftpsdc]', doc[j+1].text):
                annotation[f"eslo {n}"]["schwa_absent"].append(True)
            else:
                annotation[f"eslo {n}"]["y_absent"].append(None)
                annotation[f"eslo {n}"]["schwa_absent"].append(None)
    n += 1
        
#print(annotation)

texts.close()
ids.close()

# Generate XML
root = ET.Element("DATA")

for key, value in annotation.items():
    sms = ET.Element(corpus.upper(), id=value["source"], niveau=value["niveau"])  # Utilisation de la variable corpus pour le nom de l'élément
    has_content = False
    for token, pos, neg, y, schwa in zip(value["tokens"], value["pos"], value["neg_comp"], value["y_absent"], value["schwa_absent"]):
        attributes = {'pos': pos}
        if neg is not None:
            attributes['neg'] = str(neg)
        if y is not None:
            attributes['y'] = str(y)
        if schwa is not None:
            attributes['schwa'] = str(schwa)
        ET.SubElement(sms, "w", **attributes).text = token
        has_content = True
    if has_content:
        root.append(sms)

# Prettify the XML
def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent(root)

# Write the pretty XML to a file
output_file = f"../data/annote/{corpus.upper()}_annotation.xml"  # Utilisation de la variable corpus pour le nom du fichier de sortie
tree = ET.ElementTree(root)
with open(output_file, "wb") as fh:
    tree.write(fh, encoding="utf-8", xml_declaration=True)

print(f"Fichier XML joliment formaté pour le corpus {corpus.upper()} généré avec succès.")
