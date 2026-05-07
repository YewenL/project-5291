import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import skew, kurtosis

START = "2015-01-01"
END   = "2026-01-01"

# =========================
# 1) 读取 + 清理（删除包含 Dividend 的“文本行”）
# =========================
def read_clean_yahoo_csv(path, ticker_name):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"]) 
    df = df.set_index("Date")
    # 只保留 Adj Close
    df = df[["Date", "Adj Close"]].rename(columns={"Adj Close": ticker_name})
    df = df.dropna()

    df = df.set_index("Date")
    return df

KO  = read_clean_yahoo_csv("KO_clean.csv",  "KO")
PEP = read_clean_yahoo_csv("PEP_clean.csv", "PEP")
XOM = read_clean_yahoo_csv("XOM_clean.csv", "XOM")
CVX = read_clean_yahoo_csv("CVX_clean.csv", "CVX")

# # =========================
# # 2) Table 1: 每个 ticker 的 daily log return summary
# # =========================
# def log_returns(price_df, col):
#     r = np.log(price_df[col]).diff()
#     return r.dropna()

# rets = {
#     "KO":  log_returns(KO, "KO"),
#     "PEP": log_returns(PEP, "PEP"),
#     "XOM": log_returns(XOM, "XOM"),
#     "CVX": log_returns(CVX, "CVX"),
# }

# table1 = pd.DataFrame(index=["KO","PEP","XOM","CVX"], columns=["Mean","Std","Skew","Kurt","Min","Max"], dtype=float)

# for tkr, r in rets.items():
#     table1.loc[tkr, "Mean"] = r.mean()
#     table1.loc[tkr, "Std"]  = r.std()
#     table1.loc[tkr, "Skew"] = skew(r, bias=False)
#     # kurtosis: Fisher (excess) kurtosis，和很多课程/论文一致；若你要“普通峰度”，可设 fisher=False
#     table1.loc[tkr, "Kurt"] = kurtosis(r, fisher=True, bias=False)
#     table1.loc[tkr, "Min"]  = r.min()
#     table1.loc[tkr, "Max"]  = r.max()

# table1 = table1.round(6)
# print("\nTable 1: Daily log return summary")
# print(table1)

# # =========================
# # 3) Table 2: Pair-level diagnostics (static baseline)
# #    - 对齐每一对日期（inner join）
# #    - 静态 OLS: y = alpha + beta x  (用 log price)
# #    - spread: s = y - (alpha + beta x)
# #    - z-score: (s - mean(s)) / std(s)
# # =========================
# def pair_diagnostics(px_y, name_y, px_x, name_x):
#     # 对齐
#     pair = px_y[[name_y]].join(px_x[[name_x]], how="inner").dropna()

#     # log prices
#     y = np.log(pair[name_y])
#     x = np.log(pair[name_x])

#     # 对应的 log returns 用于 corr（同样对齐后再 diff）
#     ry = y.diff()
#     rx = x.diff()
#     rr = pd.concat([ry, rx], axis=1).dropna()
#     corr = rr.iloc[:,0].corr(rr.iloc[:,1])

#     # 静态 OLS hedge ratio
#     X = sm.add_constant(x)
#     res = sm.OLS(y, X).fit()
#     alpha = res.params["const"]
#     beta  = res.params[name_x]

#     # static spread + zscore
#     spread = y - (alpha + beta * x)
#     spread_std = spread.std()
#     z = (spread - spread.mean()) / spread_std
#     pct_tail = (np.abs(z) > 2).mean() * 100

#     return corr, beta, spread_std, pct_tail

# pairs = [
#     ("KO-PEP",  KO,  "KO",  PEP, "PEP"),
#     ("XOM-CVX", XOM, "XOM", CVX, "CVX"),
# ]

# table2 = pd.DataFrame(index=[p[0] for p in pairs],
#                       columns=["Corr(r^X,r^Y)", "β̂", "Std(s_static)", "% |z| > 2", "Notes"],
#                       dtype=object)

