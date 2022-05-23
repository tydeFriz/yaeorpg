from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
	from models.spells.action_component import ActionComponent
	from models.toon import Toon
	from models.items import Weapon

from models.action import Action
from models.enums.attribute_enum import Attribute
from models.enums.item_enums import EquipCategory
from models.enums.status_enum import Status
from models.items.weapons.weapon_noodle_fist import WeaponNoodleFist
from helpers import RangeHelper
from models.spells.action_components.component_basic_attack import ComponentBasicAttack01


class BaseWeaponAttack(Action):

	def __init__(self, toon: Toon):
		super().__init__(toon, 1)
		self.weapon: Optional[Weapon] = None

		for item in self.toon.get_equip().values():
			if item and item.category == EquipCategory.WEAPON:
				self.weapon = item
				break

		if self.weapon is None or self.toon.status == Status.DISARMED:
			self.weapon = WeaponNoodleFist()

	def toon_can_cast(self) -> bool:
		return self.toon.status not in [
			Status.ASLEEP,
			Status.BOUND,
			Status.CONTROLLED,
			Status.FROZEN,
			Status.STUNNED
		]

	def get_valid_targets(self) -> list[str]:
		return RangeHelper(
			self.toon,
			self.weapon.range_min,
			self.weapon.range_max,
			True,
			True
		).get_valid_targets()

	def get_speed(self) -> int:
		return self.toon.get_attribute(Attribute.SPEED)

	def _compose(self) -> list[ActionComponent]:
		return [ComponentBasicAttack01(self)]

	def _finalise(self, targets: list[str]) -> bool:
		if len(targets) != 1:
			return False

		self._targets = targets
		return True

	def _make_description(self) -> str:
		return "Attack"
