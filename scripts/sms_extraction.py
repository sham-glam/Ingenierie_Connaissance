from collections import defaultdict
from lxml import etree
from pprint import pprint
import regex
import os

## suppression des espaces multiples
def clean(text):
    text = regex.sub(r'\s+', ' ', text.strip(), flags=regex.MULTILINE)
    return text

## recuperation du root
def get_root():
    root = etree.parse('../data/brut/xml-SMS/cmr-88milsms-tei-v1.xml').getroot()
    return root




def get_person_niveauEtude():
    """
    Recupere le niveau d'education de chaque personne
    :return: dictionnaire {id : niveau_education}
    : exporte dans un fichier tsv
    """
    root = get_root()
    person_edu = {}
    for p, edu in zip(root.xpath('//*[name()="person"]'), root.xpath('//*[name()="education"]')):
        xml_id = p.get('{http://www.w3.org/XML/1998/namespace}id')
        education = edu.text
        person_edu[xml_id] = education    

        # export to tsv file xml_id \t education 
        # create filepath if not exists
        if not os.path.exists('../data/transformes/tsv/'):
            os.makedirs('../data/transformes/tsv/')

        ''' export to tsv file'''
        ## décommenter si on souhaite exporter à un fichier tsv
        with open('../data/transformes/tsv/SMS_id_education.tsv', 'a') as f:
            f.write(f"{xml_id}\t{education}\n")

    return person_edu


def append_to_tsv(who, edu):
    """
    AJOUTE les locuteurs avec niveau d'études inconnus au fichier tsv
    :param who: id de la personne
    :param edu: niveau d'education
    """
    with open('../data/transformes/tsv/SMS_id_education.tsv', 'a') as f:
        f.write(f"{who}\t{edu}\t\n")

def create_id_dialogues_txt(root, person_edu):
    """
    Creation des fichiers txt pour id et contenu en parallele
    :param root: root du fichier xml
    :param person_edu: dictionnaire {id : niveau_education}

    :return: dictionnaire { who : [dialogues] }
    : stockage dans des fichiers tsv

    """
    dialogues = defaultdict(lambda: defaultdict(list))
    without_edu_info = []
    #   recup { who : [dialogues] }
    for post in root.xpath('//*[name()="post"]'):
        who = post.get('who')[1:]
        for p in post.xpath('.//following-sibling::*[name()="p"]'):
            
            ## création fichier txt pour id et contenu
            try:
                # create a txt file to store the id
                if len(clean(p.text)) != 0: # exporter seulement si non vides
                    if not os.path.exists('../data/transformes/xml-SMS_id/'):
                        os.makedirs('../data/transformes/xml-SMS_id/')
                        with open('../data/transformes/xml-SMS_id/SMS_ids.txt', 'a') as f:
                            f.write(f"{who}\n")
                    if not os.path.exists('../data/transformes/xml-SMS_contenu/'):
                        os.makedirs('../data/transformes/xml-SMS_contenu/')
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

            ## creation des fichiers tsv pour id education et dialogues
            try:
                if len(clean(p.text)) != 0: # exporter seulement si non vides
                    with open('../data/transformes/tsv/SMS_id_education_dialogues.tsv', 'a') as f:
                        if who not in person_edu.keys():
                            person_edu[who] = 'inconnu'
                            append_to_tsv(who, person_edu[who])
                        f.write(f"{who}\t{person_edu[who]}\t{clean(p.text)}\n")

            except Exception as e:
                # print(f"An error occurred while updating dialogues for '{who}': {e}")
                without_edu_info.append(who)

    return dialogues




def main():
    root = get_root() # recuperation du root
    person_edu = get_person_niveauEtude() # dictionnaire {id : niveau_education}
    dialogues = create_id_dialogues_txt(root, person_edu) # creation des fichiers txt pour id et contenu


if __name__ == '__main__':
    main()