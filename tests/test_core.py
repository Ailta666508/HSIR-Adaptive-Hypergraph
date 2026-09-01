from __future__ import annotations

import collections
import importlib.util
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_hypergraph_loader(tmp_path: Path) -> None:
    hsir = load_module("hsir", ROOT / "experiments" / "HSIR.py")
    source = tmp_path / "hyperedges.txt"
    source.write_text("a,b,c\nb,c\n\n", encoding="utf-8")

    nodes, hyperedges, memberships = hsir.load_hypergraph(source)

    assert set(nodes) == {"a", "b", "c"}
    assert hyperedges == [["a", "b", "c"], ["b", "c"]]
    assert memberships["a"] == [0]
    assert memberships["b"] == [0, 1]


def test_small_simulation_returns_a_fraction() -> None:
    heatmap = load_module(
        "s_remain_heatmap", ROOT / "experiments" / "S_remain_heatmap.py"
    )
    nodes = ["a", "b", "c", "d"]
    hyperedges = [["a", "b", "c"], ["b", "c", "d"]]
    memberships = collections.defaultdict(list)
    for index, edge in enumerate(hyperedges):
        for node in edge:
            memberships[node].append(index)

    np.random.seed(7)
    result = heatmap.run(
        beta=0.02,
        mu=0.2,
        delta=0.1,
        eta=0.3,
        T=5,
        num_runs=3,
        all_nodes=nodes,
        hyperedges=hyperedges,
        node_to_he=memberships,
    )

    assert np.isfinite(result)
    assert 0.0 <= result <= 1.0

