"""
src/evaluate.py — Model değerlendirme, tahmin görselleştirme ve loss çizimi.

Metrikler:
  - MSE: Ortalama Kare Hata (büyük hataları cezalandırır)
  - RMSE: Karekök MSE (dolar cinsinden hata)

Not: scaler.inverse_transform ile ölçeklenmiş veriyi orijinal fiyata geri çevirir.
"""

import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


def evaluate_model(
    model: nn.Module,
    X_test: torch.Tensor,
    y_test: torch.Tensor,
    scaler=None,
    device: str = "cpu",
) -> tuple[np.ndarray, np.ndarray, float, float]:
    """
    Modeli test verisinde değerlendirir.

    Args:
        model: Eğitimli nn.Module
        X_test: (batch, seq_len, input_size) test verisi
        y_test: (batch, 1) test hedefleri
        scaler: Opsiyonel MinMaxScaler — tahminleri orijinal fiyata çevirir
        device: "cpu" veya "cuda"

    Returns:
        (preds, actuals, mse, rmse)
        preds/actuals: Orijinal fiyat skalasında numpy array
    """
    model.eval()
    X_test, y_test = X_test.to(device), y_test.to(device)

    with torch.no_grad():
        predictions = model(X_test)

    # CPU'ya al ve numpy'e çevir
    preds = predictions.cpu().numpy()
    actuals = y_test.cpu().numpy()

    # Eğer scaler varsa, orijinal fiyata geri çevir
    if scaler is not None:
        preds = scaler.inverse_transform(preds)
        actuals = scaler.inverse_transform(actuals)

    # Metrikler
    mse = mean_squared_error(actuals, preds)
    rmse = np.sqrt(mse)

    print(f"📊 Model Değerlendirme:")
    print(f"   MSE : {mse:.4f}")
    print(f"   RMSE: {rmse:.4f} $")

    return preds, actuals, mse, rmse


def plot_predictions(
    actuals: np.ndarray,
    preds: np.ndarray,
    title: str = "Gerçek vs Tahmin",
    save_path: str | None = None,
) -> None:
    """Gerçek fiyatlar ile tahminleri karşılaştırmalı gösterir."""
    plt.figure(figsize=(14, 5))
    plt.plot(
        actuals, label="Gerçek Fiyat", linewidth=1.5, alpha=0.8,
    )
    plt.plot(
        preds, label="Tahmin", linewidth=1.5, alpha=0.8,
    )
    plt.title(title)
    plt.xlabel("Gün")
    plt.ylabel("Fiyat ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()


def plot_loss(
    loss_history: list[float],
    title: str = "Eğitim Kaybı",
    save_path: str | None = None,
) -> None:
    """
    Loss eğrisini çizer — modelin öğrenip öğrenmediğini gösterir.

    - 📉 Düzenli düşüyor → Model öğreniyor ✅
    - 📈 Yükseliyor → Learning rate çok yüksek, patlıyor
    - ➡️ Düzleşiyor → Model doyuma ulaştı, daha fazla epoch anlamsız
    - 📊 Train düşer test yükselir → Overfitting (ezberleme) ⚠️
    """
    plt.figure(figsize=(10, 4))
    plt.plot(loss_history, linewidth=1)
    plt.title(title)
    plt.xlabel("Epoch")
    plt.ylabel("MSE Loss")
    plt.grid(True, alpha=0.3)
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.show()
