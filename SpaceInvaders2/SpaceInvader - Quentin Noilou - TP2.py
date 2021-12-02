"""! @brief [description du fichier]
 @file /home/quentin/Documents/Quentin/R107 - Prog/TP/SpaceInvaders/SpaceInvaders2/SpaceInvader - valid2.py<

 @section authors Author(s)
  - Créé par Quentin Noilou le 15/11/2021 .
"""
# Modules
from typing import Dict, List
from random import randint
import os
from time import sleep
from saisiCar import SaisiCar

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
    print("=" * infos["L"])

    # Affichage du tableau des scores
    print(" " * 4 + "SCORE"
          + " " * 4 + "VIE"
          + " " * 3 + "NIVEAU"
          )
    print(f'    {infos["score"]:5}  {infos["vie"]:5}    {infos["level"]:5}'
          )
    # ligne de séparation de fin
    print("=" * infos["L"])

    # création de la matrice de tableau pour le plateau de jeu
    # (matrice infos["L"] par infos["H"])
    # \033[0;37;40m = coloration du tableau en gris foncé

    for y in range(infos["H"]):
        for x in range(infos["L"]):
            
            # vérifie si un caractère à déjà été affiché 
            a_affiche : bool = False
            
            for alien in aliens:
                # si un alien est détecté à une position, affichage de "@" avec les couleurs
                if alien["posx"] == x and alien["posy"] == y :
                    print("\033[1;32;40m@", end="")
                    a_affiche = True
                    
            # affichage du vaisseau avec les couleurs
            if vaisseau["posx"] == x and y == infos["H"] - 1:
                print("\033[1;31;40m#", end="")
                
            # remplissage des espaces vides
            elif not(a_affiche):
                print("\033[0;37;40m ", end="")
        print("")

    # ligne de séparation de fin du plateau
    print("=" * infos["L"])


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
        @param infos : Dict[str, int] => Liste contenant les informations du plateau de jeu
        @param aliens : List[Dict[str, int]] => Liste contenant des dictionnaires pour chaque alien
    Retour de la fonction :
        @return None [Description]

    """
    sens = aliens[0]["sens"]
    bord : bool = False
    lesposx = {x['posx'] for x in aliens} 
    mx = min(lesposx)
    ma = max(lesposx)
    print(mx," ",ma)
    if sens :
        for a in aliens : 
            if a["posx"] <= 0 :
                bord = True
    else :
        for a in aliens :
            if a["posx"] >= plateau_jeu["L"] - 1 :
                bord = True
                
    for alien in aliens :
        if(bord):
            alien["posy"] += 1
            alien["sens"] = not(alien["sens"])
            
        else:
            if sens :
                alien["posx"] -= 1
            else :
                alien["posx"] += 1
                
                
                
def action_sur_vaisseau(vaisseau: Dict[str, int],
                        action: str,
                        infos: List[Dict[str, int]]) -> bool:
    """!
    @brief Fonction gérant le déplacement du vaisseau à partir des entrées clavier suivantes :
    'k' pour aller à gauche
    'm' pour aller à droite
    'o' pour tirer
    'q' pour quitter

    Paramètre(s) :
        @param vaisseau : Dict[str,int] => [description]
        @param action : str => [description]
        @param infos : List[Dict[str,int]] => [description]
    Retour de la fonction :
        @return bool [Description]

    """

    if action == 'k':
        vaisseau["posx"] -= 1
    elif action == 'm':
        vaisseau["posx"] += 1
    elif action == 'o':
        return True

    return False


def partie_finie(infos: Dict[str, int],
                 aliens: List[Dict[str, int]],
                 vaisseau: Dict[str, int]) -> bool:
    """!
    @brief Fonction déterminant si la partie est finie ou non

    Paramètre(s) :
        @param infos : Dict[str,int] => [description]
        @param aliens : List[Dict[str,int]] => [description]
        @param vaisseau : Dict[str,int] => [description]
    Retour de la fonction :
        @return bool [Description]

    """
    for i in aliens:
        if i["posy"] == infos["H"] - 3:
            return True
        else:
            return False


# Algorithme principal
if __name__ == '__main__':
    plateau_jeu: Dict[str, int] = {
        "L": 25,
        "H": 10,
        "score": 0,
        "vie": 3,
        "level": 1
    }
    leVaisseau: Dict[str, int] = {
        "posx": plateau_jeu["L"] // 2,
        "tir": 1
    }
    lesAliens: List[Dict[str, int]] = []
    print(bool(lesAliens))
    initAliens(plateau_jeu, lesAliens)

    partieFinie: bool = False
    action: str = "x"
    kb = SaisiCar()
    
    while not(partieFinie) and action != 'q':

        action = kb.recupCar(['k', 'm', 'o', 'q'])
        aTire: bool = action_sur_vaisseau(leVaisseau, action, plateau_jeu)
        affichagePlateauJeu(plateau_jeu, lesAliens, leVaisseau)
        deplacement_aliens(plateau_jeu, lesAliens)
        partieFinie = partie_finie(plateau_jeu, lesAliens, leVaisseau)
        sleep(0.1)