import sys
import spacy
import regex
import csv

def annotate_text(corpus, texts, ids):
    nlp = spacy.load("fr_core_news_md")
    print("Modèle spacy chargé...")

    annotation = {}

    list_neg = ['ne', "n'", 'n']
    list_adv_neg = ['pas', 'rien', 'jamais', 'point', 'aucunement', 'aucun', 'aucunement', 'nul', 'nullement', 'nulle', 'plus']
    list_neg_tok = list_neg + list_adv_neg

    for t, i in zip(texts, ids):
        complete_neg = None
        annotation[i] = {}
        annotation[i]["tokens"] = []
        annotation[i]["pos"] = []
        annotation[i]["neg_comp"] = []
        annotation[i]["y_absent"] = []
        annotation[i]["schwa_absent"] = []
        
        complete_negation_in_sent = None
        if regex.findall(r"\b(ne|n')\b.*\b({0})\b".format('|'.join(list_adv_neg)), t):
            complete_negation_in_sent = True
            
        doc = nlp(t)
        for j, token in enumerate(doc):
            if token.pos_ != 'SPACE':
                annotation[i]["tokens"].append(token.text)
                if token.pos_ == 'VERB':
                    if len(token.morph.get('Tense')) > 0:
                        complete_pos = token.pos_ + ':' + token.morph.get('Tense')[0]
                    else:
                        complete_pos = token.pos_ + ':' + 'Inf'
                else:
                    complete_pos = token.pos_
                annotation[i]["pos"].append(complete_pos)

                if complete_negation_in_sent:
                    if token.text in list_neg:
                        complete_neg = True

                    if complete_neg and token.text in list_adv_neg and regex.match(r"(^VERB.*|AUX)", annotation[i]["pos"][-1]):
                        annotation[i]["neg_comp"].append(True)
                    else:
                        annotation[i]["neg_comp"].append(None)

                if j < len(doc) - 1 and token.dep_ == "nsubj" and regex.match(r't\'', token.text) and regex.match(r'[aeiouy]', doc[j+1].text):
                    if token.text == 'tu':
                        annotation[i]["y_absent"].append(False)
                    else:
                        annotation[i]["y_absent"].append(True)
                elif j < len(doc) - 1 and regex.match(r'[cdjlmnqst]\'', token.text) and regex.match(r'^[^aeiouyéèhAEIOUYÉÈH]', doc[j+1].text):
                    annotation[i]["schwa_absent"].append(True)
                else:
                    annotation[i]["y_absent"].append(None)
                    annotation[i]["schwa_absent"].append(None)
    return annotation

def write_xml_output(annotations, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("<data>\n")
        for id, ann in annotations.items():
            f.write(f"<sms id='{id}'>\n")
            for token, pos in zip(ann["tokens"], ann["pos"]):
                f.write(f"<w pos='{pos}'>{token}</w>\n")
            f.write("</sms>\n")
        f.write("</data>\n")

if len(sys.argv) < 3:
    print("Usage: python3 process_tsv.py <input_tsv> <output_xml>")
    sys.exit(1)

input_tsv = sys.argv[1]
output_xml = sys.argv[2]

texts = []
ids = []

with open(input_tsv, 'r', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        ids.append(row[0])
        texts.append(row[1])

annotations = annotate_text('sms', texts, ids)
write_xml_output(annotations, output_xml) 
