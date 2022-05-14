from models.enums.attribute_enum import Attribute


class Buff:

	def __init__(
			self,
			name: str,
			duration: int,
			stackable: bool,
			attribute_alterations: dict[Attribute, int]
	):
		self.name: str = name
		self.duration: int = duration
		self.stackable: bool = stackable
		self.remaining_turns: int = self.duration
		self.attribute_alterations: dict[Attribute, int] = attribute_alterations

	def stack(self, amount: int) -> None:
		"""
		increase the buff's duration by a given amount

		:param amount: the amount to increase duration by
		"""
		self.duration = max(
			0,
			min(self.duration + amount, 9)
		)
