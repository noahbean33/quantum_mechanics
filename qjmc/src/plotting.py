"""
Functions for plotting the results of the simulations.
"""

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from qutip import Qobj, Result
from typing import List, Dict, Tuple

def plot_markov_convergence(state_history: np.ndarray, steady_state: np.ndarray, save_path: str = None):
    """Plots the convergence of a Markov chain to its steady state."""
    plt.figure(figsize=(12, 6))
    for i in range(state_history.shape[1]):
        plt.plot(state_history[:, i], label=f'State {i}')

    for i in range(steady_state.shape[0]):
        plt.axhline(y=steady_state[i], color='r', linestyle='--', label=f'Steady State {i} ({steady_state[i]:.2f})' if i == 0 else f'_Steady State {i}')

    plt.title('Convergence of a Markov Chain to Steady State')
    plt.xlabel('Time Steps')
    plt.ylabel('Probability')
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_markov_network(P: np.ndarray, save_path: str = None):
    """Visualizes the Markov chain as a network graph."""
    G = nx.MultiDiGraph()
    for i in range(P.shape[0]):
        G.add_node(i, label=f'State {i}')

    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            if P[i, j] > 0:
                G.add_edge(i, j, weight=P[i, j], label=f'{P[i, j]:.2f}')

    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'label')

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2500,
            connectionstyle='arc3,rad=0.1', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.title('Network Representation of the Markov Chain')
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_non_markovian_direct_simulation(history: List[int], save_path: str = None):
    """Plots the proportion of time spent in each state for a direct simulation."""
    state_0_proportion = np.cumsum([1 if s == 0 else 0 for s in history]) / np.arange(1, len(history) + 1)
    state_1_proportion = 1 - state_0_proportion

    plt.figure(figsize=(12, 6))
    plt.plot(state_0_proportion, label='Proportion in State 0')
    plt.plot(state_1_proportion, label='Proportion in State 1')
    plt.title('Direct Simulation of a Chain with Memory')
    plt.xlabel('Time Steps')
    plt.ylabel('Proportion of Time in State')
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_ensemble_vs_theory(
    ensemble_histories: np.ndarray,
    theoretical_prob: np.ndarray,
    num_runs: int,
    save_path: str = None
):
    """Plots the ensemble average vs. the theoretical probability."""
    ensemble_average_state1 = np.mean(ensemble_histories, axis=0)

    plt.figure(figsize=(14, 7))
    plt.plot(ensemble_average_state1,
             label=f'Average of {num_runs} Direct Simulations',
             color='dodgerblue',
             linewidth=4)
    plt.plot(theoretical_prob,
             label='Theoretical Probability from Expanded Model',
             color='red',
             linestyle='--',
             linewidth=2)
    plt.title('Ensemble Average vs. Theoretical Probability of Being in State 1')
    plt.xlabel('Time Step')
    plt.ylabel('Proportion / Probability in State 1')
    plt.grid(True)
    plt.legend()
    if save_path:
        plt.savefig(save_path)
    plt.show()

def plot_qjmc_convergence(
    mc_results: List[Result],
    me_result: Result,
    fexpt: float,
    tlist: np.ndarray,
    ntraj_list: List[int],
    save_path: str = None
):
    """Plots the convergence of QJMC trajectories to the master equation."""
    fig, axes = plt.subplots(len(ntraj_list), 1, sharex=True, figsize=(8, 12))
    fig.subplots_adjust(hspace=0.1)

    for idx, (n, mc) in enumerate(zip(ntraj_list, mc_results)):
        axes[idx].step(tlist, mc.expect[0], 'b', lw=2)
        axes[idx].plot(tlist, me_result.expect[0], 'r--', lw=1.5)
        axes[idx].axhline(y=fexpt, color='k', lw=1.5)

        axes[idx].set_yticks(np.linspace(0, 2, 5))
        axes[idx].set_ylim([0, 1.5])
        axes[idx].set_ylabel(r'$\left<N\right>$', fontsize=14)

        if idx == 0:
            axes[idx].set_title("Ensemble Averaging of Monte Carlo Trajectories")
            axes[idx].legend(('Single trajectory', 'Master equation', 'Steady state'))
        else:
            axes[idx].legend((f'{n} trajectories', 'Master equation', 'Steady state'))

    axes[-1].set_xlabel('Time (sec)', fontsize=14)
    if save_path:
        plt.savefig(save_path)
    plt.show()
