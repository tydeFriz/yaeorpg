from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from state_machine.procedures.apply_debuff_procedure import ApplyDebuffProcedure
from models.buffs.archer_lower_resistances import ArcherLowerResistances


class ComponentArcherTrackingArrow02(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[str, str]) -> dict[str, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		ApplyDebuffProcedure.run(target, ArcherLowerResistances(self.action.talent_level))
		return component_memory
