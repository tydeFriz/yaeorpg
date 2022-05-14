from abc import ABC, abstractmethod

from models.action import Action


class Spell(ABC):

	def __init__(self):
		pass  # todo

	@abstractmethod
	def make_action(self) -> Action:
		pass
