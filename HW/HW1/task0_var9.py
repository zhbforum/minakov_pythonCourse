import itertools
from utils import generate_random_matrix_uniform


def smooth_matrix(matrix):
    n = len(matrix)
    smoothed = [[0] * n for _ in range(n)]

    for i, j in itertools.product(range(n), repeat = 2):
        neighbors = [
            matrix[i + di][j + dj]
            for di, dj in itertools.product([-1, 0, 1], repeat = 2)
            if not (di == 0 and dj == 0)
            and 0 <= i + di < n
            and 0 <= j + dj < n
        ]
        smoothed[i][j] = sum(neighbors) / len(neighbors)

    return smoothed


def sum_below_main_diagonal(matrix):
    return round(sum(abs(matrix[i][j]) for i in range(1, len(matrix)) for j in range(i)), 2)


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{num:6.2f}" for num in row))
    print()


def main():
    N = 10
    k = int(input("Input amount of smooth: "))

    matrix = generate_random_matrix_uniform(N)

    print("\nOriginal matrix:")
    print_matrix(matrix)

    for _ in range(k):
        matrix = smooth_matrix(matrix)

    print("\nMatrix after smoothing:")
    print_matrix(matrix)

    result = sum_below_main_diagonal(matrix)
    print(f"\nSum of elements modules below main diagonal: {result}")


if __name__ == "__main__":
    main()
