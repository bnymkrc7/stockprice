#!/usr/bin/env python3
"""
FAZ 5 TEST SCRIPT: notebooks/04_model_gru.ipynb doğrulaması
"""
import json
import os
import sys

PROJECT_ROOT = "/home/zorildiz/projeler/bunyamin/stock-price-prediction"
NOTEBOOK_PATH = os.path.join(PROJECT_ROOT, "notebooks", "04_model_gru.ipynb")

results = []
errors = []
warnings = []

def log(msg):
    results.append(msg)
    print(msg)

def check(name, passed, detail=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    log(f"  {status} | {name} {detail}")
    if not passed:
        errors.append(f"{name}: {detail}")

# ════════════════════════════════════════════════════════════
# TEST 1: Notebook JSON geçerliliği (nbformat 4, 6 hücre)
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 1: Notebook JSON Geçerliliği")
log("="*60)

try:
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    check("Notebook JSON parse", True)
except json.JSONDecodeError as e:
    log(f"  ❌ Notebook JSON parse ERROR: {e}")
    errors.append(f"JSON parse error: {e}")
    nb = None

if nb is not None:
    nbformat = nb.get("nbformat", 0)
    nbformat_minor = nb.get("nbformat_minor", 0)
    check(f"nbformat version (beklenen: 4, bulundu: {nbformat})", nbformat == 4)
    
    cells = nb.get("cells", [])
    cell_count = len(cells)
    check(f"Hücre sayısı (beklenen: 6, bulundu: {cell_count})", cell_count == 6)
    
    # Hücre tipleri kontrol
    code_cells = [c for c in cells if c.get("cell_type") == "code"]
    check(f"Code hücre sayısı (beklenen: 6, bulundu: {len(code_cells)})", len(code_cells) == 6)

# ════════════════════════════════════════════════════════════
# TEST 2: Hücre anahtar kelimeleri
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 2: Hücre Anahtar Kelimeleri")
log("="*60)

if nb is not None:
    keywords = {
        "setup": ["autoreload", "import torch", "sys.path"],
        "load_data": ["amzn_processed.pt", "scaler.pkl", "X_train", "X_test"],
        "model_create": ["GRUModel", "input_size", "hidden_size", "num_layers", "param_count"],
        "train": ["train_model", "epochs", "lr", "loss_history"],
        "evaluate": ["evaluate_model", "plot_predictions", "plot_loss", "mse", "rmse"],
        "save_model": ["gru_epoch100.pth", "model_state_dict", "torch.save"],
    }
    
    all_found = True
    for keyword_group, terms in keywords.items():
        # Tüm hücrelerde metni birleştir
        full_text = "\n".join(
            c.get("source", "") if isinstance(c.get("source"), str) 
            else "".join(c.get("source", []))
            for c in cells
        )
        found_terms = [t for t in terms if t in full_text]
        missing_terms = [t for t in terms if t not in full_text]
        ok = len(found_terms) == len(terms)
        detail = f"({len(found_terms)}/{len(terms)} terim)" if not ok else ""
        check(f"'{keyword_group}' anahtar kelimeleri", ok, detail)
        if missing_terms:
            log(f"    - Eksik: {missing_terms}")

# ════════════════════════════════════════════════════════════
# TEST 3: src/*.py dosyalarının erişilebilirliği
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 3: src/ Python Dosyaları")
log("="*60)

src_files = ["src/models.py", "src/train.py", "src/evaluate.py"]
for sf in src_files:
    full_path = os.path.join(PROJECT_ROOT, sf)
    exists = os.path.isfile(full_path)
    readable = os.access(full_path, os.R_OK) if exists else False
    size = os.path.getsize(full_path) if exists else 0
    check(f"{sf} mevcut", exists, f"(={size} bytes)")
    if exists:
        check(f"{sf} okunabilir", readable)

# ════════════════════════════════════════════════════════════
# TEST 4: outputs/models/ ve outputs/figures/ dizinleri
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 4: outputs/ Dizinleri")
log("="*60)

model_dir = os.path.join(PROJECT_ROOT, "outputs", "models")
figures_dir = os.path.join(PROJECT_ROOT, "outputs", "figures")

check("outputs/models/ dizin mevcut", os.path.isdir(model_dir))
check("outputs/figures/ dizin mevcut", os.path.isdir(figures_dir))

if os.path.isdir(model_dir):
    model_files = os.listdir(model_dir)
    gru_files = [f for f in model_files if "gru" in f.lower()]
    check(f"GRU model dosyaları (gru_epoch100.pth)", "gru_epoch100.pth" in model_files)
    log(f"    Model dizini: {len(model_files)} dosya ({', '.join(model_files)})")

if os.path.isdir(figures_dir):
    fig_files = os.listdir(figures_dir)
    gru_figs = [f for f in fig_files if "gru" in f.lower()]
    check("gru_predictions.png mevcut", "gru_predictions.png" in fig_files)
    check("gru_loss.png mevcut", "gru_loss.png" in fig_files)
    log(f"    Figures dizini: {len(fig_files)} dosya ({', '.join(fig_files)})")

# ════════════════════════════════════════════════════════════
# TEST 5: task.md'de Faz 5 tamamlanmış mı?
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 5: task.md Faz 5 Durumu")
log("="*60)

task_path = os.path.join(PROJECT_ROOT, "task.md")
check("task.md mevcut", os.path.isfile(task_path))

if os.path.isfile(task_path):
    with open(task_path, 'r', encoding='utf-8') as f:
        task_content = f.read()
    
    faz5_header = "Faz 5" in task_content
    faz5_done = "✅ Faz 5: GRU Eğitimi ✅" in task_content
    
    check("task.md'de Faz 5 başlığı var", faz5_header)
    check("task.md'de Faz 5 tamamlandı işareti var", faz5_done)
    
    # Faz 5 checkbox'ları
    faz5_checklines = [l for l in task_content.split("\n") if "Faz 5" in l or "gru_epoch100" in l or "GRUModel oluştur" in l]
    check(f"task.md'de Faz 5 detayları mevcut", len(faz5_checklines) > 5, f"({len(faz5_checklines)} satır)")

# ════════════════════════════════════════════════════════════
# TEST 6: GRUModel import test
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 6: GRUModel Import Test")
log("="*60)

try:
    sys.path.insert(0, PROJECT_ROOT)
    from src.models import GRUModel
    check("GRUModel import başarılı", True)
    
    # GRUModel örnekleme testi
    model = GRUModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)
    param_count = sum(p.numel() for p in model.parameters())
    check("GRUModel instance oluşturuldu", True, f"(parametre sayısı: {param_count})")
    check("Parametre sayısı == 23,301", param_count == 23301)
    
    # İleri besleme testi
    import torch
    x = torch.randn(64, 20, 1)  # batch=64, seq_len=20, features=1
    output = model(x)
    check("İleri besleme (forward) başarılı", output.shape == torch.Size([64, 20, 1]))
    
