import time
from enum import Enum
from typing import Type, Any, Callable, Optional


class Color(Enum):
	GREEN = '\033[92m'
	RED = '\033[31m'
	WHITE = '\033[39m'

	def __str__(self):
		return self.value


def _color_print(text: str, color: Color):
	print(str(color) + text + str(Color.WHITE), end="")


def _green_print(text: str):
	_color_print(text, Color.GREEN)


def _red_print(text: str):
	_color_print(text, Color.RED)


class Test:

	def __init__(self):
		self.name: str = self.__class__.__name__
		self.tests: list[Callable[[], Optional[str]]] = []
		self.messages: list[str] = []
		self.setup_call = None
		self.teardown_call = None
		for method in self.__dir__():
			if method == 'setup':
				self.setup_call = self.__getattribute__(method)
			elif method == 'teardown':
				self.teardown_call = self.__getattribute__(method)
			elif method.find('test_') == 0:
				self.tests.append(self.__getattribute__(method))

	def run(self):
		print("running tests: " + self.name)

		for test in self.tests:
			if self.setup_call:
				self.setup_call()
			#time.sleep(2)
			test()
			if self.teardown_call:
				self.teardown_call()
			print("")

		for message in self.messages:
			_red_print("tests error\n")
			print(message)

		self.messages = []
		print("\ndone!\n")

	def assert_true(self, boolean_value: bool) -> None:
		self._assert(
			boolean_value,
			"failed asserting that " + str(boolean_value) + " is True"
		)

	def assert_false(self, boolean_value: bool) -> None:
		self._assert(
			not boolean_value,
			"failed asserting that " + str(boolean_value) + " is False"
		)

	def assert_int_equal(self, expected: int, actual: int) -> None:
		self._assert(
			expected == actual,
			"failed asserting that " + str(actual) + " is the expected " + str(expected)
		)

	def assert_int_not_equal(self, expected: int, actual: int) -> None:
		self._assert(
			expected != actual,
			"failed asserting that " + str(actual) + " is not the expected " + str(expected)
		)

	def assert_int_more_than(self, expected: int, actual: int) -> None:
		self._assert(
			expected <= actual,
			"failed asserting that " + str(actual) + " is more than the expected " + str(expected)
		)

	def assert_int_less_than(self, expected: int, actual: int) -> None:
		self._assert(
			expected >= actual,
			"failed asserting that " + str(actual) + " is less than the expected " + str(expected)
		)

	def assert_str_equal(self, expected: str, actual: str) -> None:
		self._assert(
			expected == actual,
			"failed asserting that '" + actual + "' is the expected '" + expected + "'"
		)

	def assert_str_not_equal(self, expected: str, actual: str) -> None:
		self._assert(
			expected != actual,
			"failed asserting that '" + actual + "' is not the expected '" + expected + "'"
		)

	def assert_dict_has_key(self, key: [str, int], dictionary: dict) -> None:
		self._assert(
			key in dictionary,
			"failed asserting that dictionary has key '" + str(key) + "'"
		)

	def assert_dict_not_key(self, key: [str, int], dictionary: dict) -> None:
		self._assert(
			key not in dictionary,
			"failed asserting that dictionary doesn't have key '" + str(key) + "'"
		)

	def assert_type(self, expected_type: Type, instance: Any) -> None:
		self._assert(
			type(instance) == expected_type,
			"failed asserting that object's type " + str(type(instance)) + " is the expected " + str(expected_type)
		)

	def _assert(self, expression: bool, error_message: str):
		if not expression:
			_red_print("-")
			self.messages.append(error_message)
		else:
			_green_print("+")
