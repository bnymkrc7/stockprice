"""
src/models.py — PyTorch ile LSTM ve GRU model sınıfları.

Mimarisi:
  Input (batch, 20, 1)
    → LSTM/GRU(hidden=50, layers=2, dropout=0.2)
    → Linear(50 → 1)
    → Output (batch, 1)

batch_first=True: girdi (batch, seq, features) formatında olur (daha doğal).
out[:, -1, :]: son adımdaki çıktıyı alırız çünkü sadece 21. günü tahmin ediyoruz.
"""

import torch
import torch.nn as nn


class LSTMModel(nn.Module):
    """
    2 katmanlı LSTM modeli.

    Neden 2 katman? Daha fazla öğrenme kapasitesi.
    Neden dropout=0.2? Overfitting'i önlemek için (nöronların %20'sini rastgele kapatır).
    Neden hidden=50? 20 günlük girdi için yeterli kapasite.
    """

    def __init__(
        self,
        input_size: int = 1,
        hidden_size: int = 50,
        num_layers: int = 2,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout,
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x shape: (batch, seq_len, input_size)
        out shape: (batch, seq_len, hidden_size)

        Son adımdaki hidden state'den linear katmana geçiş yapılır.
        """
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


class GRUModel(nn.Module):
    """
    2 katmanlı GRU modeli — LSTM ile aynı parametrelerde.

    GRU, LSTM'in basitleştirilmiş hali (3 gate → 2 gate).
    Daha az parametre → daha hızlı eğitim, çoğu görevde LSTM'e yakın performans.
    """

    def __init__(
        self,
        input_size: int = 1,
        hidden_size: int = 50,
        num_layers: int = 2,
        dropout: float = 0.2,
    ):
        super().__init__()
        self.gru = nn.GRU(
            input_size, hidden_size, num_layers,
            batch_first=True, dropout=dropout,
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        x shape: (batch, seq_len, input_size)
        out shape: (batch, seq_len, hidden_size)

        Son adımdaki hidden state'den linear katmana geçiş yapılır.
        """
        out, _ = self.gru(x)
        return self.fc(out[:, -1, :])
