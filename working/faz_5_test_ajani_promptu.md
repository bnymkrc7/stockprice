# 🧪 TEST AJANI: FAZ_5 — GRU Eğitimi (Süre: ~1-2 saat)

## 🎯 TEST VE DOĞRULAMA DETAYLARI (PLANDAN OKUNAN)
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

## 📋 TEST UYGULAMA TALİMATLARI
1. Kodlama aşamasında yazılan/değiştirilen tüm dosyaların yerlerin olduğunu doğrulayın.
2. İlgili test senaryolarını çalıştırın (örneğin import testleri, model ileri besleme testleri veya veri doğrulama testleri).
3. Test çıktılarında herhangi bir `WARNING` veya `HATA` olmadığından emin olun (oturum bulunamadığında graceful fallback kullanın).
4. Test sonuçlarını `working/test_report_faz_5.md` dosyası olarak kaydedin.
5. Başarılı sonuçları Orkestratör Ajanına rapor edin.
