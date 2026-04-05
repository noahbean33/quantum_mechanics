# From Markov Chains to Quantum Trajectories: A Unified Computational View

This repository provides a computational framework and pedagogical demonstration linking classical Markov chains, non-Markovian memory processes, and Quantum Jump Monte Carlo (QJMC) simulations. It aims to bridge the conceptual gap between classical stochastic processes and open quantum system dynamics.

The project is structured as a potential conference paper or pedagogical article. For the detailed academic framing, see `PAPER_PROPOSAL.md`.

## Project Structure

```
.qjmc_paper/
├── figures/                # Output directory for generated plots
├── notebooks/              # Original Jupyter notebook/script for reference
│   └── original_demonstration.py
├── src/                    # Refactored and modularized source code
│   ├── __init__.py
│   ├── classical_markov.py
│   ├── non_markovian.py
│   ├── plotting.py
│   └── quantum_jumps.py
├── tests/                  # Test suite for the source code (to be implemented)
├── main.py                 # Main script to run all simulations and generate plots
├── PAPER_PROPOSAL.md       # Detailed outline and framing for a potential academic paper
├── requirements.txt        # Python package dependencies
└── README.md               # This file
```

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd qjmc_paper
    ```

2.  Create and activate a virtual environment (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run all simulations and generate the plots, execute the main script from the root directory:

```bash
python main.py
```

The script will print progress to the console and save all generated figures to the `figures/` directory.

## License

This project is licensed under the terms of the [MIT License](LICENSE).
