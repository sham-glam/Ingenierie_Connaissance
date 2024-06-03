import sys
import spacy
import regex

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
    nv_etudes = open("../data/transformes/xml-eslo_nvetudes.txt", "r")
elif corpus == "sms":
    texts = open("../data/transformes/xml-SMS_contenu/SMS_contenu.txt", "r")
    ids = open("../data/transformes/xml-SMS_id/SMS_ids.txt", "r")
else:
    print("Corpus non reconnu")
    sys.exit(1)

# Charge le modèle spacy pour le français
nlp = spacy.load("fr_core_news_md")
# print("Modèle spacy chargé...")

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
for t, i, ne in zip(texts, ids, nv_etudes):
    # Initialise la variable qui va contenir l'information sur la négation complète
    complete_neg = None
    
    # if n % 1000 == 0:
    #    break
    # elif n % 100 == 0:
    #    print(f"working on eslo {n}...")

    # Ajoute les informations sur le texte et initialisation des annotations
    annotation[f"eslo {n}"] = {}
    annotation[f"eslo {n}"][f"source"] = i.strip()
    annotation[f"eslo {n}"]["nv_etudes"] = ne.strip()
    annotation[f"eslo {n}"]["tokens"] = []
    annotation[f"eslo {n}"]["pos"] = []
    annotation[f"eslo {n}"]["neg_comp"] = []
    annotation[f"eslo {n}"]["y_absent"] = []
    annotation[f"eslo {n}"]["schwa_absent"] = []
    # print("\t<eslo>")

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
            # print(f'<w pos="{token.pos_}', end='')
            complete_pos = token.pos_
            if token.pos_ == "VERB":
                if len(token.morph.get("Tense")) > 0:
                    complete_pos = token.pos_ + ":" + token.morph.get("Tense")[0]
                else:
                    complete_pos = token.pos_ + ":" + "Inf"
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
                    print(token, doc[j + 1].text, " : ypresent")
                else:
                    annotation[f"eslo {n}"]["y_absent"].append(True)
                    print(token, doc[j + 1].text, " : yabsent")

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

print(annotation)

texts.close()
ids.close()
