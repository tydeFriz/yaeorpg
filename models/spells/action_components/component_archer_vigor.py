from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from models.buffs.archer_lingering_next_spell_is_attack import ArcherLingeringNextSpellIsAttack
from state_machine.procedures.apply_lingering_procedure import ApplyLingeringProcedure
from models.enums.component_memory_enum import ComponentMemory


class ComponentArcherVigor01(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		ApplyLingeringProcedure.run(target, ArcherLingeringNextSpellIsAttack(self.action.talent_level))
		return component_memory