# for pair_name, ydf, yname, xdf, xname in pairs:
#     corr, beta, sstd, pct = pair_diagnostics(ydf, yname, xdf, xname)
#     table2.loc[pair_name, "Corr(r^X,r^Y)"] = round(corr, 6)
#     table2.loc[pair_name, "β̂"] = round(beta, 6)
#     table2.loc[pair_name, "Std(s_static)"] = round(sstd, 6)
#     table2.loc[pair_name, "% |z| > 2"] = round(pct, 3)
#     table2.loc[pair_name, "Notes"] = ""  # 你也可以写 "stable" / "more regime-sensitive" 等

# print("\nTable 2: Pair-level diagnostics (static baseline)")
# print(table2)

# # =========================
# # 4) (可选) 导出 CSV，方便放进报告/LaTeX
# # =========================
# table1.to_csv("table1_log_return_summary.csv")
# table2.to_csv("table2_pair_level_diagnostics.csv")
# print("\nSaved: table1_log_return_summary.csv and table2_pair_level_diagnostics.csv")


import matplotlib.pyplot as plt

# =========================
# 5) Figures 1–4
# =========================

WINDOW = 252  # change to 120 if you want

# --- pair alignments (use your already-loaded KO/PEP/XOM/CVX) ---
ko_pep = KO[["KO"]].join(PEP[["PEP"]], how="inner").dropna()
xom_cvx = XOM[["XOM"]].join(CVX[["CVX"]], how="inner").dropna()

log_kp = np.log(ko_pep)
log_xc = np.log(xom_cvx)

# =========================
# Figure 1 — Log price series (KO vs PEP)
# =========================
plt.figure(figsize=(11, 5))
plt.plot(log_kp.index, log_kp["KO"], label="log(KO)")
plt.plot(log_kp.index, log_kp["PEP"], label="log(PEP)")
plt.title("Figure 1 — Log Price Series: KO vs PEP")
plt.xlabel("Date")
plt.ylabel("Log Price")
plt.legend()
plt.tight_layout()
plt.show()

# =========================
# Figure 2 — Log price series (XOM vs CVX)
# =========================
plt.figure(figsize=(11, 5))
plt.plot(log_xc.index, log_xc["XOM"], label="log(XOM)")
plt.plot(log_xc.index, log_xc["CVX"], label="log(CVX)")
plt.title("Figure 2 — Log Price Series: XOM vs CVX")
plt.xlabel("Date")
plt.ylabel("Log Price")
plt.legend()
plt.tight_layout()
plt.show()

# =========================
# Figure 3 — Static spread & rolling z-score (KO-PEP)
# s_static = y - (alpha_hat + beta_hat x), with y=log(KO), x=log(PEP)
# z_t uses rolling mean/std over WINDOW
# =========================
y = log_kp["KO"]
x = log_kp["PEP"]

X = sm.add_constant(x)
res = sm.OLS(y, X).fit()
alpha_hat = res.params["const"]
beta_hat  = res.params["PEP"]

spread = y - (alpha_hat + beta_hat * x)
mu_roll = spread.rolling(WINDOW).mean()
sd_roll = spread.rolling(WINDOW).std()
z_roll = (spread - mu_roll) / sd_roll

fig, ax1 = plt.subplots(figsize=(12, 6))

# ---- Spread（左轴）----
ax1.plot(spread.index, spread,
         color="navy",
         linewidth=1.2,
         label="Static Spread (KO-PEP)")

ax1.set_xlabel("Date")
ax1.set_ylabel("Spread", color="navy")
ax1.tick_params(axis="y", labelcolor="navy")

# ---- Z-score（右轴）----
ax2 = ax1.twinx()
ax2.plot(z_roll.index, z_roll,
         color="red",
         linestyle="--",
         linewidth=1.2,
         label=f"Rolling Z-score (window={WINDOW})")

