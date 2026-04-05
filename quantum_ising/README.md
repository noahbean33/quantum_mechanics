# Quantum Ising Model – Page-Curve Analysis

A research-grade Python package and set of command-line tools to simulate the entanglement (Page) curve of a transverse-field Ising model coupled to a finite bath across multiple qubit-network topologies.

## Features
* Modular **`quantum_ising_model`** package – clean API for building Hamiltonians and running single-shot simulations.
* Reproducible data-generation script – `python -m scripts.generate_data`.
* Publication-ready plotting script – `python -m scripts.plot_results`.
* Configurable parameters collected in `quantum_ising_model.config`.
* Minimal test-suite with **pytest**.

## Installation
```bash
# Clone and install dependencies
pip install -r requirements.txt
```
(Optionally) install the package in editable mode:
```bash
pip install -e .
```

## Quick-start
Generate simulation data and figures using defaults (≈ minutes for small `NUM_RUNS`):
```bash
python -m scripts.generate_data
python -m scripts.plot_results
```
The results JSON and PNG figures will appear in `simulation_data_final/` and project root respectively.

## Repository layout
```
quantum_ising_model/        Top-level repo
├── src/quantum_ising_model/  Importable package code
│   ├── __init__.py
│   ├── config.py            Parameters & topologies
│   ├── ops.py               Pauli ops & helpers
│   └── simulation.py        Hamiltonian & evolution
├── scripts/                 CLI utilities
│   ├── generate_data.py
│   └── plot_results.py
├── tests/                   Pytest test-suite
├── requirements.txt
└── pyproject.toml           Packaging metadata
```

## Testing
```bash
pytest -q
```

## License
[MIT](LICENSE)