from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
	from models.enums.event_enum import Event
	from models.toon import Toon

from models.trigger import Trigger
from state_machine.procedures.attack_procedure import AttackProcedure


class GuardianAnchorHowlTrigger(Trigger):

	def __init__(self):
		super().__init__(Event.ON_ATTACKED, 2)

	def run(self, actor: Toon, causes: list[Toon], _: dict[str, Union[int, str]]) -> bool:
		if self.procs < 1 or not actor or not causes:
			return False
		self.procs -= 1

		target = causes[0]
		AttackProcedure.run(actor, target, damage_multiplier=1.5)
