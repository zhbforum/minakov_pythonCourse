from utils import generate_random_matrix_int, print_matrix


def get_layer_indices(n, layer):
    top = [(layer, j) for j in range(layer, n - layer)]
    right = [(i, n - layer - 1) for i in range(layer + 1, n - layer)]
    bottom = [(n - layer - 1, j) for j in range(n - layer - 2, layer - 1, -1)]
    left = [(i, layer) for i in range(n - layer - 2, layer, -1)]

    return top + right + bottom + left


def rotate_layer(matrix, layer, k):
    n = len(matrix)
    indices = get_layer_indices(n, layer)

    if not indices:
        return

    values = [matrix[i][j] for i, j in indices]
    k %= len(values)
    rotated = values[-k:] + values[:-k]

    for idx, val in enumerate(rotated):
        i, j = indices[idx]
        matrix[i][j] = val


def rotate_matrix(matrix, k):
    n = len(matrix)
    for layer in range((n + 1) // 2):
        rotate_layer(matrix, layer, k)
    return matrix


def main():
    n = int(input("Input size of matrix: "))
    while n < 1:
        print("Size of matrix should be greater than 0")
        n = int(input("Input size of matrix: "))

    k = int(input("Input amount of rotation: "))

    matrix = generate_random_matrix_int(n, 1)

    print_matrix(matrix, "Original matrix:")
    rotate_matrix(matrix, k)
    
    print_matrix(matrix, "Matrix after rotation:")


if __name__ == "__main__":
    main()
