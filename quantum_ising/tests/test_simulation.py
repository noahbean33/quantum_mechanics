"""Basic tests for simulation helpers."""
import numpy as np
import networkx as nx

from quantum_ising_model.simulation import build_hamiltonian_from_graph


def test_hamiltonian_hermitian():
    g = nx.path_graph(3)
    H = build_hamiltonian_from_graph(g, J=1.0, g=0.5)
    # Hermitian: H == H†
    assert np.allclose(H, H.conj().T)
