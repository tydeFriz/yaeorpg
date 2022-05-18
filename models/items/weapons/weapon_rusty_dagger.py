from models.enums.attribute_enum import Attribute
from models.items import Weapon


class WeaponRustyDagger(Weapon):

	def __init__(self):
		super().__init__(
			'Rusty dagger',
			{
				Attribute.AP: 1
			},
			1,
			1
		)
