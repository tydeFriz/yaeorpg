from abc import ABC, abstractmethod
from random import randint

from models.spells.action_component import ActionComponent
from models.toon import Toon


def _make_strid(size: int) -> str:
	times = 1
	number = 0
	for i in range(size):
		number += randint(0, 9) * times
		times *= 10
	return str(number)


class Action(ABC):

	def __init__(
			self,
			toon: Toon,
			talent_level: int,
			tp_cost: int = 0
	):
		self.toon: Toon = toon
		self.strid: str = toon.name + "_" + _make_strid(12)
		self.description: str = toon.name + ": " + self._make_description()
		self.ready_to_run: bool = False
		self.talent_level: int = talent_level
		self.tp_cost = tp_cost
		self._targets: list[str] = []
		self._components: list[ActionComponent] = self._compose()

	@abstractmethod
	def toon_can_cast(self) -> bool:
		"""
		Check if the toon has all the required resources to cast the action
		and if nothing prevents it from doing so

		:return: True when the toon can cast the action, False otherwise
		"""
		pass

	@abstractmethod
	def get_valid_targets(self) -> list[str]:
		"""
		Get the list of valid targets for the action

		:return: The list of toon names the action can target
		"""
		pass

	@abstractmethod
	def get_speed(self) -> int:
		"""
		Get the action's speed

		:return: the action's speed value
		"""
		pass

	def finalise(self, targets: list[str]) -> None:
		"""
		Make the action ready to cast

		:param targets: the list of toon names to target
		"""
		if not self._finalise(targets):
			raise Exception("invalid targets for action " + self.description)
		self.ready_to_run = True

	def get_targets(self) -> list[str]:
		"""
		Get the finalised targets for the action

		:return: the list of target names
		"""
		return self._targets

	def get_components(self) -> list[ActionComponent]:
		"""
		Get the action's runnable components

		:return: the list of action's component, in execution order
		"""
		return self._components

	def toon_has_mana(self):
		return self.toon.tp_current >= self.tp_cost

	@abstractmethod
	def _compose(self) -> list[ActionComponent]:
		pass

	@abstractmethod
	def _finalise(self, targets: list[str]) -> bool:
		pass

	@abstractmethod
	def _make_description(self) -> str:
		"""
		Compose the action's description for human reading

		:return: the human-readable description
		"""
		pass

