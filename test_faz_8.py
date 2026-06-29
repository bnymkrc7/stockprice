#!/usr/bin/env python3
"""Faz 8 TradingView Entegrasyonu — Ad-hoc Test Script
Proje kök dizininde çalıştırılmalıdır.
"""

import sys
import os
import json
import traceback
from datetime import datetime

# Sanal ortam kontrolü
print("=" * 70)
print("FAZ 8 — TradingView Entegrasyonu Test Raporu")
print(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

results = []

def test(name, fn):
    """Test fonksiyonu wrapper"""
    try:
        fn()
        results.append({"name": name, "status": "OK", "message": "Test geçti"})
        print(f"  ✅ {name}")
    except AssertionError as e:
        results.append({"name": name, "status": "FAIL", "message": str(e)})
        print(f"  ❌ {name}: {e}")
    except Exception as e:
        results.append({"name": name, "status": "FAIL", "message": f"{type(e).__name__}: {e}\n{traceback.format_exc()}"})
        print(f"  ❌ {name}: {type(e).__name__}: {e}")


# ============================================================
# TEST 1: src/tradingview_features.py — Sözdizimi ve Import
# ============================================================
print("\n--- TEST 1: src/tradingview_features.py ---")

def t1_syntax():
    """Sözdizimi kontrolü"""
    import ast
    with open('src/tradingview_features.py', 'r') as f:
        code = f.read()
    ast.parse(code)
    print("    Sözdizimi geçerli.")

def t1_import():
    """Import testi"""
    import src.tradingview_features as tvf
    assert hasattr(tvf, 'fetch_tradingview_indicators'), "fetch_tradingview_indicators eksik"
    assert hasattr(tvf, 'get_multiple_indicators'), "get_multiple_indicators eksik"
    assert hasattr(tvf, 'prepare_tradingview_features'), "prepare_tradingview_features eksik"
    assert hasattr(tvf, 'create_sequences_with_indicators'), "create_sequences_with_indicators eksik"

def t1_data_leakage():
    """Veri sızıntısı koruması kontrolü"""
    import src.tradingview_features as tvf
    import inspect
    source = inspect.getsource(tvf.prepare_tradingview_features)
    assert 'fit_only' in source, "fit_only parametresi eksik"
    assert 'Scaler' in source or 'scaler' in source, "Scaler kullanımı eksik"
    # fit_only varsayılan True olmalı
    sig = inspect.signature(tvf.prepare_tradingview_features)
    assert sig.parameters['fit_only'].default is True, "fit_only default True değil"

def t1_function_signatures():
    """Fonksiyon imzaları kontrolü"""
    import src.tradingview_features as tvf
    import inspect
    
    # fetch_tradingview_indicators
    sig = inspect.signature(tvf.fetch_tradingview_indicators)
    params = list(sig.parameters.keys())
    assert 'symbol' in params, "symbol parametresi eksik"
    assert 'interval' in params, "interval parametresi eksik"
    
    # prepare_tradingview_features
    sig = inspect.signature(tvf.prepare_tradingview_features)
    params = list(sig.parameters.keys())
    assert 'raw_df' in params, "raw_df parametresi eksik"
    assert 'indicators_df' in params, "indicators_df parametresi eksik"
    assert 'scaler' in params, "scaler parametresi eksik"
    
    # create_sequences_with_indicators
    sig = inspect.signature(tvf.create_sequences_with_indicators)
    params = list(sig.parameters.keys())
    assert 'data' in params, "data parametresi eksik"
    assert 'lookback' in params, "lookback parametresi eksik"

test("tradingview_features.py — Sözdizimi", t1_syntax)
test("tradingview_features.py — Import & Fonksiyonlar", t1_import)
test("tradingview_features.py — Veri Sızıntısı Koruması", t1_data_leakage)
test("tradingview_features.py — Fonksiyon İmzaları", t1_function_signatures)


# ============================================================
# TEST 2: src/models.py — input_size=5, parametre hesaplama
# ============================================================
print("\n--- TEST 2: src/models.py ---")

def t2_syntax():
    import ast
    with open('src/models.py', 'r') as f:
        code = f.read()
    ast.parse(code)

def t2_input_size():
    """input_size default değeri 5 olmalı"""
    from src.models import LSTMModel, GRUModel
    lstm = LSTMModel()
    assert lstm.input_size == 5, f"input_size={lstm.input_size}, 5 olmalı"
    gru = GRUModel()
    assert gru.input_size == 5, f"input_size={gru.input_size}, 5 olmalı"

def t2_count_parameters():
    """Parametre sayma fonksiyonu"""
    from src.models import LSTMModel, GRUModel, get_model_param_count
    lstm = LSTMModel(input_size=5)
    gru = GRUModel(input_size=5)
    count = lstm.count_parameters()
    assert count > 0, "Parametre sayısı 0"
    assert count > 10000, f"Parametre sayısı çok düşük: {count}"
    
    text = get_model_param_count(lstm, "LSTM")
    assert "LSTM" in text, "Model adı eksik"
    assert "parametre" in text.lower(), "parametre kelimesi eksik"

def t2_count_parameters_old():
    """Eski input_size=1 ile de çalışmalı (backwards compat)"""
    from src.models import LSTMModel
    lstm_old = LSTMModel(input_size=1)
    count = lstm_old.count_parameters()
    assert count > 0, "Eski model parametre sayısı 0"
    # 1 feature LSTM parametreleri ~31000 civarında
    assert count < 100000, f"Parametre sayısı beklenmedik yüksek: {count}"

test("models.py — Sözdizimi", t2_syntax)
test("models.py — input_size=5", t2_input_size)
test("models.py — count_parameters()", t2_count_parameters)
test("models.py — Eski model (input_size=1) çalışır", t2_count_parameters_old)


# ============================================================
# TEST 3: src/preprocessing.py — Yeni ve eski fonksiyonlar
# ============================================================
print("\n--- TEST 3: src/preprocessing.py ---")

def t3_syntax():
    import ast
    with open('src/preprocessing.py', 'r') as f:
        code = f.read()
    ast.parse(code)

def t3_new_functions():
    """Yeni fonksiyonlar mevcut mu?"""
    from src.preprocessing import (
        scale_multi_features,
        create_sequences_multi,
        prepare_tensors_multi,
        prepare_tradingview_data,
    )
    assert callable(scale_multi_features)
    assert callable(create_sequences_multi)
    assert callable(prepare_tensors_multi)
    assert callable(prepare_tradingview_data)

def t3_old_functions():
    """Eski fonksiyonlar korunmuş mu?"""
    from src.preprocessing import (
        scale_data,
        create_sequences,
        prepare_tensors,
    )
    assert callable(scale_data)
    assert callable(create_sequences)
    assert callable(prepare_tensors)

def t3_tradingview_import():
    """TradingView importları var mı?"""
    with open('src/preprocessing.py', 'r') as f:
        code = f.read()
    assert 'fetch_tradingview_indicators' in code, "fetch_tradingview_indicators import eksik"
    assert 'prepare_tradingview_features' in code, "prepare_tradingview_features import eksik"
    assert 'create_sequences_with_indicators' in code, "create_sequences_with_indicators import eksik"

test("preprocessing.py — Sözdizimi", t3_syntax)
test("preprocessing.py — Yeni fonksiyonlar", t3_new_functions)
test("preprocessing.py — Eski fonksiyonlar korundu", t3_old_functions)
test("preprocessing.py — TradingView importları", t3_tradingview_import)


# ============================================================
# TEST 4: src/data_loader.py — Yeni ve eski fonksiyonlar
# ============================================================
print("\n--- TEST 4: src/data_loader.py ---")

def t4_syntax():
    import ast
    with open('src/data_loader.py', 'r') as f:
        code = f.read()
    ast.parse(code)

def t4_new_function():
    """fetch_tradingview_stock_data mevcut mu?"""
    from src.data_loader import fetch_tradingview_stock_data
    assert callable(fetch_tradingview_stock_data)

def t4_old_functions():
    """Eski fonksiyonlar korunmuş mu?"""
    from src.data_loader import fetch_stock_data, load_local_data
    assert callable(fetch_stock_data)
    assert callable(load_local_data)

def t4_tradingview_import():
    """TradingView importları var mı?"""
    with open('src/data_loader.py', 'r') as f:
        code = f.read()
    assert 'tradingview_ta' in code, "tradingview_ta import eksik"
    assert 'TA_Handler' in code, "TA_Handler import eksik"

test("data_loader.py — Sözdizimi", t4_syntax)
test("data_loader.py — Yeni fonksiyon: fetch_tradingview_stock_data", t4_new_function)
test("data_loader.py — Eski fonksiyonlar korundu", t4_old_functions)
test("data_loader.py — TradingView importları", t4_tradingview_import)


# ============================================================
# TEST 5: notebooks/06_tradingview_integration.ipynb
# ============================================================
print("\n--- TEST 5: notebooks/06_tradingview_integration.ipynb ---")

def t5_json_valid():
    """JSON geçerliliği"""
    with open('notebooks/06_tradingview_integration.ipynb', 'r') as f:
        nb = json.load(f)
    assert isinstance(nb, dict), "Notebook dict değil"
    assert 'cells' in nb, "'cells' anahtarı eksik"

def t5_cell_count():
    """Hücre sayısı (7 code cell + metadata)"""
    with open('notebooks/06_tradingview_integration.ipynb', 'r') as f:
        nb = json.load(f)
    cells = nb['cells']
    code_cells = [c for c in cells if c['cell_type'] == 'code']
    assert len(code_cells) >= 7, f"Kod hücre sayısı {len(code_cells)}, 7+ olmalı"
    print(f"    Toplam hücre: {len(cells)}, Kod hücreleri: {len(code_cells)}")

def t5_keywords():
    """Anahtar kelimeler mevcut mu?"""
    with open('notebooks/06_tradingview_integration.ipynb', 'r') as f:
        content = f.read()
    keywords = ['tradingview_ta', 'TA_Handler', 'fetch_tradingview_indicators',
                'input_size=5', 'prepare_tradingview_features', 'create_sequences_with_indicators',
                'count_parameters']
    found = []
    for kw in keywords:
        if kw in content:
            found.append(kw)
    assert len(found) >= 5, f"Sadece {len(found)}/{len(keywords)} anahtar kelime bulundu: {found}"
    print(f"    {len(found)}/{len(keywords)} anahtar kelime bulundu")

def t5_notebook_metadata():
    """Notebook metadata kontrolü"""
    with open('notebooks/06_tradingview_integration.ipynb', 'r') as f:
        nb = json.load(f)
    assert 'metadata' in nb, "metadata eksik"
    # Kernel bilgisi
    metadata = nb['metadata']
    if 'kernelspec' in metadata:
        assert 'name' in metadata['kernelspec'], "kernelspec name eksik"

test("notebook — JSON geçerliliği", t5_json_valid)
test("notebook — 7+ hücre", t5_cell_count)
test("notebook — Anahtar kelimeler", t5_keywords)
test("notebook — Metadata kontrolü", t5_notebook_metadata)


# ============================================================
# TEST 6: task.md — Faz 8 [/] işareti
# ============================================================
print("\n--- TEST 6: task.md ---")

def t6_faz8_marker():
    """task.md'de Faz 8 tamamlandı işareti"""
    with open('task.md', 'r') as f:
        content = f.read()
    assert 'Faz 8' in content, "Faz 8 başlığı eksik"
    assert '- [x]' in content or 'tamamlandı' in content.lower(), "Faz 8 tamamlandı işareti eksik"
    assert 'TradingView' in content, "TradingView referansı eksik"
    print("    Faz 8 bölümü mevcut ve tamamlandı olarak işaretlenmiş.")

test("task.md — Faz 8 tamamlandı", t6_faz8_marker)


# ============================================================
# TEST 7: working/done_faz_8.md — Mevcut
# ============================================================
print("\n--- TEST 7: working/done_faz_8.md ---")

def t7_exists():
    """Dosya mevcut mu?"""
    assert os.path.exists('working/done_faz_8.md'), "done_faz_8.md dosyası eksik"
    with open('working/done_faz_8.md', 'r') as f:
        content = f.read()
    assert len(content) > 100, f"İçerik çok kısa: {len(content)} karakter"
    assert 'TradingView' in content, "TradingView referansı eksik"
    assert 'tradingview_features' in content, "tradingview_features referansı eksik"
    print(f"    Dosya mevcut ({len(content)} karakter), içerik yeterli.")

test("working/done_faz_8.md — Mevcut ve içerikli", t7_exists)


# ============================================================
# TEST 8: End-to-End Functional Test
# ============================================================
print("\n--- TEST 8: Fonksiyonel End-to-End Test ---")

def t8_pipeline():
    """Basit pipeline: scaler + sequence + model"""
    import numpy as np
    import pandas as pd
    from src.preprocessing import scale_multi_features, create_sequences_multi, prepare_tensors_multi
    from src.models import LSTMModel, get_model_param_count
    
    # Mock OHLCV verisi
    np.random.seed(42)
    n = 300
    raw_df = pd.DataFrame({
        'Open': np.random.uniform(100, 150, n),
        'High': np.random.uniform(100, 160, n),
        'Low': np.random.uniform(95, 150, n),
        'Close': np.random.uniform(100, 150, n),
        'Volume': np.random.uniform(1e6, 5e6, n),
        'RSI': np.random.uniform(20, 80, n),
        'MACD.macd': np.random.normal(0, 2, n),
        'SMA20': np.random.uniform(100, 150, n),
        'EMA20': np.random.uniform(100, 150, n),
        'Bollinger_Bands.upper': np.random.uniform(100, 170, n),
        'Bollinger_Bands.lower': np.random.uniform(90, 140, n),
        'Volume': np.random.uniform(1e6, 5e6, n),
    })
    
    # Multi-feature scaling
    columns = ['Close', 'RSI', 'MACD.macd', 'SMA20', 'Volume']
    scaled, scaler = scale_multi_features(raw_df, columns)
    assert scaled.shape == (n, len(columns)), f"scaled.shape={scaled.shape}"
    # Scaler'ın feature_range kontrolü (test verisi training range dışında olabilir)
    assert scaler.feature_range == (-1, 1), f"Scaler feature_range={scaler.feature_range}"
    
    # Sequence
    X, y = create_sequences_multi(scaled, lookback=20)
    assert X.shape[0] > 0, "X boş"
    assert X.shape[1] == 20, f"X seq_len={X.shape[1]}, 20 olmalı"
    assert X.shape[2] == 5, f"X n_features={X.shape[2]}, 5 olmalı"
    
    # Tensors
    (X_train, y_train), (X_test, y_test) = prepare_tensors_multi(X, y)
    assert X_train.shape[0] > 0, "X_train boş"
    assert X_test.shape[0] > 0, "X_test boş"
    
    # Model
    model = LSTMModel(input_size=5)
    params = model.count_parameters()
    assert params > 0, "Model parametresi 0"
    text = get_model_param_count(model, "TestLSTM")
    assert "parametre" in text.lower(), "Metin formatında 'parametre' eksik"
    
    print(f"    Pipeline tamamlandı: scaled={scaled.shape}, X={X.shape}, model_params={params:,}")

test("End-to-End Pipeline (mock data)", t8_pipeline)


# ============================================================
# SONUÇ ÖZETİ
# ============================================================
print("\n" + "=" * 70)
print("TEST SONUÇLARI ÖZETİ")
print("=" * 70)

passed = sum(1 for r in results if r['status'] == 'OK')
failed = sum(1 for r in results if r['status'] == 'FAIL')

for r in results:
    icon = "✅" if r['status'] == 'OK' else "❌"
    print(f"  {icon} {r['name']}")
    if r['status'] == 'FAIL':
        print(f"     → {r['message']}")

print(f"\n  Toplam: {len(results)} test, {passed} başarılı, {failed} başarısız")
print("=" * 70)

# Exit code
if failed > 0:
    print("⚠️  HATA: Bazı testler başarısız!")
    sys.exit(1)
else:
    print("🎉 Tüm testler başarılı!")
    sys.exit(0)
