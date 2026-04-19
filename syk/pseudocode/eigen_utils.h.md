# eigen_utils.h — Python Pseudocode

Type aliases and utility functions for linear algebra (wrapping Eigen library).

```python
import numpy as np
from scipy import sparse

# Type aliases (Eigen -> numpy equivalents)
# Mat         = complex dense matrix (Dynamic x Dynamic)
# RealMat     = real dense matrix
# RealVec     = real column vector
# Vec         = complex column vector
# SpMat       = complex sparse matrix (CSC)
# RealSpMat   = real sparse matrix
# RowMajorSpMat = complex sparse matrix (CSR), for cuSPARSE
# CpxTriplet  = (row, col, complex_value) for building sparse matrices
# RealTriplet = (row, col, real_value)

def get_random_vector(size, rng) -> np.ndarray:
    """Return a random complex vector of given size (normal dist)."""
    return np.array([complex(rng.normal(), rng.normal()) for _ in range(size)])

def get_random_real_vector(size, rng) -> np.ndarray:
    """Return a random real vector of given size (normal dist)."""
    return np.array([rng.normal() for _ in range(size)])

def get_random_matrix(rows, cols, rng) -> np.ndarray:
    """Return a random complex matrix (normal dist)."""
    return np.array([[complex(rng.normal(), rng.normal())
                      for _ in range(cols)] for _ in range(rows)])

def write_matrix_binary(out_file, matrix):
    """Write matrix dimensions and data to binary file."""
    rows, cols = matrix.shape
    out_file.write(rows, cols, matrix.data)

def read_matrix_binary(in_file) -> np.ndarray:
    """Read matrix from binary file."""
    rows, cols = in_file.read_ints(2)
    data = in_file.read_complex_array(rows * cols)
    return data.reshape(rows, cols)

def write_vector_binary(out_file, vec):
    out_file.write(len(vec), vec.data)

def read_vector_binary(in_file) -> np.ndarray:
    size = in_file.read_int()
    return in_file.read_complex_array(size)

def write_real_vector_binary(out_file, vec):
    out_file.write(len(vec), vec.data)

def read_real_vector_binary(in_file) -> np.ndarray:
    size = in_file.read_int()
    return in_file.read_float_array(size)

def get_head(v, n):
    """Return first n elements of v."""
    return v[:n]

def get_unique_elements(v, unique_eps):
    """Given sorted v, return elements differing by more than unique_eps."""
    if len(v) == 0:
        return np.array([])
    uniques = [v[0]]
    for i in range(1, len(v)):
        if abs(uniques[-1] - v[i]) > unique_eps:
            uniques.append(v[i])
    return np.array(uniques)

def add_nonzeros_to_triplets(triplets, mat, row_offset=0, col_offset=0):
    """Add non-zero elements of dense mat to triplets list with offsets."""
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] != 0:
                triplets.append((i + row_offset, j + col_offset, mat[i, j]))
```
