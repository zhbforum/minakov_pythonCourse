# Description of tasks

## 1. Smoothing a matrix and calculating the sum of the absolute values ​​of the elements (Variant 9)

### Condition
- A 10×10 array is given. The smoothing operation creates a new matrix of the same size, where each element is calculated as the arithmetic mean of its neighbors. 
- Then, in the resulting matrix, it is necessary to find the sum of the absolute values ​​of the elements located below the main diagonal.


---

## 2. Cyclic shift of the elements of a square matrix  (Variant 14)

### Condition
A square array of size M×N is given. It is necessary to perform a cyclic shift of elements to the right by k positions according to the following principle:
- the elements of the first row are moved to the last column from top to bottom,
- the elements of the last column are moved to the last row from right to left,
- the elements of the last row are moved to the first column from bottom to top,
- the elements of the first column are moved to the first row from left to right.

For the remaining nested layers, the algorithm is repeated similarly.

---

## 3. Ordering the rows and finding a column without negative elements (Variant 16)

### Condition
- Order the rows of an integer rectangular matrix by the number of identical elements in each row (in ascending order).
- Find the number of the first column in which there are no negative elements.
