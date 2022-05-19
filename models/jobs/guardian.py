from models.enums.job_name_enum import JobName
from models.enums.talent_enum import Talent
from models.enums.trait_enum import Trait
from models.helpers.talent_helper import TalentHelper
from models.job import Job


class Guardian(Job):

	def __init__(
			self,
			secondary_trait: bool,
			talents: dict[Talent, int]
	):
		trait = Trait.GUARDIAN_REGEN_HIT
		if secondary_trait:
			trait = Trait.GUARDIAN_RESIST_UP

		spells = []
		talent_attributes = {}
		for talent, value in talents.items():
			if value < 1:
				continue
			attribute_talent = TalentHelper.get_attribute(JobName.GUARDIAN, talent)
			if attribute_talent:
				talent_attributes[attribute_talent] = TalentHelper.get_value(JobName.GUARDIAN, talent) * value
			else:
				spells.append(TalentHelper.get_spell(JobName.GUARDIAN, talent)(value))

		super().__init__(
			JobName.GUARDIAN.value,
			34,
			10,
			1,
			trait,
			spells,
			talent_attributes
		)
