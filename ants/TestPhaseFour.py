from ants import *
import unittest

class TestProblemSeven(unittest.TestCase):


	""" https://docs.python.org/2/library/unittest.html """

	""" To run test: python3 -m unittest TestPhaseFour.TestProblemSeven """

	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)


	def test_WallAntParameters(self):
		self.wall = WallAnt()
		self.assertEqual(self.wall.armor, 4)

		self.assertEqual(NinjaAnt.food_cost, 5)



	def test_WallAntAction(self):
		self.place = self.colony.places['tunnel_0_4']
		self.wall = WallAnt()
		self.bee = Bee(1000)
		self.place.add_insect(self.wall)
		self.place.add_insect(self.bee)
		for i in range(3):
			self.bee.action(self.colony)
			self.wall.action(self.colony)   # WallAnt does nothing

		self.assertEqual(self.wall.armor, 1)
		self.assertEqual(self.bee.armor, 1000)
		self.assertTrue(self.wall.place is self.place)
		self.assertTrue(self.bee.place is self.place)

class TestProblemEight(unittest.TestCase):
	""" This method runs once and is essntially stuff
	that happens before each unit test. This is a method that we override and is
	part of the JUnit Framework """

	""" https://docs.python.org/2/library/unittest.html """

	""" To run test: python3 -m unittest TestPhaseFour.TestProblemEight """

	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)


	def test_Ninja_ant_parameters(self):

		self.ninja = NinjaAnt()
		self.assertEqual(self.ninja.armor, 1)
		self.assertEqual(NinjaAnt.food_cost, 5)



	def test_ninja_ant_block(self):
		self.p0 = self.colony.places["tunnel_0_0"]
		self.p1 = self.colony.places["tunnel_0_1"]
		self.bee = Bee(2)
		self.p1.add_insect(self.bee)
		self.p1.add_insect(NinjaAnt())
		self.bee.action(self.colony)  # shouldn't attack ant, move past it

		self.assertTrue(self.bee.place is self.p0)

	def test_ninja_ant_strike_all(self):
		self.test_place = self.colony.places["tunnel_0_0"]
		for _ in range(3):
			self.test_place.add_insect(Bee(2))
		self.ninja = NinjaAnt()
		self.test_place.add_insect(self.ninja)
		self.ninja.action(self.colony)   # should strike all bees in place

		self.assertListEqual([bee.armor for bee in self.test_place.bees], [1, 1, 1])


	def test_ninja_ant_strike_expire(self):
		self.test_place = self.colony.places["tunnel_0_0"]
		for _ in range(3):
			self.test_place.add_insect(Bee(1))
		self.ninja = NinjaAnt()
		self.test_place.add_insect(self.ninja)
		self.ninja.action(self.colony)   # should strike all bees in place
		self.assertEqual(len(self.test_place.bees), 0)

	def test_Damage_looked_up_in_instance(self):
		self.place = self.colony.places["tunnel_0_0"]
		self.bee = Bee(900)
		self.place.add_insect(self.bee)
		self.buffNinja = NinjaAnt()
		self.buffNinja.damage = 500  # Sharpen the sword
		self.place.add_insect(self.buffNinja)
		self.buffNinja.action(self.colony)
		self.assertEqual(self.bee.armor, 400)


	def test_crash_when_left_alone(self):
		self.ninja = NinjaAnt()
		self.colony.places["tunnel_0_0"].add_insect(self.ninja)
		self.ninja.action(self.colony)

	def test_crash_when_not_left_alone(self):
		self.bee = Bee(3)
		self.colony.places["tunnel_0_1"].add_insect(self.bee)
		self.bee.action(self.colony)
