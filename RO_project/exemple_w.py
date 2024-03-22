import pulp as lp
# Données du problème
N = 5  # Nombre total de tâches
S = 3  # Nombre de compétences requises
M = 2  # Nombre de membres de l'équipe
V = {(1, 1): 0.8, (1, 2): 0.6, (2, 1): 0.7, (2, 2): 0.9, (3, 1): 0.5, (3, 2): 0.8}  # Disponibilité des membres
B = 2000  # Budget alloué au projet
Dn = {(1, 2): 1, (1, 3): 0, (1, 4): 1, (1, 5): 0, (2, 3): 1, (2, 4): 0, (2, 5): 1,
      (3, 4): 0, (3, 5): 0, (4, 5): 1}  # Matrice de dépendance entre les tâches
K = {(1, 1): 4, (1, 2): 3, (1, 3): 2, (2, 1): 3, (2, 2): 4, (2, 3): 2}  # Matrice définissant les compétences et l'expérience des candidats
R = {(1, 1): 2, (1, 2): 3, (1, 3): 1, (2, 1): 3, (2, 2): 4, (2, 3): 2, (3, 1): 1, (3, 2): 2, (3, 3): 3,
     (4, 1): 2, (4, 2): 3, (4, 3): 1, (5, 1): 3, (5, 2): 2, (5, 3): 2}  # Matrice définissant les niveaux requis de compétence
fbeg = {1: 0, 2: 1, 3: 0, 4: 2, 5: 1}  # Heures réelles de début des tâches
fend = {1: 3, 2: 2, 3: 3, 4: 2, 5: 1}  # Heures réelles de fin des tâches (ajustées)

Cm = {1: 100, 2: 150}  # Coût de location du membre

# Date limite du projet
D = 10

# Initialisation du problème
prob = lp.LpProblem("Projet_Affectation_Taches", lp.LpMinimize)

# Variables de décision
X = lp.LpVariable.dicts("X",((n,m) for n in range(1,N+1) for m in range(1,M+1)), cat=lp.LpBinary)

# Objectif 1: Minimiser la durée du projet
prob+=lp.lpSum(lp.lpSum(X[n,m]*fend[n] for n in range(1,N+1)) for m in range(1,M+1))
# Objectif 2: Minimiser le coût d'embauche des membres de l'équipe
#prob+=lp.lpSum(lp.lpSum(V[m,d]*Cm[m] for m in range(1,M+1)) for d in range(1,D+1))
# Objectif 3: Maximiser l'expérience des candidats sélectionnés
#prob += lp.lpSum([X[n, m] * K[m, s] for n in range(1, N + 1) for m in range(1, M + 1) for s in range(1, S + 1)])
# Contraintes
# Contrainte 1: Toutes les tâches sont attribuées aux membres
for n in range(1, N + 1):
    prob += lp.lpSum([X[n,m] for m in range(1, M + 1)]) == 1

# Contrainte 2: Une tâche n'est attribuée qu'à un seul membre
for n in range(1, N + 1):
    prob += lp.lpSum([X[n,m] for m in range(1, M + 1)]) == 1

# Contrainte 3: Un membre n'effectue pas simultanément deux tâches
#for m in range(1, M + 1):
    #for n1 in range(1, N):
        #for n2 in range(n1 + 1, N + 1):
            #prob += max(0, (min(X[n1,m] * fend[n1], X[n2,m] * fend[n2])-max(X[n1,m] * fbeg[n1], X[n2,m] * fbeg[n2]))) == 0

# Contrainte 4: Tâches dépendantes ne peuvent pas être exécutées en même temps
#for je in range(1, N):
    #for j in range(je + 1, N + 1):
        #prob += Dn[je,j]fbeg[j]-Dn[je,j](fend[je]+1) >= 0

# Contrainte 5: Tâche attribuée au seul membre qui remplit les conditions
for n in range(1, N + 1):
    for m in range(1, M + 1):
        for s in range(1, S + 1):
            prob += R[n,s] <= X[n,m] * K[m,s]

# Contrainte 6: Projet se termine à l'heure
#prob += fend[N + 1] <= D

# Contrainte 7: Coûts ne dépassent pas le budget
prob += lp.lpSum([X[n,m] * Cm[m] for n in range(1, N + 1) for m in range(1, M + 1)]) <= B

# Résolution du problème
prob.solve()

# Affichage des résultats
print("Statut de la résolution:", lp.LpStatus[prob.status])

# Affichage de l'affectation des tâches
for m in range(1, M + 1):
    for n in range(1, N + 1):
        if lp.value(X[n, m]) == 1:
            print(f"Opérateur {m} effectue la tâche {n}")

# Affichage du coût minimum
print("Coût minimum d'embauche des membres:", lp.value(prob.objective))

# Affichage de la durée minimale du projet
print("Durée minimale du projet:", lp.value(prob.objective))

# Affichage de l'expérience du projet
print("Expérience du projet:", -1 * lp.value(prob.objective))

