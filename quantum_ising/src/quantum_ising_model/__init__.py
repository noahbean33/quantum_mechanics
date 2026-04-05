"""Quantum Ising Model analysis package.

This package provides tools to simulate Page curves for various network
 topologies using transverse-field Ising Hamiltonians.
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("quantum_ising_model")
except PackageNotFoundError:
    __version__ = "0.1.0"
