# 🛡️ ORKESTRATÖR AJANI GÖREVİ: FAZ_6 — Karşılaştırma & İyileştirme (Süre: ~2-3 saat)

## 🎯 FAZ HEDEFİ
Bu fazın (Karşılaştırma & İyileştirme (Süre: ~2-3 saat)) kodlama, test ve commit/push süreçlerini koordine etmek.

## 📋 YÖNERGELER
1. Geliştirici Ajan'a (Coding Agent) `working/faz_6_kodlama_ajani_promptu.md` dosyasındaki talimatları ilet ve kodlamayı başlat.
2. Geliştirici Ajan'dan `working/done_faz_6.md` bildirimini alana kadar bekle.
3. Done bildirimi geldiğinde, elindeki **`delegation` (delege etme)** veya **`invoke_subagent`** aracını kullanarak Test Ajanı'nı çağır ve ona `working/faz_6_test_ajani_promptu.md` görevini arka planda delege et.
4. Test Ajanı'nın testi tamamlamasını ve `working/test_report_faz_6.md` raporunu yazmasını bekle.
5. Test raporu başarılıysa (Warning/Hata yoksa):
   - `fazlar/TASKS.md` (veya proje kök dizinindeki `TASKS.md`) dosyasında bu faz altındaki görevleri `[x]` (tamamlandı) olarak işaretle.
   - Değişiklikleri git'e ekle ve şu mesajla commit et: `feat(faz_6): Karşılaştırma & İyileştirme (Süre: ~2-3 saat) completed`
   - Eğer github uzak sunucusu aktifse repo'ya push et.
   - `orchestrator_get_next_prompt` aracını çağırarak bir sonraki faza geçiş yap.
6. Testlerde hata çıkarsa, hata detaylarını Geliştirici Ajan'a ileterek düzeltmesini iste ve döngüyü tekrarla.
