from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner

from models.spells.action_component import ActionComponent
from models.buffs.guardian_lingering_attack_riposte import GuardianLingeringAttackRiposte
from models.triggers.guardian_anchor_howl_trigger import GuardianAnchorHowlTrigger
from state_machine.procedures.apply_lingering_procedure import ApplyLingeringProcedure
from models.enums.component_memory_enum import ComponentMemory


class ComponentGuardianAnchorHowl01(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		target = runner.get_toon_by_name(self.action.get_targets()[0])
		if not target:
			return component_memory

		ApplyLingeringProcedure.run(target, GuardianLingeringAttackRiposte())
		return component_memory


class ComponentGuardianAnchorHowl02(ActionComponent):

	def run(self, runner: Runner, component_memory: dict[ComponentMemory, str]) -> dict[ComponentMemory, str]:
		caster = runner.get_toon_by_name(self.action.get_targets()[0])
		if not caster:
			return component_memory

		for toon in runner.get_toon_allies(caster).values():
			toon.triggers.append(GuardianAnchorHowlTrigger(self.action.toon))

		return component_memory
