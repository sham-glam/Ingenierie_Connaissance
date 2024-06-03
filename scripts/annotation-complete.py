import sys
import spacy
import regex
import xml.etree.ElementTree as ET

# Vérifie que le nom du corpus à traiter est bien fourni en argument
if len(sys.argv) < 2:
    print(
        "Veuillez fournir le corpus que vous souhaitez traiter: eslo ou sms \
        \nExemple d'exécution : python3 annotation.py eslo\n"
    )
    sys.exit(1)

# Récupère le nom du corpus à traiter
corpus = sys.argv[1]

# Ouvre les fichiers contenant les textes et les identifiants et les niveaux d'étude des locuteurs
if corpus == "eslo":
    texts = open("../data/transformes/xml-ESLO_contenu/concat_contenu.txt", "r")
    ids = open("../data/transformes/xml-ESLO_id/concat_id.txt", "r")
    niv = open("../data/transformes/xml-ESLO_niv/eslo-niveaux.txt", "r")
elif corpus == "sms":
    texts = open("../data/transformes/xml-SMS_contenu/SMS_contenu.txt", "r")
    ids = open("../data/transformes/xml-SMS_id/SMS_ids.txt", "r")
    niv = open("../data/transformes/tsv/SMS_id_education.tsv", "r")
else:
    print("Corpus non reconnu")
    sys.exit(1)

# Charge le modèle spacy pour le français
nlp = spacy.load("fr_core_news_md")
print("Modèle spacy chargé...")

# Initialise le dictionnaire qui va contenir les niveaux d'étude
source_niveau = {}

for line in niv:
    source, niveau = line.split("\t")
    source_niveau[source] = niveau.rstrip()

# reinitialise the file pointer
niv.seek(0)

# Initialise le dictionnaire qui va contenir les annotations
annotation = {}

# Liste des formes de négation et des adverbes de négation
list_neg = ["ne", "n'", "n"]
list_adv_neg = [
    "pas",
    "rien",
    "jamais",
    "point",
    "aucunement",
    "aucun",
    "aucunement",
    "nul",
    "nullement",
    "nulle",
    "plus",
]
list_neg_tok = list_neg + list_adv_neg

# Boucle sur les textes et les identifiants des locuteurs
n = 1
for t, i in zip(texts, ids):
    # Initialise la variable qui va contenir l'information sur la négation complète
    complete_neg = None

    # Affiche un message tous les 1000 textes traités
    if n % 10000 == 0:
        #break
        print(f"working on eslo {n}...")
    #elif n % 1000 == 0:
    #    print(f"working on eslo {n}...")

    # Ajoute les informations sur le texte 
    annotation[f"eslo {n}"] = {}
    annotation[f"eslo {n}"][f"source"] = i.strip()

    # Récupère le niveau correspondant à la source
    niveau = source_niveau.get(i.strip())
    if niveau:
        annotation[f"eslo {n}"][f"niveau"] = niveau
    else:
        annotation[f"eslo {n}"][f"niveau"] = "inconnu"

    # Initialisation des annotations
    annotation[f"eslo {n}"]["tokens"] = []
    annotation[f"eslo {n}"]["pos"] = []
    annotation[f"eslo {n}"]["neg_comp"] = []
    annotation[f"eslo {n}"]["y_absent"] = []
    annotation[f"eslo {n}"]["schwa_absent"] = []

    # Vérifie si le texte contient une négation complète
    complete_negation_in_sent = None
    if regex.findall(r"\b(ne|n')\b.*\b({0})\b".format("|".join(list_adv_neg)), t):
        complete_negation_in_sent = True

    # Traite le texte avec spacy et boucle sur les tokens
    doc = nlp(t)
    for j, token in enumerate(doc):
        # Ignore les tokens vides
        if token.pos_ != "SPACE":
            # Ajoute le token et sa catégorie grammaticale au dictionnaire d'annotations
            annotation[f"eslo {n}"]["tokens"].append(token.text)
            complete_pos = token.pos_
            if token.pos_ == "VERB":
                if len(token.morph.get("Tense")) > 0:
                    complete_pos = token.pos_ + ":" + token.morph.get("Tense")[0]
                else:
                    complete_pos = token.pos_ + ':' + 'Inf'
            annotation[f"eslo {n}"]["pos"].append(complete_pos)

            # Ajoute l'information sur la négation complète au dictionnaire d'annotations
            if complete_negation_in_sent:
                if token.text in list_neg:
                    position = len(annotation[f"eslo {n}"]["tokens"]) - 1
                    complete_neg = True

                if (
                    complete_neg
                    and token.text in list_adv_neg
                    and regex.match(
                        r"(^VERB.*|AUX)", annotation[f"eslo {n}"]["pos"][position + 1]
                    )
                ):
                    annotation[f"eslo {n}"]["neg_comp"].append(True)
                else:
                    annotation[f"eslo {n}"]["neg_comp"].append(None)





            assert token.text == doc[j].text
            # Ajoute l'information sur l'absence de /y/ dans "tu" au dictionnaire d'annotations
            if (
                j < len(doc) - 1
                and token.dep_ == "nsubj"
                and regex.match(r"t\'", token.text)
                and regex.match(r"[aeiouy]", doc[j + 1].text)
            ):
                if token.text == "tu":
                    annotation[f"eslo {n}"]["y_absent"].append(False)
                else:
                    annotation[f"eslo {n}"]["y_absent"].append(True)

            # Ajoute l'information sur l'absence de schwa dans les clitiques au dictionnaire d'annotations
            elif (
                j < len(doc) - 1
                and regex.match(r"[cdjlmnqst]\'", token.text)
                and regex.match(r"^[^aeiouyàâéèêôhAEIOUYÉÀÂÊÔÈH]", doc[j + 1].text)
            ):
                annotation[f"eslo {n}"]["schwa_absent"].append(True)

            elif (
                j < len(doc) - 1
                and regex.match(r"^j[^aeiouyàâéèêôhAEIOUYÉÀÂÊÔÈH\']", token.text)
            ):
                annotation[f"eslo {n}"]["schwa_absent"].append(True)
            else:
                annotation[f"eslo {n}"]["y_absent"].append(None)
                annotation[f"eslo {n}"]["schwa_absent"].append(None)
    n += 1

# print(annotation)

texts.close()
ids.close()

# Generate XML
root = ET.Element("DATA")

for key, value in annotation.items():
    sms = ET.Element(
        corpus.upper(), id=value["source"], niveau=value["niveau"]
    )  # Utilisation de la variable corpus pour le nom de l'élément
    has_content = False
    for token, pos, neg, y, schwa in zip(
        value["tokens"],
        value["pos"],
        value["neg_comp"],
        value["y_absent"],
        value["schwa_absent"],
    ):
        attributes = {"pos": pos}
        if neg is not None:
            attributes["neg"] = str(neg)
        if y is not None:
            attributes["y"] = str(y)
        if schwa is not None:
            attributes["schwa"] = str(schwa)
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

print(
    f"Fichier XML joliment formaté pour le corpus {corpus.upper()} généré avec succès."
)
