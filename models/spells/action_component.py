from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.action import Action
	from state_machine.runner import Runner

from abc import abstractmethod, ABC
from models.enums.component_memory_enum import ComponentMemory


class ActionComponent(ABC):

	def __init__(
			self,
			action: Action
	):
		self.action: Action = action

	@abstractmethod
	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		"""
		Execute the component

		:param runner: the calling runner
		:param component_memory: the current component memory
		:return: the updated component memory
		"""
		pass
