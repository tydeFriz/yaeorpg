from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
	from state_machine.runner import Runner
	from models.toon import Toon

from models.spells.action_component import ActionComponent
from models.enums.component_memory_enum import ComponentMemory
from state_machine.procedures.swap_toons_procedure import SwapToonsProcedure


def _get_new_pos(team: dict[str, Optional[Toon]]) -> str:
	for p, toon in team.items():
		if 'b' in p and toon is None:
			return p
	return ''


class ComponentGuardianKnockback01(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		target_team = 1
		target_pos = ''
		target_new_pos = ''
		for p, toon in runner.p1_team.items():
			if toon and toon.name == target.name:
				target_pos = p
				target_new_pos = _get_new_pos(runner.p1_team)
				break

		if target_pos == '':
			target_team = 2
			for p, toon in runner.p2_team.items():
				if toon and toon.name == target.name:
					target_pos = p
					target_new_pos = _get_new_pos(runner.p2_team)
					break

		if target_pos == '':
			return component_memory

		if target_new_pos == '':
			return component_memory

		SwapToonsProcedure.run(
			runner,
			target_team,
			target_pos,
			target_team,
			target_new_pos,
		)
		return component_memory
