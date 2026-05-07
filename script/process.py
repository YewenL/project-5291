import pandas as pd
from pathlib import Path
def clean_yahoo_csv(path):
    df = pd.read_csv(path)

    # 删除包含 "Dividend" 字样的行
    df = df[~df.astype(str).apply(lambda row: row.str.contains("Dividend").any(), axis=1)]

    # 转换日期
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # # 删除日期无法解析的行（保险）
    # df = df.dropna(subset=['Date'])

    return df

# 清洗四个文件
ko = clean_yahoo_csv("KO.csv")
pep = clean_yahoo_csv("PEP.csv")
xom = clean_yahoo_csv("XOM.csv")
cvx = clean_yahoo_csv("CVX.csv")

print("Cleaned successfully.")
ko.to_csv("KO_clean.csv", index=False)
pep.to_csv("PEP_clean.csv", index=False)
xom.to_csv("XOM_clean.csv", index=False)
cvx.to_csv("CVX_clean.csv", index=False)

print("Cleaned files saved.")
# BASE_DIR = Path(__file__).resolve().parent.parent
# print("Base directory:", BASE_DIR)
# DATA_DIR = BASE_DIR / "Data"
# OUTPUT_DIR = BASE_DIR / "Processed_Data"

# def read_clean_yahoo_csv(path, ticker_name):
#     df = pd.read_csv(path)
#     df["Date"] = pd.to_datetime(df["Date"]) 
#     # df = df.set_index("Date")
#     # 只保留 Adj Close
#     df = df[["Date", "Adj Close"]].rename(columns={"Adj Close": ticker_name})
#     df = df.dropna()

#     df = df.set_index("Date")
#     return df

# KO  = read_clean_yahoo_csv(DATA_DIR /"KO_clean.csv",  "KO")
# PEP = read_clean_yahoo_csv(DATA_DIR /"PEP_clean.csv", "PEP")
# XOM = read_clean_yahoo_csv(DATA_DIR /"XOM_clean.csv", "XOM")
# CVX = read_clean_yahoo_csv(DATA_DIR /"CVX_clean.csv", "CVX")
# KO.to_csv(DATA_DIR /"KO_cleaned_adjclose.csv", index=False)
# PEP.to_csv(DATA_DIR /"PEP_cleaned_adjclose.csv", index=False)
# XOM.to_csv(DATA_DIR /"XOM_cleaned_adjclose.csv", index=False)
# CVX.to_csv(DATA_DIR /"CVX_cleaned_adjclose.csv", index=False)

# print("Saved cleaned files to:", OUTPUT_DIR)