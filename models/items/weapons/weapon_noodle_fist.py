from models.items.weapon import Weapon


class WeaponNoodleFist(Weapon):

	def __init__(self):
		super().__init__(
			'Unarmed',
			{},
			1,
			1
		)
