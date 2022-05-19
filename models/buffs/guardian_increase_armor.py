from models.buff import Buff
from models.enums.attribute_enum import Attribute


class GuardianIncreaseArmor(Buff):

	def __init__(self):
		duration = 4
		alterations = {
			Attribute.ARMOR: 20,
		}

		super().__init__(
			'increase armor',
			duration,
			True,
			alterations
		)
