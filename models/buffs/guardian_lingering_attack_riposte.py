from models.buff import Buff


class GuardianLingeringAttackRiposte(Buff):

	def __init__(self):
		super().__init__(
			'attack the first 2 opponents attacking an ally',
			1,
			False,
			{}
		)
		self._procs = 2

	def proc(self) -> bool:
		if self._procs < 1:
			return False
		self._procs -= 1
		return True
