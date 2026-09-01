# Release validation

Validation was performed on 2026-09-01 before the public release.

## Environment

| Component | Version |
| --- | --- |
| Python | 3.12.13 |
| NumPy | 2.5.2 |
| Matplotlib | 3.11.1 |
| Seaborn | 0.13.2 |
| pytest | 9.1.1 |

Matplotlib used the non-interactive `Agg` backend.

## Checks

- `python -m pytest -q`: **2 passed**
- `python scripts/verify_release.py`: **6 provenance artifacts verified**
- Python bytecode compilation: **passed**
- Public-scope scan for PDFs, Office documents, ZIP archives, excluded source files, and unrelated attachment markers: **passed**

## Full trajectory smoke run

`experiments/HSIR.py` was run with `PYTHONHASHSEED=0` on the archived `contact-high-school` hyperedge file and the script's default configuration: 100 time steps and 100 Monte Carlo runs.

```text
Total nodes: 327
Average final susceptible fraction (S): 0.0528
Average final infected fraction (I): 0.0001
Average final recovered fraction (R): 0.9471
```

This confirms that the released trajectory script completes on the intended data layout. It is a release smoke run, not a new scientific evaluation. The full heatmap sweep was not rerun; its calculation path was exercised on a small synthetic hypergraph, and the original bundled heatmaps are labeled as historical outputs in the README.
