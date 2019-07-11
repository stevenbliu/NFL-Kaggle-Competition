from ants import *
import unittest

class TestProblemThree1(unittest.TestCase):
	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

	# Testing water with Ants
	def test_waterWithAntsTest(self):
		self.test_ants = [HarvesterAnt(), Ant(), ThrowerAnt()]
		self.test_water = Water('Water Test1')
		for test_ant in self.test_ants:
			self.test_water.add_insect(test_ant)
			self.assertEqual(test_ant.armor, 0)  #should have 0 armor
			self.assertTrue(self.test_water.ant is None)

	def test_waterWithSoggyBeesTest(self):
		self.test_bee = Bee(1000000)
		self.test_bee.watersafe = False    # Make Bee non-watersafe
		self.test_water = Water('Water Test2')
		self.test_water.add_insect(self.test_bee)
		self.assertEqual(self.test_bee.armor, 0)   #should have 0 armor
		self.assertEqual(len(self.test_water.bees), 0)


	def test_waterWithWatersafeBeesTest(self):
		self.test_bee = Bee(1)
		self.test_water = Water('Water Test3')
		self.test_water.add_insect(self.test_bee)
		self.assertEqual(self.test_bee.armor, 1)
		self.assertTrue(self.test_bee in self.test_water.bees)

# Testing Water inheritance
class TestProblemThree2(unittest.TestCase):
	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)
		self.old_add_insect = Place.add_insect

	def tearDown(self):
		Place.add_insect = self.old_add_insect

	def test_waterInheritanceTest(self):
		def new_add_insect(self, insect):
			raise NotImplementedError()

		Place.add_insect = new_add_insect
		self.test_bee = Bee(1)
		self.test_water = Water('Water Test4')
		self.passed = False
		try:
			self.test_water.add_insect(self.test_bee)
		except NotImplementedError:
			self.passed = True
		self.assertTrue(self.passed)

	def test_antBeforeWateringTest(self):
		def new_add_insect(self, insect):
			raise NotImplementedError()
		Place.add_insect = new_add_insect
		self.test_ant = HarvesterAnt()
		self.test_water = Water('Water Test5')
		self.passed = False
		try:
			self.test_water.add_insect(self.test_ant)
		except NotImplementedError:
			self.passed = True
		self.assertTrue(self.passed)


class TestProblemFour(unittest.TestCase):

	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

	def test_fireAntParamTest(self):
		self.fire = FireAnt()
		self.assertEqual(FireAnt.food_cost, 5)
		self.assertEqual(self.fire.armor, 1)

	def test_fireDamageTest(self):
		self.place = self.colony.places['tunnel_0_4']
		self.bee = Bee(5)
		self.place.add_insect(self.bee)
		self.place.add_insect(FireAnt())
		self.bee.action(self.colony) # attack the FireAnt
		self.assertEqual(self.bee.armor, 2)

	def test_fireDamageToAllTest(self):
		self.place = self.colony.places['tunnel_0_4']
		self.place.add_insect(FireAnt())
		for i in range(100):          # Add 100 Bees
			self.place.add_insect(Bee(3))
		self.place.bees[0].action(self.colony)  # Attack the FireAnt
		self.assertEqual(len(self.place.bees), 0)

	def test_fireDamageInstanceAttributeTest(self):
		self.place = self.colony.places['tunnel_0_4']
		self.bee = Bee(900)
		self.buffAnt = FireAnt()
		self.buffAnt.damage = 500   # Feel the burn!
		self.place.add_insect(self.bee)
		self.place.add_insect(self.buffAnt)
		self.bee.action(self.colony) # attack the FireAnt
		self.assertEqual(self.bee.armor, 400)   # is damage an instance attribute?

	def test_generalFireAntTest1(self):
		self.place = self.colony.places['tunnel_0_4']
		self.bee = Bee(10)
		self.ant = FireAnt()
		self.place.add_insect(self.bee)
		self.place.add_insect(self.ant)
		self.bee.action(self.colony)    # Attack the FireAnt
		self.assertEqual(self.bee.armor, 7)
		self.assertEqual(self.ant.armor, 0)
		self.assertTrue(self.place.ant is None)   # The FireAnt should not occupy the place anymore
		self.bee.action(self.colony)
		self.assertEqual(self.bee.armor, 7)    # Bee should not get damaged again
		self.assertEqual(self.bee.place.name, 'tunnel_0_3')    # Bee should not have been blocked

	def test_generalFireAntTest2(self):
		self.place = self.colony.places['tunnel_0_4']
		self.bee = Bee(10)
		self.ant = FireAnt()
		self.place.add_insect(self.bee)
		self.place.add_insect(self.ant)
		self.ant.reduce_armor(0.1) # Poke the FireAnt
		self.assertEqual(self.bee.armor, 10)    # Bee should not get damaged
		self.assertEqual(self.ant.armor, 0.9)
		self.assertTrue(self.place.ant is self.ant)
