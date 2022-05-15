from models.buff import Buff
from models.enums.attribute_enum import Attribute


class ArcherLingeringNextSpellIsAttack(Buff):

	def __init__(self, talent_level: int):
		alterations = {
			Attribute.AP: (talent_level - 1) * 10
		}

		super().__init__(
			'next spell is also considered an attack',
			2,
			False,
			alterations
		)
