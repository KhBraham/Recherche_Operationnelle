def Dijkstra(dg, s):

    #infini étant un majorant de la plus grande longueur d'un chemin tracé sur un graphe
    infini = sum(sum(dg[sommet][s2] for s2 in dg[sommet]) for sommet in dg) + 1
    s_connu = {s : [0, [s]]} #[Longueur, plus court chemin]
    s_inconnu = {k : [infini, ''] for k in dg if k != s} #[Longueur , precedent]
    for suivant in dg[s] :
        s_inconnu[suivant] = [dg[s][suivant], s]
    print('Dans le graphe d\'origine {} dont les arcs sont :' .format(s))
    for k in dg :
        print(k, ':', dg[k])
    print()
    print('Plus court chemin de: ')

    while s_inconnu and any(s_inconnu[k][0] < infini for k in s_inconnu):
        u = min(s_inconnu, key = s_inconnu.get)
        longueur_u, precedent_u = s_inconnu[u]
        for v in dg[u]:
            if v in s_inconnu:
                d = longueur_u + dg[u][v]
                if d < s_inconnu[v][0]:
                    s_inconnu[v] = [d, u]
        s_connu[u] = [longueur_u, s_connu[precedent_u][1] + [u]]
        del s_inconnu[u]
        print('longueur', longueur_u, ':', '->'.join(map(str, s_connu[u][1])))

    for k in s_inconnu:
        print('Il n\'y a aucun chemin de {} à {}.' .format(s, k))

    return s_connu

g = {
    'K' : {'M' : 4,
           'E' : 1},
    'M' :{'E' : 2,
          'H' : 2},
    'E' :{'M' : 1,
          'H' : 2,
          'F' : 1},
    'H' :{'F' : 3},
    'F' :{'H' : 1},
    'S' :{'H' : 1,
          'F' : 2}
}
Dijkstra(g, 'M')


