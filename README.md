<h1 align="center">HSIR</h1>

<h3 align="center">Multi-Risk-Aware Adaptive Link Breaking and Spreading Dynamics on Hypergraphs</h3>

<p align="center">
  Outstanding Project for the <strong>AI for Complex Networks</strong> course
</p>

<p align="center">
  <strong>Han Feiyang</strong> · <strong>Zihan Shen</strong>
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#model">Model</a> ·
  <a href="#experiments-and-results">Results</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#reproducibility">Reproducibility</a> ·
  <a href="#citation">Citation</a>
</p>

## Overview

HSIR implements a discrete-time Monte Carlo simulation of SIR dynamics on an adaptive hypergraph. At each step, it computes infection counts and risk values from the current node states and hyperedges, samples node-state and topology events, and then applies the sampled changes. Susceptible nodes can be removed from individual hyperedges, and hyperedges whose risk exceeds a threshold can be cleared.

<p align="center">
  <img src="docs/assets/hsir-concept-overview.png" width="100%" alt="Conceptual overview of local and global risk perception, adaptive hypergraph responses, and SIR dynamics">
</p>

<p align="center"><em>Repository overview illustration (not a paper figure). Overlapping enclosures denote hyperedges; blue, red, and green nodes denote susceptible, infected, and recovered states.</em></p>

The experiments compare this adaptive topology with a fixed-topology condition over a grid of infection and recovery parameters, then measure the absolute change in the final susceptible fraction.

### Main ideas

- **Hypergraph representation.** Infection trials use the number of infected nodes in each incident hyperedge; the code does not project the data to pairwise edges.
- **Combined risk signal.** Each hyperedge combines its local infected fraction with the infected fraction across all nodes.
- **Node-level topology update.** A susceptible node may be removed from each incident hyperedge with a risk-dependent threshold.
- **Hyperedge-level topology update.** A hyperedge above the risk threshold may be replaced by an empty hyperedge.
- **Matched comparison.** Adaptive and fixed-topology conditions use the same infection and recovery grid.

## Model

For hyperedge $h$, HSIR defines perceived risk as

$$
R_h = (1-\alpha)\frac{I_h}{\lvert h \rvert} + \alpha\frac{I}{N},
$$

where $I_h$ is the number of infected nodes in $h$, $\lvert h \rvert$ is the current hyperedge size, $I$ is the total number of infected nodes, $N$ is the number of nodes, and $\alpha$ controls the local-global weighting.

At each discrete time step, the simulator evaluates four mechanisms from the current system state:

1. For every incident hyperedge $h$, a susceptible node receives an infection draw with threshold $\beta I_h^\gamma$.
2. Each infected node receives one recovery draw with threshold $\mu$.
3. For every incident hyperedge $h$, a susceptible node receives a withdrawal draw with threshold $\delta R_h$.
4. If $R_h > \phi$, hyperedge $h$ receives a dissolution draw with threshold $\eta$.

The implementation evaluates these draws from the current state while accumulating changes in copied state and hyperedge structures. It installs those copies before the next time step. A dissolved hyperedge remains in the list as an empty hyperedge; removed memberships are not restored later.

## Experiments and results

