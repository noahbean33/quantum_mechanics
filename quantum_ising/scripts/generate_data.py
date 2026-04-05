#!/usr/bin/env python
"""Generate entanglement-entropy data for the Page-curve study.

This script reproduces the heavy compute loop from the original notebook but
relies entirely on the packaged code under *quantum_ising_model*.

Usage
-----
Run from the repository root::

    python -m scripts.generate_data
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from tqdm import tqdm

from quantum_ising_model.config import (
    BASE_SEED,
    CAMPAIGNS,
    CRITICAL_POINTS,
    DATA_DIR,
    N_SYS,
    NUM_RUNS,
    RESULTS_FILE,
    get_topologies_and_couplings,
)
from quantum_ising_model.simulation import run_single_realization

# Ensure output directory ------------------------------------------------------
DATA_DIR.mkdir(exist_ok=True)

topologies = get_topologies_and_couplings()
results_data: dict = {}

print("--- Starting data generation ---")
start_time = time.time()

for campaign_name, campaign_cfg in CAMPAIGNS.items():
    param_name = campaign_cfg["param_to_sweep"]
    values = campaign_cfg["values"]
    default_params = campaign_cfg["default_params"].copy()

    results_data[campaign_name] = {}

    for topo_name, topo_info in topologies.items():
        graph = topo_info["graph"]
        g_init = CRITICAL_POINTS.get(topo_name, 1.0)
        results_data[campaign_name][topo_name] = {}

        for coupling_label, coupling_node in topo_info["coupling_points"].items():
            results_data[campaign_name][topo_name][coupling_label] = {}

            for val in values:
                params = default_params.copy()
                params[param_name] = val

                run_label = f"{topo_name}/{coupling_label}/{param_name}={val}"
                print(f"\n▶ {run_label}")
                ee_runs = []

                for run_idx in tqdm(range(NUM_RUNS), desc="runs", leave=False):
                    seed = BASE_SEED + run_idx
                    time_points, ee = run_single_realization(
                        graph, g_init, coupling_node, params, seed
                    )
                    ee_runs.append(ee)

                results_data[campaign_name][topo_name][coupling_label][str(val)] = ee_runs

# Save common time axis (same for every run)
results_data["time_points"] = time_points

print("\n--- Finished. Saving results ---")
with open(RESULTS_FILE, "w", encoding="utf-8") as fh:
    json.dump(results_data, fh)

print(f"Data stored to {RESULTS_FILE.relative_to(Path.cwd())}")
print(f"Total runtime: {(time.time() - start_time)/60:.2f} min")
