from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.spells.action_component import ActionComponent
	from models.toon import Toon

from models.action import Action
from models.enums.trait_enum import Trait
from models.enums.attribute_enum import Attribute
from models.enums.status_enum import Status
from state_machine.range_helper import RangeHelper
from models.spells.action_components.component_archer_blinding_arrow_01 import ComponentArcherBlindingArrow01


class ArcherBlindingArrow(Action):

	def __init__(self, toon: Toon, talent_level: int):
		super().__init__(toon, talent_level, 60 - (10 * talent_level))

	def toon_can_cast(self) -> bool:
		return self.toon_has_mana() and self.toon.status not in [
			Status.ASLEEP,
			Status.CONTROLLED,
			Status.FROZEN,
			Status.SILENCED,
			Status.STUNNED
		]

	def get_valid_targets(self) -> list[str]:
		range_min = 1
		range_max = 2
		if self.toon.job.trait == Trait.ARCHER_RANGE_ALL:
			range_min = 0
			range_max = 3
		return RangeHelper(
			self.toon,
			range_min,
			range_max,
			True,
			True
		).get_valid_targets()

	def get_speed(self) -> int:
		return self.toon.get_attribute(Attribute.SPEED)

	def _compose(self) -> list[ActionComponent]:
		return [
			ComponentArcherBlindingArrow01(self)
		]

	def _finalise(self, targets: list[str]) -> bool:
		if len(targets) != 1:
			return False

		self._targets = targets
		return True

	def _make_description(self) -> str:
		return "use Blinding Arrow"
