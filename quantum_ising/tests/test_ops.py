"""Unit tests for quantum_ising_model.ops."""
import numpy as np
import pytest

from quantum_ising_model.ops import SIGMA_X, SIGMA_Z, get_operator


def test_pauli_dimensions():
    assert SIGMA_X.shape == (2, 2)
    assert SIGMA_Z.shape == (2, 2)


def test_get_operator_size():
    op = get_operator(SIGMA_Z, 1, 3)  # acts on qubit 1 of 3-qubit system
    assert op.shape == (2**3, 2**3)


def test_get_operator_identity_cases():
    # If index is out of range our helper should just return identity kron product
    op = get_operator(SIGMA_Z, 10, 2)
    assert np.allclose(op, np.identity(4))
