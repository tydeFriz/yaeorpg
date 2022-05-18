from models.buff import Buff
from models.enums.attribute_enum import Attribute


class ArcherLowerSpeed(Buff):

	def __init__(self, talent_level: int):
		duration = 3 + talent_level
		alterations = {
			Attribute.SPEED: -4,
		}

		super().__init__(
			'lower turn speed',
			duration,
			False,
			alterations
		)
