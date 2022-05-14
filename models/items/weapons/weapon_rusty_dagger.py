from models.enums.attribute_enum import Attribute
from models.enums.item_enums import EquipCategory
from models.items import Weapon


class WeaponRustyDagger(Weapon):

	def __init__(self):
		super().__init__(
			'Rusty dagger',
			EquipCategory.WEAPON,
			{
				Attribute.AP: 1
			}
		)
