from utils import generate_random_matrix_int


def rotate_layer(matrix, layer, k):
    n = len(matrix)

    top = [(layer, j) for j in range(layer, n - layer)]
    right = [(i, n - layer - 1) for i in range(layer + 1, n - layer)]
    bottom = [(n - layer - 1, j) for j in range(n - layer - 2, layer - 1, -1)]
    left = [(i, layer) for i in range(n - layer - 2, layer, -1)]

    indices = top + right + bottom + left

    if not indices:
        return

    values = [matrix[i][j] for i, j in indices]
    k %= len(values)
    rotated = values[-k:] + values[:-k]

    for idx, (i, j) in enumerate(indices):
        matrix[i][j] = rotated[idx]


def rotate_matrix(matrix, k):
    n = len(matrix)
    for layer in range((n + 1) // 2):
        rotate_layer(matrix, layer, k)
    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{val:3}" for val in row))
    print()


def main():
    n = int(input("Input size of matrix: "))
    while True:
        if n < 1:
            print("Size of matrix should be greater than 0")
            n = int(input("Input size of matrix: "))
        else:
            break

    k = int(input("Input amount of rotation: "))

    matrix = generate_random_matrix_int(n, 1)

    print("\nOriginal matrix:")
    print_matrix(matrix)

    rotate_matrix(matrix, k)

    print("Matrix after rotation:")
    print_matrix(matrix)


if __name__ == "__main__":
    main()
