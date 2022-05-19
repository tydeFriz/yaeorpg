from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
	from models.action import Action
	from models.toon import Toon

from state_machine.sorter import Sorter
from models.enums.status_enum import Status

used_names = []


def _check_teams(team: dict[str, Optional[Toon]], player_name: str):
	global used_names
	slot_count = 0
	for toon in team.values():
		if not toon:
			continue
		slot_count += 1
		if toon.name in used_names:
			print(player_name + " has an invalid team: same names.")
			return False
		used_names.append(toon.name)

	if slot_count < 1 or slot_count > 5:
		print(player_name + " has an invalid team: invalid count.")
		return False

	return True


class Runner:

	def __init__(
			self,
			p1_front_1: Optional[Toon],
			p1_front_2: Optional[Toon],
			p1_front_3: Optional[Toon],
			p1_back_1: Optional[Toon],
			p1_back_2: Optional[Toon],
			p1_back_3: Optional[Toon],
			p2_front_1: Optional[Toon],
			p2_front_2: Optional[Toon],
			p2_front_3: Optional[Toon],
			p2_back_1: Optional[Toon],
			p2_back_2: Optional[Toon],
			p2_back_3: Optional[Toon]
	):
		global used_names
		used_names = []
		self.p1_team: dict[str, Optional[Toon]] = {
			'f1': p1_front_1,
			'f2': p1_front_2,
			'f3': p1_front_3,
			'b1': p1_back_1,
			'b2': p1_back_2,
			'b3': p1_back_3,
		}
		self.p2_team: dict[str, Optional[Toon]] = {
			'f1': p2_front_1,
			'f2': p2_front_2,
			'f3': p2_front_3,
			'b1': p2_back_1,
			'b2': p2_back_2,
			'b3': p2_back_3,
		}
		if not _check_teams(self.p1_team, 'p1') or not _check_teams(self.p2_team, 'p2'):
			return

		self.turn_counter: int = 0
		self._choice_dict: dict[str, Action] = {}

	def get_toon_by_name(self, toon_name: str) -> Optional[Toon]:
		"""
		Get a toon by name

		:param toon_name: the toon's name
		:return: the required toon if present, None otherwise
		"""
		for toon in self.p1_team.values():
			if toon and toon.name == toon_name:
				return toon
		for toon in self.p2_team.values():
			if toon and toon.name == toon_name:
				return toon
		return None

	def is_in_front(self, toon_name: str):
		"""
		Check whether the given toon is in a front row

		:param toon_name: the name of the toon to check
		:return: True if the toon is in a front row, false otherwise
		"""
		for toon in [
			self.p1_team['f1'],
			self.p1_team['f2'],
			self.p1_team['f3'],
			self.p2_team['f1'],
			self.p2_team['f2'],
			self.p2_team['f3']
		]:
			if toon.name == toon_name:
				return True
		return False

	def get_p1_encoded_choices(self) -> dict[str, dict[str, str]]:
		"""
		Get all actions player 1 can choose from

		:return: a dictionary where keys are toon names and values are
		a dictionary where keys are action strid and values are action descriptions
		"""
		return self._get_encoded_choices(self.p1_team)

	def get_p2_encoded_choices(self) -> dict[str, dict[str, str]]:
		"""
		Get all actions player 2 can choose from

		:return: a dictionary where keys are toon names and values are
		a dictionary where keys are action strid and values are action descriptions
		"""
		return self._get_encoded_choices(self.p2_team)

	def finalise_choice(self, choice_key: str, targets: list[str]) -> None:
		"""
		Make the given choice runnable by assigning targets

		:param choice_key: The choice's strid
		:param targets: the name of targets to assign to the choice
		"""
		self._choice_dict[choice_key].finalise(targets)

	def turn(self, p1_choices: dict[str, str], p2_choices: dict[str, str]) -> bool:
		"""
		Execute a turn based on player choices

		:param p1_choices: the dict toon.name -> Action.strid of p1 choices
		:param p2_choices: the dict toon.name -> Action.strid of p2 choices
		:return: True if somebody won, false otherwise
		"""
		sorted_choices = self._sort_choices(p1_choices, p2_choices)
		wincon = False
		for choice in sorted_choices:
			self._run_action(choice)
			wincon = self._check_wincon()

		self.turn_counter += 1
		self._choice_dict = {}

		self._tick_effects()

		return wincon

	def get_p1_team(self) -> dict[str, Toon]:
		"""
		Get all toons in p1 team as dict

		:return: a dictionary of position -> Toon entries
		"""
		return self._get_team(1)

	def get_p2_team(self) -> dict[str, Toon]:
		"""
		Get all toons in p2 team as dict

		:return: a dictionary of position -> Toon entries
		"""
		return self._get_team(2)

	def _get_team(self, player_number: int) -> dict[str, Toon]:
		team_to_get = self.p1_team
		if player_number == 2:
			team_to_get = self.p2_team

		team = {}
		for pos, toon in team_to_get.items():
			if toon:
				team[pos] = toon
		return team

	def _get_encoded_choices(self, team: dict[str, Optional[Toon]]) -> dict[str, dict[str, str]]:
		encoded_choices = {}

		for _, toon in team.items():
			if not toon:
				continue
			actions = toon.get_available_actions()
			action_id_string_map = {}

			for action in actions:
				self._choice_dict[action.strid] = action
				action_id_string_map[action.strid] = action.description

			encoded_choices[toon.name] = action_id_string_map

		return encoded_choices

	def _sort_decode_choices(self, p_choices: dict[str, str]) -> list[Action]:
		choices = []
		for toon_name, choice_id in p_choices.items():
			choices.append(self._choice_dict[choice_id])
		choices.sort(key=lambda x: x.get_speed(), reverse=True)
		return choices

	def _sort_choices(self, p1_choices: dict[str, str], p2_choices: dict[str, str]) -> list[Action]:
		decoded_p1_choices = self._sort_decode_choices(p1_choices)
		decoded_p2_choices = self._sort_decode_choices(p2_choices)

		return Sorter.sort_choices(decoded_p1_choices, decoded_p2_choices)

	def _run_action(self, action: Action):
		if not action.ready_to_run:
			raise Exception("action '" + action.description + "' not ready to run")
		if not action.toon_can_cast() or not action.get_valid_targets():
			return
		if not action.toon.consume(action.tp_cost):
			return
		component_memory = {}
		for component in action.get_components():
			component_memory = component.run(self, component_memory)

	def _tick_effects(self):
		toons = list(self.p1_team.values())
		toons.extend(self.p2_team.values())
		for toon in toons:
			if toon:
				buff_cleanup = []
				debuff_cleanup = []

				for buff in toon.buffs:
					buff.duration -= 1
					if buff.duration == 0:
						buff_cleanup.append(buff)
				for buff in buff_cleanup:
					toon.buffs.remove(buff)

				for debuff in toon.debuffs:
					debuff.duration -= 1
					if debuff.duration == 0:
						debuff_cleanup.append(debuff)
				for debuff in debuff_cleanup:
					toon.debuffs.remove(debuff)

				for effect in toon.lingering_effects:
					effect.duration -= 1
					if effect.duration == 0:
						toon.lingering_effects.remove(effect)

				if toon.status not in [#todo: tick bleed and poison
					Status.NO_STATUS,
					Status.BLEEDING,
					Status.POISONED
				]:
					toon.status_counter -= 1
					if toon.status_counter < 1:
						toon.status = Status.NO_STATUS
						toon.status_counter = Status.DEFAULT_COUNTERS.value[Status.NO_STATUS.value]

	def _check_wincon(self) -> bool:
		if self.turn_counter > 999:
			print("game over, nobody wins.")
			return True

		p1_lost = True
		for toon in self.p1_team.values():
			if toon and toon.hp_current > 0:
				p1_lost = False

		if p1_lost:
			print("game over, p2 wins.")
			return True

		p2_lost = True
		for toon in self.p2_team.values():
			if toon and toon.hp_current > 0:
				p2_lost = False

		if p2_lost:
			print("game over, p1 wins.")
			return True

		return False
