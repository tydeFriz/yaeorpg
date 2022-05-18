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
from models.spells.action_components.component_archer_piercing_arrow_01 import ComponentArcherPiercingArrow01


class ArcherPiercingArrow(Action):

	def __init__(self, toon: Toon, talent_level: int):
		super().__init__(toon, talent_level, 50)

	def toon_can_cast(self) -> bool:
		return self.toon_has_mana() and self.toon.status not in [
			Status.ASLEEP,
			Status.BOUND,
			Status.CONTROLLED,
			Status.FROZEN,
			Status.SILENCED,
			Status.STUNNED
		]
