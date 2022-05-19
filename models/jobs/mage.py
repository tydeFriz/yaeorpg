from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Mage(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.MAGE_STATUS_RES
		if secondary_trait:
			trait = Trait.MAGE_SPELL_RESIST
		super().__init__(
			JobName.MAGE.value,
			14,
			26,
			3,
			trait,
			[],#todo
			{}#todo
		)
