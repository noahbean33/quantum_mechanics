# BasisState.h — Python Pseudocode

Fock space basis state representation using the combinatorial number system.

```python
from typing import List, Optional

def state_number_to_occupations(state_number: int, Q: int) -> List[int]:
    """Convert state number (combinatorial number system) to fermion occupation indices at charge Q."""
    indices = []
    k = Q
    while k > 0:
        ck = find_maximal_ck(state_number, k)
        indices.insert(0, ck)
        state_number -= binomial(ck, k)
        k -= 1
    assert state_number == 0
    return indices

def occupations_to_state_number(indices: List[int]) -> int:
    """Convert fermion occupation indices to a state number."""
    result = 0
    for k_minus_1, i in enumerate(indices):
        result += binomial(i, k_minus_1 + 1)
    return result

def find_maximal_ck(state_number: int, k: int) -> int:
    """Find maximal c_k such that C(c_k, k) <= state_number."""
    ck = 0
    while binomial(ck, k) <= state_number:
        ck += 1
    return ck - 1


class BasisState:
    """
    A Fock space state with an integer coefficient.
    Convention: |i_1,...,i_Q> = c†_{i_1} ... c†_{i_Q} |0>, 0 <= i_1 < ... < i_Q
    Indices are 0-based.
    """

    def __init__(self, *args):
        if len(args) == 0:
            # Vacuum state
            self.indices = []
            self.coefficient = 1
        elif len(args) == 2 and isinstance(args[1], int):
            # From state_number and charge Q
            self.coefficient = 1
            self.indices = state_number_to_occupations(args[0], args[1])
        elif len(args) == 1 and isinstance(args[0], int):
            # From global state number (binary representation)
            self.coefficient = 1
            self.indices = []
            global_state_number = args[0]
            i = 0
            while global_state_number != 0:
                if global_state_number % 2 == 1:
                    self.indices.append(i)
                global_state_number //= 2
                i += 1
        elif len(args) >= 1 and isinstance(args[0], list):
            # From list of indices and optional coefficient
            self.indices = list(args[0])
            self.coefficient = args[1] if len(args) > 1 else 1

    def annihilate(self, i: int):
        """Act with c_i on this state."""
        if self.coefficient == 0:
            return
        for pos, idx in enumerate(self.indices):
            if idx == i:
                self.indices.pop(pos)
                return
            elif idx < i:
                self.coefficient *= -1  # anti-commutation sign
            else:
                break  # index not found
        self.coefficient = 0  # c_i kills the state

    def create(self, i: int):
        """Act with c†_i on this state."""
        if self.coefficient == 0:
            return
        for pos, idx in enumerate(self.indices):
            if idx == i:
                self.coefficient = 0  # double creation kills state
                return
            elif idx < i:
                self.coefficient *= -1  # anti-commutation sign
            else:
                self.indices.insert(pos, i)
                return
        self.indices.append(i)

    def get_state_number(self) -> int:
        return occupations_to_state_number(self.indices)

    def get_global_state_number(self) -> int:
        return sum(2**idx for idx in self.indices)

    def charge(self) -> int:
        assert self.coefficient != 0
        return len(self.indices)

    def is_zero(self) -> bool:
        return self.coefficient == 0

    def next_state(self) -> 'BasisState':
        return BasisState(self.get_state_number() + 1, self.charge())

    def to_string(self) -> str:
        if self.coefficient == 0:
            return "0"
        s = ""
        if self.coefficient == -1:
            s = "-"
        elif self.coefficient != 1:
            s = f"{self.coefficient}*"
        s += "|" + ",".join(str(i) for i in self.indices) + ">"
        return s


class GlobalStateIterator:
    """
    Iterates over global states, computing a parity-ordered state number
    where even charge states appear before odd charge ones.
    """

    def __init__(self, space: 'Space'):
        self.space = space
        self.global_state = 0
        self.parity_ordered_state = 0
        self.seen_states_by_charge = {Q: 0 for Q in range(space.Nd + 1)}

    def done(self) -> bool:
        return self.global_state >= self.space.D

    def next(self):
        if self.done():
            return
        self.global_state += 1
        if self.done():
            return

        state_Q = bin(self.global_state).count('1')  # popcount
        self.parity_ordered_state = self.seen_states_by_charge[state_Q]

        if state_Q % 2 == 0:
            for Q in range(0, state_Q, 2):
                self.parity_ordered_state += Q_sector_dim(self.space.Nd, Q)
        else:
            for Q in range(0, self.space.Nd + 1, 2):
                self.parity_ordered_state += Q_sector_dim(self.space.Nd, Q)
            for Q in range(1, state_Q, 2):
                self.parity_ordered_state += Q_sector_dim(self.space.Nd, Q)

        self.seen_states_by_charge[state_Q] += 1
```
