from models.buff import Buff
from models.buffs.archer_lower_resistances import ArcherLowerResistances
from models.enums.attribute_enum import Attribute
from models.enums.status_enum import Status
from models.toon import Toon
from state_machine.game import Game
from state_machine.procedures.apply_debuff_procedure import ApplyDebuffProcedure
from state_machine.runner import Runner
from tests.test import Test
from models.jobs import *


def _make_game() -> Runner:
	Game.make_runner(
		Toon('p1_warrior_01', Warrior(False), 25),
		Toon('p1_warrior_02', Warrior(False), 25),
		Toon('p1_archer_03', Archer(False), 25),
		Toon('p1_archer_01', Archer(False), 25),
		Toon('p1_archer_02', Archer(False), 25),
		None,
		Toon('p2_warrior_01', Warrior(False), 25),
		Toon('p2_warrior_02', Warrior(False), 25),
		Toon('p2_warrior_03', Warrior(False), 25),
		None,
		Toon('p2_archer_01', Archer(False), 25),
		None
	)
	return Game.get_runner()


class TestArcher(Test):

	def setup(self):
		Game._runner = None

	def test_archer_aim(self):
		runner = _make_game()

		self.assert_int_equal(100, runner.p1_team['b1'].get_attribute(Attribute.SP))

		caster_tp = runner.p1_team['b1'].tp_current

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_aim_key = None
		for k, v in p1_possible_choices['p1_archer_01'].items():
			if 'use Aim' in v:
				p1_aim_key = k
		p1_choices = {
			'p1_archer_01': p1_aim_key
		}
		self.assert_true('p1_archer_01' in p1_aim_key)
		runner.finalise_choice(p1_aim_key, [runner.p1_team['b1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(25, caster_tp - runner.p1_team['b1'].tp_current)
		self.assert_str_equal("next attack is also considered a spell", runner.p1_team['b1'].lingering_effects[0].name)
		self.assert_int_equal(1, runner.p1_team['b1'].lingering_effects[0].duration)
		self.assert_int_equal(110, runner.p1_team['b1'].get_attribute(Attribute.SP))  # todo: adapt to talent selection

		turn = runner.turn({}, {})
		self.assert_false(turn)
		self.assert_int_equal(0, len(runner.p1_team['b1'].lingering_effects))

	def test_archer_vigor(self):
		runner = _make_game()

		self.assert_int_equal(100, runner.p1_team['b1'].get_attribute(Attribute.AP))

		caster_tp = runner.p1_team['b1'].tp_current

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_vigor_key = None
		for k, v in p1_possible_choices['p1_archer_01'].items():
			if 'use Vigor' in v:
				p1_vigor_key = k
		p1_choices = {
			'p1_archer_01': p1_vigor_key
		}
		self.assert_true('p1_archer_01' in p1_vigor_key)
		runner.finalise_choice(p1_vigor_key, [runner.p1_team['b1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(25, caster_tp - runner.p1_team['b1'].tp_current)
		self.assert_str_equal("next spell is also considered an attack", runner.p1_team['b1'].lingering_effects[0].name)
		self.assert_int_equal(1, runner.p1_team['b1'].lingering_effects[0].duration)
		self.assert_int_equal(110, runner.p1_team['b1'].get_attribute(Attribute.AP))  # todo: adapt to talent selection

		turn = runner.turn({}, {})
		self.assert_false(turn)
		self.assert_int_equal(0, len(runner.p1_team['b1'].lingering_effects))

	def test_archer_tracking_arrow(self):
		runner = _make_game()

		self.assert_int_equal(0, runner.p2_team['f1'].get_attribute(Attribute.ARMOR))
		self.assert_int_equal(0, runner.p2_team['f1'].get_attribute(Attribute.SPELL_RES))

		caster_tp = runner.p1_team['b1'].tp_current

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_tracking_key = None
		for k, v in p1_possible_choices['p1_archer_01'].items():
			if 'use Tracking Arrow' in v:
				p1_tracking_key = k
		p1_choices = {
			'p1_archer_01': p1_tracking_key
		}
		self.assert_true('p1_archer_01' in p1_tracking_key)
		runner.finalise_choice(p1_tracking_key, [runner.p2_team['f1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(40, caster_tp - runner.p1_team['b1'].tp_current)
		self.assert_str_equal("lower armor and spell resistance", runner.p2_team['f1'].debuffs[0].name)
		self.assert_int_equal(4, runner.p2_team['f1'].debuffs[0].duration)
		self.assert_int_equal(-40, runner.p2_team['f1'].get_attribute(Attribute.ARMOR))  # todo: adapt to talent selection
		self.assert_int_equal(-40, runner.p2_team['f1'].get_attribute(Attribute.SPELL_RES))  # todo: adapt to talent selection

		turn = runner.turn({}, {})
		self.assert_false(turn)
		self.assert_int_equal(3, runner.p2_team['f1'].debuffs[0].duration)

		turn = runner.turn({}, {})
		self.assert_false(turn)
		self.assert_int_equal(2, runner.p2_team['f1'].debuffs[0].duration)

		turn = runner.turn({}, {})
		self.assert_false(turn)
		self.assert_int_equal(1, runner.p2_team['f1'].debuffs[0].duration)

		turn = runner.turn({}, {})
		self.assert_false(turn)
		self.assert_int_equal(0, len(runner.p2_team['f1'].debuffs))

	def test_archer_revenge_arrow(self):
		runner = _make_game()

		self.assert_int_equal(0, runner.p2_team['f1'].get_attribute(Attribute.ARMOR))
		self.assert_int_equal(0, runner.p2_team['f1'].get_attribute(Attribute.SPELL_RES))
		self.assert_int_equal(0, runner.p1_team['f3'].get_attribute(Attribute.ARMOR))
		self.assert_int_equal(0, runner.p1_team['f3'].get_attribute(Attribute.SPELL_RES))

		original_hp = runner.p2_team['f1'].hp_current
		caster_tp = runner.p1_team['f3'].tp_current

		ApplyDebuffProcedure.run(runner.p1_team['f3'], ArcherLowerResistances(2))

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_revenge_key = None
		for k, v in p1_possible_choices['p1_archer_03'].items():
			if 'use Revenge Arrow' in v:
				p1_revenge_key = k
		p1_choices = {
			'p1_archer_03': p1_revenge_key
		}
		self.assert_true('p1_archer_03' in p1_revenge_key)
		runner.finalise_choice(p1_revenge_key, [runner.p2_team['f1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(45, caster_tp - runner.p1_team['f3'].tp_current)
		self.assert_int_equal(1, len(runner.p2_team['f1'].debuffs))
		self.assert_int_equal(4, runner.p2_team['f1'].debuffs[0].duration)
		self.assert_int_equal(-40, runner.p2_team['f1'].get_attribute(Attribute.ARMOR))
		self.assert_int_equal(-40, runner.p2_team['f1'].get_attribute(Attribute.SPELL_RES))
		self.assert_int_equal(154, original_hp - runner.p2_team['f1'].hp_current)

	def test_archer_cripple(self):
		runner = _make_game()

		self.assert_int_equal(5, runner.p2_team['f1'].get_attribute(Attribute.SPEED))

		caster_tp = runner.p1_team['b1'].tp_current

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_cripple_key = None
		for k, v in p1_possible_choices['p1_archer_01'].items():
			if 'use Cripple' in v:
				p1_cripple_key = k
		p1_choices = {
			'p1_archer_01': p1_cripple_key
		}
		self.assert_true('p1_archer_01' in p1_cripple_key)
		runner.finalise_choice(p1_cripple_key, [runner.p2_team['f1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(30, caster_tp - runner.p1_team['b1'].tp_current)
		self.assert_str_equal("lower turn speed", runner.p2_team['f1'].debuffs[0].name)
		self.assert_int_equal(4, runner.p2_team['f1'].debuffs[0].duration)  # todo: adapt to talent selection
		self.assert_int_equal(1, runner.p2_team['f1'].get_attribute(Attribute.SPEED))

	def test_archer_piercing_arrow(self):
		runner = _make_game()

		runner.p2_team['f1'].buff(Buff(
			'MOCK_ARMOR_INCREASE_TEST_ONLY',
			9,
			False,
			{
				Attribute.ARMOR: 99
			}
		))

		caster_tp = runner.p1_team['b1'].tp_current
		target_hp = runner.p2_team['f1'].hp_current

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_pierce_key = None
		for k, v in p1_possible_choices['p1_archer_01'].items():
			if 'use Piercing Arrow' in v:
				p1_pierce_key = k
		p1_choices = {
			'p1_archer_01': p1_pierce_key
		}
		self.assert_true('p1_archer_01' in p1_pierce_key)
		runner.finalise_choice(p1_pierce_key, [runner.p2_team['f1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(40, caster_tp - runner.p1_team['b1'].tp_current)
		self.assert_int_equal(100, target_hp - runner.p2_team['f1'].hp_current)

	def test_archer_tripleshot(self):
		runner = _make_game()

		caster_tp = runner.p1_team['b1'].tp_current
		target_hps = [
			runner.p2_team['f1'].hp_current,
			runner.p2_team['f2'].hp_current,
			runner.p2_team['f3'].hp_current
		]

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_pierce_key = None
		for k, v in p1_possible_choices['p1_archer_01'].items():
			if 'use Tripleshot' in v:
				p1_pierce_key = k
		p1_choices = {
			'p1_archer_01': p1_pierce_key
		}
		self.assert_true('p1_archer_01' in p1_pierce_key)
		runner.finalise_choice(p1_pierce_key, [
			runner.p2_team['f1'].name,
			runner.p2_team['f2'].name,
			runner.p2_team['f3'].name
		])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(65, caster_tp - runner.p1_team['b1'].tp_current)
		self.assert_int_equal(50, target_hps[0] - runner.p2_team['f1'].hp_current)
		self.assert_int_equal(50, target_hps[1] - runner.p2_team['f2'].hp_current)
		self.assert_int_equal(50, target_hps[2] - runner.p2_team['f3'].hp_current)

	def test_archer_blinding_arrow(self):
		runner = _make_game()

		self.assert_int_equal(5, runner.p2_team['f1'].get_attribute(Attribute.SPEED))

		caster_tp = runner.p1_team['b1'].tp_current

		p1_possible_choices = runner.get_p1_encoded_choices()

		p1_blinding_key = None
		for k, v in p1_possible_choices['p1_archer_01'].items():
			if 'use Blinding Arrow' in v:
				p1_blinding_key = k
		p1_choices = {
			'p1_archer_01': p1_blinding_key
		}
		self.assert_true('p1_archer_01' in p1_blinding_key)
		runner.finalise_choice(p1_blinding_key, [runner.p2_team['f1'].name])

		turn = runner.turn(p1_choices, {})
		self.assert_false(turn)
		self.assert_int_equal(40, caster_tp - runner.p1_team['b1'].tp_current)
		self.assert_int_equal(Status.BLINDED.value, runner.p2_team['f1'].status.value)
		self.assert_int_equal(Status.DEFAULT_COUNTERS.value[Status.BLINDED.value], runner.p2_team['f1'].status_counter)

