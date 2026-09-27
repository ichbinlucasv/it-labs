#!/usr/bin/env python3
"""Build an ATT&CK Navigator layer from the mapping table in README.md.

score 1 = at least one behaviour with a linked detection (Sigma/Wazuh/tool),
score 0 = only gaps. Optional: validate every technique ID against the
official ATT&CK STIX bundle (not committed, 50 MB):

    curl -LO https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json
    python3 make_layer.py --stix enterprise-attack.json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROW = re.compile(r"^\| (\d+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|$", re.M)
TID = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")


def parse_table() -> dict[str, dict]:
    text = (HERE / "README.md").read_text(encoding="utf-8")
    table = text.split("### Mapping table", 1)[1].split("\n### ", 1)[0]
    techniques: dict[str, dict] = {}
    for num, behaviour, _tactic, technique, _source, detection in ROW.findall(table):
        detected = not detection.strip().lower().startswith("gap")
        for tid in TID.findall(technique):
            t = techniques.setdefault(tid, {"rows": [], "detected": False})
            t["rows"].append(f"#{num} {re.sub(r'[`*]', '', behaviour)}")
            t["detected"] |= detected
    return techniques


def validate(techniques: dict[str, dict], stix_path: str) -> list[str]:
    bundle = json.load(open(stix_path, encoding="utf-8"))
    known = {}
    for o in bundle["objects"]:
        if o.get("type") != "attack-pattern":
            continue
        for ref in o.get("external_references", []):
            if ref.get("source_name") == "mitre-attack":
                known[ref["external_id"]] = o
    version = next((o.get("x_mitre_version") for o in bundle["objects"]
                    if o.get("type") == "x-mitre-collection"), "?")
    problems = []
    for tid in sorted(techniques):
        o = known.get(tid)
        if o is None:
            problems.append(f"{tid}: not found")
        elif o.get("revoked") or o.get("x_mitre_deprecated"):
            problems.append(f"{tid}: revoked/deprecated")
        else:
            print(f"  {tid:<10} {o['name']}")
    print(f"checked {len(techniques)} technique IDs against ATT&CK Enterprise {version}: "
          f"{'all valid' if not problems else problems}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stix", help="path to enterprise-attack.json for validation")
    ap.add_argument("-o", default=str(HERE / "coverage-layer.json"))
    args = ap.parse_args()
    techniques = parse_table()
    if args.stix and validate(techniques, args.stix):
        return 1
    layer = {
        "name": "it-labs — synthetic scenario coverage",
        "versions": {"layer": "4.5", "navigator": "5.1.0"},
        "domain": "enterprise-attack",
        "description": "Techniques seen in the synthetic lab scenarios. "
                       "Green (1) = detection exists in this repo, red (0) = gap.",
        "gradient": {"colors": ["#ff6666", "#66cc66"], "minValue": 0, "maxValue": 1},
        "legendItems": [{"label": "Detected by my rules/tools", "color": "#66cc66"},
                        {"label": "Gap", "color": "#ff6666"}],
        "techniques": [
            {"techniqueID": tid, "score": int(t["detected"]),
             "comment": "; ".join(t["rows"]), "enabled": True}
            for tid, t in sorted(techniques.items())
        ],
    }
    Path(args.o).write_text(json.dumps(layer, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    det = sum(t["detected"] for t in techniques.values())
    print(f"wrote {args.o}: {len(techniques)} techniques, {det} with a detection, {len(techniques) - det} gaps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
