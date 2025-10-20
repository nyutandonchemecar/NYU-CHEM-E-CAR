import numpy as np

# --- Step 1: Create a 4x4 matrix as a list of lists ---
matrix_list = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]
print("Original matrix (list):")
for row in matrix_list:
    print(row)

# --- Step 2: Convert list to NumPy array ---
matrix_array = np.array(matrix_list)
print("\nMatrix as NumPy array:")
print(matrix_array)

# --- Step 3: Perform some operation (example: transpose) ---
transposed = matrix_array.T
print("\nTransposed matrix:")
print(transposed)

# --- Step 4: Convert NumPy array back to Python list ---
matrix_back_to_list = transposed.tolist()
print("\nConverted back to list:")
for row in matrix_back_to_list:
    print(row)
