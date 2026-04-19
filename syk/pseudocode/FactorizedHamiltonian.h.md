# FactorizedHamiltonian.h — Python Pseudocode

Factorized Hamiltonian: H as sum of O_L ⊗ O_R^T operator pairs, exploiting charge parity.

```python
import numpy as np
from abc import ABC, abstractmethod

class FactorizedOperatorPair:
    """A pair (O_left, O_right) with a definite charge parity."""
    def __init__(self, O_left=None, O_right=None, charge_parity=None):
        self.O_left = O_left
        self.O_right = O_right
        self.charge_parity = charge_parity

class BlockShape:
    BLOCK_DIAGONAL = 0
    BLOCK_OFF_DIAGONAL = 1

class BlockOperator2x2:
    """An operator split into top and bottom blocks based on charge-parity structure."""
    def __init__(self, op: np.ndarray, shape: int):
        self.shape = shape
        half_r, half_c = op.shape[0] // 2, op.shape[1] // 2
        if shape == BlockShape.BLOCK_DIAGONAL:
            self.top_block = op[:half_r, :half_c]
            self.bottom_block = op[half_r:, half_c:]
        else:
            self.top_block = op[:half_r, half_c:]
            self.bottom_block = op[half_r:, :half_c]

class HamiltonianTermProcessor(ABC):
    """Callback interface for processing factorized Hamiltonian terms."""
    @abstractmethod
    def process(self, left_idx: int, ops_pair: FactorizedOperatorPair):
        pass


class FactorizedHamiltonianGenericParity(HamiltonianTermProcessor):
    """
    Stores the full Hamiltonian as operator pairs grouped by how many
    indices are on the left side (0..q). Acts on a full factorized state.
    """

    def __init__(self, space: 'FactorizedSpace', Jtensor, mock=False):
        self.space = space
        self.operators = [[] for _ in range(q + 1)]  # operators[left_idx] = list of pairs
        self._init_operators(Jtensor, mock)

    def _init_operators(self, Jtensor, mock):
        generate_factorized_hamiltonian_terms(self.space, Jtensor, mock, self)

    def process(self, left_idx, ops_pair):
        self.operators[left_idx].append(ops_pair)

    def act(self, output: np.ndarray, state: np.ndarray):
        """output += sum_pairs O_L * state * O_R."""
        for left_ind in range(len(self.operators)):
            for pair in self.operators[left_ind]:
                output += pair.O_left @ state @ pair.O_right


def generate_factorized_hamiltonian_terms(space, Jtensor, mock, callback):
    """
    Generate all O_L ⊗ O_R operator pairs by splitting the 4 Majorana indices
    among left/right spaces:
      - 0 left, 4 right  →  identity_L ⊗ (sum J * psi4_R)
      - 1 left, 3 right  →  psi_L * sign_flip ⊗ (sum J * psi3_R)
      - 2 left, 2 right  →  psi2_L ⊗ (sum J * psi2_R)
      - 3 left, 1 right  →  (sum J * psi3_L) * sign_flip ⊗ psi_R
      - 4 left, 0 right  →  (sum J * psi4_L) ⊗ identity_R

    sign_flip accounts for anti-commutation when right operator has odd parity.
    All O_R are transposed at creation time.
    """
    # Compute psi matrices for left and right spaces
    # sign_flip_left = diag(+1...+1, -1...-1) for even/odd parity states
    # Loop over index combinations and call callback.process(left_idx, pair)
    pass


class FactorizedHamiltonian:
    """
    Dense block-operator Hamiltonian. Stores operators as BlockOperator2x2
    for efficient block-wise multiplication on even/odd parity states.
    """

    def __init__(self, space, Jtensor, mock=False):
        self.space = space
        # Build generic parity H, then split each operator into blocks
        H = FactorizedHamiltonianGenericParity(space, Jtensor, mock)
        self.left_operators = [[] for _ in range(q + 1)]
        self.right_operators = [[] for _ in range(q + 1)]

        for left_ind in range(q + 1):
            shape = BlockShape.BLOCK_DIAGONAL if left_ind % 2 == 0 else BlockShape.BLOCK_OFF_DIAGONAL
            for pair in H.operators[left_ind]:
                self.left_operators[left_ind].append(BlockOperator2x2(pair.O_left, shape))
                self.right_operators[q - left_ind].append(BlockOperator2x2(pair.O_right, shape))

    def act_even(self, output_tl, output_br, state_tl, state_br):
        """
        Act on even-parity state (block-diagonal: top-left + bottom-right).
        For even operators: out_tl += L_top * tl * R_top; out_br += L_bot * br * R_bot
        For odd operators:  out_tl += L_top * br * R_bot; out_br += L_bot * tl * R_top
        """
        for left_ind in range(q + 1):
            for n in range(len(self.left_operators[left_ind])):
                OL = self.left_operators[left_ind][n]
                OR = self.right_operators[q - left_ind][n]
                if left_ind % 2 == 0:
                    output_tl += OL.top_block @ state_tl @ OR.top_block
                    output_br += OL.bottom_block @ state_br @ OR.bottom_block
                else:
                    output_tl += OL.top_block @ state_br @ OR.bottom_block
                    output_br += OL.bottom_block @ state_tl @ OR.top_block

    def act_odd(self, output_tr, output_bl, state_tr, state_bl):
        """
        Act on odd-parity state (block-off-diagonal: top-right + bottom-left).
        For even operators: out_tr += L_top * tr * R_bot; out_bl += L_bot * bl * R_top
        For odd operators:  out_tr += L_top * bl * R_top; out_bl += L_bot * tr * R_bot
        """
        for left_ind in range(q + 1):
            for n in range(len(self.left_operators[left_ind])):
                OL = self.left_operators[left_ind][n]
                OR = self.right_operators[q - left_ind][n]
                if left_ind % 2 == 0:
                    output_tr += OL.top_block @ state_tr @ OR.bottom_block
                    output_bl += OL.bottom_block @ state_bl @ OR.top_block
                else:
                    output_tr += OL.top_block @ state_bl @ OR.top_block
                    output_bl += OL.bottom_block @ state_tr @ OR.bottom_block


class SparseFactorizedHamiltonian:
    """Same as FactorizedHamiltonian but with sparse block operators."""
    # (Same structure as FactorizedHamiltonian, using sparse matrices)
    pass


class HalfSparseFactorizedHamiltonian:
    """
    Hybrid: left-sparse/right-dense for 0-2 left indices,
    left-dense/right-sparse for 3-4 left indices.
    Optimizes for the typical sparsity pattern.
    """
    # (Same act_even/act_odd logic, mixing sparse and dense operators)
    pass
```
