# Release scope and provenance

This repository is a curated release assembled from the course-project archive `复杂网络与人工智能.zip`. The original work was developed locally, and a commit-by-commit history was not retained.

## Included unchanged from the archive

| Release path | Role |
| --- | --- |
| `experiments/HSIR.py` | Average HSIR trajectory simulation |
| `experiments/S_remain_heatmap.py` | Adaptive-versus-fixed topology sweep |
| `docs/assets/HSIR.jpg` | Bundled trajectory output |
| `docs/assets/S_remain_with_deletion.png` | Bundled adaptive-topology heatmap |
| `docs/assets/S_remain_without_deletion.png` | Bundled fixed-topology heatmap |
| `docs/assets/S_remain_difference.png` | Bundled difference heatmap |

SHA-256 hashes are recorded in `source-manifest.json` so the released research artifacts can be checked against the local archive.

## Added for the public release

- English project documentation and dataset instructions
- Lightweight tests on a synthetic hypergraph
- A release-integrity verification script
- Packaging metadata and ignore rules

These additions organize and validate the release; they do not reconstruct missing historical commits.

## Excluded from the archive

| Material | Reason |
| --- | --- |
| Course paper and presentation PDFs | The supplied copies contain student identifiers |
| Raw datasets and dataset ZIP files | No repository-compatible redistribution license is stated on the source page |
| Nested ZIP archives | Duplicate packaging, not source material |
| `SIR-simple.py` | Marked with a third-party author in its source header; no reuse license was supplied |
| `hyper_to_normal.py`, `hyper_heatmap.py`, `normal_heatmap.py` | Marked deprecated in the original project README; outside the final HSIR experiment path |
