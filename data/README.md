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

## `etf_reference.csv`

What each of the 100 tickers actually is: `symbol, group, name`, one row per
ETF, grouped into the same 9 asset classes `01_data.ipynb`'s clustermap
surfaces (`us_equity_broad`, `us_equity_style`, `us_sectors`,
`international_developed`, `emerging_markets`, `fixed_income`,
`commodities`, `specialty`, `currency`). Not used by any notebook
computation - it's a lookup table for reading the correlation and
eligibility figures, so "XLC" or "EWL" resolve to something recognizable
instead of staying a bare ticker. Full listing below.

### US equity, broad (10)

| Symbol | What it tracks |
|---|---|
| DIA | SPDR Dow Jones Industrial Average ETF - 30 blue chips |
| IJR | iShares Core S&P Small-Cap ETF - US small-cap |
| IVE | iShares S&P 500 Value ETF - S&P 500 value slice |
| IVW | iShares S&P 500 Growth ETF - S&P 500 growth slice |
| IWM | iShares Russell 2000 ETF - US small-cap |
| MDY | SPDR S&P MidCap 400 ETF - US mid-cap |
| QQQ | Invesco QQQ Trust - Nasdaq-100 |
| RSP | Invesco S&P 500 Equal Weight ETF - S&P 500, equal-weighted |
| SPY | SPDR S&P 500 ETF Trust - S&P 500 |
| VTI | Vanguard Total Stock Market ETF - whole US market |

### US equity, factor/style (10)

| Symbol | What it tracks |
|---|---|
| DVY | iShares Select Dividend ETF - high dividend yield |
| MTUM | iShares MSCI USA Momentum Factor ETF |
| QUAL | iShares MSCI USA Quality Factor ETF |
| SCHD | Schwab US Dividend Equity ETF |
| SDY | SPDR S&P Dividend ETF - dividend growth |
| USMV | iShares MSCI USA Min Vol Factor ETF - low volatility |
| VIG | Vanguard Dividend Appreciation ETF |
| VLUE | iShares MSCI USA Value Factor ETF |
| VTV | Vanguard Value ETF - US large-cap value |
| VUG | Vanguard Growth ETF - US large-cap growth |

### US sectors + REITs (13)

| Symbol | What it tracks |
|---|---|
| IYR | iShares U.S. Real Estate ETF |
| VNQ | Vanguard Real Estate ETF |
| XLB | Materials Select Sector SPDR Fund |
| XLC | Communication Services Select Sector SPDR Fund |
| XLE | Energy Select Sector SPDR Fund |
| XLF | Financial Select Sector SPDR Fund |
| XLI | Industrial Select Sector SPDR Fund |
| XLK | Technology Select Sector SPDR Fund |
| XLP | Consumer Staples Select Sector SPDR Fund |
| XLRE | Real Estate Select Sector SPDR Fund |
| XLU | Utilities Select Sector SPDR Fund |
| XLV | Health Care Select Sector SPDR Fund |
| XLY | Consumer Discretionary Select Sector SPDR Fund |

### International developed (18)

| Symbol | What it tracks |
|---|---|
| ACWI | iShares MSCI ACWI ETF - global, developed + EM |
| ACWX | iShares MSCI ACWI ex U.S. ETF |
| EFA | iShares MSCI EAFE ETF - developed ex US/Canada |
| EWA | iShares MSCI Australia ETF |
| EWC | iShares MSCI Canada ETF |
| EWG | iShares MSCI Germany ETF |
| EWH | iShares MSCI Hong Kong ETF |
| EWI | iShares MSCI Italy ETF |
| EWJ | iShares MSCI Japan ETF |
| EWL | iShares MSCI Switzerland ETF |
| EWN | iShares MSCI Netherlands ETF |
| EWP | iShares MSCI Spain ETF |
| EWQ | iShares MSCI France ETF |
| EWT | iShares MSCI Taiwan ETF |
| EWU | iShares MSCI United Kingdom ETF |
| IEFA | iShares Core MSCI EAFE ETF |
| VEA | Vanguard FTSE Developed Markets ETF |
| VGK | Vanguard FTSE Europe ETF |

### Emerging markets (11)

