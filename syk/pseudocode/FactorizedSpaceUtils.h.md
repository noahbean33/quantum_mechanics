# FactorizedSpaceUtils.h — Python Pseudocode

Factorized Hilbert space representation: split into left ⊗ right for efficient GPU computation.

```python
import numpy as np

class ChargeParity:
    EVEN_CHARGE = 0
    ODD_CHARGE = 1

class FactorizedSpace(Space):
    """
    Hilbert space factorized as left ⊗ right.
    For N Majorana fermions, D = 2^{N/2}, each side has dimension sqrt(D).
    States are matrices (sqrt(D) x sqrt(D)) instead of vectors.
    Basis ordering: even charge states first, then odd charge states.
    """

    def __init__(self):
        super().__init__()
        self.left = Space()
        self.right = Space()

    @staticmethod
    def from_majorana(N: int, N_left: int = None) -> 'FactorizedSpace':
        assert N % 2 == 0
        space = FactorizedSpace()
        if N_left is None:
            space._fact_init_dirac(N // 2)
        else:
            assert N_left % 2 == 0
            space._fact_init_dirac(N // 2, N_left // 2)
        return space

    @staticmethod
    def from_dirac(Nd: int, Nd_left: int = None) -> 'FactorizedSpace':
        space = FactorizedSpace()
        if Nd_left is None:
            space._fact_init_dirac(Nd)
        else:
            space._fact_init_dirac(Nd, Nd_left)
        return space

    def _fact_init_dirac(self, Nd: int, Nd_left: int = None):
        self._init_dirac(Nd)
        if Nd_left is None:
            Nd_left = Nd // 2
        Nd_right = Nd - Nd_left
        self.left = Space.from_dirac(Nd_left)
        self.right = Space.from_dirac(Nd_right)

    def state_size(self) -> int:
        return 2 * self.state_block_size()

    def state_alloc_size(self) -> int:
        return 16 * self.state_size()  # sizeof(complex128) * size

    def state_block_size(self) -> int:
        return self.state_block_rows() * self.state_block_cols()

    def state_block_rows(self) -> int:
        return self.left.D // 2

    def state_block_cols(self) -> int:
        return self.right.D // 2

    def left_block_rows(self) -> int:
        return self.left.D // 2

    def left_block_cols(self) -> int:
        return self.left.D // 2

    def left_block_size(self) -> int:
        return self.left_block_rows() * self.left_block_cols()

    def right_block_rows(self) -> int:
        return self.right.D // 2

    def right_block_cols(self) -> int:
        return self.right.D // 2

    def right_block_size(self) -> int:
        return self.right_block_rows() * self.right_block_cols()


class FactorizedParityState:
    """A factorized state with definite charge parity (even or odd)."""

    def __init__(self, space: FactorizedSpace, charge_parity, rng=None):
        self.space = space
        self.charge_parity = charge_parity
        if rng is not None:
            self.matrix = get_factorized_random_state(space, charge_parity, rng)
        else:
            self.matrix = np.zeros((space.left.D, space.right.D), dtype=complex)

    def size(self) -> int:
        return self.space.left.D * self.space.right.D // 2


def get_factorized_state(space: FactorizedSpace, state: np.ndarray) -> np.ndarray:
    """
    Convert a flat state vector to a factorized matrix representation.
    Left space = LSBs of global state. Reorder to charge-parity ordering.
    """
    unordered = np.zeros((space.left.D, space.right.D), dtype=complex)
    for i in range(space.left.D):
        for j in range(space.right.D):
            global_state = i + (j << space.left.Nd)
            unordered[i, j] = state[global_state]

    result = np.zeros((space.left.D, space.right.D), dtype=complex)
    for left_iter in GlobalStateIterator(space.left):
        for right_iter in GlobalStateIterator(space.right):
            result[left_iter.parity_ordered, right_iter.parity_ordered] = \
                unordered[left_iter.global_state, right_iter.global_state]
    return result


def get_unfactorized_state(space: FactorizedSpace, factorized: np.ndarray) -> np.ndarray:
    """Inverse of get_factorized_state: matrix -> flat vector."""
    unordered = np.zeros((space.left.D, space.right.D), dtype=complex)
    for left_iter in GlobalStateIterator(space.left):
        for right_iter in GlobalStateIterator(space.right):
            unordered[left_iter.global_state, right_iter.global_state] = \
                factorized[left_iter.parity_ordered, right_iter.parity_ordered]

    result = np.zeros(space.D, dtype=complex)
    for i in range(space.left.D):
        for j in range(space.right.D):
            global_state = i + (j << space.left.Nd)
            result[global_state] = unordered[i, j]
    return result


def get_factorized_random_state(space, charge_parity=None, rng=None) -> np.ndarray:
    """Random state in factorized form, optionally projected to a charge parity."""
    if rng is None:
        state = np.random.randn(space.left.D, space.right.D) + \
                1j * np.random.randn(space.left.D, space.right.D)
    else:
        state = np.array([[complex(rng.normal(), rng.normal())
                           for _ in range(space.right.D)]
                          for _ in range(space.left.D)])

    if charge_parity == ChargeParity.EVEN_CHARGE:
        # Block-diagonal: zero out off-diagonal blocks
        half_L, half_R = space.left.D // 2, space.right.D // 2
        state[:half_L, half_R:] = 0
        state[half_L:, :half_R] = 0
    elif charge_parity == ChargeParity.ODD_CHARGE:
        # Block-off-diagonal: zero out diagonal blocks
        half_L, half_R = space.left.D // 2, space.right.D // 2
        state[:half_L, :half_R] = 0
        state[half_L:, half_R:] = 0

    state /= np.linalg.norm(state)
    return state


def get_random_state(space: Space, rng=None) -> np.ndarray:
    """Random normalized vector state."""
    state = get_random_vector(space.D, rng)
    return state / np.linalg.norm(state)
```
