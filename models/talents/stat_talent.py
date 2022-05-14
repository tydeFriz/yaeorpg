from models.enums.talent_enums import TalentType
from models.talent import Talent


class StatTalent(Talent):

	def __init__(
			self,
			name: str
	):
		super().__init__(name, TalentType.STAT_MODIFIER)
