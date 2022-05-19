from models.enums.attribute_enum import Attribute
from models.enums.talent_enum import Talent
from models.toon import Toon
from state_machine.game import Game
from state_machine.runner import Runner
from tests.test import Test
from models.jobs import *


class TestGuardian(Test):

	def setup(self):
		Game._runner = None

	def test_guardian_talents(self):
		pass
