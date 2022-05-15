from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
	from models.action import Action
	from models.toon import Toon

from abc import ABC, abstractmethod


class Spell(ABC):

	def __init__(self, talent_level: int):
		if not 1 < talent_level < 4:
			raise Exception("cannot have a spell with " + str(talent_level) + " talent points")
		self.talent_level = talent_level

	@abstractmethod
	def make_action(self, caster: Toon) -> Action:
		"""
		Make the action that will be executed by casting this spell

		:param caster: the toon that will cast the action
		:return: the castable action
		"""
		pass
