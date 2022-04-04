def prochaine_etape(grille):

    x_max = len(grille[0])
    y_max = len(grille)
    nouvelle_grille = [[0 for x in range(x_max)] for y in range(y_max)]
    
    for y in range(y_max):
        for x in range(x_max):
            nouvelle_grille[y][x] = etat_suivant(grille, x, y)

    return nouvelle_grille

def nVoisinsComtamine(L, x, y):
    nbVoisins = O
    for changeY in range(-1, 2):
            for changeX in range(-1, 2):
                if 0 <= x + changeX < len(L) and 0 <= y + changeY < len(L):
                    if L[y+changeY][x+changeX] == 1:
                        nbVoisins += 1
    return nbVoisins

def caseContamine(L, x, y, R):
    return nVoisinsContamine(L, x, y)//R[0] > random.random()
