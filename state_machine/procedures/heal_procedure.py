from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon

from math import floor


class HealProcedure:

	@classmethod
	def run(
			cls,
			target: Toon,
			heal_amount: float,
			heal_multiplier: float = 1.0
	):

		target.heal(floor(heal_amount * heal_multiplier))
