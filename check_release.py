import json
from pathlib import Path

ROOT = Path(__file__).parent
required_json = ["data.json", "dailycube.json", "inventory.json", "stocktree.json", "mtd.json", "insights.json", "demo.json"]
required_pages = ["index.html", "retail.html", "inventory.html", "stock.html", "target.html", "insights.html", "demo.html"]

for name in required_pages:
    p = ROOT / name
    if not p.is_file() or p.stat().st_size < 100:
        raise SystemExit(f"missing or empty page: {name}")
for name in required_json:
    p = ROOT / name
    if not p.is_file() or p.stat().st_size < 2:
        raise SystemExit(f"missing or empty data: {name}")
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"invalid JSON {name}: {exc}")
print(f"release check passed: {len(required_pages)} pages, {len(required_json)} JSON files")
