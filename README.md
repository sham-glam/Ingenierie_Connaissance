## Projet Ingénierie de la Connaissance

Mise à disposition d’un corpus annoté pour étudier la variation sociolinguistique diastratique.

---

### Membres de l'équipe

- Kenza Ahmia
- Florian Jacquot
- Tifanny Nguyen
- Shami Thirion Sen

---

### Organisation du git du projet

- `./data` : le répertoire principal qui contient toutes les données des deux corpus.

  - `./data/annote` : contient tous les fichiers de sortie :

    - SMS_annotation.txm
    - ESLO_annotation.txm
    - SMS_annotation.xml
    - eslo_annotation.txt
    - eslo_annotation.xml
    - sms_annotation.txt

  - `./data/brut` : ce répertoire contient les deux répertoires des corpus bruts `xml-ESLO` et `xml-SMS`.

  - `./data/transformes` : ce répertoire contient toutes les données extraites des corpus bruts, stockées dans des sous-répertoires, comme les fichiers des contenus textuels, les identifiants, les niveaux d'études, etc.

- `./scripts` : ce répertoire contient tous les scripts utilisés tout au long du projet :

  - add_etudes_eslo.py
  - annotation-complete.py
  - annotation.py
  - eslo_to_xml.py
  - extract_eslo.py
  - sms_extraction.py

---

### Annotation

Vous avez la possibilité de tester le script d'annotation afin de reproduire les mêmes résultats que dans le répertoire `./data/annote`, c'est-à-dire un fichier XML avec toutes les annotations. Pour ce faire, il faut :

1. Cloner le git du projet

   ```bash
   git clone git@github.com:sham-glam/Ingenierie_Connaissance.git
   ```

2. Se positionner dans le répertoire `scripts` :

   ```bash
   cd Ingenierie_Connaissance/scripts
   ```

3. Annoter le corpus :

   **Le corpus 89milSMS**

   ```bash
   python annotation-complete.py sms
   ```

   **Le corpus ESLO**

   ```bash
   python3 annotation-complete.py eslo
   ```
