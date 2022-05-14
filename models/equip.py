from models.enums.attribute_enum import Attribute
from models.enums.item_enums import EquipCategory


class Equip:

	def __init__(
			self,
			name: str,
			category: EquipCategory,
			modifiers: dict[Attribute, int]
			#todo: i'd like to add onAttack(), onHit() and stuff like that in the future
	):
		self.name: str = name
		self.category: EquipCategory = category
		self.modifiers: dict[Attribute, int] = {}
		for stat in Attribute:
			self.modifiers[stat] = 0
			if stat in modifiers:
				self.modifiers[stat] = modifiers[stat]
