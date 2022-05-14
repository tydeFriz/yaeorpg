from models.enums.talent_enums import TalentType


class Talent:

	def __init__(
			self,
			name: str,
			talent_type: TalentType
	):
		self.name: str = name
		self.talent_type: TalentType = talent_type
