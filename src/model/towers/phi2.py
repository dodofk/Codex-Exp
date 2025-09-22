"""Phi-2 LoRA text tower implementation."""

from __future__ import annotations

from dataclasses import dataclass
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

    def __post_init__(self) -> None:
        if torch is None:  # pragma: no cover - import guard
            raise ImportError("torch/transformers/peft must be installed for Phi2LoRATextTower")

        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.tokenizer.model_max_length = self.max_length
        self.model = AutoModel.from_pretrained(self.checkpoint, torch_dtype=torch.float32)
        lora_config = LoraConfig(
            r=self.adapter_rank,
            lora_alpha=self.adapter_rank * 2,
            target_modules=list(self.target_modules),
            lora_dropout=0.05,
            bias="none",
        )
        self.model = get_peft_model(self.model, lora_config)
        self.embedding_dim = self.model.config.hidden_size
        self._device = torch.device(self.device)
        self.model.to(self._device)

    @classmethod
    def from_config(cls, config: Mapping[str, Any]) -> "Phi2LoRATextTower":
        params = {
            "checkpoint": config.get("checkpoint", cls.checkpoint),
            "adapter_rank": int(config.get("adapter_rank", cls.adapter_rank)),
            "target_modules": tuple(config.get("target_modules", cls.target_modules)),
            "max_length": int(config.get("max_length", cls.max_length)),
            "device": config.get("device", cls.device),
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


__all__ = ["Phi2LoRATextTower"]
