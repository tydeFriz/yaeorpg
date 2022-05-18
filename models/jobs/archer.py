from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job
from models.spells.spell_archer_aim import SpellArcherAim
from models.spells.spell_archer_piercing_arrow import SpellArcherPiercingArrow
from models.spells.spell_archer_revenge_arrow import SpellArcherRevengeArrow
from models.spells.spell_archer_vigor import SpellArcherVigor
from models.spells.spell_archer_tracking_arrow import SpellArcherTrackingArrow
from models.spells.spell_archer_cripple import SpellArcherCripple


class Archer(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.ARCHER_RANGE_ALL
		if secondary_trait:
			trait = Trait.ARCHER_DAMAGE_INCREASE
		super().__init__(
			JobName.ARCHER.value,
			22,
			12,
			7,
			trait,
			[
				SpellArcherAim(2),
				SpellArcherVigor(2),
				SpellArcherTrackingArrow(2),
				SpellArcherRevengeArrow(2),
				SpellArcherCripple(2),
				SpellArcherPiercingArrow(2),#todo
			],
			[]#todo
		)

