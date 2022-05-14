from models.enums.talent_enums import TalentType
from models.talent import Talent


class SpellTalent(Talent):

	def __init__(
			self,
			name: str
	):
		super().__init__(name, TalentType.SPELL_MODIFIER)
