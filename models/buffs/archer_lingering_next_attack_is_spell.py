from models.buff import Buff
from models.enums.attribute_enum import Attribute


class ArcherLingeringNextAttackIsSpell(Buff):

	def __init__(self, talent_level: int):
		alterations = {
			Attribute.SP: (talent_level - 1) * 10
		}

		super().__init__(
			'next attack is also considered a spell',
			2,
			False,
			alterations
		)
