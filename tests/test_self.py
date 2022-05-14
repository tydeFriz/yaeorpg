from tests.test import Test


class TestSelf(Test):

	def test_assert_true(self):
		x = True
		self.assert_true(x)
		x = False
		self.assert_true(x)

	def test_assert_false(self):
		x = False
		self.assert_false(x)
		x = True
		self.assert_false(x)

	def test_assert_int_equal(self):
		x = 5
		y = 5
		self.assert_int_equal(x, y)
		x = 5
		y = 6
		self.assert_int_equal(x, y)

	def test_assert_int_not_equal(self):
		x = 5
		y = 6
		self.assert_int_not_equal(x, y)
		x = 5
		y = 5
		self.assert_int_not_equal(x, y)

	def test_assert_str_equal(self):
		x = "abc"
		y = "abc"
		self.assert_str_equal(x, y)
		x = "abc"
		y = "123"
		self.assert_str_equal(x, y)

	def test_assert_str_not_equal(self):
		x = "abc"
		y = "123"
		self.assert_str_not_equal(x, y)
		x = "abc"
		y = "abc"
		self.assert_str_not_equal(x, y)

	def test_assert_type(self):
		x = 5
		self.assert_type(int, x)
		x = "a"
		self.assert_type(int, x)
