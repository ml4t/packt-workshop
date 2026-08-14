# Coding agent brief - live build (agenda block 4)

This is the spec handed to a coding agent (e.g. Claude Code) live during the
workshop, to build a feature-engineering + model pipeline in front of the room.
It's checked in so you can run it yourself afterward, and so the block's actual
teaching point is legible after the fact: **a precise, falsifiable spec produces
a working pipeline; a vague one produces something that looks plausible and
leaks the future.**

The notebooks in `notebooks/` were built by a human against this same repo's
data and the same library APIs - they are the answer key, not a script to be
read aloud. The point of the live block is watching the agent's *first* attempt,
including where it goes wrong, then fixing the brief rather than the code.

## The brief (paste this to the agent)

> Using the ETF panel in `data/etf_universe.parquet` (100 symbols, daily OHLCV,
> 2006-2025) and the point-in-time eligibility file in `data/eligibility.csv`:
>
> 1. Filter to eligible (symbol, date) pairs only - see `data/README.md` for
>    what "eligible" means and why it matters.
> 2. Build eight features, computed within each symbol using only data up to
>    and including the feature date: momentum at 21/63/126/252-day horizons,
>    realized volatility at 21/63-day horizons, RSI(14) via `ml4t-engineer`
>    (`ml4t.engineer.features.momentum.rsi.rsi`), and cross-sectional
>    dollar-volume rank.
> 3. Build a 21-trading-day forward return label. State explicitly: which line
>    of code could leak the future into the label, and how do you know it
>    doesn't?
> 4. Train a LightGBM regressor predicting the label from the eight features,
>    using `ml4t.diagnostic.splitters.WalkForwardCV` with `label_horizon=21` -
>    not a random train/test split, and say why not.
> 5. Evaluate with `ml4t.diagnostic.metrics.cross_sectional_ic_series` +
>    `compute_ic_hac_stats(..., label_horizon=21)`. Report the naive t-stat
>    and the HAC-corrected t-stat side by side, and explain why they differ.
>
> Stop and show me the code before running anything at step 3 (labels) and
> step 5 (evaluation) - those are the two steps most likely to hide a bug
> that produces a good-looking wrong number.

## Why this brief, specifically

- **It names the leak-prone lines explicitly** (point-in-time filter, the
  `shift`/`pct_change` direction in the label, `label_horizon` in both the
  splitter and the HAC correction). Every one of those is a place a fluent but
  unspecified agent run will get subtly wrong - usually in the direction of
  producing a *better-looking* number, which is why it doesn't get caught by
  "does this run without erroring."
- **It asks for the naive-vs-HAC comparison as a checkpoint, not a bonus.**
  `03_model_training.ipynb` in this repo found naive t ≈ 3.02 (looks
  significant) vs. HAC t ≈ 0.94 (isn't) on this exact dataset - an agent that
  only reports the naive number will confidently ship a false positive.
- **It builds in two stop-and-show checkpoints.** An agent with tool access
  will happily run a wrong pipeline to completion and report a plausible
  final number; the checkpoints exist to catch the leak before it's buried
  three cells downstream.

## If you're running this yourself, not live

Not a file diff - the agent won't produce a notebook, and `.ipynb` JSON isn't
readable that way even if it did. Check these specific points against
`notebooks/02_features_labels.ipynb` and `notebooks/03_model_training.ipynb`'s
own executed output instead:

- **Eligibility**: does it apply the point-in-time filter before building any
  feature? The reference keeps **84.2%** of (symbol, day) rows.
- **Features**: same eight - momentum at 21/63/126/252d, volatility at 21/63d,
  RSI(14), dollar-volume rank - or did it invent/drop one?
- **Split**: walk-forward (`WalkForwardCV`, `label_horizon=21`), not a random
  train/test split.
- **Evaluation**: does it report both statistics, or only the naive one? The
  reference gets naive t **≈ 3.02** and HAC-corrected t **≈ 0.94** - an agent
  that only surfaces the naive number has shipped a false positive.

Where it disagrees on any of these, that's the interesting part - not "does
the final number match to four decimal places."
