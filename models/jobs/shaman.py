from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Shaman(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.SHAMAN_TOTEM_HEAL
		if secondary_trait:
			trait = Trait.SHAMAN_TOTEM_REGEN
		super().__init__(
			JobName.SHAMAN.value,
			22,
			18,
			6,
			trait,
			[],#todo
			[]#todo
		)
