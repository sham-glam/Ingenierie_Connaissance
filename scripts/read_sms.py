from collections import defaultdict
from lxml import etree
from pprint import pprint
import regex

def clean(text):
    text = regex.sub(r'\s+', ' ', text.strip(), flags=regex.MULTILINE)
    return text

root = etree.parse('../data/brut/xml-SMS/cmr-88milsms-tei-v1.xml').getroot()
person_edu = {}

''' recup { id : niveau_education }  '''
# for p, edu in zip(root.xpath('//*[name()="person"]'), root.xpath('//*[name()="education"]')):
#     # for edu in root.xpath('//*[name()="education"]'):
#         xml_id = p.get('{http://www.w3.org/XML/1998/namespace}id')
#         education = edu.text
#         person_edu[xml_id] = education    
#         # export to a json file
# # pprint(person_edu)

dialogues = defaultdict(lambda: defaultdict(list))
'''   recup { who : [dialogues] }  '''
for post in root.xpath('//*[name()="post"]'):
    who = post.get('who')[1:]
    for p in post.xpath('.//following-sibling::*[name()="p"]'):
        
        try:
            # create a txt file to store the id
            if len(clean(p.text)) != 0: # exporter seulement si non vides
                with open('../data/transformes/xml-SMS_id/SMS_ids.txt', 'a') as f:
                    f.write(f"{who}\n")
                with open('../data/transformes/xml-SMS_contenu/SMS_contenu.txt', 'a') as f:
                    f.write(f"{clean(p.text)}\n")

            # creation du dictionnaire {id : dialogue}
            '''
            if who not in dialogues.keys():
                dialogues[who] = [clean(p.text)]
            else:
                dialogues[who].append(clean(p.text))
            '''
        except Exception as e:
            print(f"An error occurred while updating dialogues for '{who}': {e}")
 

''' impression dico'''
# for who, dialogues in dialogues.items():
#     print(f"{who} : {dialogues}")

'''exporter à un fichier json '''
# import json
# with open('../data/brut/json-SMS/dialogues.json', 'w') as f:
#     json.dump(dialogues, f, indent=4)