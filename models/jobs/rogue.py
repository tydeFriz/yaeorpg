from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Rogue(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.ROGUE_STATUS_DAMAGE
		if secondary_trait:
			trait = Trait.ROGUE_STATUS_UP
		super().__init__(
			JobName.ROGUE.value,
			22,
			8,
			8,
			trait,
			[],#todo
			{}#todo
		)
