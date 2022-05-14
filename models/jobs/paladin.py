from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Paladin(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.PALADIN_SPELL_ATTACK
		if secondary_trait:
			trait = Trait.PALADIN_ATTACK_SPELL
		super().__init__(
			JobName.PALADIN.value,
			28,
			16,
			3,
			trait,
			[],#todo
			[]#todo
		)
