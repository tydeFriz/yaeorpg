from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
	from models.toon import Toon

from state_machine.runner import Runner


class Game:

	_runner: Runner = None

	@classmethod
	def make_runner(
			cls,
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
		if cls._runner:
			raise Exception("runner already exists!")

		cls._runner = Runner(
			p1_front_1,
			p1_front_2,
			p1_front_3,
			p1_back_1,
			p1_back_2,
			p1_back_3,
			p2_front_1,
			p2_front_2,
			p2_front_3,
			p2_back_1,
			p2_back_2,
			p2_back_3
		)

	@classmethod
	def get_runner(cls) -> Runner:
		if not cls._runner:
			raise Exception("runner not yet initialised!")
		return cls._runner

	def __init__(self):
		raise Exception("Cannot instantiate a Singleton!")
