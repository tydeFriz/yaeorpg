from models.buff import Buff
from models.enums.attribute_enum import Attribute


class GuardianLowerArmor(Buff):

	def __init__(self, talent_level: int):
		duration = 4
		alterations = {
			Attribute.ARMOR: -19 - (7 * talent_level),
		}

		super().__init__(
			'decrease armor',
			duration,
			True,
			alterations
		)
