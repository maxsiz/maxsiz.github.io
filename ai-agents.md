---
layout: page
title: AI Agents
meta-title: "AI Agent Pipelines for Web3 & DeFi | Iber"
subtitle: Agents that research, verify and operate — with a human at every gate
meta-description: Iber builds AI agent pipelines for Web3 — DeFi protocol onboarding, Uniswap v4 LP strategy research with backtests, and agent-assisted operations — bounded by policy and human approval.
service-name: "AI agent pipelines for Web3"
service-type: "AI agent development and integration"
last_modified_at: 2026-11-03
faq:
  - q: What do your AI agents actually do?
    a: They take on the research and verification work around DeFi products — finding protocols and pools that fit formal criteria, writing a checkable specification or strategy, testing it against history, and explaining the result to a human who makes the decision.
  - q: Can an agent move funds on its own?
    a: Not outside the limits a human sets. Our strategy pipeline holds no agent or sponsor keys at all. In UniSafe, an agent executes only within the owner's policy, through a bounded executor, and never gets the owner's keys.
  - q: How do you stop an agent from shipping a wrong result?
    a: Every result passes checks written in code, a separate critic agent, a reference test where one exists, and a human gate. Strategies also go through paper trading and small-size stages, each with its own approval.
  - q: Which models do you use?
    a: The agents run on Anthropic's Claude models. Stronger models handle analysis and critique; lighter ones handle research and explanations. The orchestrator itself is plain code, not an agent.
  - q: Can you build an agent pipeline for our product?
    a: Yes. The pipeline core is a reusable template; a new domain needs its own criteria, artifact schema, checks and prompts. Write to the email in the footer or message us on Telegram.
---

We build AI agent pipelines for Web3 products. The agents do the slow, repetitive work —
research, specification, verification, monitoring — and a person makes every decision that
matters. Agents act only inside limits written in code and in on-chain policy, and they never
hold users' keys.

* * *

### Agent pipelines

All our pipelines share one shape: a **researcher** finds candidates by formal criteria, an
**analyst** writes a checkable artifact, code checks it, a **critic** agent challenges the
method, an **explainer** prepares the decision for a human, and only after approval does the
result reach the product. The orchestrator that moves work between stages, enforces limits and
holds the gates is code, not an agent. Every run and every decision is logged.

**DeFi protocol onboarding**

Agents find new lending and yield protocols, work out which contract calls produce each metric
and how to compute it, and prepare the integration. A golden test on historical blocks must match
before anything is merged.

* 103 candidates processed since late September 2026: 56 onboarded, 44 rejected (23 by the
  researcher's own criteria, 21 at the human gate)
* 170 instruments tracked across 25 protocols — Morpho, Aave v3 and v4, Compound v3, Spark,
  Euler, Fluid, Maple and others; 54 of them across 18 protocols were onboarded by agents
* [Live pipeline dashboard](https://detracker.github.io/ai-sandbox-dashboard) — what the agents
  are doing right now, pipeline health and the decision log

**Uniswap v4 LP strategy research**

An agent factory that finds, tests and releases concentrated-liquidity strategies for Uniswap v4.
The factory does not trade: strategies are executed by the UniSafe agent inside the owner's policy.

* Backtest on a held-out 30% of history at 1, 7 and 30-day horizons, against HODL and a reference
  ladder of models, with drawdown and a surrogate-data test
* The critic looks for overfitting, out-of-range time, depeg, oracle and cost risks
* Staged rollout — paper → small → full — with a separate human decision at each step
* 15 strategy candidates across Ethereum, Arbitrum One, Base and Unichain: 6 in staged rollout,
  7 rejected, 6 of those at the human gate
* [Strategy catalog](https://uniswapv4-lp-strategies-bff4ee.gitlab.io) and the
  [factory source code](https://gitlab.com/ai-solutions-pipelines/factory-lp-strategies)

Figures as of November 3, 2026; the dashboards show current numbers.

* * *

### Agents inside Web3 products

[UniSafe](https://unisafe.envelop.is) managers are NFT-owned Uniswap v4 liquidity managers. The
owner sets a policy; an agent can rebalance and manage positions only within it, through a bounded
executor. The agent never receives the owner's keys — ownership
stays with whoever holds the NFT. See [Ownership without custody](/2026-07-30-Ownership_Without_Custody/)
for the reasoning behind this model.

* * *

### Agentic operations

The same approach runs our production support:

* A **duty agent** runs daily, weekly and monthly quality checks across the frontend, smart
  contracts and infrastructure, and files findings
* A **healer agent** takes routine findings, fixes them in an isolated copy, and a deployer ships
  the change under a daily limit; decisions that need a person go to a merge request
* **External synthetic monitoring** checks the live product every five minutes and alerts the team
  in Telegram

* * *

### Principles

* **A human at every gate.** Agents propose and explain; people approve.
* **Bounded permissions.** Each role gets only the tools and repositories it needs.
* **No custody.** Pipelines hold no user or agent keys; on-chain actions go through owner policy.
* **Verified by code.** Schemas, checks, golden tests and backtests run before any agent's opinion
  is trusted.
* **Everything logged.** Every run, tool call and decision is recorded and reviewable.

* * *

### Related

Our broader work: [development](/development), [research](/research),
[Ethereum smart contracts](/products_eth) and [smart contract audits](/products_audit).
