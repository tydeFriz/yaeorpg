from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
	from models.enums.event_enum import Event
	from models.toon import Toon

from abc import abstractmethod, ABC


class Trigger(ABC):

	def __init__(
			self,
			event: Event,
			duration: int
	):
		self.event = event
		self.duration = duration

	@abstractmethod
	def run(self, actor: Toon, causes: list[Toon], additional_info: dict[str, Union[int, str]]) -> bool:
		pass
