from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon

from models.buffs.archer_lingering_next_attack_is_spell import ArcherLingeringNextAttackIsSpell
from models.enums.attribute_enum import Attribute


class AttackProcedure:
	# todo: missing hit rating (blind) checks

	@classmethod
	def run(cls, caster: Toon, target: Toon, damage_multiplier: float = 1.0):
		effect_attack_is_spell = None
		for lingering in caster.lingering_effects:
			if type(lingering) is ArcherLingeringNextAttackIsSpell:
				effect_attack_is_spell = lingering

		damage_amount = caster.get_attribute(Attribute.AP) * damage_multiplier
		if effect_attack_is_spell is not None:
			damage_amount += caster.get_attribute(Attribute.SP)
		damage_amount = max(damage_amount, 0)

		damage_amount = floor(damage_amount * (1.0 - (target.get_attribute(Attribute.ARMOR) / 100.0)))
		if effect_attack_is_spell is not None:
			damage_amount = floor(damage_amount * (1.0 - (target.get_attribute(Attribute.SPELL_RES) / 100.0)))

		target.damage(damage_amount)
