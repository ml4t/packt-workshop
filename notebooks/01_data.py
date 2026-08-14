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
# # 01 · The free 100-ETF universe
#
# **Block 2-3 of the workshop agenda** ("From Market Idea to Alpha Factor" /
# "The Modern Quant Stack") - everything downstream in this workshop runs on
# this dataset, so we start by loading it and confirming what it actually
# contains before trusting anything built on top of it.
#
# The data ships with this repo (`data/etf_universe.parquet`) so the session
# doesn't depend on live internet access. It's the same free, Yahoo-Finance
# -sourced universe used in the ETF case study in *Machine Learning for
# Trading, 3rd Edition* - 100 liquid ETFs, selected backward-looking on a
# $10M average-daily-volume threshold (see `data/README.md` for the point
# -in-time eligibility file and its caveats).

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
        # Colab's kernel already has numpy imported before this cell runs. Installing a
        # different numpy from requirements-colab.txt overwrites the files on disk but not
        # the compiled submodules already cached in this process, so importing a numpy
        # submodule for the first time later (e.g. via ml4t.engineer) mixes the new files
        # with the stale cached extension and raises ImportError. Put numpy back to the
        # version this process already has loaded once the rest of the install is done.
        import numpy as _colab_numpy

        colab_numpy_version = _colab_numpy.__version__
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
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-q",
                "--force-reinstall",
                "--no-deps",
                f"numpy=={colab_numpy_version}",
            ],
            check=True,
        )
        ready.touch()
    os.chdir(repo_dir / "notebooks")

# %%
import pandas as pd
import polars as pl

DATA_DIR = "../data"

prices = pd.read_parquet(f"{DATA_DIR}/etf_universe.parquet")
prices["timestamp"] = pd.to_datetime(prices["timestamp"])
prices = prices.sort_values(["symbol", "timestamp"]).reset_index(drop=True)
prices.head()

# %% [markdown]
# ## Sanity checks before we build anything
#
# A workflow starts by interrogating the data, not by trusting the file
# name. Three questions: how many names, what date range, how complete.

# %%
print(f"{prices['symbol'].nunique()} symbols")
print(f"{prices['timestamp'].min().date()} -> {prices['timestamp'].max().date()}")

coverage = prices.groupby("symbol")["timestamp"].agg(["min", "max", "count"])
coverage["years"] = ((coverage["max"] - coverage["min"]).dt.days / 365.25).round(1)
coverage.sort_values("min").head(10)

# %% [markdown]
# Coverage is **not uniform** - some ETFs (SPY, QQQ) have traded since the
# 1990s/2000s; others launched much later (XLC in 2018, sector-momentum
# funds like MTUM/VLUE in 2013). `coverage["min"]` shows this directly.
# This matters the moment you rank across the full universe on any given
# date: an equal-weight backtest starting in 2006 trades a very different,
# much smaller universe than one starting in 2020.

# %%
short_history = coverage[coverage["years"] < 10].sort_values("years")
print(f"{len(short_history)} of {len(coverage)} ETFs have under 10 years of history")
short_history.head(10)

# %% [markdown]
# ## Point-in-time eligibility
#
# `data/eligibility.csv` records, for each (symbol, year), whether that ETF
# passed the $10M-ADV eligibility bar *as of that year* - this is what a
# point-in-time backtest must filter on, not "is this symbol in the file at
# all." The full 100-symbol universe was selected **backward-looking**, so
# using all 100 from day one of any backtest is itself a survivorship-bias
# bug - the same bug documented for the book's own US-equities case study
# (Ch2 errata). Treat `eligibility.csv` as required reading before wiring
# any of this into a backtest, not an optional file.

# %%
eligibility = pd.read_csv(f"{DATA_DIR}/eligibility.csv")
eligible_per_year = eligibility.groupby("eligible_year")["symbol"].nunique()
eligible_per_year

# %% [markdown]
# ## From pandas to polars
#
# `ml4t-backtest` is polars-first. We keep pandas for exploration (it's
# what most of the room already knows) and convert once, right before it
# touches the engine - that boundary is worth being deliberate about rather
# than mixing the two libraries ad hoc through the pipeline.

# %%
prices_pl = pl.from_pandas(prices)
prices_pl.head()

# %% [markdown]
# **Next:** `02_features_labels.ipynb` - turn this raw OHLCV panel into
# momentum/volatility/RSI features and forward-return labels.
