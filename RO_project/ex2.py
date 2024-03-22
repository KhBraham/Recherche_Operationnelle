from pulp import *
import pandas as pd


# Initialise the model
model = LpProblem("Affectation_des_taches", LpMinimize)

# Sets
resources = ['R1', 'R2']  # Liste des ressource (noms ou IDs)
tasks = ['T1', 'T2']  # Liste des tâches (noms ou IDs)

# Parameters
Cmax = {'T1': 3, 'T2': 5}  # La dernière tâche réalisée
B = 100  # Budget disponible
Q = 1010
K = 2

# Matrice de dépendance entre les tâches (valeur 1 si la tâche i dépend de la tâche k sinon 0)
Dik = {
    'T1': {'T1': 0, 'T2': 0},
    'T2': {'T1': 1, 'T2': 0},
}

# Le coût pour chaque ressource pour effectuer chaque tâche
Si = {'T1': 2, 'T2': 5}

# Compétences offertes par chaque ressource humaine
Sj = {'R1': 7, 'R2': 3}

# Decision variables
x = LpVariable.dicts("x", (tasks, resources), 0, 1, LpBinary)

# Objective
model += lpSum(K * Cmax[i] * x[i][j] for i in tasks for j in resources)

# Contraintes
for i in tasks:
    model += lpSum(x[i][j] for j in resources) == 1

    for k in tasks:
        if k < i:
            for j in resources:
                model += x[i][j] * Cmax[i] <= x[k][j] * Cmax[k] + Q * (1 - Dik[i][k])

        # budget constraint
model += lpSum(Sj[j] * Si[i] * x[i][j] for i in tasks for j in resources) <= B

# Contraint de compétence
for j in resources:
    for i in tasks:
        model += Si[i] * x[i][j] <= Sj[j]

    # Résolution du problème
model.solve()

# Print des résultats
output = []
for i in tasks:
    for j in resources:
        if x[i][j].varValue > 0:
            output.append([i, j, x[i][j].varValue*100])

output_df = pd.DataFrame(output, columns=["Tache", "Ressource", "Affectation %"])
print(output_df)
