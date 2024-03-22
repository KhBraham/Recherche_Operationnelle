from pulp import *
import pandas as pd

# Initialise the model
model = LpProblem("Affectation_des_taches", LpMinimize)

# Sets
resources = ['R1', 'R2', 'R3']  # Liste des ressources humaines
tasks = ['T1', 'T2', 'T3', 'T4', 'T5']  # Liste des tâches

# Parameters
Cmax = {'T1': 3, 'T2': 5, 'T3': 2, 'T4': 4, 'T5': 6}
B = 200  # budget
Q = 1010
K = 2

# Matrice de dépendance entre les tâches (1 si la tâche i dépend de la tâche k sinon 0)
Dik = {
    'T1': {'T1': 0, 'T2': 0, 'T3': 0, 'T4': 0, 'T5': 0},
    'T2': {'T1': 1, 'T2': 0, 'T3': 0, 'T4': 0, 'T5': 0},
    'T3': {'T1': 0, 'T2': 1, 'T3': 0, 'T4': 0, 'T5': 0},
    'T4': {'T1': 0, 'T2': 0, 'T3': 1, 'T4': 0, 'T5': 0},
    'T5': {'T1': 0, 'T2': 0, 'T3': 0, 'T4': 1, 'T5': 0},
}

# Le coût pour chaque ressource pour effectuer chaque tâche
Si = {'T1': 1, 'T2': 2, 'T3': 3, 'T4': 4, 'T5': 5}

# Compétences offertes par chaque ressource humaine
Sj = {'R1': 3, 'R2': 6, 'R3': 8}

# Decision variables
x = LpVariable.dicts("x", (tasks, resources), 0, 1, LpBinary)

# Objective
model += lpSum(K * Cmax[i] * x[i][j] for i in tasks for j in resources)

# Contraintes
for i in tasks:
    model += lpSum(x[i][j] for j in resources) == 1
    for k in tasks:
        for j in resources:
            if k < i:
                model += x[i][j] * Cmax[i]   <= x[k][j] * Cmax[k]  + Q * (1 - Dik[i][k])

# budget constraint
model += lpSum(Sj[j] * Si[i] * x[i][j] for i in tasks for j in resources) <= B

# Contraint de compétence
for j in resources:
    for i in tasks:
        model += Si[i] * x[i][j] <= Sj[j]

# Create solver with tolerance
solver = CPLEX(timeLimit=300, gapRel=1e-9)  # Adjust parameters as needed

# Solve the model using the specified solver
model.solve(solver)

# Format output as integers
output = []
for i in tasks:
    for j in resources:
        if x[i][j].varValue > 0:
            output.append([i, j, int(x[i][j].varValue)])  # Convert to integer

output_df = pd.DataFrame(output, columns=["Tache", "Ressource", "Affectation"])

print(output_df)
