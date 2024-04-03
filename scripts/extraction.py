import spacy
import regex

nlp = spacy.load("fr_core_news_md")

input_file = "../DATA/ESLO2_ENT_1062_C_contenu.txt"

annotation = {}

# print()
with open(input_file, 'r') as fin:
    i = 0
    for l in fin:
        annotation[f"eslo {i}"] = {}
        annotation[f"eslo {i}"]["tokens"] = []
        annotation[f"eslo {i}"]["pos"] = []
        # print("\t<eslo>")
        doc = nlp(l)
        for token in doc:
            if token.pos_!= 'SPACE':
                annotation[f"eslo {i}"]["tokens"].append(token.text)
                annotation[f"eslo {i}"]["pos"].append(token.pos_)
        #         print(f'<w pos="{token.pos_}', end='')
        #         if token.pos_ == 'VERB':
        #             print(':', end='')
        #             if len(token.morph.get('Tense')) > 0:
        #                 print(token.morph.get('Tense')[0], end='')
        #             else:
        #                 print('Unk', end='')
        #         print('">', end='')
        #         print(token.text, end='')
        #         print('</w>', end=' ')
        # print('')
        # print("\t</sms>")
        i += 1
        
print(annotation)