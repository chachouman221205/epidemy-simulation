import random

def prochaine_etape(grille):

    x_max = len(grille[0])
    y_max = len(grille)
    nouvelle_grille = [[0 for x in range(x_max)] for y in range(y_max)]
    
    for y in range(y_max):
        for x in range(x_max):
            nouvelle_grille[y][x] = etat_suivant(grille, x, y)

    return nouvelle_grille

def n_voisins_contamine(L, x, y):
    nb_voisins = O
    for change_x in range(-1, 2):
            for change_y in range(-1, 2):
                if 0 <= x + change_x < len(L) and 0 <= y + change_y < len(L):
                    if type(L[y + change_y][x + change_x]) == int:
                        nb_voisins += 1
    return nb_voisins

def case_est_contamine(L, x, y, R):
    return n_voisins_contamine(L, x, y)/R["nb_voisins"] > random.random()

def case_contamine(L, x, y, R):
    if case_est_contamine(L, x, y, R):
        L[y][x] = random.randint(R["tps_min"], R["tps_max"])

# Initialisation des variables

R = {"nb_voisins": 3, "tps_min": 8,"tps_max": 10, "proba_mort": 0.01}
V = [[1 for y in range(10)] for x in range(10)] # Liste de vulnérabilité à la mort
