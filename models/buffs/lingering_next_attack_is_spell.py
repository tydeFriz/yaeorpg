from models.buff import Buff


class LingeringNextAttackIsSpell(Buff):

	def __init__(self):
		super().__init__(
			'next attack is also considered a spell',
			1,
			False,
			{}
		)
