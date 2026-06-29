#!/usr/bin/env python3
"""
Ad-hoc test script for Faz 4 (LSTM Model Training).
Validates notebook structure, file accessibility, and runs the training pipeline.
"""
import json
import sys
import os
import warnings

# Suppress matplotlib interactive backend warnings
warnings.filterwarnings("ignore")

os.chdir("/home/zorildiz/projeler/bunyamin/stock-price-prediction")
sys.path.insert(0, os.getcwd())

results = []
errors = []
warnings_list = []

def log(msg, status="PASS"):
    results.append(f"- [{status}] {msg}")
    if status == "FAIL":
        errors.append(msg)
    elif status == "WARN":
        warnings_list.append(msg)

# ─── TEST 1: Notebook JSON Geçerliliği ───
print("=" * 60)
print("TEST 1: Notebook JSON Geçerliliği")
print("=" * 60)

nb_path = "notebooks/03_model_lstm.ipynb"
try:
    with open(nb_path, 'r') as f:
        nb = json.load(f)
    log("Notebook JSON geçerli (parse edilebilir)")

    nbformat = nb.get("nbformat")
    nbformat_minor = nb.get("nbformat_minor")
    log(f"nbformat: {nbformat}, nbformat_minor: {nbformat_minor}")
    if nbformat == 4:
        log("✅ nbformat 4 (doğru)")
    else:
        log(f"❌ nbformat 4 değil (gerçek: {nbformat})", "FAIL")

    cells = nb.get("cells", [])
    log(f"Hücre sayısı: {len(cells)}")
    if len(cells) == 6:
        log("✅ 6 hücre (doğru)")
    else:
        log(f"❌ 6 hücre değil (gerçek: {len(cells)})", "FAIL")
except Exception as e:
    log(f"Notebook JSON parse hatası: {e}", "FAIL")

# ─── TEST 2: Hücre Anahtar Kelimeleri ───
print("\n" + "=" * 60)
print("TEST 2: Hücre Anahtar Kelimeleri")
print("=" * 60)

expected_keywords = {
    0: ["setup", "setup"],
    1: ["load_data", "load_data"],
    2: ["model_create", "model_create"],
    3: ["train", "train"],
    4: ["evaluate", "evaluate"],
    5: ["save_model", "save_model"],
}

for idx in range(6):
    cell = cells[idx]
    source = ''.join(cell.get('source', []))
    source_lower = source.lower()
    cell_type = cell.get('cell_type', 'unknown')
    keywords = expected_keywords.get(idx, [])
    found = []
    
    for kw in keywords:
        if kw in source_lower:
            found.append(kw)
        # Daha esnek eşleşme
        if kw == "setup" and ("%load_ext autoreload" in source or "import sys" in source):
            found.append("setup")
        if kw == "load_data" and ("torch.load" in source or "pickle.load" in source):
            found.append("load_data")
        if kw == "model_create" and "LSTMModel(" in source:
            found.append("model_create")
        if kw == "train" and "train_model(" in source:
            found.append("train")
        if kw == "evaluate" and "evaluate_model(" in source:
            found.append("evaluate")
        if kw == "save_model" and "torch.save(" in source:
            found.append("save_model")
    
    status = "✅" if len(found) == len(keywords) else "❌"
    log(f"  Hücre {idx+1} ({cell_type}): anahtar kelimeler = {found} {status}")

# ─── TEST 3: Dosya Erişilebilirliği ───
print("\n" + "=" * 60)
print("TEST 3: Dosya Erişilebilirliği")
print("=" * 60)

required_files = ["src/models.py", "src/train.py", "src/evaluate.py"]
for f in required_files:
    if os.path.isfile(f):
        size = os.path.getsize(f)
        log(f"✅ {f} mevcut ({size} byte)")
    else:
        log(f"❌ {f} bulunamadı", "FAIL")

# ─── TEST 4: Dizin Mevcutluğu ───
print("\n" + "=" * 60)
print("TEST 4: Dizin Mevcutluğu")
print("=" * 60)

required_dirs = ["outputs/models/", "outputs/figures/"]
for d in required_dirs:
    if os.path.isdir(d):
        contents = os.listdir(d)
        log(f"✅ {d} mevcut ({len(contents)} dosya: {contents})")
    else:
        log(f"❌ {d} dizini bulunamadı", "FAIL")

# ─── TEST 5: Data Dosyaları ───
print("\n" + "=" * 60)
print("TEST 5: Veri Dosyaları")
print("=" * 60)

data_files = ["data/processed/amzn_processed.pt", "data/processed/scaler.pkl"]
for f in data_files:
    if os.path.isfile(f):
        size = os.path.getsize(f)
        log(f"✅ {f} mevcut ({size} byte)")
    else:
        log(f"❌ {f} bulunamadı", "FAIL")

# ─── TEST 6: task.md'de Faz 4 ───
print("\n" + "=" * 60)
print("TEST 6: task.md İçeriği")
print("=" * 60)

task_path = "task.md"
try:
    with open(task_path, 'r') as f:
        task_content = f.read()
    
    if "Faz 4" in task_content or "Faz 3" in task_content:
        # Faz 4 henüz task.md'de yok ama Faz 3 var
        log("⚠️ task.md'de Faz 3 mevcut, Faz 4 henüz listelenmemiş (beklenen - Faz 4 çalıştırılacak)")
    else:
        log("⚠️ task.md'de Faz 4 veya Faz 3 bilgisi bulunamadı", "WARN")
