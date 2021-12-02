# Modules
from typing import Dict, List
from random import randint
import os
from time import sleep

# Fonctions


def affichageInfos(infos: Dict[str, int]) -> None:
    """ Procédure prenant en paramètre un dictionnaire et affiche
    de maniere textuelle ses informations


    Args:
        infos (Dict[str, int]): dictionnaire contenant les informations du plateau de jeu
    """
    print(f'largeur : {infos["L"]} cases,',
          f'hauteur : {infos["H"]} lignes,',
          f'score : {infos["score"]},',
          f'vie : {infos["vie"]},',
          f'level : {infos["level"]}.')


def affichagePlateauJeu(infos: Dict[str, int],
                        aliens: List[Dict[str, int]],
                        vaisseau: Dict[str, int]) -> None:
    """Procédure affichant le plateau de jeu

    Args:
        infos (Dict[str, int]): dictionnaire contenant les informations du plateau de jeu
        aliens (List[Dict[str, int]]): liste de dictionnaires contenant les informations de chaque alien
        vaisseau (Dict[str, int]): dictionnaire contenant les informations du vaisseau
    """
    # nettoyage du tableau
    os.system("clear")

    # ligne de séparation de début
    print("=" * 50)

    # Affichage du tableau des scores
    print(" " * 4 + "SCORE"
          + " " * 4 + "VIE"
          + " " * 4 + "NIVEAU"
          )
    print(f'    {infos["score"]:5}  {infos["vie"]:5}    {infos["level"]:5}'
          )
    # ligne de séparation de fin
    print("=" * 50)

    # création de la matrice de tableau pour le plateau de jeu
    # (matrice infos["L"] par infos["H"])
    # \033[0;37;40m = coloration du tableau en gris foncé

    for y in range(infos["H"]):
        for x in range(infos["L"]):
            for alien in aliens:
                if alien["posx"] == x and alien["posy"] == y:
                    print("\033[1;32;40m@", end="")
            if vaisseau["posx"] == x and y == infos["H"] - 1:
                print("\033[1;31;40m#", end="")
            else:
                print("\033[0;37;40m ", end="")
        print("")

    # ligne de séparation de fin du plateau
    print("=" * 50)


def initAliens(infos: Dict[str, int],
               aliens: List[Dict[str, int]]) -> None:
    """Procédure initialisant la valeur de la liste de dictionnaires contenant la valeur de chaque alien

    Args:
        infos (Dict[str, int]): dictionnaire contenant les informations du plateau de jeu
        aliens (List[Dict[str, int]]): liste de dictionnaires contenant les informations de chaque alien
    """

    assert set(infos.keys()) == {'L', 'H', 'score', 'vie', 'level'}
    assert type(aliens) == list

    # initialise le nombre d'aliens à 30 au début puis 10 aliens/niveau
    nbAliens: int = infos["level"] * 15 + 15
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


def deplacement_aliens(infos: Dict[str, int],
                       aliens: List[Dict[str, int]]) -> None:
    """!
    @brief Procédure permettant de déplacer les aliens

    Paramètre(s) :
        @param infos : Dict[str, int] => [description]
        @param aliens : List[Dict[str, int]] => [description]
    Retour de la fonction :
        @return None [Description]

    """
    for i in aliens:
        if i["sens"] :
            i["posx"] -= 1
        elif not(i["sens"]) :
            i["posx"] += 1    
            
        if i["posx"] == infos["L"] or i["posx"] == 0 :
            i["sens"] = not(i["sens"])
            i["posy"] += 1


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
    affichagePlateauJeu(plateau_jeu, lesAliens, leVaisseau)

    for i in range(20):
        affichagePlateauJeu(plateau_jeu, lesAliens, leVaisseau)
        deplacement_aliens(plateau_jeu, lesAliens)
        sleep(0.05)