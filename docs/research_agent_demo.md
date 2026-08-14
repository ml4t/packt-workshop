# Research agent walkthrough (agenda block 9)

**This is a presenter-led walkthrough of a real, already-run pipeline, not a
live LLM demo and not a hands-on exercise.** A live multi-agent pipeline run
needs API keys, the book's own Docker image, and a separate repo clone -
none of that is part of this workshop's tested setup, and a live call
failing mid-session in front of a paying room has no fallback. Instead, the
presenter walks through `docs/research_agent_trace_example.md`, a complete
real run bundled in this repo: three specialists disagree by 37 points, a
three-round debate fails to reach consensus, and the supervisor still
commits to one number. Real numbers throughout, nothing fabricated - see
that file for the full walkthrough and its exact provenance.

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
   inspectable trace - not just a number.
4. Persists the trace (see `forecast_traces/` in the book repo) so the
   reasoning is auditable after the fact, not just the output.

This is the chapter's replication of Bridgewater's publicly described
"AIA" (Artificial Intelligence Analyst) approach - the differentiator over a
single-shot LLM call is the disagreement-aware aggregation and the debate
phase. The chapter's own NB09 also demonstrates Brier-score / log-loss /
calibration-transform arithmetic - but on an author-selected synthetic
panel assembled after outcomes were known, to make the scoring-rule math
reproducible, not a live accuracy measurement of this pipeline's forecasts.
Don't present NB09's numbers as this pipeline's real calibration - see the
last section of `research_agent_trace_example.md` for why.

## Why the live pipeline isn't in this repo

Running it needs live LLM API calls (not reproducible on a fixed schedule
for 150 concurrent attendees), the book's own Docker image, and API keys -
none of which belong in a repo meant to run offline on the free ETF
dataset. What *is* in this repo is one complete, real, already-run trace
(`research_agent_trace_example.md`) - the presenter walks through that
instead of executing the pipeline live.

## If you want to run it after the workshop

Clone `github.com/stefan-jansen/machine-learning-for-trading` (linked from the
main README), read Chapter 24 for the full walkthrough, and start at
`24_autonomous_agents/01_react_reasoning.ipynb` - the pipeline in
`08_forecasting_pipeline.py` composes NB04 (research agent), NB05
(aggregation), and NB07 (adversarial debate), so it reads best after those
three, not cold.
