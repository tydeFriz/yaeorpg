from models.enums.attribute_enum import Attribute


class Gem:

	def __init__(
			self,
			name: str,
			attribute: Attribute,
			value: int
	):
		self.name: str = name
		self.attribute: Attribute = attribute
		self.value: int = value
