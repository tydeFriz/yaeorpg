from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Hexer(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.HEXER_DRAIN_HP
		if secondary_trait:
			trait = Trait.HEXER_DRAIN_TP
		super().__init__(
			JobName.HEXER.value,
			16,
			24,
			4,
			trait,
			[],#todo
			{}#todo
		)
