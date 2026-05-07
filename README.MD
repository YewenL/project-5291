Preliminary Models
→ Spread Construction Methods

Model 1: Static / Rolling OLS
Model 2: Kalman Filter

Then:
Strategy 1–4 Backtest

# S1 / S3
static OLS
fixed beta
# S2 / S4
Kalman filter
dynamic beta_t

Strategy	Spread Construction	Trading Rule	Purpose
S1	Static OLS residual	z-score only	Traditional baseline
S2	Kalman dynamic residual	z-score only	Test dynamic hedge ratio
S3	Static OLS residual	z-score + ML filter	Test ML timing
S4	Kalman dynamic residual	z-score + ML filter	Test combined improvement
