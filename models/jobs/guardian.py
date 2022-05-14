from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Guardian(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.GUARDIAN_REGEN_HIT
		if secondary_trait:
			trait = Trait.GUARDIAN_RESIST_UP
		super().__init__(
			JobName.GUARDIAN.value,
			34,
			10,
			1,
			trait,
			[],#todo
			[]#todo
		)
