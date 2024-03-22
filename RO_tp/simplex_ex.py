import numpy as np
from numpy.linalg import inv

def simplex_iteration(A, b, C, m: int, n: int):
    # initialization
    Iteration = 0
    Z = 0
    X = np.zeros((n + m))
    CB = np.zeros((m))
    RC = np.zeros((n + m))
    Basis = np.arange(n, n + m)  # Initialize Basis
    B = A[:, n:]  # Initial Basis matrix
    Index_Enter = 0
    eps = 1e-12

    while Iteration < 1000:  # Added iteration limit
        Iteration += 1
        print("=> Iteration: ", Iteration)

        print(" Index_Enter: ", Index_Enter)
        Index_Leave = -1
        MinVal = 1000000
        print("Enter B: ", B)
        for i in range(m):
            if np.dot(inv(B), A[:, Index_Enter])[i] > 0:
                bratio = np.dot(inv(B), b)[i] / np.dot(inv(B), A[:, Index_Enter])[i]
                print("  bratio: ", bratio)
                if MinVal > bratio:
                    Index_Leave = i
                    print("  Index_Leave: ", Index_Leave)
                    MinVal = bratio
                    print("  MinVal: ", MinVal)

        if Index_Leave == -1:
            print("Problem Unbounded.")
            return Z, X, RC

        Basis[Index_Leave] = Index_Enter
        print("updated Basis", Basis)

        # Sort Basis for consistency
        Basis = Basis[np.argsort(Basis)]

        # Update Basis matrix
        B = A[:, Basis - n]

        print("Exit Basis", Basis)
        print("Exit B: ", B)

        RC = C - CB @ inv(B) @ A
        MaxRC = max(RC)
        print("MaxRC", MaxRC)

        X = inv(B) @ b
        Z = CB @ X

        if MaxRC <= eps:
            break

        Index_Enter = np.argmax(RC)

    return Z, X, RC

# Example4:
C = np.array([[2], [3], [2], [0], [0]])
A = np.array([[1, 3, 2, 1, 0], [2, 2, 1, 0, 1]])
b = np.array([[4], [2]])

Z, X, RC = simplex_iteration(A, b, C, 2, 3)

print("Z", Z)
print("X", X)
print("RC", RC)
