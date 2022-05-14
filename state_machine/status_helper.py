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
