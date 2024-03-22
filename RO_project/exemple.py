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

B = 40

def formulate_problem(Ti, Di, Dj, Cij, dik, B):
    inf = 10 ** 10
    num_tasks = len(Di)
    num_resources = len(Dj)

    prob = lp.LpProblem('Minimize_Cost', lp.LpMinimize)
    Tf = lp.LpVariable.dicts('TaskEndTime', (i for i in range(num_tasks)), lowBound=0)
    x = lp.LpVariable.dicts("X", ((i, j) for j in range(num_resources) for i in range(num_tasks)), cat=lp.LpBinary)

    # Objective Function
    prob += lp.lpSum(Ti[i][j] * Cij[i][j] * x[i, j] for i in range(num_tasks) for j in range(num_resources))

    # Constraints
    add_constraints(prob, x, Tf, Ti, Di, Dj, dik, num_tasks, num_resources, inf, B)

    return prob, x, Tf


def add_constraints(prob, x, Tf, Ti, Di, Dj, dik, num_tasks, num_resources, inf, B):
    for i in range(num_tasks):
        # Each task is done once
        prob += lp.lpSum(x[i, j] for j in range(num_resources)) == 1

        # Task finish time >= task duration
        prob += Tf[i] >= lp.lpSum(x[i, j] * Ti[i][j] for j in range(num_resources))

        for k in range(i):
            # Precedence and resource constraints
            prob += Tf[i] >= Tf[k] + lp.lpSum(x[i, j] * Ti[i][j] for j in range(num_resources)) - inf * (1 - dik[i][k])
            for j in range(num_resources):
                prob += Tf[i] >= Tf[k] + x[i, j] * Ti[i][j] - inf * (2 - x[i, j] - x[k, j])

        # Task finish time <= task deadline
        prob += Tf[i] <= Di[i]

    for j in range(num_resources):
        # Check resource availability for each task
        for i in range(num_tasks):
            prob += Dj[j] >= x[i, j]

    # Budget constraint
    prob += lp.lpSum(Ti[i][j] * x[i, j] * Cij[i][j] for i in range(num_tasks) for j in range(num_resources)) <= B


def solve_problem(prob, x, Tf, num_tasks, num_resources):
    prob.solve()

    for i in range(num_tasks):
        for j in range(num_resources):
            if x[i, j].varValue == 1:
                print(f'X({i + 1},{j + 1}) =', x[i, j].varValue)

    print('Earliest completion time : Tmin =', max(Tf[i].varValue for i in range(num_tasks)))
    print('Project cost: W=', prob.objective.value())


# usage
problem, x, Tf = formulate_problem(Ti, Di, Dj, Cij, dik, B)
solve_problem(problem, x, Tf, len(Di), len(Dj))