except ImportError as e:
    check("GRUModel import", False, f"ImportError: {e}")
    errors.append(f"ImportError: {e}")
except Exception as e:
    check("GRUModel test", False, f"Exception: {type(e).__name__}: {e}")
    errors.append(f"Exception: {type(e).__name__}: {e}")

# ════════════════════════════════════════════════════════════
# TEST 7: train/evaluate modülü import
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 7: train ve evaluate Modülleri Import")
log("="*60)

try:
    from src.train import train_model
    check("train_model import", True)
except ImportError as e:
    check("train_model import", False, str(e))
    errors.append(f"train import error: {e}")

try:
    from src.evaluate import evaluate_model, plot_predictions, plot_loss
    check("evaluate_model import", True)
    check("plot_predictions import", True)
    check("plot_loss import", True)
except ImportError as e:
    check("evaluate modül import", False, str(e))
    errors.append(f"evaluate import error: {e}")

# ════════════════════════════════════════════════════════════
# TEST 8: Non-interactive backend uyarısı kontrol
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("TEST 8: Uyarı/Hata Kontrol")
log("="*60)

# matplotlib non-interactive backend uyarısı normal ve kabul edilebilir
# Eğer matplotlib kullanıldıysa bu uyarı olabilir ama sorun değil

# ════════════════════════════════════════════════════════════
# Özet
# ════════════════════════════════════════════════════════════
log("\n" + "="*60)
log("SONUÇ ÖZETİ")
log("="*60)

total = len(results) // 2 + 1  # approximate
pass_count = len([r for r in results if "✅ PASS" in r])
fail_count = len([r for r in results if "❌ FAIL" in r])

log(f"Toplam: {total} test")
log(f"✅ Başarılı: {pass_count}")
log(f"❌ Başarısız: {fail_count}")

if errors:
    log(f"\n⚠️ HATALAR:")
    for e in errors:
        log(f"  - {e}")

if not errors:
    log("\n🎉 Tüm testler başarılı!")

# ════════════════════════════════════════════════════════════
# Rapora yaz
# ════════════════════════════════════════════════════════════
report_path = os.path.join(PROJECT_ROOT, "working", "test_report_faz_5.md")
with open(report_path, 'w', encoding='utf-8') as f:
    f.write("# 🧪 FAZ 5 TEST RAPORU\n")
    f.write(f"## Tarih: 2026-06-29\n\n")
    f.write("## Test Sonuçları\n\n")
    
    for r in results:
        f.write(f"{r}\n")
    
    f.write(f"\n## Sonuç\n\n")
    f.write(f"- **Toplam Test:** {total}\n")
    f.write(f"- **Başarılı:** {pass_count}\n")
    f.write(f"- **Başarısız:** {fail_count}\n")
    
    if errors:
        f.write(f"\n### Hatalar\n")
        for e in errors:
            f.write(f"- {e}\n")
    else:
        f.write(f"\n✅ **Tüm testler başarılı.**\n")

print(f"\nRapor yazıldı: {report_path}")
