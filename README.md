# Refund Assistant Evaluation

A tool-using conversational agent for handling refund requests, with an evaluation suite built on LangChain, LangGraph, and DeepEval.

The agent checks a customer's purchase history and refund eligibility, calculates refunds for eligible requested items, and creates a refund ticket when appropriate. The evaluation dataset covers eligible and ineligible requests, unknown users, and questions that should not create a refund.

## Requirements

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/)
- A [Groq API key](https://console.groq.com/keys)

## Setup

Clone the repository, then install the locked dependencies:

```bash
uv sync
```

Create a `.env` file in the repository root and add your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Keep `.env` private. It is excluded from Git.

## Run an evaluation

Run an evaluation script from the repository root:

```bash
uv run python evaluation/plan_adherence.py
```

Available evaluations:

```bash
uv run python evaluation/plan_adherence.py
uv run python evaluation/plan_quality.py
uv run python evaluation/step_efficiency.py
uv run python evaluation/task_completion.py
uv run python evaluation/tool_correctness.py
```

Each script invokes the agent against the examples in `evaluation/dataset.py` and scores its behavior with the corresponding DeepEval metric.

## Project layout

```text
agent/       LangChain agent, prompts, tools, and sample purchase data
evaluation/ Evaluation dataset, Groq judge model, and metric scripts
```

Both the agent and the evaluation judge use Groq's `openai/gpt-oss-20b` model. Evaluation runs make multiple model calls and can consume the account's rate limits; if Groq returns a `429` rate-limit error, wait for the retry window in the error message or use a model/account with available quota.