| Symbol | What it tracks |
|---|---|
| EEM | iShares MSCI Emerging Markets ETF - broad EM |
| EWW | iShares MSCI Mexico ETF |
| EWY | iShares MSCI South Korea ETF |
| EWZ | iShares MSCI Brazil ETF |
| EZA | iShares MSCI South Africa ETF |
| FXI | iShares China Large-Cap ETF |
| IEMG | iShares Core MSCI Emerging Markets ETF |
| INDA | iShares MSCI India ETF |
| MCHI | iShares MSCI China ETF |
| THD | iShares MSCI Thailand ETF |
| VWO | Vanguard FTSE Emerging Markets ETF |

### Fixed income (15)

| Symbol | What it tracks |
|---|---|
| AGG | iShares Core U.S. Aggregate Bond ETF |
| BIL | SPDR Bloomberg 1-3 Month T-Bill ETF - cash-like |
| BND | Vanguard Total Bond Market ETF |
| BNDX | Vanguard Total International Bond ETF (hedged) |
| EMB | iShares J.P. Morgan USD Emerging Markets Bond ETF |
| GOVT | iShares U.S. Treasury Bond ETF - broad Treasuries |
| HYG | iShares iBoxx $ High Yield Corporate Bond ETF - junk bonds |
| IEF | iShares 7-10 Year Treasury Bond ETF |
| JNK | SPDR Bloomberg High Yield Bond ETF - junk bonds |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF |
| MUB | iShares National Muni Bond ETF |
| SHY | iShares 1-3 Year Treasury Bond ETF - short duration |
| TIP | iShares TIPS Bond ETF - inflation-protected Treasuries |
| TLT | iShares 20+ Year Treasury Bond ETF - long duration |
| VCSH | Vanguard Short-Term Corporate Bond ETF |

### Commodities (9)

| Symbol | What it tracks |
|---|---|
| DBA | Invesco DB Agriculture Fund - wheat, corn, soybeans, sugar |
| DBC | Invesco DB Commodity Index Tracking Fund - broad basket |
| GLD | SPDR Gold Shares - gold bullion |
| GSG | iShares S&P GSCI Commodity-Indexed Trust - energy-heavy basket |
| IAU | iShares Gold Trust - gold bullion |
| PPLT | abrdn Physical Platinum Shares ETF |
| SLV | iShares Silver Trust - silver bullion |
| UNG | United States Natural Gas Fund - natural gas futures |
| USO | United States Oil Fund - WTI crude futures |

### Specialty / industry (10)

| Symbol | What it tracks |
|---|---|
| IBB | iShares Biotechnology ETF |
| ITA | iShares U.S. Aerospace & Defense ETF |
| ITB | iShares U.S. Home Construction ETF |
| KRE | SPDR S&P Regional Banking ETF |
| OIH | VanEck Oil Services ETF |
| SMH | VanEck Semiconductor ETF |
| SOXX | iShares Semiconductor ETF |
| XBI | SPDR S&P Biotech ETF - equal-weighted biotech |
| XME | SPDR S&P Metals & Mining ETF |
| XRT | SPDR S&P Retail ETF |

### Currency (4)

| Symbol | What it tracks |
|---|---|
| FXB | Invesco CurrencyShares British Pound Sterling Trust |
| FXE | Invesco CurrencyShares Euro Trust |
| FXY | Invesco CurrencyShares Japanese Yen Trust |
| UUP | Invesco DB US Dollar Index Bullish Fund - long USD |

## `eligibility.csv`

Point-in-time membership: for each (symbol, year), whether that ETF had passed a
$10M average-daily-volume threshold *as of that year*. The 100-symbol universe
itself was selected **backward-looking** - i.e. with survivorship bias baked into
which 100 ETFs made the list at all - so this file is what makes it possible to
run something closer to a point-in-time backtest, not an optional filter.
`02_features_labels.ipynb` applies it before building any feature.

The $10M threshold is not inflation-adjusted across the 20-year window.

## `research_agent_trace.json`

One complete, real run of the book's Chapter 24 `AIAForecaster` pipeline -
not this workshop's data, not ETF-related, walked through in
`notebooks/05_research_agent_trace.ipynb` as agenda block 9's research-agent
segment instead of a live LLM call. Trimmed from the full raw trace (source
path and run metadata are in the file's own `provenance` key): every
agent-generated number and piece of reasoning is kept verbatim, only the raw
web search results each specialist queried along the way are dropped (third-
party scraped content, not needed for the walkthrough, and the bulk of the
original 114KB). See `docs/research_agent_demo.md` for why this segment
traces a frozen run instead of executing the pipeline live.

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