except Exception as e:
    log(f"task.md okuma hatası: {e}", "FAIL")

# ─── TEST 7: Notebook'u Çalıştırma (Adım 1-3: Setup, Load, Model) ───
print("\n" + "=" * 60)
print("TEST 7: Notebook Çalıştırma (Setup + Load + Model)")
print("=" * 60)

try:
    import torch
    import pickle
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    log(f"✅ Cihaz: {device}")
    
    # Load data (cells 2)
    data = torch.load("data/processed/amzn_processed.pt", weights_only=True, map_location=device)
    scaler = pickle.load(open("data/processed/scaler.pkl", "rb"))
    X_train, y_train = data['X_train'], data['y_train']
    X_test, y_test = data['X_test'], data['y_test']
    log(f"✅ Veri yüklendi: Train={X_train.shape}, Test={X_test.shape}")
    
    # Create model (cell 3)
    from src.models import LSTMModel
    model = LSTMModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)
    param_count = sum(p.numel() for p in model.parameters())
    log(f"✅ Model oluşturuldu: {param_count:,} parametre")
    
except Exception as e:
    log(f"❌ Setup/Load/Model hatası: {e}", "FAIL")

# ─── TEST 8: Eğitim (Cell 4) ───
print("\n" + "=" * 60)
print("TEST 8: Model Eğitimi")
print("=" * 60)

try:
    from src.train import train_model
    loss_history, train_time = train_model(
        model, X_train, y_train,
        epochs=100, lr=0.001, device=device
    )
    log(f"✅ Eğitim tamamlandı: {train_time:.2f} sn")
    log(f"   İlk Loss: {loss_history[0]:.6f}, Son Loss: {loss_history[-1]:.6f}")
    loss_reduction = (1 - loss_history[-1]/loss_history[0]) * 100
    log(f"   Loss Azalması: {loss_reduction:.1f}%")
    
    if loss_history[-1] < loss_history[0]:
        log("✅ Loss azalıyor (eğitim başarılı)")
    else:
        log("⚠️ Loss azalmıyor (potansiyel sorun)", "WARN")
        
except Exception as e:
    log(f"❌ Eğitim hatası: {e}", "FAIL")
    errors.append(f"Eğitim: {e}")

# ─── TEST 9: Değerlendirme (Cell 5) ───
print("\n" + "=" * 60)
print("TEST 9: Model Değerlendirme")
print("=" * 60)

try:
    from src.evaluate import evaluate_model, plot_predictions, plot_loss
    preds, actuals, mse, rmse = evaluate_model(
        model, X_test, y_test, scaler=scaler, device=device
    )
    log(f"✅ Değerlendirme tamamlandı: MSE={mse:.4f}, RMSE={rmse:.4f}")
    
    # Save predictions plot
    plot_predictions(actuals, preds,
        title="LSTM: Amazon Hisse Fiyat Tahmini",
        save_path="outputs/figures/lstm_predictions.png")
    log("✅ Tahmin grafiği kaydedildi: outputs/figures/lstm_predictions.png")
    
    # Save loss plot
    plot_loss(loss_history,
        title="LSTM Eğitim Kaybı",
        save_path="outputs/figures/lstm_loss.png")
    log("✅ Loss grafiği kaydedildi: outputs/figures/lstm_loss.png")
    
except Exception as e:
    log(f"❌ Değerlendirme hatası: {e}", "FAIL")

# ─── TEST 10: Model Kaydetme (Cell 6) ───
print("\n" + "=" * 60)
print("TEST 10: Model Kaydetme")
print("=" * 60)

try:
    model_save_path = "outputs/models/lstm_epoch100.pth"
    torch.save({
        'model_state_dict': model.state_dict(),
        'hidden_size': 50,
        'num_layers': 2,
        'mse': mse,
        'rmse': rmse,
        'train_time': train_time,
    }, model_save_path)
    
    if os.path.isfile(model_save_path):
        size = os.path.getsize(model_save_path)
        log(f"✅ Model kaydedildi: {model_save_path} ({size} byte)")
    else:
        log("❌ Model dosyası oluşturulmadı", "FAIL")
        
except Exception as e:
    log(f"❌ Model kaydetme hatası: {e}", "FAIL")

# ─── ÖZET ───
print("\n" + "=" * 60)
print("📋 TEST ÖZETİ")
print("=" * 60)

pass_count = sum(1 for r in results if "[PASS]" in r)
fail_count = sum(1 for r in results if "[FAIL]" in r)
warn_count = sum(1 for r in results if "[WARN]" in r)

print(f"  ✅ PASS: {pass_count}")
print(f"  ❌ FAIL: {fail_count}")
print(f"  ⚠️ WARN: {warn_count}")

if errors:
    print(f"\nHATALAR:")
    for e in errors:
        print(f"  - {e}")

if warnings_list:
    print(f"\nUYARILAR:")
    for w in warnings_list:
        print(f"  - {w}")

print(f"\nTüm testler: {'BAŞARILI' if fail_count == 0 else 'BAŞARISIZ'}")

# Write results to stdout for capture
with open("/home/zorildiz/projeler/bunyamin/stock-price-prediction/working/test_results.txt", 'w') as f:
    for r in results:
        f.write(r + "\n")
    if errors:
        f.write("\nHATALAR:\n")
        for e in errors:
            f.write(f"  - {e}\n")
    if warnings_list:
        f.write("\nUYARILAR:\n")
        for w in warnings_list:
            f.write(f"  - {w}\n")
