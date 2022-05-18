from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon
	from models.buff import Buff


class ApplyLingeringProcedure:

	@classmethod
	def run(cls, target: Toon, effect: Buff):
		for lingering in target.lingering_effects:
			if type(lingering) is type(effect):
				if lingering.stackable:
					lingering.stack(effect.duration)
				return

		target.lingering_effects.append(effect)
