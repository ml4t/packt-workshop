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
# # 02 · From market idea to alpha factor, and the labels that don't leak
#
# **Supports agenda blocks 3 and 5** ("The Modern Quant Stack" /
# "The Judgment You Don't Delegate"). We turn the raw OHLCV panel into a
# small, interpretable feature set and a forward-return label - then spend
# as much time checking that neither leaks information from the future as
# we spent building them. That check is the actual content of block 5: it's
# the discipline an agent won't apply for you unless you specify it.

# %%
import os
import subprocess
import sys
from pathlib import Path

if "COLAB_RELEASE_TAG" in os.environ:
    repo_dir = Path(os.environ.get("PACKT_WORKSHOP_DIR", "/content/packt-workshop"))
    if not repo_dir.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "https://github.com/ml4t/packt-workshop.git",
                repo_dir,
            ],
            check=True,
        )
    ready = repo_dir.parent / ".packt-workshop-ready"
    if not ready.exists():
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-q",
                "-r",
                repo_dir / "requirements-colab.txt",
            ],
            check=True,
        )
        ready.touch()
    os.chdir(repo_dir / "notebooks")

# %%
import numpy as np
import pandas as pd
from ml4t.engineer.features.momentum.rsi import rsi

DATA_DIR = "../data"

prices = pd.read_parquet(f"{DATA_DIR}/etf_universe.parquet")
prices["timestamp"] = pd.to_datetime(prices["timestamp"])
prices = prices.sort_values(["symbol", "timestamp"]).reset_index(drop=True)

eligibility = pd.read_csv(f"{DATA_DIR}/eligibility.csv")
eligible_pairs = set(zip(eligibility["symbol"], eligibility["eligible_year"], strict=True))

# %% [markdown]
# ## Point-in-time eligibility, applied
#
# We drop any (symbol, date) where that ETF wasn't yet eligible in that
# calendar year. This is the fix for the survivorship-style bug the
# `01_data` notebook flagged - without it, the 100-symbol universe is
# implicitly "the 100 winners as selected today," present on day one of a
# 2006 backtest where in reality most of them didn't exist yet.

# %%
prices["year"] = prices["timestamp"].dt.year
prices["eligible"] = [
    (sym, yr) in eligible_pairs for sym, yr in zip(prices["symbol"], prices["year"], strict=True)
]
print(f"{prices['eligible'].mean():.1%} of (symbol, day) rows are eligible")
prices = prices[prices["eligible"]].drop(columns=["eligible", "year"]).reset_index(drop=True)

# %% [markdown]
# ## Features
#
# Eight features across three families - momentum, volatility, and a
# mean-reversion oscillator (RSI). Each is computed **within symbol**
# (`groupby("symbol")`), using only information available up to and
# including the feature date. `ml4t.engineer` supplies RSI with Wilder's
# smoothing (the TA-Lib-compatible version, not a naive SMA-based one);
# momentum and volatility are direct enough to compute inline.

# %%
prices["ret_1d"] = prices.groupby("symbol")["close"].pct_change()


def add_features(g: pd.DataFrame) -> pd.DataFrame:
    g = g.copy()
    for h in (21, 63, 126, 252):
        g[f"mom_{h}d"] = g["close"].pct_change(h)
    for h in (21, 63):
        g[f"vol_{h}d"] = g["ret_1d"].rolling(h).std()
    g["rsi_14"] = rsi(g["close"].to_numpy(), period=14)
    g["dollar_vol_21d"] = (g["close"] * g["volume"]).rolling(21).mean()
    return g


features = prices.groupby("symbol", group_keys=False).apply(add_features, include_groups=False)
features["symbol"] = prices["symbol"].to_numpy()
features["timestamp"] = prices["timestamp"].to_numpy()

# Cross-sectional dollar-volume rank needs the whole universe on each date,
# not a per-symbol rolling window - a different axis from every feature above.
features["dollar_vol_rank"] = features.groupby("timestamp")["dollar_vol_21d"].rank(pct=True)

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
features[["timestamp", "symbol", *feature_cols]].dropna().describe()

# %% [markdown]
# ## Labels: forward returns, not a classification target in disguise
#
# The case study this workshop draws on uses **21-trading-day forward
# return** (`fwd_ret_21d`) as its primary label, with a 5-day variant. We
# use the same horizons here rather than inventing our own - matching the
# book's own choice keeps this notebook consistent with what the case study
# actually validated, not a workshop-only convention.
#
# `shift(-h)` looks *forward* - this line is the single most common source
# of look-ahead leakage in a labeling pipeline, so it deserves being named
# explicitly rather than buried in a helper function.


# %%
def add_labels(g: pd.DataFrame) -> pd.DataFrame:
    g = g.copy()
    g["fwd_ret_21d"] = g["close"].pct_change(21).shift(-21)
    g["fwd_ret_5d"] = g["close"].pct_change(5).shift(-5)
    return g


labels = prices.groupby("symbol", group_keys=False).apply(add_labels, include_groups=False)
labels["symbol"] = prices["symbol"].to_numpy()
labels["timestamp"] = prices["timestamp"].to_numpy()

# %% [markdown]
# ## Prove the label doesn't leak
#
# Don't take "shift(-21) is forward-looking" on faith - check it. For a
# handful of (symbol, date) pairs, `fwd_ret_21d` on day *t* must equal the
# realized return from day *t* to day *t+21*, using **only** rows that come
# strictly after *t* in the raw price series.

# %%
check_symbol, check_idx = "SPY", 500
spy = prices[prices["symbol"] == "SPY"].reset_index(drop=True)
spy_labels = labels[labels["symbol"] == "SPY"].reset_index(drop=True)

p0 = spy.loc[check_idx, "close"]
p21 = spy.loc[check_idx + 21, "close"]
manual_fwd_ret = p21 / p0 - 1
computed_fwd_ret = spy_labels.loc[check_idx, "fwd_ret_21d"]

print(f"manual:   {manual_fwd_ret:.6f}")
print(f"computed: {computed_fwd_ret:.6f}")
assert np.isclose(manual_fwd_ret, computed_fwd_ret), "label does not match manual forward return"
print("label matches a manual forward-return calculation - no off-by-one leak")

# %% [markdown]
# ## Assemble and save the model dataset
#
# One row per (timestamp, symbol) with features and both label horizons.
# Rows with any NaN feature (the first ~252 days per symbol, before the
# longest rolling window is full) or missing label (the last 21 days per
# symbol, where there's no future to look forward into) are dropped -
# **dropped, not filled** - filling them would itself be a leakage-adjacent
# choice that needs its own justification.

# %%
dataset = features.merge(labels, on=["timestamp", "symbol"], suffixes=("", "_dup"))
dataset = dataset[["timestamp", "symbol", *feature_cols, "fwd_ret_21d", "fwd_ret_5d"]]
dataset = dataset.dropna(subset=[*feature_cols, "fwd_ret_21d"]).reset_index(drop=True)

print(
    f"{len(dataset):,} rows, {dataset['symbol'].nunique()} symbols, "
    f"{dataset['timestamp'].min().date()} -> {dataset['timestamp'].max().date()}"
)
dataset.to_parquet(f"{DATA_DIR}/model_dataset.parquet", index=False)

# %% [markdown]
# **Next:** `03_model_training.ipynb` - walk-forward cross-validation,
# LightGBM, and the Information Coefficient as the metric that actually
# tells you whether any of this is worth trading.