ax2.axhline(0, color="black", linewidth=1)
ax2.axhline(2, color="gray", linestyle=":")
ax2.axhline(-2, color="gray", linestyle=":")

ax2.set_ylabel("Z-score", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# ---- Legend 合并 ----
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title(f"Figure 3 — Static Spread & Rolling Z-score (KO-PEP), window={WINDOW}")
plt.tight_layout()
plt.show()


# =========================
# Figure 4 — Rolling hedge ratio β_OLS(t) for KO-PEP and XOM-CVX (one plot)
# Rolling OLS: y = alpha + beta x, beta varies over time
# =========================
def rolling_beta(y, x, window):
    betas = pd.Series(index=y.index, dtype=float)
    for i in range(window - 1, len(y)):
        y_w = y.iloc[i - window + 1 : i + 1]
        x_w = x.iloc[i - window + 1 : i + 1]
        Xw = sm.add_constant(x_w)
        fit = sm.OLS(y_w, Xw).fit()
        betas.iloc[i] = fit.params[x.name]
    return betas

beta_kp = rolling_beta(log_kp["KO"], log_kp["PEP"], WINDOW)
beta_xc = rolling_beta(log_xc["XOM"], log_xc["CVX"], WINDOW)

plt.figure(figsize=(12, 5))
plt.plot(beta_kp.index, beta_kp, label=f"β_OLS(t): KO~PEP (window={WINDOW})")
plt.plot(beta_xc.index, beta_xc, label=f"β_OLS(t): XOM~CVX (window={WINDOW})")
plt.title("Figure 4 — Rolling Hedge Ratio β(t) (Rolling OLS)")
plt.xlabel("Date")
plt.ylabel("β(t)")
plt.legend()
plt.tight_layout()
plt.show()


# Figure 5
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ADF_WINDOW = 252   # 也可以设成 120 或 252

# =========================
# Rolling ADF p-value on spread
# =========================
adf_p = pd.Series(index=spread.index, dtype=float)

# ADF 对窗口长度比较敏感，窗口太短会不稳定；252一般比较稳
for i in range(ADF_WINDOW - 1, len(spread)):
    s_w = spread.iloc[i - ADF_WINDOW + 1 : i + 1].dropna()
    if len(s_w) < ADF_WINDOW:
        continue
    # ADF 回归项: constant only ('c')；滞后让 AIC 自动选
    try:
        adf_p.iloc[i] = adfuller(s_w, regression="c", autolag="AIC")[1]
    except Exception:
        adf_p.iloc[i] = np.nan

# 对齐：z_roll 本身前 WINDOW-1 会是 NaN；ADF 也一样
plot_df = pd.DataFrame({
    "z": z_roll,
    "pval": adf_p
}).dropna()

# =========================
# Figure 5 — Time vs z-score, colored by rolling ADF p-value
# =========================
plt.figure(figsize=(12, 5))

# 把时间转成数值轴（便于 scatter）
x_num = plot_df.index.map(pd.Timestamp.toordinal)

sc = plt.scatter(
    x_num,
    plot_df["z"].values,
    c=plot_df["pval"].values,
    s=12,
    alpha=0.85
)

# x 轴显示为日期刻度（选一些点作为 tick）
tick_locs = np.linspace(x_num.min(), x_num.max(), 8).astype(int)
tick_labels = [pd.Timestamp.fromordinal(int(v)).strftime("%Y-%m") for v in tick_locs]
plt.xticks(tick_locs, tick_labels, rotation=45)

plt.axhline(0, color="black", linewidth=1)
plt.axhline(2, color="gray", linestyle=":")
plt.axhline(-2, color="gray", linestyle=":")

cbar = plt.colorbar(sc)
cbar.set_label("Rolling ADF p-value (spread)")

plt.title(f"Figure 5 — Time vs Z-score (KO-PEP), colored by rolling ADF p-value (window={ADF_WINDOW})")
plt.xlabel("Time")
plt.ylabel("Rolling Z-score")
plt.tight_layout()
plt.show()