import random


def generate_random_matrix_uniform(n):
    return [[round(random.uniform(-10, 10), 2) for _ in range(n)] for _ in range(n)]


def generate_random_matrix_int(n, min_val=1, max_val=100):
    return [[random.randint(min_val, max_val) for _ in range(n)] for _ in range(n)]


def generate_random_rect_matrix(rows, cols, min_val=-10, max_val=10):
    return [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]


def print_matrix(matrix, title=None, float_format=False):
    if title:
        print(f"\n{title}")
    for row in matrix:
        print(" ".join(f"{val:6.2f}" if float_format else f"{val:3}" for val in row))
    print()