The course study uses the labeled `contact-high-school` network from the [Cornell Higher-Order Network Data collection](https://www.cs.cornell.edu/~arb/data/contact-high-school-labeled/). The dataset contains 327 nodes and 7,818 hyperedges, with a mean hyperedge size of 2.3 and a maximum size of 5.

The initial infected node is the node incident to the largest number of hyperedges. The published scripts use the following settings:

| Experiment | $\beta$ | $\mu$ | $\delta$ | $\eta$ |
| --- | ---: | ---: | ---: | ---: |
| Average trajectory | 0.03 | 0.10 | 0.10 | 0.30 |
| Adaptive grid | 10 values from 0.004 to 0.040 | 10 values from 0.02 to 0.20 | 0.10 | 0.30 |
| Fixed-topology grid | same grid | same grid | 0 | 0 |

All three settings use $\gamma=1.5$, $\alpha=0.5$, $\phi=0.4$, 100 time steps, and 100 Monte Carlo runs. The grid evaluation metric is the final susceptible fraction, $S_{\mathrm{remain}}$.

The four figures below are the experiment figures used in the course paper and preserved unchanged from the original project archive. They document the reported study rather than a fresh rerun performed for this repository release.

### Epidemic trajectory

<p align="center">
  <img src="docs/assets/HSIR.jpg" width="78%" alt="Average susceptible, infected, and recovered fractions over 100 time steps">
</p>

<p align="center"><em>Figure 1. Average S/I/R trajectory over 100 Monte Carlo runs using the trajectory settings above.</em></p>

### Fixed-topology baseline

<p align="center">
  <img src="docs/assets/S_remain_without_deletion.png" width="100%" alt="Final susceptible fraction without adaptive link breaking">
</p>

<p align="center"><em>Figure 2. Final susceptible fraction across the infection-recovery grid without node withdrawal or hyperedge dissolution.</em></p>

### Adaptive topology

<p align="center">
  <img src="docs/assets/S_remain_with_deletion.png" width="100%" alt="Final susceptible fraction with adaptive link breaking">
</p>

<p align="center"><em>Figure 3. Final susceptible fraction with multi-risk-aware node withdrawal and hyperedge dissolution.</em></p>

### Intervention gain

<p align="center">
  <img src="docs/assets/S_remain_difference.png" width="100%" alt="Absolute gain in final susceptible fraction from adaptive link breaking">
</p>

<p align="center"><em>Figure 4. Absolute gain in final susceptible fraction: adaptive topology minus fixed topology.</em></p>

At $\beta=0.004$ and $\mu=0.02$, the archived grids report final susceptible fractions of 0.400 with topology updates and 0.015 without them, an absolute difference of **0.385** (38.5 percentage points). The reported difference becomes smaller across much of the higher-infection or higher-recovery region. These simulation outputs describe the implemented model under the tested settings; they do not establish statistical significance or effectiveness in a real population.

## Repository structure

```text
.
├── experiments/
│   ├── HSIR.py                  # averaged S/I/R trajectory
│   └── S_remain_heatmap.py      # adaptive vs fixed-topology sweep
├── data/
│   └── README.md                # dataset retrieval and placement
├── docs/
│   ├── assets/                  # overview graphic and paper figures
│   ├── CODE_SCOPE.md            # release boundaries
│   ├── VALIDATION.md            # validation record
│   └── source-manifest.json     # hashes of original artifacts
├── scripts/
│   └── verify_release.py
└── tests/
    └── test_core.py
```

## Quick start

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/Ailta666508/HSIR-Adaptive-Hypergraph.git
cd HSIR-Adaptive-Hypergraph
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Download `hyperedges-contact-high-school.txt` from the official [dataset page](https://www.cs.cornell.edu/~arb/data/contact-high-school-labeled/) and place it at:

```text
data/contact-high-school/hyperedges-contact-high-school.txt
```

Generate the averaged trajectory:

```bash
PYTHONHASHSEED=0 MPLBACKEND=Agg python experiments/HSIR.py --data contact-high-school
```

Generate the adaptive-versus-fixed parameter sweep:

```bash
PYTHONHASHSEED=0 MPLBACKEND=Agg python experiments/S_remain_heatmap.py --data contact-high-school
```

The full sweep evaluates 100 parameter pairs under two topology conditions, with 100 Monte Carlo runs and 100 time steps per condition, so it takes substantially longer than the trajectory script.

## Reproducibility

Run the lightweight synthetic tests and release-integrity checks with:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/verify_release.py
```

The release was smoke-tested on the archived `contact-high-school` data using the default trajectory configuration. The full 10 × 10 heatmap sweep was not rerun for the public release; its `run` path was exercised only on a small synthetic hypergraph. [`docs/VALIDATION.md`](docs/VALIDATION.md) records the environment, checks, and validation boundary; [`docs/source-manifest.json`](docs/source-manifest.json) records SHA-256 hashes for the original code and paper figures.

The scripts seed NumPy with `42`, but node identifiers are collected in a Python `set`. Set `PYTHONHASHSEED` before launching Python when process-to-process node ordering must be stable.

## Limitations

- Link removal is irreversible; the code does not model reconnection.
- The same $\alpha$, $\phi$, $\delta$, and $\eta$ values are applied across nodes and hyperedges within an experiment.
- The global-risk term uses the current aggregate infected fraction without information delay or observation noise.
- The parameters are simulation settings rather than estimates fitted to longitudinal epidemiological data.
- The stored figures are historical project outputs. Exact reproduction depends on the data, environment, and random-state control documented above.

## Authorship and repository contribution

The course project was completed by **Han Feiyang** and **Zihan Shen**. **Zihan Shen** curated and maintains this public code release. GitHub's contributor list reflects commits to the curated repository and should not be interpreted as sole authorship of the underlying research project.

No open-source license is granted by this repository. Contact the project authors before reusing the code.

## Citation

If you use this code, cite the repository metadata in [`CITATION.cff`](CITATION.cff):

```bibtex
@software{han_shen_hsir_2026,
  author = {Han, Feiyang and Shen, Zihan},
  title = {HSIR: Multi-Risk-Aware Adaptive Link Breaking on Hypergraphs},
  year = {2026},
  url = {https://github.com/Ailta666508/HSIR-Adaptive-Hypergraph}
}
```

**Note:** This project was initially developed locally. The Git repository was created when the codebase was prepared for publication, so the early development history is unavailable. Subsequent updates are tracked in this repository.
