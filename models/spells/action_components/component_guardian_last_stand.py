from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from state_machine.procedures.apply_buff_procedure import ApplyBuffProcedure
from models.spells.action_component import ActionComponent
from models.enums.component_memory_enum import ComponentMemory
from models.buffs.guardian_last_stand import GuardianLastStand


class ComponentGuardianLastStand01(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		ApplyBuffProcedure.run(target, GuardianLastStand())
		return component_memory
