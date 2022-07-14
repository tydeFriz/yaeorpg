from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from models.enums.component_memory_enum import ComponentMemory
from state_machine.procedures.heal_procedure import HealProcedure


class ComponentGuardianHealthBoost01(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		amount = 250 / (26 - self.action.toon.level)
		HealProcedure.run(target, amount)
		return component_memory
