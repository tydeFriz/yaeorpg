from models.toon import Toon
from state_machine.game import Game
from state_machine.runner import Runner
from tests.test import Test
from models.jobs import *


def _make_game() -> Runner:
	Game.make_runner(
		Toon('p1_warrior_01', Warrior(False)),
		Toon('p1_warrior_02', Warrior(False)),
		None,
		Toon('p1_archer_01', Archer(False)),
		Toon('p1_archer_02', Archer(False)),
		Toon('p1_archer_03', Archer(False)),
		Toon('p2_warrior_01', Warrior(False)),
		Toon('p2_warrior_02', Warrior(False)),
		Toon('p2_warrior_03', Warrior(False)),
		None,
		Toon('p2_archer_01', Archer(False)),
		None
	)
	return Game.get_runner()


class TestGame(Test):

	def setup(self):
		Game._runner = None

	def test_game_init(self):
		runner = _make_game()
		self.assert_int_equal(0, runner.turn_counter)

		# check p1 team size
		p1_count = 0
		for toon in runner.p1_team.values():
			if not toon:
				p1_count += 1
		self.assert_int_equal(1, p1_count)

		# check p2 team size
		p2_count = 0
		for toon in runner.p2_team.values():
			if not toon:
				p2_count += 1
		self.assert_int_equal(2, p2_count)

		# check p1 team names
		self.assert_type(Toon, runner.p1_team['f1'])
		self.assert_str_equal("p1_warrior_01", runner.p1_team['f1'].name)
		self.assert_type(Toon, runner.p1_team['f2'])
		self.assert_str_equal("p1_warrior_02", runner.p1_team['f2'].name)
		self.assert_type(type(None), runner.p1_team['f3'])
		self.assert_type(Toon, runner.p1_team['b1'])
		self.assert_str_equal("p1_archer_01", runner.p1_team['b1'].name)
		self.assert_type(Toon, runner.p1_team['b2'])
		self.assert_str_equal("p1_archer_02", runner.p1_team['b2'].name)
		self.assert_type(Toon, runner.p1_team['b3'])
		self.assert_str_equal("p1_archer_03", runner.p1_team['b3'].name)

		# check p2 team names
		self.assert_type(Toon, runner.p2_team['f1'])
		self.assert_str_equal("p2_warrior_01", runner.p2_team['f1'].name)
		self.assert_type(Toon, runner.p2_team['f2'])
		self.assert_str_equal("p2_warrior_02", runner.p2_team['f2'].name)
		self.assert_type(Toon, runner.p2_team['f3'])
		self.assert_str_equal("p2_warrior_03", runner.p2_team['f3'].name)
		self.assert_type(type(None), runner.p2_team['b1'])
		self.assert_type(Toon, runner.p2_team['b2'])
		self.assert_str_equal("p2_archer_01", runner.p2_team['b2'].name)
		self.assert_type(type(None), runner.p2_team['b3'])

	def test_choices(self):
		runner = _make_game()
		p1_possible_choices = runner.get_p1_encoded_choices()
		self.assert_type(dict, p1_possible_choices)
		self.assert_dict_has_key("p1_warrior_01", p1_possible_choices)
		self.assert_type(dict, p1_possible_choices["p1_warrior_01"])
		self.assert_dict_has_key("p1_warrior_02", p1_possible_choices)
		self.assert_type(dict, p1_possible_choices["p1_warrior_02"])
		self.assert_dict_has_key("p1_archer_01", p1_possible_choices)
		self.assert_type(dict, p1_possible_choices["p1_archer_01"])
		self.assert_dict_has_key("p1_archer_02", p1_possible_choices)
		self.assert_type(dict, p1_possible_choices["p1_archer_02"])
		self.assert_dict_has_key("p1_archer_03", p1_possible_choices)
		self.assert_type(dict, p1_possible_choices["p1_archer_03"])

		p2_possible_choices = runner.get_p2_encoded_choices()
		self.assert_type(dict, p2_possible_choices)
		self.assert_dict_has_key("p2_warrior_01", p2_possible_choices)
		self.assert_type(dict, p2_possible_choices["p2_warrior_01"])
		self.assert_dict_has_key("p2_warrior_02", p2_possible_choices)
		self.assert_type(dict, p2_possible_choices["p2_warrior_02"])
		self.assert_dict_has_key("p2_warrior_03", p2_possible_choices)
		self.assert_type(dict, p2_possible_choices["p2_warrior_03"])
		self.assert_dict_has_key("p2_archer_01", p2_possible_choices)
		self.assert_type(dict, p2_possible_choices["p2_archer_01"])

		p1_choices = {}
		for toon_name, choice in p1_possible_choices.items():
			choice_key, choice_description = list(choice.items())[0]
			p1_choices[toon_name] = choice_key
		p2_choices = {}
		for toon_name, choice in p2_possible_choices.items():
			choice_key, choice_description = list(choice.items())[0]
			p2_choices[toon_name] = choice_key

		actions = runner._sort_choices(p1_choices, p2_choices)
		current_speed = 999999
		for action in actions:
			self.assert_int_less_than(current_speed, action.get_speed())
			current_speed = action.get_speed()

	def test_turn(self):
		runner = _make_game()
		p1_possible_choices = runner.get_p1_encoded_choices()
		p2_possible_choices = runner.get_p2_encoded_choices()

		p1_choices = {}
		for toon_name, choice in p1_possible_choices.items():
			choice_key, choice_description = list(choice.items())[-1]
			p1_choices[toon_name] = choice_key
		p2_choices = {}
		for toon_name, choice in p2_possible_choices.items():
			choice_key, choice_description = list(choice.items())[-1]
			p2_choices[toon_name] = choice_key

		for choice_key in p1_choices.values():
			runner.finalise_choice(choice_key, [runner.p2_team['f1'].name])  # bad target for archers!
		for choice_key in p2_choices.values():
			runner.finalise_choice(choice_key, [runner.p1_team['f1'].name])  # bad target for archers!

		victim1 = runner.p1_team['f1']
		victim2 = runner.p2_team['f1']
		current_victim1_hp = victim1.hp_current
		current_victim2_hp = victim2.hp_current

		turn = runner.turn(p1_choices, p2_choices)
		self.assert_false(turn)
		self.assert_int_equal(1, runner.turn_counter)
		self.assert_int_less_than(current_victim1_hp, victim1.hp_current)
		self.assert_int_less_than(current_victim2_hp, victim2.hp_current)

	def test_archer_aim(self):
		runner = _make_game()
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
		self.assert_str_equal("next attack is also considered a spell", runner.p1_team['b1'].lingering_effects[0].name)
		self.assert_int_equal(1, runner.p1_team['b1'].lingering_effects[0].duration)

		turn = runner.turn({}, {})
		self.assert_false(turn)
		self.assert_int_equal(0, len(runner.p1_team['b1'].lingering_effects))
