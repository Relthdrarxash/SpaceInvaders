"""! @brief [description du fichier]
 @file /home/quentin/Documents/Quentin/R107 - Prog/TP/SpaceInvaders/SpaceInvaders1/spaceinvaders.py
 @section libs Librairies/Modules
  - [Nom du module] (lien)

 @section authors Author(s)
  - Créé par [Prénom] [Nom] le [Date] .
"""

# Modules
from typing import Dict, List
from random import randint

# Fonctions


def affichageInfos(infos: Dict[str, int]) -> None:
    """!
    @brief Procédure prenant en paramètre un dictionnaire et affiche de maniere textuelle ses informations

    Paramètre(s) : 
        @param infos : Dict[str,int] => [description]
    Retour de la fonction : 
        @return None [Description]

    """
    print(f'largeur : {infos["L"]} cases,',
          f'hauteur : {infos["H"]} lignes,',
          f'score : {infos["score"]},',
          f'vie : {infos["vie"]},',
          f'level : {infos["level"]}.')


def affichagePlateauJeu(infos: Dict[str, int], aliens: List[Dict[str, int]], vaisseau: Dict[str, int]) -> None:
    """!
    @brief Procédure affichant le tableau des scores

    Paramètre(s) : 
        @param infos : Dict[str,int] => [description]
        @param aliens : List[Dict[str,int]] => [description]
        @param vaisseau : Dict[str,int] => [description]
    Retour de la fonction : 
        @return None [Description]

    """
    # ligne de séparation de début
    print("=" * 50)

    # Affichage du tableau des scores
    print(" " * 4 + "SCORE"
          + " " * 4 + "VIE"
          + " " * 4 + "NIVEAU"
          )
    print(" " * 8 + str(infos["score"])
          + " " * 6 + str(infos["vie"])
          + " " * 9 + str(infos["level"])
          )
    # ligne de séparation de fin
    print("=" * 50)

    # création de la matrice de tableau pour le plateau de jeu
    # (matrice infos["L"] par infos["H"])
    # \033[0;37;40m = coloration du tableau en gris foncé
    tableau: List[List[str]] = [
                                ["\033[0;37;40m " for j in range(plateau_jeu["L"])]
                                for i in range(plateau_jeu["H"])
                                ]

    # affichage des aliens dans la matrice "tableau" [y][x]
    for i in aliens:
        # plateau_jeu["L"]//2 - 5 sert à centrer les aliens sans changer la valeur de départ
        # (éviter les conflits lors du retour au début du tableau au changement de ligne)
        # \033[1;32;47m = coloration des aliens en vert sur fond blanc
        tableau[i["posy"]][i["posx"] +
                           plateau_jeu["L"] // 2 - 5] = "\033[1;32;40m @"

    # affichage du vaisseau dans le tableau
    # \033[1;31;40m = coloration du vaisseau en rouge
    tableau[-1][vaisseau["posx"]] = "\033[1;31;40m #"
    # affichage du tableau
    for ligne in tableau:
        for caractere in ligne:
            print(caractere, end="")
        print("")

    # ligne de séparation de fin du plateau
    print("=" * 50)


def initAliens(infos: Dict[str, int], aliens: List[Dict[str, int]]) -> None:
    """!
    @brief Explication de la fonction

    Paramètre(s) : 
        @param infos : Dict[str,int] => [description]
        @param aliens : List[Dict[str,int]] => [description]
    Retour de la fonction : 
        @return None [Description]

    """
    
    # initialise le nombre d'aliens à 30 au début puis 10 aliens/niveau
    nbAliens: int = infos["level"] * 10 + 20
    nbAliensParLigne: int = 10

    # initialisé à -1 pour ne pas l'initialiser à 1 dans la boucle plus bas
    posy: int = -1

    # nombre d'aliens avec un tir à 2 ou 3
    nbChanceux: int = 0

    # création des aliens
    for i in range(nbAliens):
        # 9 % 10 = 9 : garde la position de chaque alien
        posx = i % nbAliensParLigne
        if posx == 0:
            posy += 1

        aleatoire = randint(0, 1)
        if aleatoire and nbChanceux < 5:
            aliens.append({
                "posx": posx,
                "posy": posy,
                "tir": randint(2, 3),
                "sens": 0
            })
            nbChanceux += 1

        else:
            aliens.append({
                "posx": posx,
                "posy": posy,
                "tir": 0,
                "sens": 0
            })


# Algorithme principal
if __name__ == '__main__':
    plateau_jeu: Dict[str, int] = {
        "L": 25,
        "H": 20,
        "score": 0,
        "vie": 3,
        "level": 1
    }
    leVaisseau: Dict[str, int] = {
        "posx": plateau_jeu["L"] // 2,
        "tir": 1
    }
    lesAliens: List[Dict[str, int]] = []

    initAliens(plateau_jeu, lesAliens)
    affichagePlateauJeu(plateau_jeu, lesAliens, leVaisseau)