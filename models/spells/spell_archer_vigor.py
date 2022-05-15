from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon
	from models.action import Action

from models.spell import Spell
from models.spells.actions.archer_vigor import ArcherVigor


class SpellArcherVigor(Spell):

	def make_action(self, caster: Toon) -> Action:
		return ArcherVigor(caster, self.talent_level)
