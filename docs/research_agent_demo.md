# Research agent demo (agenda block 9)

**This is a live demo, not a hands-on exercise** — the agenda deliberately
doesn't ask 150 attendees to run a multi-agent LLM pipeline in a 20-minute
block. What follows is what's being demoed and where to find it if you want
to run it yourself afterward.

## What it is

The book's own forecasting agent from Chapter 24 ("Autonomous Agents"),
`08_forecasting_pipeline.py` in the book's companion code
(`24_autonomous_agents/` in
[`github.com/stefan-jansen/machine-learning-for-trading`](https://github.com/stefan-jansen/machine-learning-for-trading)).
It's an **agent → aggregation → debate → supervisor** pipeline (the
`AIAForecaster` class) that:

1. Takes a market-relevant forecasting question (e.g. "will the Fed cut rates
   at the next meeting") as input.
2. Runs a `SupervisorAgent` over multiple specialist research agents, each
   producing an independent probability estimate with cited reasoning.
3. Aggregates disagreement, runs an adversarial debate phase when agents
   diverge, and produces a single calibrated probability with a full,
   inspectable trace — not just a number.
4. Persists the trace (see `forecast_traces/` in the book repo) so the
   reasoning is auditable after the fact, not just the output.

This is the chapter's replication of Bridgewater's publicly described
"AIA" (Artificial Intelligence Analyst) approach — the differentiator over a
single-shot LLM call is the disagreement-aware aggregation and the debate
phase, both scored for calibration (Brier score, log-loss) against resolved
outcomes in the chapter's NB09.

## Why it's not in this repo

It needs live LLM API calls (not reproducible on a fixed schedule for 150
concurrent attendees), the book's own Docker image, and API keys — none of
which belong in a repo meant to run offline on the free ETF dataset. The demo
runs from the presenter's own environment.

## If you want to run it after the workshop

Clone `github.com/stefan-jansen/machine-learning-for-trading` (linked from the
main README), read Chapter 24 for the full walkthrough, and start at
`24_autonomous_agents/01_react_reasoning.ipynb` — the pipeline in
`08_forecasting_pipeline.py` composes NB04 (research agent), NB05
(aggregation), and NB07 (adversarial debate), so it reads best after those
three, not cold.
