# Machine Learning for Trading in the Age of AI Agents

**A Packt book-launch workshop with Stefan Jansen, author of *Machine Learning
for Trading*.** Saturday, August 15, 2026 · 9:30 AM–1:00 PM ET (1:30–5:00 PM
UTC) · [tickets on Eventbrite](https://www.eventbrite.co.uk/e/machine-learning-for-trading-in-the-age-of-ai-agents-tickets-1994299755253).

Build, test, and validate an end-to-end ML trading strategy on real market
data - and use coding and research agents to build and validate it the way
production quant teams do in 2026, not the way a 2020 tutorial does.

This repo is everything you need for the session: the free 100-ETF dataset,
four working notebooks that take you from raw prices to a cost-aware
backtest, and the briefs behind the two live agent segments. Clone it before
Saturday and you're ready; nothing here depends on a paid data subscription,
a brokerage account, or a GPU.

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
   Docker, or Colab. Pick one and verify it *before* Saturday.
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

180 minutes, one break: the ML4T workflow - data → alpha factors → labels &
validation → model → cost-aware backtest → live handoff - with two live agent
segments woven through it (a coding agent builds part of the pipeline; the
book's own research-agent pipeline runs a live forecast). Full agenda and
timing on the [Eventbrite page](https://www.eventbrite.co.uk/e/machine-learning-for-trading-in-the-age-of-ai-agents-tickets-1994299755253).

## About the instructor

Stefan Jansen is the author of *Machine Learning for Trading* (Packt), now in
its 3rd edition, and founder of Applied AI. The book's companion code -
450+ notebooks across 27 chapters and 9 case studies, including the full,
non-simplified version of the ETF pipeline this workshop draws on - is at
[`github.com/stefan-jansen/machine-learning-for-trading`](https://github.com/stefan-jansen/machine-learning-for-trading).

## Where to go next

This workshop is deliberately a 3-hour slice of a much larger workflow. If
you want to go deeper after Saturday: **Foundations** (self-paced, the same
ETF workflow end to end, Quantopian Community) for the hands-on version of
everything this workshop moved quickly through; the **Agent Engineering**
workshop for the coding-agent and research-agent threads specifically; or
**Research to Production** (Maven, live cohort) for the same discipline
applied across nine case studies with the full production/deployment arc.
Links and current dates: [ml4trading.io](https://www.ml4trading.io).

## License

Code and notebooks: MIT, see [`LICENSE`](LICENSE). Bundled market data: see
[`data/README.md`](data/README.md) for its own terms.
