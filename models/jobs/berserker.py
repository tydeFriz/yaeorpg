from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Berserker(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.BERSERKER_HEAL_HIT
		if secondary_trait:
			trait = Trait.BERSERKER_AP_UP
		super().__init__(
			JobName.BERSERKER.value,
			32,
			8,
			6,
			trait,
			[],#todo
			[]#todo
		)
