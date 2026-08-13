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
# # 04 · Backtesting the strategy - with real costs
#
# **Supports agenda block 8** ("Backtesting the Strategy") and sets up
# block 10 ("Where to Go Next... why most backtests break"). We turn the
# out-of-sample predictions from `03_model_training` into a monthly
# top-N, equal-weight ETF portfolio and run it through `ml4t-backtest`'s
# event-driven engine - **with commissions and slippage switched on
# explicitly**.
#
# That last clause is not boilerplate. `BacktestConfig` defaults
# `commission_type` and `slippage_type` to `NONE` - a config that *sets*
# `commission_rate`/`slippage_rate` without also setting the corresponding
# `*_type` field runs at **zero cost**, silently. It's an easy mistake to
# make (and one worth checking for explicitly if you ever hand this brief
# to a coding agent) since the cost fields look like they should be enough
# on their own.

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
    if not (repo_dir / "data/model_dataset.parquet").exists():
        print("Preparing the feature-and-label dataset required by this notebook.")
        subprocess.run([sys.executable, "02_features_labels.py"], check=True)
    if not (repo_dir / "data/oos_predictions.parquet").exists():
        print("Preparing the out-of-sample predictions required by this notebook.")
        subprocess.run([sys.executable, "03_model_training.py"], check=True)

# %%
from dataclasses import asdict

import pandas as pd
import polars as pl
from ml4t.backtest import (
    BacktestConfig,
    Broker,
    RebalanceConfig,
    Strategy,
    TargetWeightExecutor,
    run_backtest,
)
from ml4t.backtest.config import CommissionType, ShareType, SlippageType, SpreadConvention
from ml4t.backtest.execution.schedule import RebalanceCadence, RebalanceSchedule

DATA_DIR = "../data"

prices = pd.read_parquet(f"{DATA_DIR}/etf_universe.parquet")
prices["timestamp"] = pd.to_datetime(prices["timestamp"])

oos = pd.read_parquet(f"{DATA_DIR}/oos_predictions.parquet")
oos["timestamp"] = pd.to_datetime(oos["timestamp"]).dt.tz_localize(None)

# The engine wants prices covering exactly the OOS prediction window -
# trading on dates the model never produced a signal for isn't meaningful.
prices = prices[
    (prices["timestamp"] >= oos["timestamp"].min())
    & (prices["timestamp"] <= oos["timestamp"].max())
]

prices_pl = pl.from_pandas(
    prices[["timestamp", "symbol", "open", "high", "low", "close", "volume"]]
)
signals_pl = pl.from_pandas(oos[["timestamp", "symbol", "prediction"]])

print(f"backtest window: {prices['timestamp'].min().date()} -> {prices['timestamp'].max().date()}")
print(f"{prices_pl.height:,} price rows, {signals_pl.height:,} signal rows")

# %% [markdown]
# ## The cost model - matches the book's own ETF case study
#
# `$0.0035`/share commission and tiered half-spread slippage are the same
# numbers the case study's `config/setup.yaml` uses (`per_share_plus_spread`,
# IBKR Pro tiered pricing). We use the real numbers rather than a round
# "50 bps" placeholder, because the point of this block is that the *shape*
# of a realistic cost model - fixed-plus-spread, not a flat percentage -
# changes which trades are worth making at all, especially for the
# less-liquid names in a 100-ETF universe.

# %%
ASSET_SPREADS = {
    "SPY": 0.005,
    "QQQ": 0.005,
    "IWM": 0.005,
    "EFA": 0.005,
    "EEM": 0.005,
    "DIA": 0.005,
    "VTI": 0.005,
    "XLK": 0.01,
    "XLF": 0.01,
    "XLV": 0.01,
    "XLE": 0.01,
    "XLY": 0.01,
    "XLI": 0.01,
    "XLP": 0.01,
    "XLU": 0.01,
    "XLB": 0.01,
    "XLRE": 0.01,
    "XLC": 0.01,
}

config = BacktestConfig(
    initial_cash=100_000.0,
    share_type=ShareType.INTEGER,
    commission_type=CommissionType.PER_SHARE,
    commission_per_share=0.0035,
    slippage_type=SlippageType.SPREAD,
    slippage_spread=0.02,  # default half-spread for anything not in the table below
    slippage_spread_by_asset=ASSET_SPREADS,
    slippage_spread_convention=SpreadConvention.HALF_SPREAD,
)
print(config.validate())  # empty list = no configuration warnings

# %% [markdown]
# ## The strategy: monthly top-10, equal weight
#
# Rank the current cross-section by predicted 21-day forward return, take
# the top 10, equal-weight them, rebalance at month end. `RebalanceConfig`
# carries the same trade-filtering thresholds as the case study
# (`min_weight_change=0.005`, `min_trade_value=$100`) so the backtest
# doesn't churn on economically meaningless rebalances.

