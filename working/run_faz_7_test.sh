#!/bin/bash
# Faz 7 Test Scripti
# README.md ve .gitignore dosyalarının çalıştığını doğrular.

cd /home/zorildiz/projeler/bunyamin/stock-price-prediction

echo "=========================================="
echo " 🧪 FAZ 7 TEST SCRIPTI"
echo "=========================================="
echo ""

PASS=0
FAIL=0
WARN=0

# ---------------------------------------------------
# TEST 1: README.md Mevcutluğu
# ---------------------------------------------------
echo "--- TEST 1: README.md Mevcutluğu ---"
if [ -f "README.md" ]; then
    echo "✅ README.md dosyası mevcut"
    PASS=$((PASS+1))
else
    echo "❌ README.md dosyası mevcut DEĞİL"
    FAIL=$((FAIL+1))
fi
echo ""

# ---------------------------------------------------
# TEST 2: README.md İçerik Kontrolü
# ---------------------------------------------------
echo "--- TEST 2: README.md İçerik Kontrolü ---"

# Bölüm: Proje Amacı
if grep -qi "proje amacı\|🎯\|proje.*amaç" README.md; then
    echo "✅ 'Proje Amacı' bölümü mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'Proje Amacı' bölümü YOK"
    FAIL=$((FAIL+1))
fi

# Bölüm: Kurulum
if grep -qi "kurulum\|🛠️\|venv\|activate" README.md; then
    echo "✅ 'Kurulum' bölümü mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'Kurulum' bölümü YOK"
    FAIL=$((FAIL+1))
fi

# Bölüm: Dosya Yapısı
if grep -qi "dosya yapısı\|📁\|tree\|notebooks\|src/" README.md; then
    echo "✅ 'Dosya Yapısı' bölümü mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'Dosya Yapısı' bölümü YOK"
    FAIL=$((FAIL+1))
fi

# Bölüm: Çalıştırma
if grep -qi "çalıştır\|🚀\|notebook.*sıra\|01_veri" README.md; then
    echo "✅ 'Nasıl Çalıştırılır' bölümü mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'Nasıl Çalıştırılır' bölümü YOK"
    FAIL=$((FAIL+1))
fi

# Bölüm: Sonuçlar
if grep -qi "sonuç\|📊\|karşılaştırma\|MSE\|RMSE" README.md; then
    echo "✅ 'Sonuçlar' bölümü mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'Sonuçlar' bölümü YOK"
    FAIL=$((FAIL+1))
fi

# Bölüm: Çıkarımlar
if grep -qi "çıkarım\|🧠\|model.*daha.*iyi\|verimlilik" README.md; then
    echo "✅ 'Çıkarımlar' bölümü mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'Çıkarımlar' bölümü YOK"
    FAIL=$((FAIL+1))
fi
echo ""

# ---------------------------------------------------
# TEST 3: .gitignore Mevcutluğu
# ---------------------------------------------------
echo "--- TEST 3: .gitignore Mevcutluğu ---"
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore dosyası mevcut"
    PASS=$((PASS+1))
else
    echo "❌ .gitignore dosyası mevcut DEĞİL"
    FAIL=$((FAIL+1))
fi
echo ""

# ---------------------------------------------------
# TEST 4: .gitignore İçerik Kontrolü
# ---------------------------------------------------
echo "--- TEST 4: .gitignore İçerik Kontrolü ---"

# .venv/
if grep -q "\.venv/" .gitignore; then
    echo "✅ '.venv/' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ '.venv/' pattern YOK"
    FAIL=$((FAIL+1))
fi

# __pycache__/
if grep -q "__pycache__/" .gitignore; then
    echo "✅ '__pycache__/' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ '__pycache__/' pattern YOK"
    FAIL=$((FAIL+1))
fi

# *.pyc
if grep -q "\*\.pyc" .gitignore; then
    echo "✅ '*.pyc' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ '*.pyc' pattern YOK"
    FAIL=$((FAIL+1))
fi

# data/raw/
if grep -q "data/raw/" .gitignore; then
    echo "✅ 'data/raw/' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'data/raw/' pattern YOK"
    FAIL=$((FAIL+1))
fi

# data/processed/
if grep -q "data/processed/" .gitignore; then
    echo "✅ 'data/processed/' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'data/processed/' pattern YOK"
    FAIL=$((FAIL+1))
fi

# outputs/models/*.pth
if grep -q "outputs/models/\*\.pth" .gitignore; then
    echo "✅ 'outputs/models/*.pth' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'outputs/models/*.pth' pattern YOK"
    FAIL=$((FAIL+1))
