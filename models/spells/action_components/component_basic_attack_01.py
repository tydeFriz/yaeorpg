from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner
	from state_machine.procedures.attack_procedure import AttackProcedure

from models.spells.action_component import ActionComponent


class ComponentBasicAttack01(ActionComponent):

	def run(self, runner: Runner) -> None:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return

		AttackProcedure.run(self.action.toon, target)
