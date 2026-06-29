# 🧪 TEST AJANI: FAZ_6 — Karşılaştırma & İyileştirme (Süre: ~2-3 saat)

## 🎯 TEST VE DOĞRULAMA DETAYLARI (PLANDAN OKUNAN)
> **Ne öğreneceksin:** İki modeli objektif karşılaştırmayı, hiperparametre optimizasyonunu, overfitting tespitini.

### 📓 Notebook: `05_karsilastirma.ipynb`

**Hücre 1:** İki modeli de yükle
```python
lstm_ckpt = torch.load("../outputs/models/lstm_epoch100.pth", weights_only=True)
gru_ckpt = torch.load("../outputs/models/gru_epoch100.pth", weights_only=True)

comparison = pd.DataFrame({
    'Metrik': ['MSE', 'RMSE ($)', 'Eğitim Süresi (sn)', 'Parametre Sayısı'],
    'LSTM': [lstm_ckpt['mse'], lstm_ckpt['rmse'], lstm_ckpt['train_time'], 40401],
    'GRU': [gru_ckpt['mse'], gru_ckpt['rmse'], gru_ckpt['train_time'], 30601],
})
print(comparison.to_string(index=False))
```

**Hücre 2:** Yan yana grafik
```python
# İki tahmini aynı grafikte göster
plt.figure(figsize=(14, 5))
plt.plot(actuals, label='Gerçek', linewidth=2, alpha=0.8)
plt.plot(lstm_preds, label='LSTM Tahmin', linewidth=1.5, alpha=0.7)
plt.plot(gru_preds, label='GRU Tahmin', linewidth=1.5, alpha=0.7)
plt.title('LSTM vs GRU: Amazon Hisse Fiyat Tahmini')
plt.legend()
plt.savefig("../outputs/figures/comparison.png", dpi=150)
```

### 🔧 Hiperparametre İyileştirme (Opsiyonel)

İlk sonuçlar kötüyse dene:

| Parametre | Varsayılan | Dene | Neden? |
|-----------|-----------|------|--------|
| `lookback` | 20 | 10, 30, 50 | Kısa/uzun vadeli trendler |
| `hidden_size` | 50 | 32, 64, 128 | Model kapasitesi |
| `num_layers` | 2 | 1, 3 | Derinlik |
| `dropout` | 0.2 | 0, 0.3, 0.5 | Overfitting kontrolü |
| `learning_rate` | 0.001 | 0.01, 0.0001 | Öğrenme hızı |
| `epochs` | 100 | 50, 200 | Eğitim süresi |

### 🧠 TradingView Entegrasyonu (Ek Özellik)

Modelin tahmin gücünü artırmak için teknik indikatörleri ek girdi olarak kullanabiliriz:

```python
from tradingview_ta import TA_Handler, Interval

# TradingView'dan teknik indikatör al
handler = TA_Handler(
    symbol="AMZN",
    screener="america",
    exchange="NASDAQ",
    interval=Interval.INTERVAL_1_DAY
)
analysis = handler.get_analysis()

# İndikatörleri al
indicators = {
    'RSI': analysis.indicators['RSI'],
    'MACD': analysis.indicators['MACD.macd'],
    'SMA20': analysis.indicators['SMA20'],
    'Volume': analysis.indicators['volume'],
}

# Bunları modelin input'una ek feature olarak ekleyebiliriz
# (ileri seviye — ilk versiyonda sadece Close fiyatı kullan)
```

---

## 📋 TEST UYGULAMA TALİMATLARI
1. Kodlama aşamasında yazılan/değiştirilen tüm dosyaların yerlerin olduğunu doğrulayın.
2. İlgili test senaryolarını çalıştırın (örneğin import testleri, model ileri besleme testleri veya veri doğrulama testleri).
3. Test çıktılarında herhangi bir `WARNING` veya `HATA` olmadığından emin olun (oturum bulunamadığında graceful fallback kullanın).
4. Test sonuçlarını `working/test_report_faz_6.md` dosyası olarak kaydedin.
5. Başarılı sonuçları Orkestratör Ajanına rapor edin.
