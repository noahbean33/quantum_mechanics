# sparse-example.cc — Python Pseudocode

Minimal example of building a sparse matrix from triplets (demo/scratch file).

```python
from scipy import sparse

def main():
    # Build a sparse matrix from triplets
    N = 10  # example size
    col = 10
    x = 1.0

    rows = []
    cols = []
    vals = []

    for row in range(N):
        rows.append(row)
        cols.append(col)
        vals.append(x)

    mat = sparse.csc_matrix((vals, (rows, cols)), shape=(N, N))
    return 0

if __name__ == "__main__":
    main()
```
