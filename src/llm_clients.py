"""Unified LLM client interface for OpenAI, Gemini, DeepSeek.

Each call returns a dict with the same structure regardless of provider.
"""

from __future__ import annotations
import os
import time
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class LLMResponse:
    """Unified response across providers."""
    provider: str
    model_id: str
    model_id_returned: Optional[str] = None
    text: str = ""
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    finish_reason: Optional[str] = None
    elapsed_s: Optional[float] = None
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


# ------------------------------------------------------------------
# Pricing (USD per 1M tokens) — keep in sync with src/llm_config.yaml
# ------------------------------------------------------------------
PRICING = {
    "gpt": {"input": 2.50, "output": 10.00},
    "gpt-4.1": {"input": 2.50, "output": 10.00},
    "gpt-5": {"input": 2.50, "output": 10.00},
    "gemini": {"input": 3.50, "output": 10.50},
    "gemini-2.5-pro": {"input": 3.50, "output": 10.50},
    "deepseek": {"input": 0.27, "output": 1.10},
    "deepseek-chat": {"input": 0.27, "output": 1.10},
}


def _compute_cost(model_key: str, in_tok: Optional[int], out_tok: Optional[int]) -> Optional[float]:
    p = PRICING.get(model_key)
    if not p or in_tok is None or out_tok is None:
        return None
    return (in_tok / 1_000_000) * p["input"] + (out_tok / 1_000_000) * p["output"]


# ------------------------------------------------------------------
# OpenAI / DeepSeek (DeepSeek is OpenAI-compatible)
# ------------------------------------------------------------------
def call_openai_compatible(
    *,
    provider: str,                  # "gpt" | "deepseek"
    model_id: str,
    system: str,
    user: str,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    seed: Optional[int] = 42,
    api_key_env: str = "OPENAI_API_KEY",
    base_url: Optional[str] = None,
    timeout_s: float = 120.0,
) -> LLMResponse:
    """Call OpenAI or any OpenAI-compatible endpoint (e.g. DeepSeek)."""
    from openai import OpenAI

    api_key = os.environ.get(api_key_env)
    if not api_key:
        return LLMResponse(provider=provider, model_id=model_id,
                           error=f"Missing env var {api_key_env}")

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=timeout_s)
    t0 = time.time()
    try:
        kwargs = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            # Force JSON-parseable output (OpenAI + DeepSeek both support this)
            "response_format": {"type": "json_object"},
        }
        if seed is not None:
            kwargs["seed"] = seed
        resp = client.chat.completions.create(**kwargs)
        elapsed = time.time() - t0
        choice = resp.choices[0]
        text = choice.message.content or ""
        usage = resp.usage
        in_tok = getattr(usage, "prompt_tokens", None) if usage else None
        out_tok = getattr(usage, "completion_tokens", None) if usage else None
        total = getattr(usage, "total_tokens", None) if usage else None
        return LLMResponse(
            provider=provider,
            model_id=model_id,
            model_id_returned=getattr(resp, "model", None),
            text=text,
            input_tokens=in_tok,
            output_tokens=out_tok,
            total_tokens=total,
            cost_usd=_compute_cost(provider, in_tok, out_tok),
            finish_reason=choice.finish_reason,
            elapsed_s=elapsed,
        )
    except Exception as e:
        return LLMResponse(
            provider=provider, model_id=model_id,
            elapsed_s=time.time() - t0,
            error=f"{type(e).__name__}: {e}",
        )


# ------------------------------------------------------------------
# Google Gemini
# ------------------------------------------------------------------
def call_gemini(
    *,
    model_id: str,
    system: str,
    user: str,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    seed: Optional[int] = 42,
    api_key_env: str = "GEMINI_API_KEY",
    timeout_s: float = 120.0,
) -> LLMResponse:
    """Call Google Gemini via google-generativeai SDK."""
    import google.generativeai as genai

    api_key = os.environ.get(api_key_env)
    if not api_key:
        return LLMResponse(provider="gemini", model_id=model_id,
                           error=f"Missing env var {api_key_env}")

    genai.configure(api_key=api_key)
    t0 = time.time()
    try:
        model = genai.GenerativeModel(
            model_name=model_id,
            system_instruction=system,
        )
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        # NOTE: google-generativeai SDK does not accept `seed` in GenerationConfig.
        # Gemini reproducibility is best-effort via T=0.
        resp = model.generate_content(user, generation_config=generation_config)
        elapsed = time.time() - t0
        text = resp.text if hasattr(resp, "text") else ""
        # Token counts
        in_tok = getattr(resp.usage_metadata, "prompt_token_count", None) if hasattr(resp, "usage_metadata") else None
        out_tok = getattr(resp.usage_metadata, "candidates_token_count", None) if hasattr(resp, "usage_metadata") else None
        total = getattr(resp.usage_metadata, "total_token_count", None) if hasattr(resp, "usage_metadata") else None
        finish_reason = None
        if hasattr(resp, "candidates") and resp.candidates:
            finish_reason = str(getattr(resp.candidates[0], "finish_reason", None))
        return LLMResponse(
            provider="gemini",
            model_id=model_id,
            model_id_returned=model_id,
            text=text,
            input_tokens=in_tok,
            output_tokens=out_tok,
            total_tokens=total,
            cost_usd=_compute_cost("gemini", in_tok, out_tok),
            finish_reason=finish_reason,
            elapsed_s=elapsed,
        )
    except Exception as e:
        return LLMResponse(
            provider="gemini", model_id=model_id,
            elapsed_s=time.time() - t0,
            error=f"{type(e).__name__}: {e}",
        )


# ------------------------------------------------------------------
# Dispatcher
# ------------------------------------------------------------------
def call_llm(
    *,
    provider: str,
    model_id: str,
    system: str,
    user: str,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    seed: Optional[int] = 42,
) -> LLMResponse:
    """Provider-agnostic dispatcher."""
    if provider == "gpt":
        return call_openai_compatible(
            provider="gpt", model_id=model_id,
            system=system, user=user,
            temperature=temperature, max_tokens=max_tokens, seed=seed,
            api_key_env="OPENAI_API_KEY",
        )
    elif provider == "deepseek":
        return call_openai_compatible(
            provider="deepseek", model_id=model_id,
            system=system, user=user,
            temperature=temperature, max_tokens=max_tokens, seed=seed,
            api_key_env="DEEPSEEK_API_KEY",
            base_url="https://api.deepseek.com",
        )
    elif provider == "gemini":
        return call_gemini(
            model_id=model_id,
            system=system, user=user,
            temperature=temperature, max_tokens=max_tokens, seed=seed,
        )
    else:
        return LLMResponse(provider=provider, model_id=model_id,
                           error=f"Unknown provider: {provider}")
