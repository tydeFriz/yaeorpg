from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Medic(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.MEDIC_CRIT_HEAL
		if secondary_trait:
			trait = Trait.MEDIC_REGEN_HIT
		super().__init__(
			JobName.MEDIC.value,
			16,
			20,
			4,
			trait,
			[],#todo
			[]#todo
		)
