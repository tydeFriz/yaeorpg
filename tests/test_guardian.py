from models.enums.attribute_enum import Attribute
from models.enums.talent_enum import Talent
from models.toon import Toon
from state_machine.game import Game
from state_machine.runner import Runner
from tests.test import Test
from models.jobs import *


def _make_game() -> Runner:
	g_talents = {
		Talent.GUARDIAN_DEFENSIVE_STANCE: 2,
	}

	Game.make_runner(
		Toon('p1_guardian_01', Guardian(False, g_talents), 25),
		Toon('p1_warrior_01', Warrior(False), 25),
		None,
		Toon('p1_archer_01', Archer(False, {}), 25),
		Toon('p1_archer_02', Archer(False, {}), 25),
		Toon('p1_archer_03', Archer(False, {}), 25),
		Toon('p2_guardian_01', Guardian(False, g_talents), 25),
		Toon('p2_warrior_02', Warrior(False), 25),
		Toon('p2_warrior_03', Warrior(False), 25),
		None,
		Toon('p2_archer_01', Archer(False, {}), 25),
		None
	)
	return Game.get_runner()


class TestGuardian(Test):

	def setup(self):
		Game._runner = None

	def test_guardian_talents(self):
		talents = {
		#	Talent.GUARDIAN_TRAIT_UP: 3, todo: clueless
			Talent.GUARDIAN_AP_UP: 3,
			Talent.GUARDIAN_HP_UP: 3,
			Talent.GUARDIAN_TP_UP: 3,
			Talent.GUARDIAN_ARMOR_UP: 3,
			Talent.GUARDIAN_DEFENSIVE_STANCE: 1
			#todo: spells
		}

		Game.make_runner(
			Toon('p1_guardian_01', Guardian(False, talents), 25), None, None,
			None, None, None,
			Toon('p2_warrior_01', Warrior(False), 25), None, None,
			None, None, None
		)
		runner = Game.get_runner()

		p1_guardian = runner.p1_team['f1']
		self.assert_int_equal(106, p1_guardian.get_attribute(Attribute.AP))
		self.assert_int_equal(910, p1_guardian.get_attribute(Attribute.HP))
		self.assert_int_equal(295, p1_guardian.get_attribute(Attribute.TP))
		self.assert_int_equal(15, p1_guardian.get_attribute(Attribute.ARMOR))
		self.assert_int_equal(910, p1_guardian.hp_current)
		self.assert_int_equal(295, p1_guardian.tp_current)

		actions = runner.get_p1_encoded_choices()
		self.assert_true(p1_guardian.name in actions)
		actions = actions[p1_guardian.name].values()
		self.assert_true(p1_guardian.name + ': use Defensive Stance' in actions)

	def test_guardian_defensive_stance(self):
		runner = _make_game()

		self.assert_int_equal(0, runner.p2_team['f1'].get_attribute(Attribute.ARMOR))

		caster_tp = runner.p1_team['f1'].tp_current

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_defensive_key = None
		for k, v in p1_possible_choices['p1_guardian_01'].items():
			if 'use Defensive Stance' in v:
				p1_defensive_key = k
		p1_choices = {
			'p1_guardian_01': p1_defensive_key
		}
		self.assert_true('p1_guardian_01' in p1_defensive_key)
		runner.finalise_choice(p1_defensive_key, [runner.p1_team['f1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(25, caster_tp - runner.p1_team['f1'].tp_current)
		self.assert_str_equal("increase armor", runner.p1_team['f1'].buffs[0].name)
		self.assert_int_equal(3, runner.p1_team['f1'].buffs[0].duration)
		self.assert_int_equal(20, runner.p1_team['f1'].get_attribute(Attribute.ARMOR))
