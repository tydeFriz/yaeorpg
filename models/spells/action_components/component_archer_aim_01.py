from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from models.buffs.archer_lingering_next_attack_is_spell import ArcherLingeringNextAttackIsSpell
from state_machine.procedures.apply_lingering_procedure import ApplyLingeringProcedure


class ComponentArcherAim01(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[str, str]) -> None:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return

		ApplyLingeringProcedure.run(target, ArcherLingeringNextAttackIsSpell(self.action.talent_level))
