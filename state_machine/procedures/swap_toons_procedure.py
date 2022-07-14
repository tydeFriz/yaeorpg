from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from state_machine.runner import Runner


class SwapToonsProcedure:

	@classmethod
	def run(
			cls,
			runner: Runner,
			target_a_team: int,
			target_a_pos: str,
			target_b_team: int,
			target_b_pos: str
	):
		team_dict = {
			1: runner.p1_team,
			2: runner.p2_team
		}

		toon_a = team_dict[target_a_team][target_a_pos]
		toon_b = team_dict[target_b_team][target_b_pos]

		team_dict[target_a_team][target_a_pos] = toon_b
		team_dict[target_b_team][target_b_pos] = toon_a
