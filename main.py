def prochaine_etape(grille):

    x_max = len(grille[0])
    y_max = len(grille)
    nouvelle_grille = [[0 for x in range(x_max)] for y in range(y_max)]
    
    for y in range(y_max):
        for x in range(x_max):
            nouvelle_grille[y][x] = etat_suivant(grille, x, y)

    return nouvelle_grille


grille = [  [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0]]
            
print(grille)
