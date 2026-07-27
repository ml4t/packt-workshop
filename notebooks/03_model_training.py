# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3 (ml4t-packt-workshop)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 03 · Training and evaluating the model
#
# **Supports agenda block 6** ("Training & Evaluating the Model"). LightGBM
# with walk-forward cross-validation — never a random shuffle-split, which
# would train on the future and validate on the past — and the
# **Information Coefficient (IC)**, HAC-corrected for the autocorrelation
# that a 21-day-overlapping label mechanically introduces, as the metric
# that actually says whether the model found anything.

# %%
import lightgbm as lgb
import pandas as pd
from ml4t.diagnostic.metrics import compute_ic_hac_stats, cross_sectional_ic_series
from ml4t.diagnostic.splitters import WalkForwardCV

DATA_DIR = "../data"
LABEL_HORIZON = 21  # trading days — must match the label built in 02_features_labels

dataset = pd.read_parquet(f"{DATA_DIR}/model_dataset.parquet")
feature_cols = [
    "mom_21d",
    "mom_63d",
    "mom_126d",
    "mom_252d",
    "vol_21d",
    "vol_63d",
    "rsi_14",
    "dollar_vol_rank",
]

dataset["timestamp"] = pd.to_datetime(dataset["timestamp"]).dt.tz_localize("UTC")
dataset = dataset.sort_values("timestamp").set_index("timestamp")
X, y = dataset[feature_cols], dataset["fwd_ret_21d"]

# %% [markdown]
# ## Walk-forward cross-validation
#
# `label_horizon=21` is the load-bearing argument here — it tells the
# splitter that a training row's label is only *fully known* 21 trading
# days after its feature date, so it purges the training rows whose label
# window would otherwise overlap the validation period. Skip this argument
# and the "CV" silently leaks the validation period's own future into
# training, which is exactly the kind of mistake a coding agent will
# reproduce faithfully if you don't specify it in the brief.

# %%
cv = WalkForwardCV(
    n_splits=16,
    test_size="1Y",
    label_horizon=LABEL_HORIZON,
    expanding=True,
    consecutive=True,
)

lgb_params = dict(
    objective="regression",
    n_estimators=200,
    learning_rate=0.05,
    num_leaves=15,
    min_child_samples=200,
    verbosity=-1,
)

fold_predictions = []
for fold, (train_idx, test_idx) in enumerate(cv.split(X)):
    X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
    X_test = X.iloc[test_idx]

    model = lgb.LGBMRegressor(**lgb_params)
    model.fit(X_train, y_train)

    preds = dataset.iloc[test_idx][["symbol", "fwd_ret_21d"]].copy()
    preds["prediction"] = model.predict(X_test)
    preds["fold"] = fold
    fold_predictions.append(preds)

    print(
        f"fold {fold}: train {X_train.index.min().date()}..{X_train.index.max().date()} "
        f"({len(X_train):,} rows) -> test {X_test.index.min().date()}..{X_test.index.max().date()} "
        f"({len(X_test):,} rows)"
    )

# %% [markdown]
# ## The Information Coefficient
#
# Every prediction above came from a fold where the model never saw that
# period during training — this is out-of-sample by construction, not by
# promise. We pool all four test folds and compute the cross-sectional
# Spearman IC per date, then HAC-correct the resulting t-statistic.

# %%
oos = pd.concat(fold_predictions).reset_index().rename(columns={"index": "timestamp"})

ic_series = cross_sectional_ic_series(
    oos,
    oos,
    pred_col="prediction",
    ret_col="fwd_ret_21d",
    date_col="timestamp",
    entity_col="symbol",
    method="spearman",
)
print(ic_series.describe())

# %%
hac_stats = compute_ic_hac_stats(ic_series, ic_col="ic", label_horizon=LABEL_HORIZON)
print(hac_stats)

# %% [markdown]
# `hac_stats["mean_ic"]` is the honest headline number — not the naive
# t-statistic you'd get from treating each daily IC observation as
# independent. Because the label is a 21-day forward return, consecutive
# daily ICs share ~20 days of the same underlying return window and are
# mechanically autocorrelated; the naive t-stat overstates significance.
# `label_horizon=21` tells the HAC correction the minimum lag to account
# for, rather than relying on order selection alone.
#
# **Run this notebook and the two t-stats disagree with each other**: naive
# ≈ 2.18 (nominally "significant" at 5%), HAC ≈ 0.65 (nowhere close). That
# gap *is* the lesson, not a bug to fix — eight simple technical features
# on a monthly-rebalanced ETF panel do not reliably beat noise once the
# autocorrelation induced by the overlapping 21-day label is priced in.
# A model with an IC this weak has no business going anywhere near a
# backtest that claims a live edge; block 7 puts it through one anyway, on
# purpose, to show what "weak signal, meet real costs" actually looks like.

# %% [markdown]
# ## Feature importance
#
# Cheap to compute, easy to over-read. Treat this as "what the last fold's
# model leaned on," not as a causal or stable ranking across the full
# 18-year history — `13_model_analysis.py` in the full case study goes much
# further (SHAP, permutation importance, stability across folds) than this
# workshop has time for.

# %%
importance = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print(importance)

# %% [markdown]
# **Next:** `04_backtest.ipynb` — turn these predictions into positions and
# run a cost-aware backtest. Save the pooled out-of-sample predictions so
# the backtest notebook doesn't need to retrain anything.

# %%
oos.to_parquet(f"{DATA_DIR}/oos_predictions.parquet", index=False)
