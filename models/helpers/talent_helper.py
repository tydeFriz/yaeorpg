from typing import Optional
from models.enums.attribute_enum import Attribute
from models.enums.job_name_enum import JobName
from models.enums.talent_enum import Talent
from models.spell import Spell
from models.spells.spell_archer_aim import SpellArcherAim
from models.spells.spell_archer_blinding_arrow import SpellArcherBlindingArrow
from models.spells.spell_archer_piercing_arrow import SpellArcherPiercingArrow
from models.spells.spell_archer_poison_arrow import SpellArcherPoisonArrow
from models.spells.spell_archer_revenge_arrow import SpellArcherRevengeArrow
from models.spells.spell_archer_slowing_arrow import SpellArcherSlowingArrow
from models.spells.spell_archer_tripleshot import SpellArcherTripleshot
from models.spells.spell_archer_vigor import SpellArcherVigor
from models.spells.spell_archer_tracking_arrow import SpellArcherTrackingArrow
from models.spells.spell_archer_cripple import SpellArcherCripple


class TalentHelper:

	_ATTRIBUTES = {
		JobName.ARCHER: {
			Talent.ARCHER_AP_UP: (Attribute.AP, 3),
			Talent.ARCHER_SP_UP: (Attribute.SP, 3),
			Talent.ARCHER_TS_UP: (Attribute.SPEED, 1),
			Talent.ARCHER_HP_UP: (Attribute.HP, 15),
			Talent.ARCHER_TP_UP: (Attribute.TP, 15)
		},
		JobName.BARD: {},
		JobName.BERSERKER: {},
		JobName.GUARDIAN: {
			Talent.GUARDIAN_AP_UP: (Attribute.AP, 2),
			Talent.GUARDIAN_HP_UP: (Attribute.HP, 20),
			Talent.GUARDIAN_TP_UP: (Attribute.TP, 15),
			Talent.GUARDIAN_ARMOR_UP: (Attribute.ARMOR, 5)
		},
		JobName.HEXER: {},
		JobName.MAGE: {},
		JobName.MEDIC: {},
		JobName.PALADIN: {},
		JobName.ROGUE: {},
		JobName.SHAMAN: {},
		JobName.WARRIOR: {}
	}

	_SPELLS = {
		JobName.ARCHER: {
			Talent.ARCHER_AIM: SpellArcherAim,
			Talent.ARCHER_VIGOR: SpellArcherVigor,
			Talent.ARCHER_TRACKING_ARROW: SpellArcherTrackingArrow,
			Talent.ARCHER_REVENGE_ARROW: SpellArcherRevengeArrow,
			Talent.ARCHER_CRIPPLE: SpellArcherCripple,
			Talent.ARCHER_PIERCING_ARROW: SpellArcherPiercingArrow,
			Talent.ARCHER_TRIPLESHOT: SpellArcherTripleshot,
			Talent.ARCHER_BLINDING_ARROW: SpellArcherBlindingArrow,
			Talent.ARCHER_SLOWING_ARROW: SpellArcherSlowingArrow,
			Talent.ARCHER_POISON_ARROW: SpellArcherPoisonArrow
		},
		JobName.BARD: {},
		JobName.BERSERKER: {},
		JobName.GUARDIAN: {},#wip
		JobName.HEXER: {},
		JobName.MAGE: {},
		JobName.MEDIC: {},
		JobName.PALADIN: {},
		JobName.ROGUE: {},
		JobName.SHAMAN: {},
		JobName.WARRIOR: {}
	}

	@classmethod
	def get_attribute(cls, job: JobName, talent: Talent) -> Optional[Attribute]:
		if talent not in cls._ATTRIBUTES[job]:
			return None
		return cls._ATTRIBUTES[job][talent][0]

	@classmethod
	def get_value(cls, job: JobName, talent: Talent) -> Optional[int]:
		if talent not in cls._ATTRIBUTES[job]:
			return None
		return cls._ATTRIBUTES[job][talent][1]

	@classmethod
	def get_spell(cls, job: JobName, talent: Talent) -> Spell.__subclasses__():
		return cls._SPELLS[job][talent]
