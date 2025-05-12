from utils import generate_random_rect_matrix, print_matrix
from collections import defaultdict


ROWS = 5
COLS = 7


def count_repeats(row):
    counts = defaultdict(int)
    for num in row:
        counts[num] += 1
    return sum(c - 1 for c in counts.values() if c > 1)


def sort_matrix_by_repeats(matrix):
    return sorted(matrix, key=count_repeats)


def find_first_non_negative_column(matrix):
    if not matrix or not matrix[0]:
        return -1

    num_cols = len(matrix[0])
    num_rows = len(matrix)

    for col in range(num_cols):
        if all(matrix[row][col] >= 0 for row in range(num_rows)):
            return col
    return None


def main():
    matrix = generate_random_rect_matrix(ROWS, COLS)
    sorted_matrix = sort_matrix_by_repeats(matrix)
    first_non_negative_col = find_first_non_negative_column(sorted_matrix)

    print_matrix(matrix, "Original matrix:")
    print_matrix(sorted_matrix, "Matrix sorted by repeated elements count:")

    print(f"\nFirst column without negative elements: {first_non_negative_col}")


if __name__ == "__main__":
    main()
