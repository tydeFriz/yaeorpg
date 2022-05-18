from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon

from random import randint
from math import floor
from models.buffs.archer_lingering_next_attack_is_spell import ArcherLingeringNextAttackIsSpell
from models.enums.attribute_enum import Attribute


class AttackProcedure:

	@classmethod
	def run(
			cls,
			caster: Toon,
			target: Toon,
			damage_multiplier: float = 1.0,
			armor_multiplier: float = 1.0,
			spell_res_multiplier: float = 1.0,
			hit_rate_multiplier: float = 1.0
	):
		if hit_rate_multiplier < 1.0:
			success = int(hit_rate_multiplier * 1000) < randint(1, 1000)
			if not success:
				print("attack missed!")
				return

		effect_attack_is_spell = None
		for lingering in caster.lingering_effects:
			if type(lingering) is ArcherLingeringNextAttackIsSpell:
				effect_attack_is_spell = lingering

		damage_amount = caster.get_attribute(Attribute.AP) * damage_multiplier
		if effect_attack_is_spell is not None:
			damage_amount += caster.get_attribute(Attribute.SP)
		damage_amount = max(damage_amount, 0)

		armor = target.get_attribute(Attribute.ARMOR) * armor_multiplier
		spell_res = target.get_attribute(Attribute.SPELL_RES) * spell_res_multiplier

		damage_amount = damage_amount * (1.0 - (armor / 100.0))
		if effect_attack_is_spell is not None:
			damage_amount = damage_amount * (1.0 - (spell_res / 100.0))

		target.damage(floor(damage_amount))
