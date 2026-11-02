import sys
from pathlib import Path
from uuid import uuid4

import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "agent")
)

from agent import agent
from dataset import dataset
from model import eval_model

from deepeval.metrics import StepEfficiencyMetric
from deepeval.integrations.langchain import CallbackHandler
from deepeval.evaluate.configs import AsyncConfig


metrics = [StepEfficiencyMetric(threshold=0.8,model=eval_model,include_reason=True)]


for golden in dataset.evals_iterator(
    metrics=metrics,
    async_config=AsyncConfig(run_async=True, max_concurrent=1, throttle_value=60),
):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": golden.input}]},
        config={"configurable": {"thread_id": str(uuid4())},
        "callbacks": [CallbackHandler()]}
    )