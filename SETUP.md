# Setup

Three ways to get running. Pick the one that matches your machine. Complete
the verification before the workshop so the guided checkpoints can focus on
the research decisions rather than environment setup.

## Option A - local, with `uv` (recommended if you're on Python 3.12+)

```bash
git clone https://github.com/ml4t/packt-workshop.git
cd packt-workshop
uv sync
uv run jupyter lab notebooks/
```

The repository's `.python-version` asks `uv` for Python 3.12 and installs it
for you if necessary. Verify the install:

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
`04_backtest`). The notebooks expect the repository's `data/` directory next
to `notebooks/`. In a fresh Colab runtime, run this once before the notebook's
first cell:

```python
!git clone https://github.com/ml4t/packt-workshop.git
%cd packt-workshop
!pip install -q .
%cd notebooks
```

## Verifying you're actually ready

Whichever option you pick, `01_data.ipynb` must execute without error before
the workshop starts. From a local `uv` checkout, run:

```bash
uv run jupyter nbconvert --to notebook --execute --stdout notebooks/01_data.ipynb > /dev/null && echo "ready"
```

(swap `uv run` for `docker run --rm ml4t-packt-workshop uv run ...` under
Option B).

The complete guided sequence is `01_data` → `02_features_labels` →
`03_model_training` → `04_backtest`. The later notebooks create intermediate
files in `data/`, so run them in order.
