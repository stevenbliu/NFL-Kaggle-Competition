from ants import *
import unittest


class TestProblemOne(unittest.TestCase):


	""" https://docs.python.org/2/library/unittest.html """

	""" To run test: python3 -m unittest TestPhaseOne.TestProblemOne """

	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

	def test_harvesterTest(self):
		self.assertEqual(HarvesterAnt.food_cost, 2)
		self.assertEqual(ThrowerAnt.food_cost, 3)


	def test_actionTest(self):
		self.colony.food = 4
		HarvesterAnt().action(self.colony)
		self.assertEqual(self.colony.food, 5)


		HarvesterAnt().action(self.colony)
		self.assertEqual(self.colony.food, 6)


class TestProblemTwo(unittest.TestCase):
	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

	def test_single_place(self):
		self.place0 = Place('place_0')
		self.assertEqual(self.place0.exit, None)
		self.assertEqual(self.place0.entrance, None)
		self.place1 = Place('place_1', self.place0)
		self.assertEqual(self.place1.exit, self.place0)
		self.assertEqual(self.place0.entrance, self.place1)

	def test_route(self):
		self.tunnel_len = 9
		for entrance in self.colony.bee_entrances:
			num_places = 0
			place = entrance
			while place is not self.colony.queen:
				num_places += 1
				self.assertIsNotNone(place.entrance)
				place = place.exit
			self.assertEqual(num_places, self.tunnel_len)


	def test_places(self):
		for place in self.colony.places.values():
			self.assertNotEqual(place, place.exit)
			self.assertNotEqual(place, place.entrance)
			if place.exit and place.entrance:
				self.assertNotEqual(place.exit, place.entrance)
