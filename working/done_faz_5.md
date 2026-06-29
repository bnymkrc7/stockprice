# Faz 5 — GRU Eğitimi: Tamamlandı

## Yapılan İşler

### 1. `notebooks/04_model_gru.ipynb` Notebook'u Oluşturuldu
- LSTM notebook'u ile **aynı yapıda** (6 hücre), sadece GRU kullanılıyor
- Tüm hücreler **code** tipinde, çalıştırılabilir

#### Notebook Hücreleri:
| Hücre | İçerik | Açıklama |
|-------|--------|----------|
| 0 | Setup | `%load_ext autoreload`, `torch`, `pickle`, `src.models.GRUModel`, `src.train`, `src.evaluate` importları |
| 1 | Veri Yükleme | `amzn_processed.pt` + `scaler.pkl` (Faz 2'den güvenli şekilde kaydedilmiş) |
| 2 | Model Oluştur | `GRUModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)` — 23,301 parametre |
| 3 | Eğitim | `train_model()` — 100 epoch, lr=0.001, Adam optimizer, batch_size=64 |
| 4 | Değerlendirme | `evaluate_model`, `plot_predictions` (gru_predictions.png), `plot_loss` (gru_loss.png) |
| 5 | Model Kaydetme | `outputs/models/gru_epoch100.pth` — state_dict + hiperparametreler + metrikler |

### 2. `task.md` Güncellendi
- Faz 5 bölümü eklendi (başarıyla işaretli)
- Sıradaki adım: Faz 6 (Model Karşılaştırma & Sonuç Analizi)

### 3. Çıktı Dizinleri Hazırlandı
- `outputs/models/` — GRU model ağırlıkları için
- `outputs/figures/` — GRU grafikleri için

## Teknik Detaylar
- **Model:** GRU (Gated Recurrent Unit) — LSTM'in basitleştirilmiş hali (3 gate → 2 gate)
- **Karşılaştırma:** Fair comparison için LSTM ile aynı hiperparametreler (hidden=50, layers=2, dropout=0.2)
- **GRU Avantajı:** Daha az parametre (23,301 vs LSTM 31,051) → daha hızlı eğitim
- **Veri Sızıntısı:** ENGELLENDİ — scaler sadece %80 training verisine fit edildi (Faz 2'den)

## Dosyalar
- ✅ `notebooks/04_model_gru.ipynb` — GRU eğitim notebook'u (6 hücre)
- ✅ `task.md` — Faz 5 tamamlandı olarak işaretlendi
- ✅ `outputs/models/` — Model kaydetme dizini hazır
- ✅ `outputs/figures/` — Grafik kaydetme dizini hazır

## Sıradaki Adım
Faz 6: Model Karşılaştırma & Sonuç Analizi (LSTM vs GRU karşılaştırma raporu)
