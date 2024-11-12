import sys
from ortools.sat.python import cp_model

def Input():
    [n,m,s,L] = [int(x) for x in sys.stdin.readline().split()]
    A = {}
    for v in range (1, n+1):
        A[v] = []

    for k in range (m):
       [u,v,t,c] = [int(x) for x in sys.stdin.readline().split()]
       A[u].append([v,t,c])
       A[v].append([u,t,c])

    return n,m,s,L,A

def InputFile(filename):
    with open(filename, "r") as f:
        [n,m,s,L] = [int(x) for x in f.readline().split()]
        A = {}
        for v in range (1, n+1):
            A[v] = []

        for k in range (m):
            [u,v,t,c] = [int(x) for x in f.readline().split()]
            A[u].append([v,t,c])
            A[v].append([u,t,c])

    return n,m,s,L,A

n,m,s,L,A = Input()

E = []
for i in range(1,n+1):
    for [j,t,c] in A[i]:
        E.append([i,j,t,c])

model = cp_model.CpModel()

x = {}  #x[i,j]=1 mean that node i sends to node j
y = {}  #y[i]: time-point nodes i receive data

for i in range(1,n+1):
    for [j,t,c] in A[i]:
        x[i,j] = model.NewIntVar(0,1, 'x(' + str(i) + ',' + str(j) + ')')
for i in range(1,n+1):
    y[i] = model.NewIntVar(0,L, 'y(' + str(i) + ')')

obj = model.NewIntVar(0,10000, 'obj')

for i in range(1,n+1):
    for [j,t,c] in A[i]:
        b = model.NewBoolVar('')
        model.Add(x[i,j] == 1).OnlyEnforceIf(b)
        model.Add(x[i,j] == 0).OnlyEnforceIf(b.Not())
        model.Add(y[j] >= y[i] + t).OnlyEnforceIf(b)

model.Add(y[s] == 0) #start node s=0

for i in range(1,n+1):
    model.Add(y[i] <= L)

for j in range(1, n+1):
    if j != s:
        model.Add(sum(x[i,j] for [i,t,c] in A[j]) == 1)

model.Add(sum(x[i,j]*c for [i,j,t,c] in E) == obj)

model.Minimize(obj)

solver = cp_model.CpSolver()

solver.parameters.max_time_in_seconds = 5.0

status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(solver.Value(obj))

    # for [i,j,t,c] in E:
    #     if solver.Value(x[i,j]) > 0:
    #         print('select link from', i, 'to', j, 'with cost', c)
else:
    print('NO_SOLUTION')