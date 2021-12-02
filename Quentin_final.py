"""! @brief Programme pour faire un jeu SpaceInvaders en Python pour le projet de Programmation - R107
 @file Quentin_final.py
 @section libs Librairies/Modules
  - typing https://docs.python.org/3/library/typing.html
  - random https://docs.python.org/3/library/random.html
  - os https://docs.python.org/3/library/os.html
  - time https://docs.python.org/3/library/time.html
  - SaisiCar du module saisiCar 
  - platform https://docs.python.org/3/library/platform.html

 @section authors Author(s)
  - Créé par Quentin Noilou le 22/11/2021.
"""


# Modules
import platform
from typing import Dict, List, Tuple
from random import randint
import os
from time import sleep
from saisiCar import SaisiCar
from platform import system 

# Fonctions
def affichageInfos(infos: Dict[str, int]) -> None:
    """!
    @brief Procédure prenant en paramètre un dictionnaire et affiche
    de maniere textuelle ses informations

    Paramètre(s) :
        @param infos : Dict[str, int] => Dictionnaire contenant les informations du plateau de jeu
    Retour de la fonction :
        @return None

    """
    print(f'largeur : {infos["L"]} cases,',
          f'hauteur : {infos["H"]} lignes,',
          f'score : {infos["score"]},',
          f'vie : {infos["vie"]},',
          f'level : {infos["level"]}.')


def affichagePlateauJeu(infos: Dict[str, int],
                        aliens: List[Dict[str, int]],
                        vaisseau: Dict[str, int],
                        y_alien: bool or int = None) -> None:
    """!
    @brief Procédure affichant le plateau de jeu et tous ses composants (aliens, vaisseau, tirs spéciaux, tableau des scores)

    Paramètre(s) :
        @param infos : Dict[str, int] => Dictionnaire contenant les informations du plateau de jeu
        @param aliens : List[Dict[str, int]] => Liste de dictionnaires contenant les informations de chaque alien
        @param vaisseau : Dict[str, int] => Dictionnaire contenant les informations du vaisseau
        @param y_alien : bool or int = None => Position en y de l'alien le plus bas aligné avec le vaisseau. None par défaut (pas de tir à afficher)
    Retour de la fonction :
        @return None

    """

    # nettoyage du tableau selon l'OS  
    # pas optimisé, on pourrait le mettre à la fin et faire deux boucles de jeu différentes
    # pour réduire le nombre de tests mais alourdissement non nécessaire de la taille du code
    # si l'os est linux : utilisation de la commande clear
    if platform.system() == 'Linux' :
        os.system("clear")
    # si l'os est windows : utilisation de la commande cls
    elif platform.system() == 'Windows' :
        os.system("cls")

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
            a_affiche: bool = False
            
            # Par ordre d'importance, celui qui arrive en premier sera celui affiché
            
            # affichage du vaisseau avec les couleurs
            if vaisseau["posx"] == x and y == infos["H"] - 1:
                print("\033[1;31;40m#", end="")
                a_affiche = True
                
            # Boucle d'affichage de chaque alien
            for alien in aliens:
                # si un alien est détecté à une position, affichage de "@" avec
                # les couleurs
                if not(a_affiche) and alien["posx"] == x and alien["posy"] == y and not a_affiche:
                    print("\033[1;32;40m@", end="")
                    a_affiche = True
            
            # affichage du tir spécial des aliens
            if not(a_affiche) and infos["tirS"] != None and x == infos["tirS"][0] and y == infos["tirS"][1]:
                print(infos["tirS"][2], end="")
                if y == infos["H"] - 1:
                    if x == leVaisseau["posx"]:
                        leVaisseau["tir"] = max(leVaisseau["tir"], infos["tirS"][2])
                    infos["tirS"] = None
                a_affiche = True
                # On fait tomber le paquet de l'alien
                if infos["tirS"] != None :
                    while infos["tirS"][1] <= infos["H"] - 1 :
                        infos["tirS"] = (infos["tirS"][0], infos["tirS"][1] + 1, infos["tirS"][2])
                        sleep(0.01)
                
            # évolution du niveau de tir du vaisseau
            if not(a_affiche) and y_alien is not None and x == vaisseau["posx"] and y_alien < y and y < infos["H"] - 1:
                if vaisseau["tir"] == 1:
                    print("\033[1;31;40m:", end="") 
                elif vaisseau["tir"] == 2:
                    print("\033[1;31;40m§", end="")
                elif vaisseau["tir"] == 3:
                    print("\033[1;31;40m_", end="")

                a_affiche = True

            # remplissage des espaces vides
            elif not(a_affiche):
                print("\033[0;37;40m ", end="")

        print("|")

    # ligne de séparation de fin du plateau
    print("=" * infos["L"])


