from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon

from models.enums.status_enum import Status
from models.enums.attribute_enum import Attribute


class ApplyStatusProcedure:

	@classmethod
	def run(cls, target: Toon, status: Status, counter: int = -1):

		target_resistance = target.get_attribute(Attribute.STATUS_RES)
		if randint(1, 100) < target_resistance:
			return

		target.status = status

		if counter != -1:
			target.status_counter = counter
		else:
			target.status_counter = Status.DEFAULT_COUNTERS[status]
