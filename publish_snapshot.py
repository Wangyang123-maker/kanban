"""Build the public, read-only GitHub Pages snapshot from the local dashboard."""
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

SOURCE = Path(r"C:\Users\路飞\Documents\kimi\workspace\retail-site")
ROOT = Path(__file__).parent
PAGES = [
    "index.html", "inventory.html", "stock.html", "finance.html",
    "product.html", "sales.html", "insights.html", "target.html",
    "launch.html", "demo.html", "guide.html",
]
DATA = [
    "data.json", "dailycube.json", "inventory.json", "stocktree.json",
    "mtd.json", "insights.json", "demo.json", "targets.json", "spumap.json",
]
ASSETS = ["apple.css"]
RUNTIME_TAG = '<script src="public-runtime.js?v=20260822-public1"></script>'


def public_page(source_name: str, target_name: str | None = None) -> None:
    target_name = target_name or source_name
    text = (SOURCE / source_name).read_text(encoding="utf-8")
    if RUNTIME_TAG not in text:
        text = text.replace("</head>", f"{RUNTIME_TAG}\n</head>", 1)
    if source_name == "guide.html":
        text = text.replace(
            "http://100.108.39.124:8017",
            "https://wangyang123-maker.github.io/kanban/",
        ).replace(
            "首次使用：手机需先安装 <b>Tailscale</b> 并用邀请账号登录（找管理员开通），保持 Tailscale 开关打开即可，之后直接输网址。",
            "无需安装软件或登录账号，手机和电脑只要能联网即可打开。建议收藏这个公网地址。",
        ).replace(
            "先检查手机上的 <b>Tailscale 开关是否打开</b>；开着还打不开，截屏联系管理员。",
            "先切换一次 WiFi/手机流量并刷新；仍打不开时截屏联系管理员。",
        ).replace(
            "打开看板的「<b>手动上传</b>」页",
            "在数据主机打开本地「<b>手动上传</b>」页",
        ).replace(
            "打开「<b>手动上传</b>」页",
            "在数据主机打开本地「<b>手动上传</b>」页",
        )
    (ROOT / target_name).write_text(text, encoding="utf-8")


for name in PAGES:
    public_page(name)
public_page("index.html", "retail.html")
for name in DATA + ASSETS:
    shutil.copy2(SOURCE / name, ROOT / name)

guide_assets = SOURCE / "guide-assets"
if guide_assets.is_dir():
    shutil.copytree(guide_assets, ROOT / "guide-assets", dirs_exist_ok=True)

checks = {}
for name in PAGES + DATA + ASSETS + ["retail.html", "public-runtime.js"]:
    checks[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
release = {
    "updated": datetime.now().astimezone().isoformat(timespec="seconds"),
    "mode": "public-readonly-snapshot",
    "checksumStatus": "passed",
    "files": checks,
}
(ROOT / "release.json").write_text(
    json.dumps(release, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(f"public snapshot built: {len(PAGES) + 1} pages, {len(DATA)} data files")
