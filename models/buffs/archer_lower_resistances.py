from models.buff import Buff
from models.enums.attribute_enum import Attribute


class ArcherLowerResistances(Buff):

	def __init__(self, talent_level: int):
		alterations = {
			Attribute.ARMOR: - 20 - (talent_level * 10),
			Attribute.SPELL_RES: - 20 - (talent_level * 10)
		}

		super().__init__(
			'lower armor and spell resistance',
			5,
			True,
			alterations
		)
