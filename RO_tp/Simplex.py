import numpy as np
from numpy import linalg as LA  # import linear algebra
from numpy.linalg import inv


def simplex_iteration(A, b, C, m: int, n: int):
    """Computes the optimal solution to the linear Program:
      Max C^tX
      Subject to: AX=b
      X >=0

    Arguments
      A: m × (n+m) array
      b: initial vector (length m)
      C: Objective coefficients (length n+m)
      n+m: dimension of X, must be >= 1

    Returns
      X: (n+m) x 1 vetor, solution to AX=b
      RC: 1x(n + m) vector, reduced costs of X and slack variables.
      Z: Objective value

    Intermediary
    B: m x m, Basis matrix.
    NB: n x m, Non-basis matrix
    """
    # intialization
    Iteration = 0
    Z = 0
    X = np.zeros((n + m))
    XB = np.zeros((m))
    CB = np.zeros((m))
    XN = np.zeros((n))
    CN = np.zeros((n))
    RC = np.zeros((n + m))
    Basis: int = np.zeros((m))
    B = np.zeros((m, m))
    NB = np.zeros((m, n))
    Index_Enter = -1
    Index_Leave = -1
    eps = 1e-12

    for i in range(0, m):
        Basis[i] = n + i
        for j in range(0, m):
            B[i, j] = A[i, n + j]
        for j in range(0, n):
            NB[i, j] = A[i, j]

    for i in range(0, n):
        CN[i] = C[i]
        print("CN: ", CN[i])

    RC = C - np.dot(CB.transpose(), np.dot(inv(B), A))
    MaxRC = 0
    for i in range(0, n + m):
        if (MaxRC < RC[i]):
            MaxRC = RC[i]
            Index_Enter = i

    print("Basis", Basis)
    while (MaxRC > eps):
        Iteration = Iteration + 1
        print("=> Iteration: ", Iteration)

        print(" Index_Enter: ", Index_Enter)
        Index_Leave = -1
        MinVal = 1000000
        print("Enter B: ", B)
        for i in range(0, m):
            if (np.dot(inv(B), A)[i, Index_Enter] > 0):
                bratio = np.dot(inv(B), b)[i] / np.dot(inv(B), A)[i, Index_Enter]
                print("  bratio: ", bratio)
                if (MinVal > bratio):
                    Index_Leave = i
                    print("  Index_Leave: ", Index_Leave)
                    MinVal = bratio
                    print("  MinVal: ", MinVal)
        if (Index_Leave == -1):
            print("Problem Unbounded.")
            return Z, X, RC
        Basis[Index_Leave] = Index_Enter
        print("before updated Basis", Basis)
        print("  Index_Leave: ", Index_Leave)
        for i in range(m - 1, 0, -1):
            if (Basis[i] < Basis[i - 1]):
                temp = Basis[i - 1]
                Basis[i - 1] = Basis[i]
                Basis[i] = temp

        print("updated Basis", Basis)

        for i in range(0, m):
            for j in range(0, n + m):
                if (j == Basis[i]):
                    B[:, i] = A[:, j]
                    CB[i] = C[j]

        print("Exit Basis", Basis)
        print("Exit B: ", B)

        RC = C - np.dot(CB.transpose(), np.dot(inv(B), A))
        MaxRC = 0
        for i in range(0, n + m):
            if (MaxRC < RC[i]):
                MaxRC = RC[i]
                Index_Enter = i
        print("MaxRC", MaxRC)
        X = np.dot(inv(B), b)
        Z = np.dot(CB, X)
    return Z, X, RC


# Example4:

C = np.array([[2], [3], [2], [0], [0]])
A = np.array([[1, 3, 2, 1, 0], [2, 2, 1, 0, 1]])
b = np.array([[4], [2]])

Z, X, RC = simplex_iteration(A, b, C, 2, 3)

print("Z", Z)
print("X", X)
print("RC", RC)

# Example1:
# A=np.array([[1,1,1,3,1,1,0,0],[1,4,1,3,1,0,1,0],[1,2,1,4,1,0,0,1]])
# b=np.array([[1],[2],[3]])
# C=np.array([5,3,4,2,3,0,0,0])


# Example2:
# A=np.array([[1,3,2,1,0,0],[2,2,1,0,1,0],[1,1,2,0,0,1]])
# b=np.array([[4],[2],[3]])
# C=np.array([2,3,2,0,0,0])

# Example3:
# A=np.array([[1,2,1,2,1,3,1,1,0,0],[1,3,4,2,1,3,1,0,1,0],[3,2,2,1,5,4,1,0,0,1]])
# b=np.array([[4],[4],[4]])
# C=np.array([4,3,5,3,3,4,3,0,0,0])

