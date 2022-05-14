from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.action import Action
	from state_machine.runner import Runner

from abc import abstractmethod, ABC


class ActionComponent(ABC):

	def __init__(
			self,
			action: Action
	):
		self.action: Action = action

	@abstractmethod
	def run(self, runner: Runner) -> None:
		"""
		Execute the component
		"""
		pass
