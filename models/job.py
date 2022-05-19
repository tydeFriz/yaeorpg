from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.action import Action
	from models.spell import Spell
	from models.toon import Toon

from models.enums.trait_enum import Trait
from models.enums.attribute_enum import Attribute
from models.spells.actions.base_weapon_attack import BaseWeaponAttack


class Job:

	def __init__(
			self,
			name: str,
			hp_base: int,
			tp_base: int,
			speed: int,
			trait: Trait,
			spells: list[Spell],
			talent_attributes: dict[Attribute, int]
	):
		self.name: str = name
		self.hp_base: int = hp_base
		self.tp_base: int = tp_base
		self.speed: int = speed
		self.trait: Trait = trait
		self.spells: list[Spell] = spells
		self.talent_attributes = talent_attributes

	def get_available_actions(self, toon: Toon) -> list[Action]:
		"""
		Get a list of all action the toon can take

		:param toon: the toon to check
		:return: the list of available actions
		"""
		actions = self._get_actions(toon)
		actions.append(BaseWeaponAttack(toon))

		available_actions = []

		for action in actions:
			if action.toon_can_cast() and len(action.get_valid_targets()) > 0:
				available_actions.append(action)

		return available_actions

	def _get_actions(self, caster: Toon) -> list[Action]:
		actions = []
		for spell in self.spells:
			actions.append(spell.make_action(caster))
		return actions

	def _get_custom_actions(self) -> list[Action]:
		pass
