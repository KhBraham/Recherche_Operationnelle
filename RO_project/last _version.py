import pulp as lp


def formuler_projet_planification(Q, K, T, di, si, sj, Dj, B, Cj, dik):
    nb_taches = len(di)
    nb_ressources = len(Dj)

    probleme = lp.LpProblem("Minimiser_Cout", lp.LpMinimize)
    x = lp.LpVariable.dicts("X", ((i, j) for j in range(nb_ressources) for i in range(nb_taches)), cat=lp.LpBinary)
    CT = lp.LpVariable.dicts("CT", (i for i in range(nb_taches)), lowBound=0)
    Cmax = lp.LpVariable("Cmax", lowBound=0)

    # Fonction Objectif
    probleme += K * Cmax + lp.lpSum(x[i, j] * T[i][j] * Cj[j] for j in range(nb_ressources) for i in range(nb_taches))

    # Contraintes
    for i in range(nb_taches):
        probleme += lp.lpSum(x[i, j] for j in range(nb_ressources)) == 1
        probleme += CT[i] >= lp.lpSum(x[i, j] * T[i][j] for j in range(nb_ressources))

        for k in range(i):
            probleme += CT[i] >= CT[k] + lp.lpSum(x[i, j] * T[i][j] for j in range(nb_ressources)) - Q * (1 - dik[i][k])

            for j in range(nb_ressources):
                probleme += CT[i] >= CT[k] + x[i, j] * T[i][j] - Q * (2 - x[i, j] - x[k, j])

        probleme += CT[i] <= di[i]
        probleme += lp.lpSum(x[i, j] * sj[j] for j in range(nb_ressources)) >= si[i]

    for j in range(nb_ressources):
        probleme += lp.lpSum(x[i, j] * T[i][j] for i in range(nb_taches)) <= Dj[j]

    probleme += lp.lpSum(x[i, j] * T[i][j] * Cj[j] for j in range(nb_ressources) for i in range(nb_taches)) <= B

    for i in range(nb_taches):
        probleme += Cmax >= CT[i]

    return probleme, x, CT, Cmax


def resoudre_projet_planification(probleme, x, CT, Cmax, nb_taches, nb_ressources):
    probleme.solve()

    for i in range(nb_taches):
        for j in range(nb_ressources):
            if x[i, j].varValue == 1:
                print(f'X({i + 1},{j + 1}) =', x[i, j].varValue)
                print('\t --> la tache ', i + 1, 'affectée à le ressource humaine', j + 1)
        print('\t --> la date limite du tache ', i + 1, ': le', int(CT[i].varValue), '[UT]')
    print()
    print('la date limite minimum de réalisation du projet : dans le ', Cmax.varValue, '[UT]')
    print('Coût minimum pour realisée ce projet : ', probleme.objective.value(), '[UM]')


if __name__ == '__main__':
    # Exemple d'utilisation
    Q = 10 ** 10
    K = 10
    T = [[3, 6, 4], [7, 6, 8], [5, 4, 6]]
    di = [5, 9, 7]
    si = [4, 3, 5]
    sj = [5, 5, 4]
    Dj = [11, 10, 12]
    B = 150
    Cj = [10, 6, 8]
    dik = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]

    probleme, x, CT, Cmax = formuler_projet_planification(Q, K, T, di, si, sj, Dj, B, Cj, dik)
    resoudre_projet_planification(probleme, x, CT, Cmax, len(di), len(Dj))
