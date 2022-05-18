from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from state_machine.procedures.attack_procedure import AttackProcedure
from models.enums.trait_enum import Trait
from models.enums.component_memory_enum import ComponentMemory


class ComponentArcherPiercingArrow01(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		multiplier = 1.0
		if self.action.toon.job.trait == Trait.ARCHER_DAMAGE_INCREASE and runner.is_in_front(target.name):
			multiplier += 0.5

		AttackProcedure.run(self.action.toon, target, damage_multiplier=multiplier, armor_multiplier=0.0)
		return component_memory
