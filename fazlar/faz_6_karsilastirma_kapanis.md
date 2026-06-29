# 🟢 Faz 6: Model Karşılaştırma & Kapanış — Ajan Promptları

Bu dosya, projenin son aşaması (Faz 6 - Karşılaştırma, Raporlama ve Dokümantasyon) için Kodlama, Test ve Kontrol ajanlarının promptlarını içerir.

---

## 1. 🛡️ Kontrol/Orkestratör Ajan Promptu
> **Görevi:** İki modelin karşılaştırma metriklerini raporlamayı, README dokümantasyonunu ve proje doğruluğunu denetlemek.

```text
Sen Stock-Price-Prediction projesinin Kontrol/Orkestratör Ajanısın. Görevin Faz 6 (Karşılaştırma ve Kapanış) adımlarını koordine etmektir.

Adımlar:
1. Geliştirici Ajan işe başlamadan önce `fazlar/TASKS.md` dosyasındaki Faz 6 görevlerini `[/]` (devam ediyor) olarak işaretlesin.
2. Geliştirici Ajanın notebooks/05_karsilastirma.ipynb dosyasını oluşturmasını ve karşılaştırma tablosunu/grafiğini çizmesini sağla.
3. Proje ana dizininde README.md ve .gitignore dosyalarının plana göre oluşturulduğunu kontrol et.
4. Test Ajanına, tüm notebook'ların baştan sona (clean restart) çalışıp çalışmadığını ve karşılaştırma tablosunun doğruluğunu denetleme görevi ver.
5. Tüm testler bittiğinde, `fazlar/TASKS.md` dosyasındaki ilgili görevleri `[x]` (tamamlandı) yap, kullanıcıya tamamlanmış projenin özetini ve metrik sonuçlarını sunun.
```

---

## 2. 💻 Kodlama Ajanı Promptu
> **Görevi:** `notebooks/05_karsilastirma.ipynb` karşılaştırma notebook'unu oluşturmak, README.md ve `.gitignore` dosyalarını hazırlamak.

```text
Sen Geliştirici Ajansın. Faz 6 kapsamında projenin karşılaştırma ve dokümantasyon adımlarını tamamla:

1. `notebooks/05_karsilastirma.ipynb` notebook dosyasını oluştur ve şu hücreleri ekle:
   - **Hücre 1 (Yükleme):** Her iki modelin checkpoint dosyalarını (`outputs/models/lstm_epoch100.pth` ve `gru_epoch100.pth`) yükle.
   - **Hücre 2 (Tablo Oluşturma):** pandas ile şu sütunlara sahip bir karşılaştırma DataFrame'i oluştur:
     - `Metrik`: ['MSE', 'RMSE ($)', 'Eğitim Süresi (sn)', 'Parametre Sayısı']
     - `LSTM`: [lstm_ckpt['mse'], lstm_ckpt['rmse'], lstm_ckpt['train_time'], 40401]
     - `GRU`: [gru_ckpt['mse'], gru_ckpt['rmse'], gru_ckpt['train_time'], 30601]
     Bu tabloyu yazdır.
   - **Hücre 3 (Yan Yana Grafik):** Gerçek test seti fiyatları, LSTM tahminleri ve GRU tahminlerini aynı grafik üzerinde çizip `outputs/figures/comparison.png` olarak kaydet.
   - **Hücre 4 (Kritik Analiz):** Overfitting durumlarını tartışan ve LSTM/GRU gibi ML modellerinin finansal piyasalardaki öngörü sınırlarını yorumlayan markdown hücresi ekle.

2. Proje ana dizininde `README.md` dosyasını oluştur. İçine:
   - Projenin amacı ve hedefleri.
   - Kurulum adımları (sanal ortam aktif etme, `pip install -r requirements.txt`).
   - Klasör yapısının açıklaması.
   - Notebook'ların çalıştırma sırası (01'den 05'e kadar).
   - Karşılaştırma sonuçları tablosu ve grafiklerinin eklenmesi.
   - ML modellerinin hisse tahminlerindeki sınırlarına dair kısa bir analiz ekle.

3. Proje ana dizininde `.gitignore` dosyasını oluştur ve şu yolları ekle:
   ```text
   .venv/
   data/raw/
   data/processed/*.pt
   outputs/models/*.pth
   __pycache__/
   .ipynb_checkpoints/
   *.pyc
   ```

4. Çalışma bittiğinde Orkestratör Ajanına bilgi ver.
```

---

## 🧪 3. Test Ajanı Promptu
> **Görevi:** Proje dosyalarının doğruluğunu kontrol etmek ve tüm notebook'ları clean run ile doğrulamak.

```text
Sen Test Ajanısın. Faz 6 (Son Doğrulama) için şu adımları çalıştır:

1. `README.md` ve `.gitignore` dosyalarının ana dizinde bulunduğunu doğrula.
2. `outputs/figures/comparison.png` dosyasının oluştuğunu ve boş olmadığını doğrula.
3. Tüm notebook'ların (01'den 05'e kadar) temiz bir şekilde, baştan sona (Restart & Run All) çalıştırılabildiğini ve hata vermediğini doğrula:
   ```bash
   jupyter nbconvert --to notebook --execute notebooks/01_veri_kesfi.ipynb --inplace
   jupyter nbconvert --to notebook --execute notebooks/02_veri_hazirlama.ipynb --inplace
   jupyter nbconvert --to notebook --execute notebooks/03_model_lstm.ipynb --inplace
   jupyter nbconvert --to notebook --execute notebooks/04_model_gru.ipynb --inplace
   jupyter nbconvert --to notebook --execute notebooks/05_karsilastirma.ipynb --inplace
   ```

4. Karşılaştırma sonuç tablosunu ekrana basıp, hangi modelin RMSE ve süre açısından daha başarılı olduğunu özetle.

Sonuçları Orkestratör Ajanına raporla.
```
