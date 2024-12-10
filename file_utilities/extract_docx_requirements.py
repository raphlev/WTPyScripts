import sys
import os
from docx import Document
from openpyxl import Workbook
import re

############################################
#              PARAMETRES GLOBAUX
############################################

# Liste des styles de titre (headings) considérés comme chapitres
CHAPTER_STYLES = ["Heading 1", "Heading 2", "Heading 3", "Heading 4", "Heading 5"]

# Expression régulière pour détecter la ligne annonçant les exigences
# "Exigences :" ou "Exigence :"
EXIGENCES_TRIGGER_REGEX = r"^Exigences?\s*:"

# Liste des suffixes/keywords utilisés pour nommer l'exigence
SUFFIX_KEYWORDS = ["Création", "Créer", "Filtre", "Filtrer", "Recherche", "Rechercher" , "Service", "Interface", "Data Model", "UI", "Contrôle"]

# Suffixe par défaut si aucun des mots-clés ci-dessus n'est trouvé
DEFAULT_SUFFIX = "Exigence"

# Noms des colonnes dans le fichier Excel
EXCEL_COLUMNS = ["Titre", "Nom Exigence", "Description"]

############################################
#             FONCTION PRINCIPALE
############################################

def extract_requirements(docx_path, xlsx_path):
    # Ouvrir le document Word
    document = Document(docx_path)
    
    # Préparer une structure pour stocker (Chapitre, Liste d'exigences)
    # format: { "Chapitre": ["exigence1", "exigence2", ...], ... }
    chapter_requirements = {}
    
    current_chapter = None
    collecting = False  # Indique si on est en train de collecter des exigences
    
    # Parcourir tous les paragraphes du document
    for para in document.paragraphs:
        style_name = para.style.name if para.style else ""
        
        # Vérifier si le paragraphe est un chapitre
        if style_name in CHAPTER_STYLES:
            # Nouveau chapitre détecté : on arrête la collecte d'exigences en cours
            collecting = False
            current_chapter = para.text.strip()
            if current_chapter not in chapter_requirements:
                chapter_requirements[current_chapter] = []
        else:
            # Paragraphe "normal" (corps)
            text = para.text.strip()
            if not text:
                continue
            
            # Si on détecte la ligne déclenchant la collecte
            if re.match(EXIGENCES_TRIGGER_REGEX, text, re.IGNORECASE):
                collecting = True
                continue
            
            # Si on est en mode collecte, chaque paragraphe non vide est une exigence
            if collecting and current_chapter is not None:
                chapter_requirements[current_chapter].append(text)
    
    # Génération du fichier Excel
    if os.path.exists(xlsx_path):
        os.remove(xlsx_path)
    
    wb = Workbook()
    ws = wb.active
    
    # Ecrire les en-têtes
    ws.append(EXCEL_COLUMNS)
    
    # Définir une fonction locale pour générer le nom d'exigence
    def generate_requirement_name(chapter_title, requirement_text):
        # Retirer les espaces du titre pour le nom
        base_name = chapter_title.replace(" ", "")
        
        # Chercher un suffixe parmi les mots clés
        chosen_suffix = None
        for s in SUFFIX_KEYWORDS:
            if re.search(rf"\b{s}\b", requirement_text, re.IGNORECASE):
                chosen_suffix = s
                break
        if chosen_suffix is None:
            # Si aucun suffixe trouvé, utiliser le suffixe par défaut
            chosen_suffix = DEFAULT_SUFFIX
        
        return f"{base_name} - {chosen_suffix}"
    
    # Remplir le tableau
    for chapter, req_list in chapter_requirements.items():
        for req in req_list:
            req_name = generate_requirement_name(chapter, req)
            ws.append([chapter, req_name, req])
    
    # Enregistrer le fichier Excel
    wb.save(xlsx_path)

############################################
#                  MAIN
############################################

if __name__ == "__main__":
    # Exemple d'utilisation:
    # python extract_requirements.py input.docx output.xlsx
    if len(sys.argv) < 3:
        print("Usage: python script.py input.docx output.xlsx")
        sys.exit(1)
    docx_path = sys.argv[1]
    xlsx_path = sys.argv[2]
    extract_requirements(docx_path, xlsx_path)
    print(f"Fichier Excel généré : {xlsx_path}")
