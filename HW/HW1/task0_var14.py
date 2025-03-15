import random

def generateRandomMatrix(n, min_val = 1, max_val = 100):
    return [[random.randint(min_val, max_val) for _ in range(n)] for _ in range(n)]

def rotateLayer(matrix, layer, k):
    n = len(matrix)
    indices = []

    for j in range(layer, n - layer):
        indices.append((layer, j))
        
    for i in range(layer + 1, n - layer):
        indices.append((i, n - layer - 1))
        
    for j in range(n - layer - 2, layer - 1, -1):
        indices.append((n - layer - 1, j))
        
    for i in range(n - layer - 2, layer, -1):
        indices.append((i, layer))

    if not indices:
        return

    values = [matrix[i][j] for i, j in indices]

    k = k % len(values)
    
    rotated = values[-k:] + values[:-k]

    for idx, (i, j) in enumerate(indices):
        matrix[i][j] = rotated[idx]

def rotateMatrix(matrix, k):
    n = len(matrix)
    layers = (n + 1) // 2
    for layer in range(layers):
        rotateLayer(matrix, layer, k)
    return matrix

if __name__ == "__main__":
    n = int(input("Input size of matrix: "))
    while True:
        if n < 1:
            print("Size of matrix should be greater than 0")
            n = int(input("Input size of matrix: "))
        else:
            break
        
    k = int(input("Input amount of rotation: "))  
    
    matrix = generateRandomMatrix(n, 1, 20)  

    print("Original matrix: ")
    for row in matrix:
        print(row)

    rotateMatrix(matrix, k)

    print("\nMatrix after rotation: ")
    for row in matrix:
        print(row)
