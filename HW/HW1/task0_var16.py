import random

def countRepeats(row):
    counts = {}
    for num in row:
        counts[num] = counts.get(num, 0) + 1
    return sum(c - 1 for c in counts.values() if c > 1)

def sortMatrixByRepeats(matrix):
    return sorted(matrix, key=countRepeats)

def findFirstNonNegativeColumn(matrix):
    if not matrix or not matrix[0]:
        return -1  
    numCols = len(matrix[0])
    numRows = len(matrix)
    for col in range(numCols):
        if all(matrix[row][col] >= 0 for row in range(numRows)):
            return col  
    return "There is no non-negative element in any of the columns"

def generateRandomMatrix(rows, cols, minVal=-10, maxVal=10):
    return [[random.randint(minVal, maxVal) for _ in range(cols)] for _ in range(rows)]

if __name__ == '__main__':
    rows = 5        
    cols = 7        
    minVal = -10    
    maxVal = 10     
    
    matrix = generateRandomMatrix(rows, cols, minVal, maxVal)
    sortedMatrix = sortMatrixByRepeats(matrix)
    firstNonNegativeCol = findFirstNonNegativeColumn(sortedMatrix)
    
    print("Original matrix:")
    for row in matrix:
        print(row)
    
    print("\nOrdered matrix:")
    for row in sortedMatrix:
        print(row)
    
    print("\nFirst column without negative elements:", firstNonNegativeCol)
