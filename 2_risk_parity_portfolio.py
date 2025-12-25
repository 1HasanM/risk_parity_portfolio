import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["AKBNK.IS", "SISE.IS", "THYAO.IS", "BIMAS.IS", "ASELS.IS"]
data = yf.download(tickers, start="2024-12-25", end="2025-12-25")["Close"]

# Log getiriler
returns = np.log(data / data.shift(1)).dropna()

# =========================
# RISK PARITY
# =========================

# Yıllık volatilite
volatility = returns.std() * np.sqrt(252)

# Ters volatilite ile ağırlıklar
inv_vol = 1 / volatility
rp_weights = inv_vol / inv_vol.sum()

# Risk Parity portföy getirisi (günlük)
rp_portfolio_returns = returns.dot(rp_weights)

# Risk Parity yıllık getiri & volatilite
rp_annual_return = rp_portfolio_returns.mean() * 252
rp_annual_vol = rp_portfolio_returns.std() * np.sqrt(252)

# =========================
# EŞİT AĞIRLIKLI PORTFÖY
# =========================

equal_weights = np.array([1 / len(tickers)] * len(tickers))

eq_portfolio_returns = returns.dot(equal_weights)

eq_annual_return = eq_portfolio_returns.mean() * 252
eq_annual_vol = eq_portfolio_returns.std() * np.sqrt(252)

# =========================
# TABLOLAR
# =========================

weights_df = pd.DataFrame({
    "Ticker": tickers,
    "Annual Volatility": volatility.values,
    "Risk Parity Weight": rp_weights.values,
    "Equal Weight": equal_weights
})

portfolio_metrics = pd.DataFrame({
    "Portfolio": ["Risk Parity", "Equal Weight"],
    "Annual Return": [rp_annual_return, eq_annual_return],
    "Annual Volatility": [rp_annual_vol, eq_annual_vol]
})

# =========================
# GRAFİK – RISK PARITY AĞIRLIKLARI
# =========================

plt.bar(weights_df["Ticker"], weights_df["Risk Parity Weight"])
plt.title("Risk Parity Portföy Ağırlıkları")
plt.ylabel("Portföy Ağırlığı")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.show()

# =========================
# ÇIKTILAR
# =========================

print("📌 Portföy Ağırlıkları")
print(weights_df)

print("\n📌 Portföy Performans Karşılaştırması")
print(portfolio_metrics)
