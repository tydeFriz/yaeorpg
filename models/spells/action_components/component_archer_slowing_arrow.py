from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from state_machine.procedures.apply_status_procedure import ApplyStatusProcedure
from models.enums.component_memory_enum import ComponentMemory
from models.enums.status_enum import Status


class ComponentArcherSlowingArrow01(ActionComponent):
	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		ApplyStatusProcedure.run(target, Status.SLOWED)
		return component_memory
