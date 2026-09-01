#!/usr/bin/env python3
"""Verify provenance hashes and public-release boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "source-manifest.json"
FORBIDDEN_SUFFIXES = {".doc", ".docx", ".pdf", ".ppt", ".pptx", ".zip"}
FORBIDDEN_NAMES = {"SIR-simple.py", "hyper_heatmap.py", "hyper_to_normal.py", "normal_heatmap.py"}
FORBIDDEN_TEXT = ("Hard" + "-Minor GAN", "@author:" + " shang" + "keke")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []

    for item in manifest["artifacts"]:
        path = ROOT / item["path"]
        if not path.is_file():
            errors.append(f"missing artifact: {item['path']}")
        elif sha256(path) != item["sha256"]:
            errors.append(f"hash mismatch: {item['path']}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden document/archive: {path.relative_to(ROOT)}")
        if path.name in FORBIDDEN_NAMES:
            errors.append(f"excluded source present: {path.relative_to(ROOT)}")
        if path.suffix.lower() in {".md", ".py", ".txt"}:
            text = path.read_text(encoding="utf-8", errors="replace")
            for marker in FORBIDDEN_TEXT:
                if marker in text and path != ROOT / "docs" / "CODE_SCOPE.md":
                    errors.append(f"forbidden marker {marker!r}: {path.relative_to(ROOT)}")

    if errors:
        raise SystemExit("Release verification failed:\n- " + "\n- ".join(errors))

    print(f"Release verification passed ({len(manifest['artifacts'])} artifacts checked).")


if __name__ == "__main__":
    main()
