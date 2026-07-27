# Setup

Three ways to get running. Pick the one that matches your machine - don't
troubleshoot a local environment during the workshop when a working fallback
is one click away.

## Option A - local, with `uv` (recommended if you're on Python 3.12+)

```bash
git clone https://github.com/ml4t/packt-workshop.git
cd packt-workshop
uv sync
uv run jupyter lab notebooks/
```

`uv` installs Python 3.12 for you if you don't have it - you don't need to
manage that yourself. Verify the install:

```bash
uv run python3 -c "import ml4t.engineer, ml4t.diagnostic, ml4t.backtest, lightgbm; print('OK')"
```

## Option B - Docker (works regardless of your local Python)

```bash
git clone https://github.com/ml4t/packt-workshop.git
cd packt-workshop
docker build -t ml4t-packt-workshop .
docker run --rm -p 8888:8888 -v "$(pwd)":/workshop ml4t-packt-workshop
```

Then open the printed `http://localhost:8888` link (no token - fine for a
disposable local container, don't publish this port anywhere).

## Option C - Colab (nothing to install)

Open a notebook directly from GitHub:

```
https://colab.research.google.com/github/ml4t/packt-workshop/blob/main/notebooks/01_data.ipynb
```

(swap `01_data` for any of `02_features_labels`, `03_model_training`,
`04_backtest`). The first cell of each notebook in this repo assumes the
repo's own `data/` directory is a sibling - on Colab, run this once per
session before the notebook's own first cell:

```python
!git clone https://github.com/ml4t/packt-workshop.git
%cd packt-workshop
!pip install -q ml4t-engineer ml4t-diagnostic ml4t-backtest lightgbm
%cd notebooks
```

## Verifying you're actually ready

Whichever option you pick, this should run without error before the workshop
starts:

```bash
uv run jupyter nbconvert --to notebook --execute --stdout notebooks/01_data.ipynb > /dev/null && echo "ready"
```

(swap `uv run` for `docker run --rm ml4t-packt-workshop uv run ...` under
Option B).
