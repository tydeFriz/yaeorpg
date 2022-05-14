from models.enums.attribute_enum import Attribute
from models.enums.item_enums import EquipCategory
from models.equip import Equip


class Weapon(Equip):

	def __init__(
			self,
			name: str,
			modifiers: dict[Attribute, int],
			range_min: int,
			range_max: int
	):
		super().__init__(
			name,
			EquipCategory.WEAPON,
			modifiers
		)

		self.range_min: int = range_min
		self.range_max: int = range_max
