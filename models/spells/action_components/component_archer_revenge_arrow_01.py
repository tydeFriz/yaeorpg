from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from state_machine.procedures.apply_debuff_procedure import ApplyDebuffProcedure
from models.enums.component_memory_enum import ComponentMemory


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
