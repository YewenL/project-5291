# from pair data, get log price and log return
# drop missing observations
import numpy as np
import pandas as pd
from pathlib import Path
import yfinance as yf

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
INPUT_DIR = DATA_DIR / "yfinance_data"
OUTPUT_DIR = DATA_DIR / "log_price_log_return"
# pair1_y = 'KO'
# pair1_x = 'PEP'
# pair2_y = 'XOM'
# pair2_x = 'CVX'

KO_PEP  = pd.read_csv(INPUT_DIR/"KO_PEP.csv")
# PEP = pd.read_csv(DATA_DIR + "/PEP_clean.csv")
XOM_CVX = pd.read_csv(INPUT_DIR/"XOM_CVX.csv")
# CVX = pd.read_csv(DATA_DIR + "/CVX_clean.csv")
# Censor missing data
KO_PEP = KO_PEP.set_index("Date")
XOM_CVX = XOM_CVX.set_index("Date")

KO_log_prices = np.log(KO_PEP['KO'])
PEP_log_prices = np.log(KO_PEP['PEP'])
XOM_log_prices = np.log(XOM_CVX['XOM'])
CVX_log_prices = np.log(XOM_CVX['CVX'])

KO_log_returns = KO_log_prices.diff().dropna()
PEP_log_returns = PEP_log_prices.diff().dropna()
XOM_log_returns = XOM_log_prices.diff().dropna()
CVX_log_returns = CVX_log_prices.diff().dropna()

KO_log_prices.to_csv(OUTPUT_DIR/"KO_log_prices.csv")
PEP_log_prices.to_csv(OUTPUT_DIR/"PEP_log_prices.csv")
XOM_log_prices.to_csv(OUTPUT_DIR/"XOM_log_prices.csv")
CVX_log_prices.to_csv(OUTPUT_DIR/"CVX_log_prices.csv")
KO_log_returns.to_csv(OUTPUT_DIR/"KO_log_returns.csv")
PEP_log_returns.to_csv(OUTPUT_DIR/"PEP_log_returns.csv")
XOM_log_returns.to_csv(OUTPUT_DIR/"XOM_log_returns.csv")
CVX_log_returns.to_csv(OUTPUT_DIR/"CVX_log_returns.csv")