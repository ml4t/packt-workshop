# One real forecasting-agent run (agenda block 9)

This is a single, complete, real run of the book's Chapter 24 `AIAForecaster`
pipeline - not a mock-up and not paraphrased numbers. It's what the presenter
walks through live during the research-agent segment instead of firing a new
live LLM pipeline run at the room (see `docs/research_agent_demo.md` for why).

**Provenance**: `24_autonomous_agents/forecast_traces/
08_forecasting_pipeline_20260609T142158Z_24e083e7fe54.json` in the book's
companion repo (`github.com/stefan-jansen/machine-learning-for-trading`),
model `claude-sonnet-4-20250514`, run `2026-06-09T14:21:58Z`, run id
`24e083e7fe54`. The full raw trace (including every search query and result
each specialist issued) lives at that path if you want to go deeper than
this excerpt - it's ~114KB of JSON, too much to paste into a slide or a
21-minute segment.

## The question

> Will the Federal Reserve hike rates in 2026?

Resolves YES if the upper bound of the federal funds target rate is raised
at any point between January 1, 2026 and the Fed's December 8-9, 2026
meeting. **Market-implied probability at the time of this run: 0.545.**
The question had not resolved as of the run - this is a real open forecast,
not a graded one.

## Step 1 - three specialists, independently

| Agent | p(yes) | Rationale (excerpt) |
|---|---:|---|
| `agent_0` | 0.25 | "The Fed is currently maintaining rates at 3.50%-3.75%... Goldman Sachs and other forecasters expect rate cuts in 2026, not hikes... unemployment is projected to rise to 4.5% by Q3 2026." |
| `agent_1` | 0.25 | "The Fed's December 2025 dot plot shows officials expect only one 25bp rate cut in 2026... However, significant upside risks exist: Trump tariffs are already raising core goods PCE..." |
| `agent_2` | 0.62 | "Inflation running at 2.9%, well above the Fed's 2% target... CNBC reports traders pricing 51% probability of a December 2026 hike and 71% by March 2027..." |

Two agents read the same Fed guidance as disinflationary; one reads the same
inflation print as hike-forcing. A 37-percentage-point spread on the same
underlying facts is exactly the disagreement the next two steps exist to
surface, not paper over.

## Step 2 - aggregation (Neyman, correlation-adjusted)

- Raw average of the three probabilities: **0.3733**
- Extremization factor (accounts for agents sharing information, ρ = 0.3):
  **1.3693**
- Extremized probability: **0.3266**
- Effective number of independent agents: **1.88** of 3 - most of the
  "three opinions" overlap.

## Step 3 - adversarial debate, three rounds

A bull and a bear agent argue from the same evidence base and are scored
each round:

| Round | Bull p(yes) | Bear p(yes) | Consensus? |
|---|---:|---:|---|
| 1 | 0.68 | 0.18 | No |
| 2 | 0.68 | 0.20 | No |
| 3 | 0.65 | 0.20 | No |

Consensus was never reached. The disagreement doesn't move much across
rounds either - both sides settle rather than converge, and the trace shows
exactly why: bull and bear keep re-reading the same December 2025 dot plot
in opposite directions (bull calls it "outdated guidance," bear calls it
"the collective judgment of Fed officials"). The debate doesn't manufacture
agreement; it makes the disagreement legible.

## Step 4 - supervisor's final call

The supervisor reviews the full record (specialist estimates, aggregation,
debate transcript), flags the same four disagreements a careful reader
would flag, runs three of its own clarifying research queries, and commits
to one number anyway:

- **Final probability: 0.2737**
- **Final confidence: 0.6**
- Versus the market-implied 0.545 at the time - the pipeline lands well
  below the market, driven mainly by the bear case's Fed-guidance reading
  and the two specialists who agreed with it.

## Why this is the example to walk through live

A system that always converges to consensus would be suspicious - it would
mean the debate phase does nothing. This run didn't converge, and the trace
shows exactly where and why the two readings diverge (the December 2025 dot
plot), which is the actual audit value: not "the agents agreed," but "you
can see precisely what they disagreed about and why the supervisor weighted
it the way it did."

## What NOT to claim from this

This one run has no resolved outcome yet (it resolves no earlier than
December 2026), so there is no accuracy or calibration number to report
here - "0.2737" is a probability, not a graded prediction. Chapter 24's
notebook 9 does demonstrate Brier-score / log-loss / calibration-transform
arithmetic, but on an **author-selected synthetic panel assembled after
outcomes were known**, built to make the scoring-rule math reproducible -
not a measurement of this pipeline's real forecasting accuracy. Don't
present those notebook-9 numbers as if they were.
