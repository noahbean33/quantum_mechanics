"""Basic Pauli operators and helper utilities."""
from __future__ import annotations

import numpy as np
from numpy import kron

__all__ = [
    "SIGMA_Z",
    "SIGMA_X",
    "get_operator",
]

SIGMA_Z: np.ndarray = np.array([[1, 0], [0, -1]])
SIGMA_X: np.ndarray = np.array([[0, 1], [1, 0]])


def get_operator(op: np.ndarray, i: int, n_qubits: int) -> np.ndarray:  # noqa: N802
    """Return an operator acting with *op* on qubit *i* of an *n_qubits*-qubit system.

    The operator is constructed as a Kronecker product of identity matrices with
    *op* inserted at position *i*.
    """
    op_list = [np.identity(2) for _ in range(n_qubits)]
    if i < n_qubits:
        op_list[i] = op
    full_op = op_list[0]
    for k in range(1, n_qubits):
        full_op = kron(full_op, op_list[k])
    return full_op
