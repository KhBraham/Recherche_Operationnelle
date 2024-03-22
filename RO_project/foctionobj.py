import pulp as lp
inf = 10**10

Ti = [[4, 5, 4],
      [5, 4, 5],
      [4, 6, 5]]
Di = [3, 4, 8]
Dj = [8, 5, 3]
Cij = [[2, 5, 4],
       [5, 6, 7],
       [4, 3, 5]]
dik = [[0, 0, 0],
       [1, 0, 0],
       [0, 0, 0]]

B = 400
e = range(len(Dj))
t = range(len(Di))

fonction = lp.LpProblem('Cout', lp.LpMinimize)

x = lp.LpVariable.dicts("X", ((i, j) for j in e for i in t), cat=lp.LpBinary)
Tf = lp.LpVariable.dicts('Tf', (i for i in t), lowBound=0)

fonction += lp.lpSum(lp.lpSum(x[(I,J)]*Ti[I][J]*Cij[I][J] for J in e) for I in t)
for I in t:
    fonction += lp.lpSum(x[(I,J)] for J in e) == 1

for I in t:
    fonction += Tf[I] >= lp.lpSum(x[(I,J)]*Ti[I][J] for J in e)

for I in t:
    for k in range(I):
        fonction += Tf[I] >= Tf[k] + lp.lpSum(x[(I, J)]*Ti[I][J] for J in e) - inf*(1-dik[I][k])

for I in t:
    for k in range(I):
        for J in e:
            fonction += Tf[I] >= Tf[k] + x[(I,J)]*Ti[I][J] - inf*(2 - x[(I,J)] - x[(k,J)])

for I in t:
    fonction += Tf[I] <= Di[I]

for J in e:
    for I in t:
        fonction += Dj[J] >= x[(I,J)]

fonction += lp.lpSum(lp.lpSum(x[(I,J)]*Ti[I][J]*Cij[I][J] for I in t) for J in e) <= B

fonction.solve()

for I in t:
    for J in e:
        if x[(I,J)].varValue==1:
            print(f'X({I+1},{J+1})=', x[(I, J)].varValue)
print('temps min de realisation de projet : Tmin =', max(Tf[i].varValue for i in t))
print('cout de projet: W=', fonction.objective.value())