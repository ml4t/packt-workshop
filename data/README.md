# Data

Everything in this directory ships with the repo - no download step, no API key,
no brokerage account. That's deliberate: the workshop should run identically
whether you're on hotel wifi or a plane.

## `etf_universe.parquet`

Daily OHLCV for **100 liquid ETFs**, **2006-01-03 to 2025-12-31**, sourced from
Yahoo Finance. Same universe as the ETF case study in *Machine Learning for
Trading, 3rd Edition* (`case_studies/etfs/`) - long format, one row per
(symbol, day): `timestamp, open, high, low, close, volume, symbol`.

Coverage is **not uniform**. SPY and QQQ go back decades; XLC (2018) and several
smart-beta funds (MTUM, VLUE, both 2013) are much younger. `01_data.ipynb` checks
this explicitly before anything downstream relies on it.

## `eligibility.csv`

Point-in-time membership: for each (symbol, year), whether that ETF had passed a
$10M average-daily-volume threshold *as of that year*. The 100-symbol universe
itself was selected **backward-looking** - i.e. with survivorship bias baked into
which 100 ETFs made the list at all - so this file is what makes it possible to
run something closer to a point-in-time backtest, not an optional filter.
`02_features_labels.ipynb` applies it before building any feature.

The $10M threshold is not inflation-adjusted across the 20-year window.

## License / attribution

Yahoo Finance data, redistributed for educational use in this workshop. Not for
commercial redistribution. If you outgrow this dataset, `ml4t-data`
(`pip install ml4t-data`) covers live refresh from the same and other free
sources, and the book's companion repo (`ml4t/public`, linked from the main
README) carries the full case-study data pipeline this was drawn from.

## Regenerated files (not shipped, gitignored)

Running the notebooks in order writes two intermediate files here:
`model_dataset.parquet` (from `02_features_labels.ipynb`) and
`oos_predictions.parquet` (from `03_model_training.ipynb`). Both are fully
reproducible from `etf_universe.parquet` + `eligibility.csv` - they're gitignored
on purpose, not missing.
