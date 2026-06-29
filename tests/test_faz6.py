#!/usr/bin/env python3
"""Faz 6 ad-hoc test scripti."""

import json
import os
import sys

ROOT = "/home/zorildiz/projeler/bunyamin/stock-price-prediction"

# 1) Notebook JSON geçerliliği
notebook_path = os.path.join(ROOT, "notebooks", "05_karsilastirma.ipynb")
ok = True
results = []

try:
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
except FileNotFoundError:
    print("HATA: notebooks/05_karsilastirma.ipynb bulunamadı")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"HATA: Notebook JSON decode hatası: {e}")
    sys.exit(1)

if nb.get("nbformat") == 4 and nb.get("nbformat_minor", 0) >= 1:
    results.append(f"OK: Notebook nbformat={nb['nbformat']}.{nb['nbformat_minor']}")
else:
    results.append(f"FAIL: Notebook nbformat={nb.get('nbformat')}")
    ok = False

n_cells = len(nb.get("cells", []))
if n_cells == 5:
    results.append(f"OK: Notebook'da {n_cells} hücre")
else:
    results.append(f"FAIL: Notebook'da {n_cells} hücre (5 bekleniyordu)")
    ok = False

# 2) Tüm 5 hücrenin anahtar kelimeleri
required_keywords = {
    "setup": "setup",
    "comparison_table": "comparison_table",
    "comparison_graph": "comparison_graph",
    "hyperparameters": "hyperparameters",
    "tradingview": "tradingview",
}

found_keywords = {}
for i, cell in enumerate(nb["cells"]):
    src = "".join(cell.get("source", []))
    for kw_name, kw in required_keywords.items():
        if kw in src:
            found_keywords[kw_name] = cell["cell_type"]
            results.append(f"OK: Hücre {i} ({cell['cell_type']}) — '{kw}' bulundu")

for kw_name in required_keywords:
    if kw_name not in found_keywords:
        results.append(f"FAIL: '{kw_name}' anahtar kelimesi hiçbir hücrede bulunamadı")
        ok = False

# 3) Model dosyaları
for fname in ["lstm_epoch100.pth", "gru_epoch100.pth"]:
    fpath = os.path.join(ROOT, "outputs", "models", fname)
    if os.path.isfile(fpath):
        results.append(f"OK: {fpath} mevcut ({os.path.getsize(fpath)} bayt)")
    else:
        results.append(f"FAIL: {fpath} mevcut değil")
        ok = False

# 4) outputs/figures/ dizini
figures_dir = os.path.join(ROOT, "outputs", "figures")
if os.path.isdir(figures_dir):
    contents = os.listdir(figures_dir)
    results.append(f"OK: outputs/figures/ mevcut, {len(contents)} dosya/klasör: {contents}")
else:
    results.append(f"FAIL: outputs/figures/ dizini mevcut değil")
    ok = False

# 5) task.md'de Faz 6
task_md = os.path.join(ROOT, "task.md")
if os.path.isfile(task_md):
    with open(task_md, "r", encoding="utf-8") as f:
        task_content = f.read()
    if "Faz 6" in task_content:
        results.append("OK: task.md'de 'Faz 6' kelimesi mevcut")
    else:
        results.append("FAIL: task.md'de 'Faz 6' kelimesi bulunamadı")
        ok = False
else:
    results.append("FAIL: task.md mevcut değil")

print("=" * 60)
print("FAZ 6 TEST SONUÇLARI")
print("=" * 60)
for r in results:
    print(r)
print("-" * 60)
print(f"GENEL SONUÇ: {'BAŞARILI' if ok else 'BAŞARISIZ'}")
print(f"Toplam kontrol: {len(results)}")
failures = [r for r in results if r.startswith("FAIL")]
print(f"Hatalar: {len(failures)}")
sys.exit(0 if ok else 1)
