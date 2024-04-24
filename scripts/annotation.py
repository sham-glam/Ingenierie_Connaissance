import spacy
import regex

nlp = spacy.load("fr_core_news_md")

input_file = "../data/transformes/xml-ESLO_contenu/ESLO2_ENT_1001_C_contenu.txt"

annotation = {}

list_neg = ['ne', "n'", 'n']
list_adv_neg = ['pas', 'rien', 'jamais', 'point', 'aucunement', 'aucun', 'aucunement', 'nul', 'nullement', 'nulle', 'plus']
list_neg_tok = list_neg + list_adv_neg

# print()
with open(input_file, 'r') as fin:
    i = 1
    for l in fin:
        complete_neg = None
        if i % 100 == 0:
            print(f"working on eslo {i}...")
            
        annotation[f"eslo {i}"] = {}
        annotation[f"eslo {i}"]["tokens"] = []
        annotation[f"eslo {i}"]["pos"] = []
        annotation[f"eslo {i}"]["neg_comp"] = []
        # print("\t<eslo>")
        
        complete_negation_in_sent = None
        if regex.findall(r"\b(ne|n')\b.*\b({0})\b".format('|'.join(list_adv_neg)), l):
            complete_negation_in_sent = True
            # in_complete_neg = False
            
        # if complete_negation_in_sent:
        #     annotation[f"eslo {i}"]["neg"] = True
            
        doc = nlp(l)
        for token in doc:
            if token.pos_!= 'SPACE':
                annotation[f"eslo {i}"]["tokens"].append(token.text)
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
                annotation[f"eslo {i}"]["pos"].append(complete_pos)
                
                if complete_negation_in_sent:
                    if token.text in list_neg:
                        position = len(annotation[f"eslo {i}"]["tokens"]) - 1
                        # position_verb = len(annotation[f"eslo {i}"]["neg_comp"]) + 1
                        # position_adv = len(annotation[f"eslo {i}"]["neg_comp"]) + 2
                        complete_neg = True
                #     elif token.text in list_adv_neg and complete_neg:
                #         complete_neg = False

                    if complete_neg and token.text in list_adv_neg and regex.match(r"(^VERB.*|AUX)", annotation[f"eslo {i}"]["pos"][position+1]):
                        annotation[f"eslo {i}"]["neg_comp"].append(True)
                        # print(annotation[f"eslo {i}"])
                    else:
                        annotation[f"eslo {i}"]["neg_comp"].append(None)
                        
                    # if complete_neg and                         annotation[f"eslo {i}"]["pos"][position_verb] == "VERB":
                    #     annotation[f"eslo {i}"]["neg_comp"].append(True)
                    # else:
                    #     annotation[f"eslo {i}"]["neg_comp"].append(None)
                    
                    # print(annotation[f"eslo {i}"])
                    
                # print('">', end='')
                # print(token.text, end='')
                # print('</w>', end=' ')

            
        # print('')
        i += 1
        
print(annotation)