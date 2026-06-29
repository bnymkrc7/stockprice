# 💻 GELİŞTİRİCİ GÖREVİ: FAZ_5 — GRU Eğitimi (Süre: ~1-2 saat)

## 🎯 GÖREV DETAYLARI (PLANDAN OKUNAN)
> **Ne yapacağız:** Aynı veriyi GRU ile eğit, sonuçları karşılaştırmaya hazırlan.

### 📓 Notebook: `04_model_gru.ipynb`

Aynı LSTM notebook'unun aynısı, sadece:

```python
from src.models import GRUModel  # ← LSTM yerine GRU

model = GRUModel(input_size=1, hidden_size=50, num_layers=2, dropout=0.2)

# ... eğit, değerlendir, kaydet ...

torch.save({...}, "../outputs/models/gru_epoch100.pth")  # ← farklı isim
```

📌 **Neden aynı parametreler?** Fair comparison (adil karşılaştırma) için. İkisi de aynı koşullarda eğitilmeli ki hangisinin daha iyi olduğunu görebilelim.

---

## 🔄 GELİŞTİRİCİ İŞ AKIŞI
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki FAZ_5 görevini `[/]` (devam ediyor) olarak işaretlesin.
2. Yukarıda belirtilen kodlama hedeflerini, modülerlik ve veri sızıntısını önleme kurallarına uyarak kodlayın.
3. Çalışma bittiğinde `working/done_faz_5.md` adında bir done dosyası oluşturarak yapılan işleri özetleyin.
4. Değişikliklerinizi test ajanı ile doğrulamaya hazır hale getirin.