# %%
TOP_N = 10

executor = TargetWeightExecutor(
    config=RebalanceConfig(
        schedule=RebalanceSchedule(cadence=RebalanceCadence.MONTH_END),
        min_weight_change=0.005,
        min_trade_value=100.0,
    )
)


class TopNRebalanceStrategy(Strategy):
    def __init__(self, top_n: int, executor: TargetWeightExecutor):
        self.top_n = top_n
        self.executor = executor

    def on_prepare(self, broker: Broker, timestamps, config=None) -> None:
        self.executor.prepare_schedule(timestamps)

    def on_data(self, timestamp, data, context, broker: Broker) -> None:
        preds = {
            asset: bar["signals"]["prediction"]
            for asset, bar in data.items()
            if bar.get("signals") and bar["signals"].get("prediction") is not None
        }
        if not preds:
            return
        ranked = sorted(preds.items(), key=lambda kv: kv[1], reverse=True)[: self.top_n]
        weight = 1.0 / len(ranked)
        target_weights = {asset: weight for asset, _ in ranked}
        self.executor.execute(target_weights, data, broker, timestamp=timestamp)


strategy = TopNRebalanceStrategy(top_n=TOP_N, executor=executor)

# %% [markdown]
# ## Run it twice: with and without costs
#
# The only way to see what costs actually cost is to run the identical
# strategy both ways and diff the result - not to quote a rule-of-thumb
# bps haircut.

# %%
result_with_costs = run_backtest(prices_pl, strategy, signals=signals_pl, config=config)

zero_cost_config = BacktestConfig(initial_cash=100_000.0, share_type=ShareType.INTEGER)
strategy_zero_cost = TopNRebalanceStrategy(
    top_n=TOP_N,
    executor=TargetWeightExecutor(
        config=RebalanceConfig(
            schedule=RebalanceSchedule(cadence=RebalanceCadence.MONTH_END),
            min_weight_change=0.005,
            min_trade_value=100.0,
        )
    ),
)
result_zero_cost = run_backtest(
    prices_pl, strategy_zero_cost, signals=signals_pl, config=zero_cost_config
)

# %%
comparison = pd.DataFrame(
    {
        "zero_cost": result_zero_cost.metrics,
        "with_costs": result_with_costs.metrics,
    }
)
print(
    comparison.loc[
        ["total_return_pct", "sharpe", "max_drawdown_pct", "cagr", "avg_turnover", "total_costs"]
    ]
)

assert abs(comparison.loc["sharpe", "zero_cost"] - 0.477991) < 1e-5
assert abs(comparison.loc["sharpe", "with_costs"] - 0.440466) < 1e-5
assert abs(comparison.loc["avg_turnover", "with_costs"] - 0.059523) < 1e-5
assert abs(comparison.loc["total_costs", "with_costs"] - 8_596.84) < 1.0

# %% [markdown]
# ## Read this like a practitioner, not a scoreboard
#
# `03_model_training` already showed a HAC-corrected IC that isn't
# distinguishable from noise (t ≈ 0.94). Whatever this backtest reports
# is the honest downstream consequence of that - not a separate, better
# story. Two things worth checking regardless of the top-line number:
#
# - **The cost gap.** `with_costs` vs `zero_cost` on the *same* signal,
#   same rebalance dates, same ranking - the only thing that changed is
#   whether commissions and spread are switched on. That gap is what
#   "cost-aware" means in practice, not a modifier applied after the fact.
# - **Turnover.** A monthly top-10-of-100 rebalance can still churn
#   heavily if the ranking is unstable month to month; check
#   `result_with_costs.trades` before trusting any Sharpe number here.
#
# Across the eight validation folds from late 2015 through 2023, this
# strategy's Sharpe drops from 0.48 (zero cost) to 0.44 (with costs) - a
# real but modest reduction because monthly rebalancing keeps turnover near
# 6.0% per rebalance. Commissions and spread total **$8,597 on a $100,000
# starting account**. The 2024-2025 holdout remains sealed; this result is
# validation evidence, not a final test result.

# %%
trades = pd.DataFrame([asdict(t) for t in result_with_costs.trades])
print(f"trades (with costs): {len(trades)}")
assert len(trades) == 597
trades.head()

# %% [markdown]
# **This is where the pre-built notebooks stop.** Block 9 (research
# agents) and block 10 (where to go next) are delivered live - see
# `../docs/research_agent_demo.md` and the closing slides for what comes
# after "the backtest looks weak, now what."
