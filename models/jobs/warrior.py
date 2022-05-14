from models.action import Action
from models.enums.job_name_enum import JobName
from models.enums.trait_enum import Trait
from models.job import Job


class Warrior(Job):

	def __init__(self, secondary_trait: bool):
		trait = Trait.WARRIOR_REGEN_TURN
		if secondary_trait:
			trait = Trait.WARRIOR_REGEN_HIT
		super().__init__(
			JobName.WARRIOR.value,
			24,
			10,
			5,
			trait,
			[],#todo
			[]#todo
		)

	def _get_custom_actions(self) -> list[Action]:
		return []
