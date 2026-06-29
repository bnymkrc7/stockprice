# Stock Price Prediction with PyTorch (LSTM & GRU)

This project implements stock price prediction using **Amazon (AMZN)** historical data. It compares **LSTM** (Long Short-Term Memory) and **GRU** (Gated Recurrent Unit) neural networks for time series forecasting, focusing on avoiding data leakage and ensuring reproducible results.

---

## 🎯 Project Goal

Predict the future price of Amazon (AMZN) stocks using deep learning models (LSTM and GRU). The project demonstrates:
- Data collection and preprocessing (2015-2025)
- Time series transformation (sliding window)
- Model training with proper train/test split
- Model comparison and hyperparameter optimization suggestions

---

## 🛠️ Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Steps

1. **Clone the repository** (if applicable)
```bash
cd /home/zorildiz/projeler/bunyamin/stock-price-prediction
```

2. **Activate virtual environment**
```bash
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Verify installation**
```bash
python -c "import torch; print(torch.__version__)"
python -c "import pandas; print(pandas.__version__)"
```

---

## 📁 Project Structure

```
stock-price-prediction/
├── data/
│   ├── raw/                  # Raw CSV data (AMZN_2015-2025.csv)
│   └── processed/            # Processed tensors (scaler.pkl, amzn_processed.pt)
├── notebooks/                # Jupyter notebooks (01→05 sequence)
│   ├── 01_veri_kesfi.ipynb   # EDA and data exploration
│   ├── 02_veri_hazirlama.ipynb   # Data preprocessing
│   ├── 03_model_lstm.ipynb   # LSTM model training
│   ├── 04_model_gru.ipynb    # GRU model training
│   └── 05_karsilastirma.ipynb    # Model comparison
├── src/                      # Python modules
│   ├── data_loader.py        # Data download (yfinance)
│   ├── preprocessing.py      # MinMaxScaler, create_sequences, prepare_tensors
│   ├── models.py             # LSTMModel and GRUModel classes
│   ├── train.py              # Training loop function
│   └── evaluate.py           # Evaluation and plotting functions
├── outputs/
│   ├── models/               # Saved model checkpoints (.pth files)
│   └── figures/              # Generated plots (.png files)
├── .venv/                    # Virtual environment
├── requirements.txt          # Python dependencies
├── README.md                 # Turkish documentation
└── README_eng.md             # English documentation (this file)
```

---

## 🚀 How to Run

### Sequential Execution (Recommended)

Run notebooks in order:

1. **Data Collection & EDA**
```bash
cd notebooks/01_veri_kesfi.ipynb
jupyter nbconvert --to notebook --execute --inplace 01_veri_kesfi.ipynb
```

2. **Data Preprocessing**
```bash
cd notebooks/02_veri_hazirlama.ipynb
jupyter nbconvert --to notebook --execute --inplace 02_veri_hazirlama.ipynb
```

3. **LSTM Training**
```bash
cd notebooks/03_model_lstm.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_model_lstm.ipynb
```

4. **GRU Training**
```bash
cd notebooks/04_model_gru.ipynb
jupyter nbconvert --to notebook --execute --inplace 04_model_gru.ipynb
```

5. **Model Comparison**
```bash
cd notebooks/05_karsilastirma.ipynb
jupyter nbconvert --to notebook --execute --inplace 05_karsilastirma.ipynb
```

### Quick Execution (All Notebooks)

```bash
for nb in notebooks/0*.ipynb; do
    jupyter nbconvert --to notebook --execute --inplace "$nb"
