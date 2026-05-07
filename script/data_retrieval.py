# download raw data
# → pair each pair
# → align trading dates
# → drop missing observations within each pair
import numpy as np
import pandas as pd
from pathlib import Path
import yfinance as yf

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"
OUTPUT_DIR = DATA_DIR/"yfinance_data"
pair1_y = 'KO'
pair1_x = 'PEP'
pair2_y = 'XOM'
pair2_x = 'CVX'

start_date = '2010-01-01'
end_date = '2026-01-01'

data = yf.download([pair1_y, pair1_x, pair2_y, pair2_x],
                   start=start_date, end=end_date,
                   auto_adjust=False)['Adj Close']

KO =  yf.download(pair1_y, start=start_date, end=end_date, auto_adjust=False)['Adj Close']
PEP = yf.download(pair1_x, start=start_date, end=end_date, auto_adjust=False)['Adj Close']
XOM = yf.download(pair2_y, start=start_date, end=end_date, auto_adjust=False)['Adj Close']
CVX = yf.download(pair2_x, start=start_date, end=end_date, auto_adjust=False)['Adj Close']

KO.to_csv(OUTPUT_DIR/"KO_raw.csv")
PEP.to_csv(OUTPUT_DIR/"PEP_raw.csv")
XOM.to_csv(OUTPUT_DIR/"XOM_raw.csv")
CVX.to_csv(OUTPUT_DIR/"CVX_raw.csv")

#pair and align the dates and drop missing observations
KO_PEP = pd.concat([KO, PEP], axis=1)
KO_PEP.columns = ['KO', 'PEP']

XOM_CVX = pd.concat([XOM, CVX], axis=1)
XOM_CVX.columns = ['XOM', 'CVX']

KO_PEP = KO_PEP.dropna()
XOM_CVX = XOM_CVX.dropna()

KO_PEP.to_csv(OUTPUT_DIR/"KO_PEP.csv")
XOM_CVX.to_csv(OUTPUT_DIR/"XOM_CVX.csv")