from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from state_machine.procedures.apply_debuff_procedure import ApplyDebuffProcedure
from models.enums.component_memory_enum import ComponentMemory
from state_machine.procedures.attack_procedure import AttackProcedure
from models.enums.trait_enum import Trait


class ComponentArcherRevengeArrow01(ActionComponent):
	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		debuffs_to_move = []
		while self.action.toon.debuffs:
			debuffs_to_move.append(self.action.toon.un_debuff())
		component_memory[ComponentMemory.REVENGE_ARROW_MOVED_DEBUFFS] = str(len(debuffs_to_move))

		for debuff in debuffs_to_move:
			ApplyDebuffProcedure.run(target, debuff)

		return component_memory


class ComponentArcherRevengeArrow02(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		if ComponentMemory.REVENGE_ARROW_MOVED_DEBUFFS not in component_memory:
			component_memory[ComponentMemory.REVENGE_ARROW_MOVED_DEBUFFS] = '0'

		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		multiplier = 0.1 \
			* (self.action.talent_level - 1) \
			* int(component_memory[ComponentMemory.REVENGE_ARROW_MOVED_DEBUFFS])
		if self.action.toon.job.trait == Trait.ARCHER_DAMAGE_INCREASE and runner.is_in_front(target.name):
			multiplier += 0.5

		AttackProcedure.run(self.action.toon, target, damage_multiplier=1.0 + multiplier)
		return component_memory
