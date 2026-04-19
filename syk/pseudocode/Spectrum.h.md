# Spectrum.h — Python Pseudocode

Stores and manages eigenvalue spectra.

```python
import numpy as np
from typing import Optional

class Spectrum:
    """
    Stores eigenvalues of a Dirac SYK Hamiltonian, organized by Q-sector.
    Can be constructed from a diagonalized Hamiltonian or loaded from a TSV file.
    """

    def __init__(self, source):
        if isinstance(source, KitaevHamiltonian):
            H = source
            self.N = H.N
            self.evs_by_Q = {}
            for Q in range(H.N + 1):
                self.evs_by_Q[Q] = H.blocks[Q].eigenvalues()
        elif isinstance(source, str):
            self._load_from_file(source)

    def _load_from_file(self, filename: str):
        """Load spectrum from TSV: columns = Q, eigenvalue."""
        self.evs_by_Q = {}
        f = TSVFile(filename)
        while not f.eof():
            Q = f.read_int()
            ev = f.read_double()
            if f.eof():
                break
            if Q not in self.evs_by_Q:
                self.evs_by_Q[Q] = []
            self.evs_by_Q[Q].append(ev)
        f.close()
        # Convert lists to numpy arrays
        for Q in self.evs_by_Q:
            self.evs_by_Q[Q] = np.array(self.evs_by_Q[Q])
        self.N = max(self.evs_by_Q.keys())

    def dim(self) -> int:
        return sum(len(v) for v in self.evs_by_Q.values())

    def Q_eigenvalues(self, Q: int) -> np.ndarray:
        return self.evs_by_Q[Q]

    def all_eigenvalues(self) -> np.ndarray:
        all_evs = np.concatenate(list(self.evs_by_Q.values()))
        return np.sort(all_evs)

    def save(self, filename: str):
        with open(filename, 'w') as f:
            f.write("# Q eigenvalue\n")
            for Q in sorted(self.evs_by_Q.keys()):
                for ev in self.evs_by_Q[Q]:
                    f.write(f"{Q}\t{ev}\n")


class MajoranaSpectrum:
    """
    Stores eigenvalues of a Majorana SYK Hamiltonian.
    """

    def __init__(self, filename: str):
        self.evs = []
        f = TSVFile(filename)
        while not f.eof():
            charge_parity = f.read_int()
            ev = f.read_double()
            if f.eof():
                break
            self.evs.append(ev)
        f.close()
        self.evs = np.array(self.evs)
        # Infer N from dimension: D = 2^{N/2}
        self.majorana_N = int(2 * np.log2(len(self.evs)))

    def all_eigenvalues(self) -> np.ndarray:
        return np.sort(self.evs)
```
