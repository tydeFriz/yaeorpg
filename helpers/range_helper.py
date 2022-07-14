from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.toon import Toon

from state_machine.game import Game

DISTANCE_MATRIX = {
	'f': [1, 1, 1, 2],
	'b': [1, 1, 2, 3]
}
KEYS = {
	'f': ['f1', 'f2', 'f3'],
	'b': ['b1', 'b2', 'b3']
}


class RangeHelper:

	def __init__(
			self,
			toon: Toon,
			range_min: int,
			range_max: int,
			can_target_friend: bool,
			can_target_enemy: bool
	):
		self.toon: Toon = toon
		self.range_min: int = range_min
		self.range_max: int = range_max
		self.can_target_friend: bool = can_target_friend
		self.can_target_enemy: bool = can_target_enemy

	def get_valid_targets(self) -> list[str]:
		"""
		Get the list of valid targets in the allowed range

		:return: The list of toon names that can be targeted
		"""
		runner = Game.get_runner()
		toon_team = runner.get_p1_team()
		enemy_team = runner.get_p2_team()
		toon_row = 'f'

		for position, toon in runner.p2_team.items():
			if not toon:
				continue
			if toon.name == self.toon.name:
				toon_team = runner.get_p2_team()
				enemy_team = runner.get_p1_team()
				break

		for position, toon in toon_team.items():
			if toon.name == self.toon.name and position.find('b') == 0:
				toon_row = 'b'
				break

		friend_back = DISTANCE_MATRIX[toon_row][0]
		friend_front = DISTANCE_MATRIX[toon_row][1]
		enemy_front = DISTANCE_MATRIX[toon_row][2]
		enemy_back = DISTANCE_MATRIX[toon_row][3]

		valid_targets = []

		if self.can_target_friend:
			if self.range_min <= friend_back <= self.range_max:
				for key in KEYS['b']:
					if key in toon_team:
						valid_targets.append(toon_team[key].name)
			if self.range_min <= friend_front <= self.range_max:
				for key in KEYS['f']:
					if key in toon_team:
						valid_targets.append(toon_team[key].name)

			if self.range_min > 0:  # cannot target self
				valid_targets.remove(self.toon.name)

		if self.can_target_enemy:
			if self.range_min <= enemy_front <= self.range_max:
				for key in KEYS['f']:
					if key in enemy_team:
						valid_targets.append(enemy_team[key].name)
			if self.range_min <= enemy_back <= self.range_max:
				for key in KEYS['b']:
					if key in enemy_team:
						valid_targets.append(enemy_team[key].name)

		return valid_targets
