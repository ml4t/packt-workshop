# Machine Learning for Trading in the Age of AI Agents

**A Packt book-launch workshop with Stefan Jansen, author of *Machine Learning
for Trading*.**

## Quick start

Run the notebooks in order. Each Colab notebook installs this repository in a
fresh runtime and uses the bundled ETF data; no local setup is required. This
is the compact ETF quick start for the full [*Machine Learning for Trading*
companion repository](https://github.com/stefan-jansen/machine-learning-for-trading).

| Notebook | Open in Colab |
|---|---|
| 1. Data and eligibility | [Open `01_data.ipynb`](https://colab.research.google.com/github/ml4t/packt-workshop/blob/main/notebooks/01_data.ipynb) |
| 2. Features and labels | [Open `02_features_labels.ipynb`](https://colab.research.google.com/github/ml4t/packt-workshop/blob/main/notebooks/02_features_labels.ipynb) |
| 3. Model training | [Open `03_model_training.ipynb`](https://colab.research.google.com/github/ml4t/packt-workshop/blob/main/notebooks/03_model_training.ipynb) |
| 4. Cost-aware backtest | [Open `04_backtest.ipynb`](https://colab.research.google.com/github/ml4t/packt-workshop/blob/main/notebooks/04_backtest.ipynb) |

Notebooks 3 and 4 regenerate any missing intermediate files when opened
directly in a fresh Colab runtime. Running 1-4 in order avoids that repeated
work and follows the workshop narrative.

Prefer local files? [Download the complete repository as a ZIP](https://github.com/ml4t/packt-workshop/archive/refs/heads/main.zip),
extract it, and follow [`SETUP.md`](SETUP.md).

Build, test, and validate an end-to-end ML trading strategy on real market
data - and use coding and research agents to build and validate it with
current ML4T libraries and explicit checks at each stage.

This repo is everything you need to run the hands-on side of the session: the
free 100-ETF dataset, four working notebooks that take you from raw prices to
a cost-aware backtest, and the briefs behind the two live agent segments.
Clone it before the workshop and you're ready; nothing here depends on a paid data
subscription, a brokerage account, or a GPU. The slide decks are provided
through the workshop platform, not this repo.

## How the guided build-along works

Keep the slide deck (provided separately) and this repo's current notebook
open side by side. When a green
**Guided checkpoint** slide appears, run the named notebook section with
Stefan, stop at the expected output, and compare your result before moving on.
The notebooks are prepared: you are checking the research decisions and their
outputs, not recreating the whole pipeline from an empty file.

Run the notebooks in this order:

1. `01_data.ipynb` - inspect the data and point-in-time eligibility.
2. `02_features_labels.ipynb` - build features, verify the label, and save the model panel.
3. `03_model_training.ipynb` - train eight walk-forward validation folds, keep the
   2024-2025 holdout sealed, and compare IC statistics.
4. `04_backtest.ipynb` - run the same strategy with and without trading costs.

The coding-agent build and research-agent forecast are presenter-led
demonstrations. You receive both briefs, but you do not need an LLM API key or
coding-agent subscription to complete the four-notebook build.

## What you'll build

By the end of the session you'll have run, end to end, on 18 years of real
ETF data:

- A point-in-time-correct feature set (momentum, volatility, RSI, liquidity)
  on a 100-ETF universe - and know exactly which line of code would leak the
  future if you got it wrong.
- A LightGBM model validated with walk-forward, leakage-aware cross-validation,
  scored with the Information Coefficient - naive t-stat *and* the
  HAC-corrected one, and why they can disagree by a factor of three.
- A cost-aware backtest with real commission and spread modeling, so you've
  seen the actual dollar gap between "the backtest" and "the backtest with
  costs switched on" - not a rule-of-thumb haircut.
- A live look at a coding agent building part of this pipeline from a spec,
  and a live demo of the book's own multi-agent forecasting pipeline
  (Chapter 24) producing a calibrated, auditable probability estimate.

## Start here

1. **[`docs/prerequisites.md`](docs/prerequisites.md)** - what you need
   installed (spoiler: Python 3.12+, and a Docker/Colab fallback if that's
   inconvenient).
2. **[`SETUP.md`](SETUP.md)** - three ways to get running: local `uv`,
   Docker, or Colab. Pick one and verify it *before* the workshop.
3. **[`notebooks/`](notebooks/)** - run in order: `01_data` →
   `02_features_labels` → `03_model_training` → `04_backtest`. Each one runs
   standalone against the data in this repo; each ends by pointing at the
   next.

## Repository layout

```
notebooks/            01-04, run in order - the hands-on spine of the workshop
data/                  the free 100-ETF dataset (ships with the repo, see data/README.md)
docs/
  prerequisites.md     what you need before Saturday
  coding_agent_brief.md    the spec used in the live coding-agent build
  research_agent_demo.md  what the live forecasting-agent demo is and where to find it
SETUP.md               uv / Docker / Colab, pick one
```

## The agenda, briefly

210 minutes, one break: the ML4T workflow - data → alpha factors → labels &
validation → model → cost-aware backtest → live handoff - with two live agent
segments woven through it (a coding agent builds part of the pipeline; the
book's own research-agent pipeline runs a live forecast).

## About the instructor

Stefan Jansen is the author of *Machine Learning for Trading* (Packt), now in
its 3rd edition, and founder of Applied AI. The book's companion code -
450+ notebooks across 27 chapters and 9 case studies, including the full,
non-simplified version of the ETF pipeline this workshop draws on - is at
[`github.com/stefan-jansen/machine-learning-for-trading`](https://github.com/stefan-jansen/machine-learning-for-trading).

## Where to go next

This workshop is a compact entry point into a larger workflow. Continue with
the third-edition book and companion code, free **Lightning Lessons**,
**Foundations**, **Loop Engineering: Reliable Work From Coding Agents**,
**Engineering a Multi-Agent Forecasting System**, or **Machine Learning for
Trading: From Research to Production**. Choose by the work you want to do
next, not by a fixed sequence.

- Book, companion code, and Foundations: [ml4trading.io](https://www.ml4trading.io)
- Lightning Lessons, workshops, and live course:
  [maven.com/stefan-jansen](https://maven.com/stefan-jansen)

## License

Code and notebooks: MIT, see [`LICENSE`](LICENSE). Bundled market data: see
[`data/README.md`](data/README.md) for its own terms.
