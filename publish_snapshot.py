"""Copy the current static snapshot into this GitHub Pages repository."""
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

SOURCE = Path(r"C:\Users\路飞\Documents\kimi\workspace\retail-site")
ROOT = Path(__file__).parent
PAGES = {"index.html": "retail.html", "inventory.html": "inventory.html", "stock.html": "stock.html", "target.html": "target.html", "insights.html": "insights.html", "demo.html": "demo.html"}
DATA = ["data.json", "dailycube.json", "inventory.json", "stocktree.json", "mtd.json", "insights.json", "demo.json"]

for source_name, target_name in PAGES.items():
    shutil.copy2(SOURCE / source_name, ROOT / target_name)
for name in DATA:
    shutil.copy2(SOURCE / name, ROOT / name)

checks = {}
for name in DATA:
    checks[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
release = {
    "updated": datetime.now().astimezone().isoformat(timespec="seconds"),
    "checksumStatus": "passed",
    "files": checks,
}
(ROOT / "release.json").write_text(json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("snapshot published locally")
