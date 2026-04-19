# defs.h — Python Pseudocode

Global definitions and utility constants for the SYK model.

```python
import math
from typing import Complex

# Constants
epsilon = 1e-10
precision = 17  # std::numeric_limits<double>::digits10 + 2
q = 4  # total number of fermions in an interaction term

# Type alias
cpx = complex  # complex<double>

# Enum
class TIME_TYPE:
    REAL_TIME = 1
    EUCLIDEAN_TIME = 2

def SQR(x):
    return x * x

def binomial(n, k):
    """Compute binomial coefficient C(n, k)."""
    if n < 0 or k < 0 or n < k:
        return 0
    return int(math.comb(n, k))

def djb2_hash(s: str) -> int:
    """djb2 hash by Dan Bernstein."""
    hash_val = 5381
    for c in s:
        hash_val = ((hash_val << 5) + hash_val) + ord(c)
    return hash_val

def get_random_seed(run_name: str) -> int:
    """Generate a random seed from run name, time, and /dev/urandom."""
    dev_urandom_bytes = read_random_bytes_from_os()
    s = f"{run_name}!!!{current_time_seconds()}???{dev_urandom_bytes}"
    return djb2_hash(s)

def get_base_filename(data_dir: str, run_name: str) -> str:
    return f"{data_dir}/{run_name}"

def relative_err(expected: float, actual: float) -> float:
    return abs((expected - actual) / expected)
```
