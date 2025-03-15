import random

def generateRandomMatrix(n = 10):
    return [[round(random.uniform(-10, 10), 2) for _ in range(n)] for _ in range(n)]

def smoothMatrix(matrix, n = 0):
    new_matrix = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            neighbors = []
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and (ni != i or nj != j):
                        neighbors.append(matrix[ni][nj])

            new_matrix[i][j] = sum(neighbors) / len(neighbors)

    return new_matrix

def sumDiagonal(matrix, n = 10):
    return round(sum(abs(matrix[i][j]) for i in range(1, n) for j in range(i)), 2)

def printMatrix(matrix):
    for row in matrix:
        print(" ".join(f"{num:6.2f}" for num in row))
    print()

if __name__ == "__main__":
    n = 10  
    k = int(input("Input amount of smooth: "))

    matrix = generateRandomMatrix(n)

    print("\nOriginal matrix:")
    printMatrix(matrix)

    for _ in range(k):
        matrix = smoothMatrix(matrix, n)

    print("\nMatrix after smoothing:")
    printMatrix(matrix)

    result = sumDiagonal(matrix, n)
    print(f"\nSum of elements modules below main diagonal: {result}")
