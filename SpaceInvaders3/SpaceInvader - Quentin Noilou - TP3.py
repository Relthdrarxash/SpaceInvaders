"""! @brief [description du fichier]
 @file /home/quentin/Documents/Quentin/R107 - Prog/TP/SpaceInvaders/SpaceInvaders2/SpaceInvader - valid2.py<

 @section authors Author(s)
  - Créé par Quentin Noilou le 22/11/2021 .
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
                        vaisseau: Dict[str, int],
                        y_alien : bool or int = None) -> None:
    """!
    @brief Procédure affichant le plateau de jeu

    Paramètre(s) : 
        @param infos : Dict[str, int] => dictionnaire contenant les informations du plateau de jeu
        @param aliens : List[Dict[str, int]] => liste de dictionnaires contenant les informations de chaque alien
        @param vaisseau : Dict[str, int] => dictionnaire contenant les informations du vaisseau
        @param y_alien : bool or int = None => Position en y de l'alien le plus bas aligné avec le vaisseau. None par défaut (pas de tir à afficher)
    Retour de la fonction : 
        @return None 

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
                if alien["posx"] == x and alien["posy"] == y and not a_affiche:
                    print("\033[1;32;40m@", end="")
                    a_affiche = True
                    
            # affichage du vaisseau avec les couleurs
            if vaisseau["posx"] == x and y == infos["H"] - 1:
                print("\033[1;31;40m#", end="")
                a_affiche = True
            
            if y_alien != None and x == vaisseau["posx"] and y_alien < y and y < infos["H"] - 1:
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


def deplacement_aliens(aliens: List[Dict[str, int]]) -> None:
    """!
    @brief Procédure permettant de déplacer les aliens

    Paramètre(s) :
        @param infos : Dict[str, int] => Liste contenant les informations du plateau de jeu
        @param aliens : List[Dict[str, int]] => Liste contenant des dictionnaires pour chaque alien
    Retour de la fonction :
        @return None [Description]

    """
    if len(aliens) :
        sens = aliens[0]["sens"]
        bord : bool = False
        lesposx = {x['posx'] for x in aliens} 
        mx = min(lesposx)
        ma = max(lesposx)
        # print(mx," ",ma)
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

    if action == 'k' and vaisseau["posx"] > 0 :
        vaisseau["posx"] -= 1
    elif action == 'm' and vaisseau["posx"] < infos["L"] -1 :
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
        @param infos : Dict[str,int] => [description]
        @param aliens : List[Dict[str,int]] => [description]
    Retour de la fonction :
        @return bool [Description]

    """
    fin : bool = False
    i : int = 0
    
    if not(len(aliens)) :
        fin = True
    
    while i < len(aliens) and not(fin) :
        if aliens[i]["posy"] == infos["H"] - 1:
            fin = True
        i += 1
    
    return fin

def alien_atteignable(aliens : List[Dict[str,int]],
                      vaisseau : Dict[str,int]) -> None or int:
    """!
    @brief Procédure permettant de trouver l'alien le plus bas sur la même colonne que le vaisseau
    

    Paramètre(s) : 
        @param aliens : List[Dict[str,int]] => Liste contenant des dictionnaires pour chaque alien
        @param vaisseau : Dict[str,int] =>  Dictionnaire contenant les informations du vaisseau
    Retour de la fonction : 
        @return None si aucun alien n'est atteignable or int la position en y de l'alien atteignable le plus proche

    """
    y_max : int = 0
    for alien in aliens:
        if alien["posx"] == vaisseau["posx"]:
            if alien["posy"] >= y_max:
                y_max = alien["posy"]
        
    if not(y_max):    
        y_max = None
    print(y_max)
    return y_max

def alien_tue(vaisseau : Dict[str, int],
              aliens : List[Dict[str, int]],
              a_shoote : int or None) -> int :
    """!
    @brief Fonction gérant la mort des aliens

    Paramètre(s) : 
        @param vaisseau : Dict[str, int] => [description]
        @param aliens : List[Dict[str, int]] => [description]
        @param a_shoote : int or None => [description]
    Retour de la fonction : 
        @return int le nombre d'aliens morts

    """

    nb_amorts : int = 0
    
    for alien in reversed(aliens) :
        if a_shoote and alien["posx"] == vaisseau["posx"] and alien["posy"] == y_atteignable :
            aliens.remove(alien)
            nb_amorts +=1
            plateau_jeu["score"] += 5
    
    return nb_amorts
    
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
    print(bool(lesAliens))
    

    partieFinie: bool = False
    action: str = "x"
    kb = SaisiCar()
    initAliens(plateau_jeu, lesAliens)
    
    while plateau_jeu["vie"] > 0 and action != 'q':
        
        partieFinie = partie_finie(plateau_jeu, lesAliens)
        if partieFinie :
            if len(lesAliens) > 0 :
                plateau_jeu["vie"] -= 1
                leVaisseau["tir"] = 1
                lesAliens.clear()
            else :
                plateau_jeu["level"] += 1
            initAliens(plateau_jeu, lesAliens)
                
        action = kb.recupCar(['k', 'm', 'o', 'q'])
        deplacement_aliens(lesAliens)
        aTire: bool = action_sur_vaisseau(leVaisseau, action, plateau_jeu)
        y_atteignable : int or None = None
        if aTire :
            y_atteignable = alien_atteignable(lesAliens, leVaisseau)
            alien_tue(leVaisseau, lesAliens, aTire)
        affichagePlateauJeu(plateau_jeu, lesAliens, leVaisseau, y_atteignable)
        
        sleep(0.05)