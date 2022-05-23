from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
	from models.toon import Toon

from models.enums.event_enum import Event
from models.trigger import Trigger
from state_machine.procedures.attack_procedure import AttackProcedure
from models.buffs.guardian_lingering_attack_riposte import GuardianLingeringAttackRiposte


class GuardianAnchorHowlTrigger(Trigger):

	def __init__(self, caster: Toon):
		super().__init__(Event.ON_ATTACKED, 1)
		self.caster = caster

	def run(self, actor: Toon, causes: list[Toon], _: dict[str, Union[int, str]]) -> bool:

		if len(causes) != 1:
			return False
		if not causes[0]:
			return False

		for effect in self.caster.lingering_effects:
			if isinstance(effect, GuardianLingeringAttackRiposte):
				if not effect.proc():
					continue

				target = causes[0]
				AttackProcedure.run(actor, target, damage_multiplier=1.5)
				return True

		return False

