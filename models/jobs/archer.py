from models.enums.job_name_enum import JobName
from models.enums.talent_enum import Talent
from models.enums.trait_enum import Trait
from models.helpers.talent_helper import TalentHelper
from models.job import Job


class Archer(Job):

	def __init__(
			self,
			secondary_trait: bool,
			talents: dict[Talent, int]
	):
		trait = Trait.ARCHER_RANGE_ALL
		if secondary_trait:
			trait = Trait.ARCHER_DAMAGE_INCREASE

		spells = []
		talent_attributes = {}
		for talent, value in talents.items():
			if value < 1:
				continue
			attribute_talent = TalentHelper.get_attribute(JobName.ARCHER, talent)
			if attribute_talent:
				talent_attributes[attribute_talent] = TalentHelper.get_value(JobName.ARCHER, talent) * value
			else:
				spells.append(TalentHelper.get_spell(JobName.ARCHER, talent)(value))

		super().__init__(
			JobName.ARCHER.value,
			22,
			12,
			7,
			trait,
			spells,
			talent_attributes
		)
