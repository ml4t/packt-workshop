# Prerequisites

## Technical

- **Python 3.12+.** (The Eventbrite listing says "3.11+" - `ml4t-backtest`
  raised its floor to 3.12 after that copy was written. If you're on exactly
  3.11, don't fight it: use the Docker image or the Colab notebook below,
  both pinned to 3.12.)
- A ready-to-run **Docker image** and a **Colab notebook** are provided as
  fallbacks - see `SETUP.md` - so a local environment mismatch doesn't cost
  you workshop time.

## Libraries

`pandas`, `scikit-learn`, `lightgbm`, and the `ml4t` companion libraries for
feature engineering, validation, and backtesting (`ml4t-engineer`,
`ml4t-diagnostic`, `ml4t-backtest`). All open source, all installed from
this repo's `pyproject.toml` - see `SETUP.md`.

## Optional

- Free Nasdaq Data Link / Yahoo Finance access - **not required**. The full
  100-ETF dataset ships with this repo (`data/etf_universe.parquet`); no paid
  data or brokerage account is used anywhere in the workshop.
- A coding agent (e.g. [Claude Code](https://claude.com/claude-code)) to
  follow along with the agent-assisted build in block 4. Not required to
  follow the rest of the session. The coding-agent build and research-agent
  forecast are presenter-led demonstrations; the four guided notebooks need
  no LLM API key. `docs/coding_agent_brief.md` has the brief used live if you
  want to run it yourself afterward.

## Experience

Intermediate Python (comfortable with pandas). Familiarity with basic ML and
market terminology (returns, features, cross-validation) is helpful but not
assumed - block 2 covers the alpha-factor framing from first principles.