def initAliens(infos: Dict[str, int],
               aliens: List[Dict[str, int]]) -> None:
    """!
    @brief Procédure initialisant la valeur de la liste de dictionnaires contenant la valeur de chaque alien

    Paramètre(s) : 
        @param infos : Dict[str, int] => Dictionnaire contenant les informations du plateau de jeu
        @param aliens : List[Dict[str, int]] => Liste de dictionnaires contenant les informations de chaque alien
    Retour de la fonction : 
        @return None

    """

    assert set(infos.keys()) == {'L', 'H', 'score', 'vie', 'level', 'tirS'}
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

        # 50% de chance qu'un alien ai un tir entre 2 et 3
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


def deplacement_aliens(aliens: List[Dict[str, int]]) -> None:
    """!
    @brief Procédure permettant de déplacer les aliens

    Paramètre(s) :
        @param infos : Dict[str, int] => Dictionnaire contenant les informations du plateau de jeu
        @param aliens : List[Dict[str, int]] => Liste contenant des dictionnaires pour chaque alien
    Retour de la fonction :
        @return None or Tuple(int,int or None) le tuple contient le nombre d'aliens et le niveau de tir de l'alien tué sinon None

    """
    if len(aliens):
        sens = aliens[0]["sens"]
        bord: bool = False

        # si les aliens vont à gauche
        if sens:
            for a in aliens:
                # et qu'un alien a une posx à 0 alors ils ont atteint le bord
                if a["posx"] <= 0:
                    bord = True
        # si les aliens vont à droite
        else:
            for a in aliens:
                # et qu'un alien a une posx à la fin du plateau à droite alors
                # ils ont atteint le bord
                if a["posx"] >= plateau_jeu["L"] - 1:
                    bord = True

        for alien in aliens:
            # si les aliens on atteint le bord, ont déplace tous les aliens en
            # même temps et on change leur sens de déplacement
            if(bord):
                alien["posy"] += 1
                alien["sens"] = not(alien["sens"])

            else:
                # sinon on continue de les déplacer dans le sens qu'ils
                # suivaient
                if sens:
                    alien["posx"] -= 1
                else:
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
        @param vaisseau : Dict[str,int] => Dictionnaire contenant les informations du vaisseau
        @param action : str => Input clavier avec pour valeur parmi k,m,o ou q
        @param infos : List[Dict[str,int]] => Dictionnaire contenant les informations du plateau de jeu
    Retour de la fonction :
        @return bool : true si le vaisseau doit tirer, false sinon

    """

    if action == 'k' and vaisseau["posx"] > 0:
        vaisseau["posx"] -= 1
    elif action == 'm' and vaisseau["posx"] < infos["L"] - 1:
        vaisseau["posx"] += 1
    elif action == 'o':
        return True

    return False


def partie_finie(infos: Dict[str, int],
                 aliens: List[Dict[str, int]]) -> bool:
    """!
    @brief Fonction déterminant si la partie est finie ou non
    La partie est finie si les aliens ont atteint le bas du plateau ou si il n'y a plus d'aliens sur le plateau

    Paramètre(s) :
        @param infos : Dict[str,int] => Dictionnaire contenant les informations du plateau de jeu
        @param aliens : List[Dict[str,int]] => Liste de dictionnaires contenant les informations de chaque alien
    Retour de la fonction :
        @return bool true si la partie est finie, false sinon

    """
    fin: bool = False
    i: int = 0

    if not(len(aliens)):
        fin = True

    while i < len(aliens) and not(fin):
        if aliens[i]["posy"] == infos["H"] - 1:
            fin = True
        i += 1

    return fin


def alien_atteignable(aliens: List[Dict[str, int]],
                      vaisseau: Dict[str, int]) -> None or int:
    """!
    @brief Procédure permettant de trouver l'alien le plus bas sur la même colonne que le vaisseau

    Paramètre(s) :
        @param aliens : List[Dict[str,int]] => Liste contenant des dictionnaires pour chaque alien
        @param vaisseau : Dict[str,int] =>  Dictionnaire contenant les informations du vaisseau
    Retour de la fonction :
        @return None si aucun alien n'est atteignable or int la position en y de l'alien atteignable le plus proche

    """
    y_max: int = 0
    for alien in aliens:
        if alien["posx"] == vaisseau["posx"]:
            if alien["posy"] >= y_max:
                y_max = alien["posy"]

    if not(y_max):
        y_max = None

    return y_max


def alien_tue(vaisseau: Dict[str, int],
              aliens: List[Dict[str, int]],
              a_shoote: int or None,
              infos : Dict[str,int]) -> int:
    """!
    @brief Fonction gérant la mort des aliens

    Paramètre(s) :
        @param vaisseau : Dict[str,int] =>  Dictionnaire contenant les informations du vaisseau
        @param aliens : List[Dict[str,int]] => Liste contenant des dictionnaires pour chaque alien
        @param a_shoote : int or None => Permet de savoir si le vaisseau a tiré ou non
        @param infos : Dict[str,int] => Dictionnaire contenant les informations du plateau de jeu
    Retour de la fonction :
        @return int : le niveau max de tir des aliens mourus

    """

    # Liste des aliens morts
    a_morts : List[Dict[str,int]] = []
    
    # niveau de tir maximum rencontré dans les aliens tués
    niv_tir_max : int = 0
    # on parcourt la liste des aliens par la fin puisque ce sont eux qui arrivent en premier
    for alien in reversed(aliens) :
        # Si le vaisseau tir sur un alien
        if a_shoote and alien["posx"] == vaisseau["posx"] and alien["posy"] == y_atteignable:
            # on ajoute l'alien aux morts et on l'enlève de la liste des aliens vivants
            a_morts.append(alien)
            aliens.remove(alien)
            # score +5 par alien tué
            infos["score"] += 5
            
    for alien in a_morts :
        print(niv_tir_max)
        niv_tir_max = max(alien["tir"], niv_tir_max)
            
    nb_amorts = len(a_morts)        
    return niv_tir_max


# Algorithme principal
if __name__ == '__main__':
    # définition des caractéristiques du plateau de jeu
    plateau_jeu: Dict[str, int] = {
        "L": 25,
        "H": 20,
        "score": 0,
        "vie": 3,
        "level": 1,
        "tirS" : None
    }
    
    # définition des caractéristiques du vaisseau
    leVaisseau: Dict[str, int] = {
        "posx": plateau_jeu["L"] // 2,
        "tir": 1
    }
    
    # initialisation du dictionnaire des aliens (rempli plus tard)
    lesAliens: List[Dict[str, int]] = []

    # initialisation des variables utilisées dans la boucle principale
    partieFinie: bool = False
    action: str = "x"
    kb = SaisiCar()
    
    # première initialisations du dictionnaire des aliens pour commencer le jeu
    initAliens(plateau_jeu, lesAliens)

    while plateau_jeu["vie"] > 0 and action != 'q':

        # test de fin de partie
        partieFinie = partie_finie(plateau_jeu, lesAliens)
        
        # si la partie est finie
        if partieFinie:
            # si la partie est finie et qu'il reste des aliens c'est qu'ils ont atteint le bas du plateau
            # on recharge alors tous les aliens, on enlève une vie et on remet les tirs du vaisseau à 0
            if len(lesAliens) > 0:
                plateau_jeu["vie"] -= 1
                leVaisseau["tir"] = 1
                lesAliens.clear()
                
            # sinon c'est que le joueur a tué tous les aliens et on monte de niveau
            # on ajoute également un niveau de tir au vaisseau s'il n'est pas encore à 3
            else:
                plateau_jeu["level"] += 1
                if leVaisseau["tir"] < 3:
                    leVaisseau["tir"] += 1
            initAliens(plateau_jeu, lesAliens)

        action = kb.recupCar(['k', 'm', 'o', 'q'])
        deplacement_aliens(lesAliens)
        aTire: bool = action_sur_vaisseau(leVaisseau, action, plateau_jeu)
        y_atteignable: int or None = None
        
        if aTire:
            y_atteignable = alien_atteignable(lesAliens, leVaisseau)
            tirS : int = alien_tue(leVaisseau, lesAliens, aTire, plateau_jeu)
            
            if tirS in [2,3] :
                plateau_jeu["tirS"] = (leVaisseau["posx"], y_atteignable, tirS)
        
        affichagePlateauJeu(plateau_jeu, lesAliens, leVaisseau, y_atteignable)

        sleep(0.05)