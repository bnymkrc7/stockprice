"""
src/train.py — Standart PyTorch eğitim döngüsü.

Adımlar:
  1. forward pass (tahmin yap)
  2. loss hesapla (tahmin ile gerçek arasındaki fark)
  3. backward pass (gradyan hesapla)
  4. optimizer.step() (ağırlıkları güncelle)
"""

import time

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset


def train_model(
    model: nn.Module,
    X_train: torch.Tensor,
    y_train: torch.Tensor,
    X_val: torch.Tensor | None = None,
    y_val: torch.Tensor | None = None,
    epochs: int = 100,
    lr: float = 0.001,
    batch_size: int = 64,
    device: str = "cpu",
    verbose: bool = True,
) -> tuple[list[float], float]:
    """
    PyTorch ile model eğitim döngüsü.

    Args:
        model: nn.Module (LSTMModel veya GRUModel)
        X_train: (batch, seq_len, input_size) formatında eğitim verisi
        y_train: (batch, 1) formatında eğitim hedefleri
        X_val: Opsiyonel validation verisi (overfitting tespiti)
        y_val: Opsiyonel validation hedefleri
        epochs: Eğitim periyodu sayısı
        lr: Adam optimizer learning rate
        batch_size: Mini-batch boyutu
        device: "cpu" veya "cuda"
        verbose: Epoch bilgisi yazdırma

    Returns:
        (loss_history, elapsed_seconds)
    """
    model = model.to(device)
    X_train, y_train = X_train.to(device), y_train.to(device)

    criterion = nn.MSELoss()
    # Adam: Adaptive learning rate, genelde SGD'den iyi çalışır
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    # Mini-batch eğitimi için DataLoader
    train_dataset = TensorDataset(X_train, y_train)
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
    )

    # Validation verisi varsa
    val_criterion = nn.MSELoss()
    loss_history = []
    val_history = []

    start_time = time.time()

    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0

        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)

            # Forward
            predictions = model(X_batch)
            loss = criterion(predictions, y_batch)

            # Backward
            optimizer.zero_grad()  # Önceki gradyanları sıfırla
            loss.backward()        # Gradyanları hesapla
            optimizer.step()       # Ağırlıkları güncelle

            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(train_loader)
        loss_history.append(avg_loss)

        # Validation (eğer verisi varsa)
        if X_val is not None and y_val is not None:
            model.eval()
            X_val, y_val = X_val.to(device), y_val.to(device)
            with torch.no_grad():
                val_preds = model(X_val)
                val_loss = val_criterion(val_preds, y_val).item()
            val_history.append(val_loss)

        if verbose and (epoch + 1) % 10 == 0:
            val_msg = f" Val Loss: {val_history[-1]:.6f}" if val_history else ""
            print(f"Epoch [{epoch+1}/{epochs}] Loss: {avg_loss:.6f}{val_msg}")

    elapsed = time.time() - start_time
    print(f"✅ Eğitim tamamlandı! Süre: {elapsed:.2f} sn")
    print(f"   Son Loss: {loss_history[-1]:.6f}")
    if val_history:
        print(f"   Son Val Loss: {val_history[-1]:.6f}")

    return loss_history, elapsed
