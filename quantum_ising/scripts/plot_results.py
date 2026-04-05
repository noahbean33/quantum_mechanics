#!/usr/bin/env python
"""Plot entanglement-entropy results produced by *scripts.generate_data*.

This is a refactor of the plotting logic from the original notebook.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from quantum_ising_model.config import CAMPAIGNS, RESULTS_FILE, get_topologies_and_couplings

plt.style.use("seaborn-v0_8-whitegrid")

def _plot_dynamics_grid(campaign_name: str, campaign_data: dict, time_points: list[float], topologies):
    cfg = CAMPAIGNS[campaign_name]
    param_values = cfg["values"]
    param_name = cfg["param_to_sweep"]

    n_topos = len(topologies)
    n_coupling_types = max(len(t["coupling_points"]) for t in topologies.values())

    fig, axes = plt.subplots(
        n_coupling_types,
        n_topos,
        figsize=(8 * n_topos, 6 * n_coupling_types),
        sharex=True,
        squeeze=False,
    )
    fig.suptitle(f"Campaign: {campaign_name}", fontsize=24, y=1.03)

    for c_idx, (topo_name, topo_info) in enumerate(topologies.items()):
        for r_idx, coupling_label in enumerate(topo_info["coupling_points"].keys()):
            ax = axes[r_idx, c_idx]
            plot_data = campaign_data[topo_name][coupling_label]

            for val in param_values:
                runs = np.array(plot_data[str(val)])
                mean = runs.mean(axis=0)
                std = runs.std(axis=0)

                label = f"{param_name} = {val}"
                ax.plot(time_points, mean, label=label)
                ax.fill_between(time_points, mean - std, mean + std, alpha=0.2)

            ax.set_title(f"{topo_name} (Coupling: {coupling_label})", fontsize=14)
            ax.grid(True, ls="--")
            ax.legend(fontsize=8)
            ax.set_xlabel("Time ($t J_{sys}$)")
            if c_idx == 0:
                ax.set_ylabel("Entanglement entropy (bits)")

    for ax_row in axes:
        for ax in ax_row:
            if not ax.has_data():
                ax.set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    fname = f"fig_{campaign_name.replace(' ', '_').lower()}.png"
    plt.savefig(fname, dpi=300, bbox_inches="tight")
    print(f"Saved {fname}")
    plt.show()


def _plot_summary_barchart(campaign_name: str, campaign_data: dict, topologies):
    cfg = CAMPAIGNS[campaign_name]
    param_values = cfg["values"]

    labels = list(topologies.keys())
    x = np.arange(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(14, 8))

    for i, val in enumerate(param_values):
        peak_means, peak_errs = [], []
        for topo_name, topo_info in topologies.items():
            peaks = []
            for coupling_label in topo_info["coupling_points"].keys():
                runs = np.array(campaign_data[topo_name][coupling_label][str(val)])
                peaks.extend(runs.max(axis=1))
            peak_means.append(np.mean(peaks))
            peak_errs.append(np.std(peaks))

        ax.bar(x + i * width - width, peak_means, width, yerr=peak_errs, label=f"{val}", capsize=5)

    ax.set_ylabel("Peak entanglement entropy (bits)")
    ax.set_title("Peak entanglement by topology & coupling strength")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(title=cfg["param_to_sweep"])
    ax.grid(True, axis="y", ls="--")

    plt.tight_layout()
    fname = "fig_peak_entanglement_summary.png"
    plt.savefig(fname, dpi=300, bbox_inches="tight")
    print(f"Saved {fname}")
    plt.show()


def main() -> None:
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(f"Results file not found: {RESULTS_FILE}. Run scripts.generate_data first.")

    with open(RESULTS_FILE, "r", encoding="utf-8") as fh:
        results = json.load(fh)

    time_points = results.pop("time_points")
    topologies = get_topologies_and_couplings()

    for campaign_name, campaign_data in results.items():
        print(f"Plotting {campaign_name} …")
        _plot_dynamics_grid(campaign_name, campaign_data, time_points, topologies)
        if campaign_name == "Effect of Coupling Strength":
            _plot_summary_barchart(campaign_name, campaign_data, topologies)


if __name__ == "__main__":
    main()