# Example4:
# A=np.array([[1, 2, 2, 2, 5, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [3, 5, 1, 4, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
# [4, 3, 2, 7, 1, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
# [2, 1, 7, 2, 6, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
# [3, 2, 1, 4, 3, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
# [1, 2, 5, 2, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
# [3, 2, 1, 4, 2, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
# [4, 3, 2, 8, 1, 6, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
# [2, 1, 4, 2, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
# [4, 2, 1, 4, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
# b=np.array([[9],[4],[5],[8],[7],[9],[6],[4],[3],[4]])
# C=np.array([5, 4, 3, 5, 8, 4,0,0,0,0,0,0,0,0,0,0])import numpy as np
# from numpy import linalg as LA # import linear algebra
# from numpy.linalg import inv
#
# def simplex_iteration(A, b, C, m: int, n: int):
#     """Computes the optimal solution to the linear Program:
#       Max C^tX
#       Subject to: AX=b
#       X >=0
#
#     Arguments
#       A: m × (n+m) array
#       b: initial vector (length m)
#       C: Objective coefficients (length n+m)
#       n+m: dimension of X, must be >= 1
#
#     Returns
#       X: (n+m) x 1 vetor, solution to AX=b
#       RC: 1x(n + m) vector, reduced costs of X and slack variables.
#       Z: Objective value
#
#     Intermediary
#     B: m x m, Basis matrix.
#     NB: n x m, Non-basis matrix
#     """
#     #intialization
#     Iteration=0
#     Z=0
#     X=np.zeros((n+m))
#     XB=np.zeros((m))
#     CB=np.zeros((m))
#     XN=np.zeros((n))
#     CN=np.zeros((n))
#     RC = np.zeros((n+m))
#     Basis:int=np.zeros((m))
#     B = np.zeros((m,m))
#     NB = np.zeros((m,n))
#     Index_Enter=-1
#     Index_Leave=-1
#     eps = 1e-12
#
#     for i in range(0,m):
#         Basis[i]=n+i
#         for j in range(0,m):
#          B[i, j]=A[i,n+j]
#         for j in range(0,n):
#          NB[i, j]=A[i,j]
#
#     for i in range(0,n):
#         CN[i]=C[i]
#         print("CN: ", CN[i])
#
#     RC=C-np.dot(CB.transpose(),np.dot(inv(B),A))
#     MaxRC=0
#     for i in range(0,n+m):
#         if(MaxRC<RC[i]):
#          MaxRC=RC[i]
#          Index_Enter=i
#
#     print("Basis", Basis)
#     while(MaxRC > eps):
#       Iteration=Iteration+1
#       print("=> Iteration: ",Iteration)
#
#       print(" Index_Enter: ",  Index_Enter)
#       Index_Leave=-1
#       MinVal=1000000
#       print("Enter B: ",B)
#       for i in range(0,m):
#        if(np.dot(inv(B),A)[i,  Index_Enter] > 0):
#          bratio=np.dot(inv(B),b)[i]/np.dot(inv(B),A)[i,  Index_Enter]
#          print("  bratio: ", bratio)
#          if(MinVal > bratio ):
#            Index_Leave=i
#            print("  Index_Leave: ",Index_Leave)
#            MinVal=bratio
#            print("  MinVal: ", MinVal)
#       if (Index_Leave == -1):
#          print("Problem Unbounded.")
#          return Z,X,RC
#       Basis[Index_Leave]=Index_Enter
#       print("before updated Basis", Basis)
#       print("  Index_Leave: ",Index_Leave)
#       for i in range(m-1,0,-1):
#         if(Basis[i] < Basis[i-1]):
#             temp=Basis[i-1]
#             Basis[i-1]=Basis[i]
#             Basis[i]=temp
#
#       print("updated Basis", Basis)
#
#       for i in range(0,m):
#           for j in range(0,n+m):
#               if(j==Basis[i]):
#                 B[:, i]=A[:,j]
#                 CB[i]=C[j]
#
#       print("Exit Basis", Basis)
#       print("Exit B: ",B)
#
#       RC=C-np.dot(CB.transpose(),np.dot(inv(B),A))
#       MaxRC=0
#       for i in range(0,n+m):
#         if(MaxRC<RC[i]):
#          MaxRC=RC[i]
#          Index_Enter=i
#       print("MaxRC",MaxRC)
#       X=np.dot(inv(B),b)
#       Z=np.dot(CB,X)
#     return Z, X, RC
#
# # Example4:
#
# C=np.array([[2],[3],[2],[0],[0]])
# A=np.array([[1,3,2,1,0],[2,2,1,0,1]])
# b=np.array([[4],[2]])
#
# Z,X,RC=simplex_iteration(A,b,C,2,3)
#
# print("Z", Z)
# print("X",X)
# print("RC",RC)
#
#
# # Example1:
# #A=np.array([[1,1,1,3,1,1,0,0],[1,4,1,3,1,0,1,0],[1,2,1,4,1,0,0,1]])
# #b=np.array([[1],[2],[3]])
# #C=np.array([5,3,4,2,3,0,0,0])
#
#
# #Example2:
# #A=np.array([[1,3,2,1,0,0],[2,2,1,0,1,0],[1,1,2,0,0,1]])
# #b=np.array([[4],[2],[3]])
# #C=np.array([2,3,2,0,0,0])
#
# # Example3:
# #A=np.array([[1,2,1,2,1,3,1,1,0,0],[1,3,4,2,1,3,1,0,1,0],[3,2,2,1,5,4,1,0,0,1]])
# #b=np.array([[4],[4],[4]])
# #C=np.array([4,3,5,3,3,4,3,0,0,0])
#
# # Example4:
# #A=np.array([[1, 2, 2, 2, 5, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #[3, 5, 1, 4, 2, 2, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
# #[4, 3, 2, 7, 1, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
# #[2, 1, 7, 2, 6, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
# #[3, 2, 1, 4, 3, 7, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
# #[1, 2, 5, 2, 5, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
# #[3, 2, 1, 4, 2, 7, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
# #[4, 3, 2, 8, 1, 6, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
# #[2, 1, 4, 2, 6, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
# #[4, 2, 1, 4, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
# #b=np.array([[9],[4],[5],[8],[7],[9],[6],[4],[3],[4]])
# #C=np.array([5, 4, 3, 5, 8, 4,0,0,0,0,0,0,0,0,0,0])