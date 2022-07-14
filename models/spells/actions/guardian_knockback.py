from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.spells.action_component import ActionComponent
	from models.toon import Toon

from models.action import Action
from models.enums.status_enum import Status
from models.enums.attribute_enum import Attribute
from models.spells.action_components.component_guardian_knockback import ComponentGuardianKnockback01
from helpers import RangeHelper


class GuardianKnockback(Action):
	def __init__(self, toon: Toon, talent_level: int):
		super().__init__(toon, talent_level, 30)

	def toon_can_cast(self) -> bool:
		return self.toon_has_mana() and self.toon.status not in [
			Status.ASLEEP,
			Status.CONTROLLED,
			Status.FROZEN,
			Status.SILENCED,
			Status.STUNNED
		]

	def get_valid_targets(self) -> list[str]:
		return RangeHelper(
			self.toon,
			1,
			1,
			False,
			True
		).get_valid_targets()

	def get_speed(self) -> int:
		speed = self.toon.get_attribute(Attribute.SPEED) + (5 * self.talent_level)
		return speed

	def _compose(self) -> list[ActionComponent]:
		return [
			ComponentGuardianKnockback01(self)
		]

	def _finalise(self, targets: list[str]) -> bool:
		if len(targets) != 1:
			return False

		self._targets = targets
		return True

	def _make_description(self) -> str:
		return "use Knockback"
