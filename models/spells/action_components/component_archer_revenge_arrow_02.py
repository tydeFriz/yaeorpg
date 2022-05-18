from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from state_machine.procedures.attack_procedure import AttackProcedure
from models.enums.trait_enum import Trait


class ComponentArcherRevengeArrow02(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[str, str]) -> dict[str, str]:
		if 'removed_debuffs' not in component_memory:
			component_memory['removed_debuffs'] = '0'

		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		multiplier = 0.1 * (self.action.talent_level - 1) * int(component_memory['removed_debuffs'])
		if self.action.toon.job.trait == Trait.ARCHER_DAMAGE_INCREASE and runner.is_in_front(target.name):
			multiplier += 0.5

		AttackProcedure.run(self.action.toon, target, 1.0 + multiplier)
		return component_memory
