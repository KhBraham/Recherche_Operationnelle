from pulp import *

# Définition des données
T = [[3, 6], [7, 6]]
di = [5, 9]
si = [4, 3]
sj = [5, 5]
Dj = [11, 10]
B = 124
Cj = [10, 6]
dik = [[0, 0], [1, 0]]
Q = 1000

# Définition des variables
Emp = range(len(sj))
Tch = range(len(si))
x = LpVariable.dicts("X", ((i,j) for j in Emp for i in Tch), cat=LpBinary)
CT = LpVariable.dicts("CT", (i for i in Tch), lowBound=0)
Cmax = LpVariable("Cmax", lowBound=0)

# Définition du problème
problem = LpProblem("pr",LpMinimize)

# Fonction objectif
problem += 3*Cmax+lpSum(lpSum(x[(I,J)]*T[I][J]*Cj[J] for J in Emp) for I in Tch)

# Contrainte d'affectation unique
for I in Tch:
  problem += lpSum(x[(I,J)] for J in Emp) == 1

# Contrainte de durée minimale
for I in Tch:
  problem += CT[I] >= lpSum(x[(I,J)]*T[I][J] for J in Emp)

# Contrainte de précédence
for I in Tch:
  for K in range(I):
    problem += CT[I] >= CT[K]+lpSum(x[(I, J)]*T[I][J] for J in Emp)-Q*(1-dik[I][K])

# Contrainte de disjonction
for I in Tch:
  for K in range(I):
    for J in Emp:
      problem += CT[I] >= CT[K]+x[(I, J)]*T[I][J]-Q*(2-x[(I, J)]-x[(K, J)])

# Contrainte de durée maximale
for I in Tch:
  problem += CT[I] <= di[I]

# Contrainte de capacité minimale
for I in Tch:
  problem += lpSum(x[(I, J)]*sj[J] for J in Emp) >= si[I]

# Contrainte de date limite
for J in Emp:
  problem += lpSum(x[(I,J)]*T[I][J] for I in Tch) <= Dj[J]

# Contrainte budgétaire
problem += lpSum(lpSum(x[(I,J)]*T[I][J]*Cj[J] for I in Tch)*Cj[J] for J in Emp) <= B

# Contrainte de Cmax
for I in Tch:
  problem += Cmax >= CT[I]

# Résolution du problème
problem.solve()

# Affichage des résultats
for I in Tch:
  for J in Emp:
    print(f'X({I+1},{J+1})=', x[(I, J)].varValue)
print('temps min de realisation de projet : Cmax=', Cmax.varValue)
print('cout min: W=', problem.objective.value())