fi

# outputs/figures/
if grep -q "outputs/figures/" .gitignore; then
    echo "✅ 'outputs/figures/' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'outputs/figures/' pattern YOK"
    FAIL=$((FAIL+1))
fi

# logs/
if grep -q "logs/" .gitignore; then
    echo "✅ 'logs/' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'logs/' pattern YOK"
    FAIL=$((FAIL+1))
fi

# .DS_Store
if grep -q "\.DS_Store" .gitignore; then
    echo "✅ '.DS_Store' pattern mevcut"
    PASS=$((PASS+1))
else
    echo "❌ '.DS_Store' pattern YOK"
    FAIL=$((FAIL+1))
fi
echo ""

# ---------------------------------------------------
# TEST 5: task.md'de Faz 7'nin Tamamlandığını Kontrol
# ---------------------------------------------------
echo "--- TEST 5: task.md Faz 7 Kontrolü ---"
if grep -qi "faz 7" task.md; then
    echo "✅ 'Faz 7' task.md'de mevcut"
    PASS=$((PASS+1))
else
    echo "❌ 'Faz 7' task.md'de YOK"
    FAIL=$((FAIL+1))
fi

if grep -qi "tamamlandı\|✅\|\[x\]" task.md; then
    echo "✅ Faz 7 tamamlandı olarak işaretlenmiş"
    PASS=$((PASS+1))
else
    echo "⚠️ Faz 7 tamamlanma durumu belirsiz"
    WARN=$((WARN+1))
fi
echo ""

# ---------------------------------------------------
# TEST 6: working/done_faz_7.md Mevcutluğu
# ---------------------------------------------------
echo "--- TEST 6: working/done_faz_7.md Mevcutluğu ---"
if [ -f "working/done_faz_7.md" ]; then
    echo "✅ working/done_faz_7.md dosyası mevcut"
    PASS=$((PASS+1))
else
    echo "❌ working/done_faz_7.md dosyası mevcut DEĞİL"
    FAIL=$((FAIL+1))
fi
echo ""

# ---------------------------------------------------
# TEST 7: README.md Satır Sayısı
# ---------------------------------------------------
echo "--- TEST 7: README.md Boyut Kontrolü ---"
readme_lines=$(wc -l < README.md)
readme_chars=$(wc -c < README.md)
echo "📄 README.md: $readme_lines satır, $readme_chars byte"
if [ "$readme_lines" -ge 20 ]; then
    echo "✅ README.md yeterli uzunlukta ($readme_lines satır)"
    PASS=$((PASS+1))
else
    echo "⚠️ README.md kısa ($readme_lines satır)"
    WARN=$((WARN+1))
fi
echo ""

# ---------------------------------------------------
# TEST 8: .gitignore Satır Sayısı
# ---------------------------------------------------
echo "--- TEST 8: .gitignore Boyut Kontrolü ---"
gitignore_lines=$(wc -l < .gitignore)
gitignore_entries=$(grep -v "^#\|^$" .gitignore | wc -l)
echo "📄 .gitignore: $gitignore_lines satır, $gitignore_entries aktif pattern"
if [ "$gitignore_entries" -ge 8 ]; then
    echo "✅ .gitignore yeterli pattern'a sahip ($gitignore_entries)"
    PASS=$((PASS+1))
else
    echo "⚠️ .gitignore yetersiz pattern ($gitignore_entries)"
    WARN=$((WARN+1))
fi
echo ""

# ---------------------------------------------------
# SONUÇLAR
# ---------------------------------------------------
echo "=========================================="
echo " 📋 TEST SONUÇLARI"
echo "=========================================="
echo "✅ Başarılı (PASS): $PASS"
echo "⚠️  Uyarı (WARN):   $WARN"
echo "❌ Hata (FAIL):    $FAIL"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo "🎉 TÜM KRİTİK TESTLER BAŞARILI!"
else
    echo "⚠️  $FAIL adet kritk test BAŞARISIZ — düzeltilmeli."
fi
echo ""

# JSON formatında sonuç (rapor için)
echo "JSON SONUÇ:"
echo "{\"pass\": $PASS, \"fail\": $FAIL, \"warn\": $WARN, \"total_checks\": $((PASS+FAIL+WARN)), \"status\": \"$( [ $FAIL -eq 0 ] && echo 'SUCCESS' || echo 'FAILED' )\"}"
