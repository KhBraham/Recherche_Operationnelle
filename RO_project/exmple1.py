import numpy as np
import pulp as lp
Q = 1000000
K = 10

T = [[3, 6],
     [7, 6]]

di = [5, 9]

si = [4, 3]

sj = [5, 5]

Dj = [11, 10]

B = 124

Cj = [10, 6]

dik = [[0, 0],
       [1, 0]]


Emp = range(len(sj))
Tch = range(len(si))
problem = lp.LpProblem("pr",lp.LpMinimize)

x = lp.LpVariable.dicts("X", ((i,j) for j in Emp for i in Tch), cat=lp.LpBinary)
CT = lp.LpVariable.dicts("CT", (i for i in Tch), lowBound=0)
Cmax = lp.LpVariable("Cmax", lowBound=0)
problem += K*Cmax+lp.lpSum(lp.lpSum(x[(I,J)]*T[I][J]*Cj[J] for J in Emp) for I in Tch)

for I in Tch:
    problem += lp.lpSum(x[(I,J)] for J in Emp) == 1

for I in Tch:
    problem += CT[I] >= lp.lpSum(x[(I,J)]*T[I][J] for J in Emp)

for I in Tch:
    for K in range(I):
        problem += CT[I] >= CT[K]+lp.lpSum(x[(I, J)]*T[I][J] for J in Emp)-Q*(1-dik[I][K])

for I in Tch:
    for K in range(I):
        for J in Emp:
            problem += CT[I] >= CT[K]+x[(I, J)]*T[I][J]-Q*(2-x[(I, J)]-x[(K, J)])

for I in Tch:
    problem += CT[I] <= di[I]

for I in Tch:
    problem += lp.lpSum(x[(I, J)]*sj[J] for J in Emp) >= si[I]

for J in Emp:
    problem += lp.lpSum(x[(I,J)]*T[I][J] for I in Tch) <= Dj[J]

problem += lp.lpSum(lp.lpSum(x[(I,J)]*T[I][J] for I in Tch)*Cj[J] for J in Emp) <= B


for I in Tch:
    problem += Cmax >= CT[I]

problem.solve()

for I in Tch:
    for J in Emp:
        #if x[(I,J)].varValue==1:
            print(f'X({I+1},{J+1})=', x[(I, J)].varValue)
print('temps min de realisation de projet : Cmax=', Cmax.varValue)
print('cout min: W=', problem.objective.value())


