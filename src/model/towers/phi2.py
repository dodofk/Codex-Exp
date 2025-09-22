"""Phi-2 LoRA text tower implementation."""

from __future__ import annotations

from dataclasses import dataclass
import warnings
from typing import Any, Iterable, Mapping

try:  # pragma: no cover - optional heavy deps
    import torch
    from transformers import AutoModel, AutoTokenizer
    from peft import LoraConfig, get_peft_model
except ImportError:  # pragma: no cover - torch stack optional
    torch = None  # type: ignore

from ..interfaces import Batch, Configurable, TextTower
from ..registries import register_text_tower


@dataclass
class Phi2LoRATextTower(TextTower, Configurable):
    """Text tower backed by Phi-2 (or compatible) with LoRA adapters."""

    checkpoint: str = "microsoft/phi-2"
    adapter_rank: int = 16
    target_modules: tuple[str, ...] = ("q_proj", "v_proj")
    max_length: int = 256
    device: str = "cpu"
    enable_lora: bool = True
    torch_dtype: str = "float32"
    trust_remote_code: bool = False
    pad_token: str | None = None
    padding_side: str = "left"

    def __post_init__(self) -> None:
        if torch is None:  # pragma: no cover - import guard
            raise ImportError("torch/transformers/peft must be installed for Phi2LoRATextTower")

        tokenizer_kwargs: dict[str, Any] = {}
        if self.trust_remote_code:
            tokenizer_kwargs["trust_remote_code"] = True
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint, **tokenizer_kwargs)
        if self.pad_token:
            self.tokenizer.pad_token = self.pad_token
        elif self.tokenizer.pad_token is None:
            # GPT-style tokenizers often lack padding tokens; fall back to EOS for batching.
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = self.padding_side
        self.tokenizer.model_max_length = self.max_length

        dtype_lookup = {
            "float32": torch.float32,
            "fp32": torch.float32,
            "float16": torch.float16,
            "fp16": torch.float16,
            "half": torch.float16,
            "bfloat16": torch.bfloat16,
            "bf16": torch.bfloat16,
        }
        dtype = dtype_lookup.get(self.torch_dtype.lower(), torch.float32)

        model_kwargs: dict[str, Any] = {"torch_dtype": dtype}
        if self.trust_remote_code:
            model_kwargs["trust_remote_code"] = True

        base_model = AutoModel.from_pretrained(self.checkpoint, **model_kwargs)

        self.model = base_model
        if self.enable_lora and self.adapter_rank > 0:
            lora_config = LoraConfig(
                r=self.adapter_rank,
                lora_alpha=self.adapter_rank * 2,
                target_modules=list(self.target_modules),
                lora_dropout=0.05,
                bias="none",
            )
            try:
                self.model = get_peft_model(base_model, lora_config)
            except ValueError:
                warnings.warn(
                    "LoRA target modules not found on base model; continuing without adapter injection.",
                    RuntimeWarning,
                )
                self.model = base_model
        self.embedding_dim = self.model.config.hidden_size
        self._device = torch.device(self.device)
        self.model.to(self._device)

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "Phi2LoRATextTower":
        def _to_tuple(value: Any) -> tuple[str, ...]:
            if value is None:
                return cls.target_modules
            if isinstance(value, (list, tuple)):
                return tuple(str(v) for v in value)
            return tuple(str(value).split(","))

        def _to_bool(value: Any, default: bool = False) -> bool:
            if value is None:
                return default
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.strip().lower() in {"1", "true", "yes", "y"}
            return bool(value)

        params = {
            "checkpoint": config.get("checkpoint", cls.checkpoint),
            "adapter_rank": int(config.get("adapter_rank", cls.adapter_rank)),
            "target_modules": _to_tuple(config.get("target_modules", cls.target_modules)),
            "max_length": int(config.get("max_length", cls.max_length)),
            "device": config.get("device", cls.device),
            "enable_lora": _to_bool(config.get("enable_lora"), cls.enable_lora),
            "torch_dtype": str(config.get("torch_dtype", cls.torch_dtype)),
            "trust_remote_code": _to_bool(config.get("trust_remote_code"), cls.trust_remote_code),
            "pad_token": config.get("pad_token", cls.pad_token),
            "padding_side": config.get("padding_side", cls.padding_side),
        }
        return cls(**params)

    def embed_text(self, batch: Batch) -> Any:
        if torch is None:  # pragma: no cover - defensive
            raise RuntimeError("torch not available")

        if "text_tokens" in batch:
            tokens = torch.tensor(batch["text_tokens"], dtype=torch.long, device=self._device)
            attention_mask = torch.ones_like(tokens)
        elif "text" in batch:
            encoded = self.tokenizer(
                batch["text"],
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.max_length,
            )
            tokens = encoded["input_ids"].to(self._device)
            attention_mask = encoded["attention_mask"].to(self._device)
        else:
            raise ValueError("Batch must contain 'text_tokens' or 'text'")

        with torch.no_grad():
            outputs = self.model(input_ids=tokens, attention_mask=attention_mask)
            hidden = outputs.last_hidden_state  # shape: [batch, seq, hidden]
            embeddings = hidden.mean(dim=1)  # mean pooling
        return embeddings

    def to(self, device: Any) -> None:
        if torch is None:  # pragma: no cover
            return
        self._device = torch.device(device)
        self.model.to(self._device)

    def parameters(self) -> Iterable[Any]:
        if torch is None:  # pragma: no cover
            return []
        return self.model.parameters()


register_text_tower("phi2_lora", Phi2LoRATextTower)


@dataclass
class Qwen3TextTower(Phi2LoRATextTower):
    """CPU-friendly default configuration for Qwen3 checkpoints."""

    checkpoint: str = "Qwen/Qwen3-0.6B"
    adapter_rank: int = 8
    target_modules: tuple[str, ...] = ("q_proj", "k_proj", "v_proj", "o_proj")
    enable_lora: bool = False
    trust_remote_code: bool = True


@dataclass
class Qwen3LoRATextTower(Qwen3TextTower):
    """Qwen3 variant with LoRA enabled by default."""

    enable_lora: bool = True


register_text_tower("qwen3", Qwen3TextTower)
register_text_tower("qwen3_lora", Qwen3LoRATextTower)


__all__ = [
    "Phi2LoRATextTower",
    "Qwen3TextTower",
    "Qwen3LoRATextTower",
]
