from models.enums.attribute_enum import Attribute
from models.enums.item_enums import EquipCategory
from models.equip import Equip


class ArmorClothScraps(Equip):

	def __init__(self):
		super().__init__(
			'Cloth scraps',
			EquipCategory.ARMOR,
			{
				Attribute.ARMOR: 1
			}
		)
