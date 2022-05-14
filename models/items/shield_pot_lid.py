from models.enums.attribute_enum import Attribute
from models.enums.item_enums import EquipCategory
from models.equip import Equip


class ShieldPotLid(Equip):

	def __init__(self):
		super().__init__(
			'Pot lid',
			EquipCategory.SHIELD,
			{
				Attribute.ARMOR: 2,
				Attribute.SPEED: -1
			}
		)
