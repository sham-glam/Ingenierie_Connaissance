from collections import defaultdict
from lxml import etree
from pprint import pprint

root = etree.parse('cmr-88milsms-tei-v1.xml').getroot()

# print(f'{root.tag} {root.attrib}')

person_edu = {}

''' recup { id : education }  '''
# for p, edu in zip(root.xpath('//*[name()="person"]'), root.xpath('//*[name()="education"]')):
#     # for edu in root.xpath('//*[name()="education"]'):
#         xml_id = p.get('{http://www.w3.org/XML/1998/namespace}id')
#         education = edu.text
#         person_edu[xml_id] = education
 
    
# pprint(person_edu)

dialogues = defaultdict(lambda: defaultdict(list))


'''   recup { who : [dialogues] }  '''
for post in root.xpath('//*[name()="post"]'):
    who = post.get('who')
    for p in post.xpath('.//following-sibling::*[name()="p"]'):
        try:
            if who not in dialogues.keys():
                # try:
                dialogues[who] = [p.text]
                # print(f"dialogues[who] : {dialogues[who]}")
                # except:
            else:
                dialogues[who].append(p.text)
                pprint(f"dialogues[who] : {dialogues}")
        except Exception as e:
            print(f"An error occurred while updating dialogues for '{who}': {e}")
 
