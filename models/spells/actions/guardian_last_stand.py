from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.spells.action_component import ActionComponent
	from models.toon import Toon

from models.action import Action
from models.enums.attribute_enum import Attribute
from models.enums.status_enum import Status
from helpers import RangeHelper
from models.spells.action_components.component_guardian_last_stand import ComponentGuardianLastStand01


class GuardianLastStand(Action):

	def __init__(self, toon: Toon, talent_level: int):
		super().__init__(toon, talent_level, 70 - (10 * talent_level))

	def toon_can_cast(self) -> bool:
		return self.toon_has_mana() and self.toon.status not in [
			Status.ASLEEP,
			Status.CONTROLLED,
			Status.FROZEN,
			Status.SILENCED,
			Status.STUNNED
		]

	def get_valid_targets(self) -> list[str]:
		return [self.toon.name]

	def get_speed(self) -> int:
		return self.toon.get_attribute(Attribute.SPEED) + 10

	def _compose(self) -> list[ActionComponent]:
		return [
			ComponentGuardianLastStand01(self)
		]

	def _finalise(self, targets: list[str]) -> bool:
		if len(targets) != 1:
			return False

		self._targets = targets
		return True

	def _make_description(self) -> str:
		return "use Last Stand"
