from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from state_machine.procedures.apply_debuff_procedure import ApplyDebuffProcedure


class ComponentArcherRevengeArrow01(ActionComponent):
	def run(self, runner: Runner, component_memory: dict[str, str]) -> dict[str, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		debuffs_to_move = []
		while self.action.toon.debuffs:
			debuffs_to_move.append(self.action.toon.un_debuff())

		for debuff in debuffs_to_move:
			ApplyDebuffProcedure.run(target, debuff)

		return component_memory
