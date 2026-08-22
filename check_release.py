import json
from pathlib import Path

ROOT = Path(__file__).parent
required_json = [
    "data.json", "dailycube.json", "inventory.json", "stocktree.json",
    "mtd.json", "insights.json", "demo.json", "targets.json", "spumap.json",
]
required_pages = [
    "index.html", "retail.html", "inventory.html", "stock.html",
    "finance.html", "product.html", "sales.html", "insights.html",
    "target.html", "launch.html", "demo.html", "guide.html", "upload.html",
]
required_assets = ["apple.css", "public-runtime.js", "manifest.json", "sw.js"]

for name in required_pages + required_assets:
    path = ROOT / name
    if not path.is_file() or path.stat().st_size < 100:
        raise SystemExit(f"missing or empty file: {name}")
for name in required_json:
    path = ROOT / name
    if not path.is_file() or path.stat().st_size < 2:
        raise SystemExit(f"missing or empty data: {name}")
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"invalid JSON {name}: {exc}")
for name in required_pages:
    text = (ROOT / name).read_text(encoding="utf-8")
    if name != "upload.html" and "public-runtime.js" not in text:
        raise SystemExit(f"public runtime missing from {name}")
print(f"release check passed: {len(required_pages)} pages, {len(required_json)} JSON files")
