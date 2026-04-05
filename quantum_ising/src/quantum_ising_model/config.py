"""Configuration constants and helper functions for the Quantum-Ising Page-curve
analysis package.

This file centralises all parameters that control the simulations so that they
can be modified from a single place.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import networkx as nx

# -----------------------------------------------------------------------------
# 1. Simulation control
# -----------------------------------------------------------------------------
N_SYS: int = 8  # Number of physical qubits in the system under study
NUM_RUNS: int = 20  # Monte-Carlo realisations for statistical averaging
BASE_SEED: int = 2025  # Base RNG seed for reproducibility

T_MAX: float = 20.0  # Maximum simulation time J_sys * t
T_STEPS: int = 150  # Number of time points to sample between 0 and T_MAX

# Data storage ----------------------------------------------------------------
DATA_DIR: Path = Path("simulation_data_final")
RESULTS_FILE: Path = DATA_DIR / f"results_N{N_SYS}.json"

# -----------------------------------------------------------------------------
# 2. Physics parameters (defaults)
# -----------------------------------------------------------------------------
PHYSICS_DEFAULTS: Dict[str, float | int] = {
    "J_sys": 1.0,
    "g_bath": 0.5,
    "J_couple": 0.5,
    "N_bath": 2,  # Total qubits = N_SYS + N_bath = 10
    "bath_noise_strength": 0.1,
}

# -----------------------------------------------------------------------------
# 3. Topology definitions & coupling points
# -----------------------------------------------------------------------------

def get_topologies_and_couplings() -> Dict[str, Dict]:
    """Return a dict mapping topology names to graphs & coupling points.

    Each item has the structure::

        {
            "graph": <networkx.Graph>,
            "coupling_points": {"description": int, ...}
        }
    """
    topologies: Dict[str, Dict] = {}

    # 1D chain ----------------------------------------------------------------
    topologies["1D Chain"] = {
        "graph": nx.path_graph(N_SYS),
        "coupling_points": {"end": 0},
    }

    # 2D lattice (4×2) ---------------------------------------------------------
    topologies["2D Lattice"] = {
        "graph": nx.convert_node_labels_to_integers(nx.grid_2d_graph(4, 2)),
        "coupling_points": {"corner": 0, "middle": 2},
    }

    # Heavy-Hex graph ----------------------------------------------------------
    g_hh = nx.Graph()
    g_hh.add_edges_from(
        [
            (0, 1),
            (2, 3),
            (1, 4),
            (3, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        ]
    )
    topologies["Heavy-Hex"] = {
        "graph": g_hh,
        "coupling_points": {"degree-2_corner": 0, "degree-3_middle": 1},
    }

    return topologies

# -----------------------------------------------------------------------------
# 4. Critical points for ground-state preparation -----------------------------
# -----------------------------------------------------------------------------
CRITICAL_POINTS = {
    "1D Chain": 1.0,
    "2D Lattice": 3.044,
    "Heavy-Hex": 2.25,
}

# -----------------------------------------------------------------------------
# 5. Experimental campaigns ----------------------------------------------------
# -----------------------------------------------------------------------------
CAMPAIGNS = {
    "Effect of Coupling Strength": {
        "param_to_sweep": "J_couple",
        "values": [0.2, 0.5, 1.0],
        "default_params": PHYSICS_DEFAULTS.copy(),
    }
}

__all__ = [
    "N_SYS",
    "NUM_RUNS",
    "BASE_SEED",
    "T_MAX",
    "T_STEPS",
    "DATA_DIR",
    "RESULTS_FILE",
    "PHYSICS_DEFAULTS",
    "CRITICAL_POINTS",
    "CAMPAIGNS",
    "get_topologies_and_couplings",
]
