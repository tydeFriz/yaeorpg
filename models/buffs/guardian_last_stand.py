from models.buff import Buff


class GuardianLastStand(Buff):

	def __init__(self):
		super().__init__(
			'last stand',
			2,
			True,
			{}
		)
