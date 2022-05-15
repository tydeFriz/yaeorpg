from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon
	from models.buff import Buff


class ApplyBuffProcedure:

	@classmethod
	def run(cls, target: Toon, effect: Buff):
		target.buff(effect)
