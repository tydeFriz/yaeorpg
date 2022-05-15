from models.buff import Buff
from models.enums.attribute_enum import Attribute


class LingeringNextAttackIsSpell(Buff):

	def __init__(self, talent_level: int):
		alterations = {}
		if talent_level > 0:
			alterations[Attribute.SP] = talent_level * 10

		super().__init__(
			'next attack is also considered a spell',
			2,
			False,
			alterations
		)
