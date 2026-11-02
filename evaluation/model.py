import os
import json
from pathlib import Path
from typing import Any

from deepeval.models import DeepEvalBaseLLM
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


class GroqEvalModel(DeepEvalBaseLLM):
    """Use the project's Groq model as the DeepEval evaluation model."""

    def load_model(self) -> ChatGroq:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. Add it to D:\\Agent_eval\\.env."
            )

        return ChatGroq(
            model="openai/gpt-oss-20b",
            api_key=api_key,
            temperature=0,
            reasoning_effort="low",
            max_tokens=512,
            max_retries=6,
        )

    def generate(self, prompt: str, schema: Any = None) -> str:
        model = self._model_for_schema(schema)
        response = model.invoke(self._limit_prompt(self._prompt_for_schema(prompt, schema)))
        if schema is not None:
            return self._serialize_structured_response(response)
        return response.content

    async def a_generate(self, prompt: str, schema: Any = None) -> str:
        model = self._model_for_schema(schema)
        response = await model.ainvoke(
            self._limit_prompt(self._prompt_for_schema(prompt, schema))
        )
        if schema is not None:
            return self._serialize_structured_response(response)
        return response.content

    def get_model_name(self) -> str:
        return "groq/openai/gpt-oss-20b"

    def _model_for_schema(self, schema: Any) -> Any:
        if schema is None:
            return self.model
        return self.model.with_structured_output(
            method="json_mode",
        )

    @staticmethod
    def _prompt_for_schema(prompt: str, schema: Any) -> str:
        if schema is None:
            return prompt

        schema_json = schema.model_json_schema()
        return (
            f"{prompt}\n\nReturn only valid JSON matching this schema:\n"
            f"{json.dumps(schema_json)}"
        )

    @staticmethod
    def _serialize_structured_response(response: Any) -> str:
        if hasattr(response, "model_dump"):
            return json.dumps(response.model_dump())
        if isinstance(response, dict):
            return json.dumps(response)
        raise TypeError(
            f"Structured evaluation response has unsupported type: {type(response)!r}"
        )

    @staticmethod
    def _limit_prompt(prompt: str) -> str:
        max_chars = 4000
        if len(prompt) <= max_chars:
            return prompt

        half = max_chars // 2
        return (
            prompt[:half]
            + "\n\n[Middle of evaluation trace omitted to respect Groq limits.]\n\n"
            + prompt[-half:]
        )


eval_model = GroqEvalModel()
