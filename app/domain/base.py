from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Self
from pydantic import BaseModel, ConfigDict

P = TypeVar("P")


class ProtoModel(BaseModel, Generic[P], ABC):
    model_config = ConfigDict(extra="forbid")

    @abstractmethod
    def to_proto(self) -> P: ...

    @classmethod
    @abstractmethod
    def from_proto(cls, pb: P) -> Self: ...
