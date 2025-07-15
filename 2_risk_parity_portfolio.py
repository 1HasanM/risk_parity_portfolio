import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AKBNK.IS", "SISE.IS", "THYAO.IS", "BIMAS.IS", "ASELS.IS"]
data = yf.download(tickers, start="2024-07-01", end="2025-07-14")["Close"]

# Log getiri
returns = np.log(data / data.shift(1)).dropna()

# Yıllık volatilite
volatility = returns.std() * np.sqrt(252)

# Ters volatilite ile ağırlıklar
inv_vol = 1 / volatility
weights = inv_vol / inv_vol.sum()

# Portföy tablosu
df = pd.DataFrame({
    "Ticker": tickers,
    "Annual Volatility": volatility.values,
    "Risk Parity Weight": weights.values
})

# Grafik
plt.bar(df["Ticker"], df["Risk Parity Weight"], color="steelblue")
plt.title("Risk Parity Portföy Ağırlıkları")
plt.ylabel("Portföy Ağırlığı")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

print(df)
