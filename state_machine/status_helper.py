from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon

from models.buff import Buff
from models.enums.attribute_enum import Attribute
from models.enums.status_enum import Status


class StatusHelper:

	@classmethod
	def get_alterations_from_status(cls, status: Status) -> list[Buff]:
		if status == Status.SLOWED:
			return [Buff(
				"abstract_slow_debuff",
				0,
				False,
				{
					Attribute.SPEED: -5
				}
			)]

		return []

	@classmethod
	def is_toon_immune(cls, toon: Toon, status: Status) -> bool:
		return False #todo
