from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Bard(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.BARD_MORE_TARGETS
		if secondary_trait:
			trait = Trait.BARD_HEAL_TURN
		super().__init__(
			JobName.BARD.value,
			20,
			16,
			9,
			trait,
			[],#todo
			{}#todo
		)
