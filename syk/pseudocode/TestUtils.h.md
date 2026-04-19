# TestUtils.h — Python Pseudocode

Testing utility functions (GTest-like assertions for matrices and eigenvalues).

```python
import numpy as np

def assert_matrix_is_zero(mat: np.ndarray, eps: float = 1e-10):
    """Assert that all matrix elements are below eps."""
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            assert abs(mat[i, j]) < eps, f"Element ({i},{j}) = {mat[i,j]} is not zero"

def assert_equal_matrices(A: np.ndarray, B: np.ndarray, eps: float = 1e-10):
    """Assert that two matrices are element-wise equal within eps."""
    assert A.shape == B.shape
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            assert abs(A[i, j] - B[i, j]) < eps, \
                f"Mismatch at ({i},{j}): {A[i,j]} vs {B[i,j]}"

def assert_equal_vectors(a: np.ndarray, b: np.ndarray, eps: float = 1e-10):
    """Assert that two vectors are element-wise equal within eps."""
    assert len(a) == len(b)
    for i in range(len(a)):
        assert abs(a[i] - b[i]) < eps, f"Mismatch at [{i}]: {a[i]} vs {b[i]}"

def assert_cpx_equal(a: complex, b: complex, eps: float = 1e-10):
    assert abs(a - b) < eps, f"Complex mismatch: {a} vs {b}"

def verify_same_evs(evs1: np.ndarray, evs2: np.ndarray, eps: float = 1e-10):
    """Verify two sorted eigenvalue lists are the same within eps."""
    s1 = np.sort(evs1)
    s2 = np.sort(evs2)
    assert len(s1) == len(s2), f"Length mismatch: {len(s1)} vs {len(s2)}"
    for i in range(len(s1)):
        assert abs(s1[i] - s2[i]) < eps, \
            f"Eigenvalue mismatch at [{i}]: {s1[i]} vs {s2[i]}"
```