done
```

---

## 📊 Results

### Data Summary
- **Dataset:** AMZN (Amazon.com, Inc.)
- **Period:** 2015-01-01 to 2025-01-01
- **Total Rows:** 2,516
- **Price Range:** $14.35 - $232.93 (raw)
- **Scaled Range:** -1.00 to 1.54 (normalized)
- **Train Set:** 1,996 samples (80% of data)
- **Test Set:** 500 samples (20% of data)
- **Lookback Window:** 20 days
- **Data Leakage:** Prevented (Scaler fitted only on training data)

### Model Architecture

#### LSTM Model
- **Input Size:** 1 (Close price only)
- **Hidden Size:** 50
- **Number of Layers:** 2
- **Dropout:** 0.2
- **Parameters:** 31,051
- **Training:** 100 epochs, lr=0.001, Adam optimizer, MSELoss

#### GRU Model
- **Input Size:** 1 (Close price only)
- **Hidden Size:** 50
- **Number of Layers:** 2
- **Dropout:** 0.2
- **Parameters:** 23,301
- **Training:** 100 epochs, lr=0.001, Adam optimizer, MSELoss

### Comparison Results

| Metric | LSTM | GRU | Winner |
|--------|------|-----|--------|
| **MSE (Test)** | [Value] | [Value] | [Lower is better] |
| **RMSE ($ Test)** | [Value] | [Value] | [Lower is better] |
| **Training Time (s)** | [Value] | [Value] | [Lower is better] |
| **Parameters** | 31,051 | 23,301 | GRU (lighter) |

*Note: Exact values are displayed in the comparison notebook output.*

### Visualizations
- `lstm_predictions.png` — LSTM predictions vs actual
- `lstm_loss.png` — LSTM training loss curve
- `gru_predictions.png` — GRU predictions vs actual
- `gru_loss.png` — GRU training loss curve
- `comparison_full.png` — Full comparison plot (all test set)
- `comparison_zoomed.png` — Last 50 days zoomed view

---

## 🧠 Key Takeaways

### Which Model is Better?

Both models show similar performance, but:
- **GRU** has **25% fewer parameters** (23,301 vs 31,051), making it lighter and faster
- **GRU** is less prone to vanishing gradient problems compared to LSTM
- For this task (AMZN stock prediction), **GRU is recommended** for efficiency

### Why This Matters

1. **Data Leakage Prevention** — Critical for reliable evaluation
2. **Model Efficiency** — Fewer parameters = faster inference, less memory
3. **Reproducibility** — All steps documented and sequential

---

## 🔄 Hyperparameter Optimization Suggestions

If performance is unsatisfactory, try these:

| Parameter | Default | Suggested Tests | Reason |
|-----------|---------|-----------------|--------|
| **lookback** | 20 | 10, 30, 50 | Short/long-term trends |
| **hidden_size** | 50 | 32, 64, 128 | Model capacity |
| **num_layers** | 2 | 1, 3 | Network depth |
| **dropout** | 0.2 | 0, 0.3, 0.5 | Overfitting control |
| **learning_rate** | 0.001 | 0.01, 0.0001 | Learning speed |
| **epochs** | 100 | 50, 200 | Training duration |

### Recommended First Experiment
- **hidden_size=64, num_layers=1, dropout=0.1**
- This combination may yield better results with GRU's fewer parameters

---

## 🔗 TradingView Integration (Advanced) - Completed!

The TradingView technical indicators integration has been successfully implemented in the `feat/tradingview-integration` branch. You can check `notebooks/06_tradingview_integration.ipynb` to see the multi-dimensional prediction models using:
1. Close price
2. RSI
3. MACD
4. SMA20
5. Volume

## 🐳 Future Enhancements

1. **Hyperparameter Optimization:** Additional testing with lookback window, hidden size, and learning rate.
2. **Dockerization:** Containerize the entire project to ensure consistent execution across any system.
3. **WebUI:** Convert the prediction backend into an interactive web interface (dashboard) for live stock tracking and visualization.

---

## ⚠️ Common Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| **Overfitting** | Training loss decreases, test loss high | Add dropout, reduce epochs, simplify model |
| **Underfitting** | Loss never decreases | Increase learning rate, add epochs, expand model |
| **Vanishing Gradient** | Loss decreases very slowly | Try GRU (less affected than LSTM) |
| **Data Leakage** | Test results too good | Ensure scaler is fitted only on training data |
| **Wrong Window** | Model predicts same value always | Check lookback parameter, too short/small |

---

## 📚 References

1. **yfinance:** https://github.com/ranaroussi/yfinance
2. **PyTorch LSTM/GRU:** https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
3. **TradingView Screener:** https://github.com/shner-elmo/tradingview-screener
4. **TradingView TA:** https://github.com/analyzerrest/python-tradingview-ta
5. **Reference Article:** Stock Price Prediction with PyTorch (Medium)
6. **MinMaxScaler:** https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html

---

## ⏱️ Estimated Timeline

| Phase | What You'll Learn | Time |
|-------|-------------------|------|
| **0** | Environment setup, TradingView auth | 30 min |
| **1** | yfinance, Pandas exploration, visualization | 2-3 hours |
| **2** | MinMaxScaler, sliding window, tensors | 2 hours |
| **3** | PyTorch nn.Module, LSTM/GRU theory | 2-3 hours |
| **4** | First model training (LSTM) 🎉 | 2-3 hours |
| **5** | Second model (GRU) | 1-2 hours |
| **6** | Comparison, hyperparameters, TradingView | 2-3 hours |
| **7** | README, .gitignore, final verification | 1 hour |
| **Total** | | **~12-17 hours** |

---

## 📜 License

This project is for educational purposes.

---

## 🤝 Contact

For questions or contributions, please refer to the project repository.

---

**Note:** This README is the English version. For Turkish documentation, see `README.md`.