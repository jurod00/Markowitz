import numpy as np

class Minimization:
    def __init__(self):
        pass

    def quadraticProgramming(self, Q: np.ndarray, A: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
        m = A.shape[0]
        n = Q.shape[0]

        tol = 1e-9
        tau = 0.995
        sigma = 0.1

        x = np.ones(n)/n
        y = np.zeros(m)
        z = np.ones(n)/n

        for i in range(int(1e+3)):
            residualP = A @ x - b # Primal feasibility
            residualD = Q @ x + c - A.T @ y - z # Dual feasibility

            my = (x.T @ z)/n

            if np.linalg.norm(residualP) < tol and np.linalg.norm(residualD) < tol and my < tol:
                return x

            diagX = np.diag(x)
            diagZ = np.diag(z)

            ones = np.ones(n)

            residualC = diagX @ z - sigma*my*ones # Complementary slackness

            M = np.block(
                [
                    [Q, -A.T, -np.eye(n)], 
                    [A, np.zeros((m, m)), np.zeros((m, n))], 
                    [diagZ, np.zeros((n, m)), diagX]
                ]
            )
            residual = np.concatenate([-residualD, -residualP, -residualC])
            direction = np.linalg.solve(M, residual)

            alphaMaxP = 1
            alphaMaxD = 1

            for i in range(n):
                if direction[i] < 0:
                    alphaMaxP = min(alphaMaxP, -x[i]/direction[i])
                if direction[n+m+i] < 0:
                    alphaMaxD = min(alphaMaxD, -z[i]/direction[n+m+i])

            alphaP = min(1, tau*alphaMaxP)
            alphaD = min(1, tau*alphaMaxD)

            x += alphaP*direction[:n]
            y += alphaD*direction[n:n+m]
            z += alphaD*direction[n+m:]

        print("Warning: Maximum number of iterations reached in quadratic programming.")
        return x