from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon
	from models.action import Action

from models.spell import Spell
from models.spells.actions.guardian_anchor_howl import GuardianAnchorHowl


class SpellGuardianAnchorHowl(Spell):
	def make_action(self, caster: Toon) -> Action:
		return GuardianAnchorHowl(caster, self.talent_level)
