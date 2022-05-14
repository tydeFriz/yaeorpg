from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from models.action import Action

from random import randint


class Sorter:

	@classmethod
	def sort_choices(cls, decoded_p1_choices: list[Action], decoded_p2_choices: list[Action]) -> list[Action]:
		"""
		Sort the given actions by speed

		:param decoded_p1_choices: p1 actions
		:param decoded_p2_choices: p2 actions
		:return: the sorted actions
		"""
		sorted_choices = []
		p1_index = 0
		p2_index = 0
		while p1_index < len(decoded_p1_choices) \
			or p2_index < len(decoded_p2_choices):

			if len(decoded_p1_choices) <= p1_index:  # no actions left for p1
				sorted_choices.append(decoded_p2_choices[p2_index])
				p2_index += 1
			elif len(decoded_p2_choices) <= p2_index:  # no actions left for p2
				sorted_choices.append(decoded_p1_choices[p1_index])
				p1_index += 1
			elif decoded_p1_choices[p1_index].get_speed() > decoded_p2_choices[p2_index].get_speed():
				sorted_choices.append(decoded_p1_choices[p1_index])
				p1_index += 1
			elif decoded_p1_choices[p1_index].get_speed() < decoded_p2_choices[p2_index].get_speed():
				sorted_choices.append(decoded_p2_choices[p2_index])
				p2_index += 1
			elif randint(1, 2) == 1:  # tie-break roll
				sorted_choices.append(decoded_p1_choices[p1_index])
				p1_index += 1
			else:
				sorted_choices.append(decoded_p2_choices[p2_index])
				p2_index += 1

		return sorted_choices
