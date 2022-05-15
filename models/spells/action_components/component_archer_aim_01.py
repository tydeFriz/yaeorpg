from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from models.buffs.lingering_next_attack_is_spell import LingeringNextAttackIsSpell
from state_machine.procedures.apply_lingering_procedure import ApplyLingeringProcedure


class ComponentArcherAim01(ActionComponent):

	def run(self, runner: Runner) -> None:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return

		ApplyLingeringProcedure.run(target, LingeringNextAttackIsSpell(self.action.talent_level))
