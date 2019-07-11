from ants import *
import unittest

class TestProblemNine(unittest.TestCase):
    def setUp(self):
        self.hive, self.layout = Hive(AssaultPlan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)
        self.old_thrower_action = ThrowerAnt.action
        self.old_throw_at = ThrowerAnt.throw_at

    def tearDown(self):
        ThrowerAnt.action = self.old_thrower_action
        ThrowerAnt.throw_at = self.old_throw_at

    def test_ScubaThrower_params(self):
        self.scuba = ScubaThrower()
        self.assertEqual(self.scuba.food_cost, 6)
        self.assertEqual(self.scuba.armor, 1)


    def test_watersafe(self):
        self.water = Water('Water')
        self.ant = ScubaThrower()
        self.water.add_insect(self.ant)
        self.assertEqual(self.ant.place, self.water)
        self.assertEqual(self.ant.armor, 1)


    def test_on_land(self):
        self.place1 = self.colony.places["tunnel_0_0"]
        self.place2 = self.colony.places["tunnel_0_4"]
        self.ant = ScubaThrower()
        self.bee = Bee(3)
        self.place1.add_insect(self.ant)
        self.place2.add_insect(self.bee)
        self.ant.action(self.colony)
        self.assertEqual(self.bee.armor, 2) # Scuba Thrower can throw on land


    def test_in_water(self):
        self.water = Water("water")
        self.water.entrance = self.colony.places["tunnel_0_1"]
        self.target = self.colony.places["tunnel_0_4"]
        self.ant = ScubaThrower()
        self.bee = Bee(3)
        self.water.add_insect(self.ant)
        self.target.add_insect(self.bee)
        self.ant.action(self.colony)
        self.assertEqual(self.bee.armor, 2)


    def test_inheritance(self):
        def new_action(self, colony):
            raise NotImplementedError()
        def new_throw_at(self, target):
            raise NotImplementedError()
        ThrowerAnt.action = new_action
        self.test_scuba = ScubaThrower()
        self.passed = 0
        try:
            self.test_scuba.action(self.colony)
        except NotImplementedError:
            self.passed += 1
        ThrowerAnt.action = self.old_thrower_action
        ThrowerAnt.throw_at = new_throw_at
        self.test_scuba = ScubaThrower()
        try:
            self.test_scuba.throw_at(Bee(1))
        except NotImplementedError:
            self.passed += 1
        ThrowerAnt.throw_at = self.old_throw_at

        self.assertEqual(self.passed, 2)


""" @ Project 2 Team Emaulate below and also look at Yelp Maps testers """
class TestProblemTen(unittest.TestCase):
    """ This method runs once and is essntially stuff
    that happens before each unit test. This is a method that we override and is
    part of the JUnit Framework """

    """ https://docs.python.org/2/library/unittest.html """

    """ To run test: python3 -m unittest TestPhaseFive.TestProblemTen """
    def setUp(self):
        self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)


    def test_HungryAntTest(self):

        self.hungry = HungryAnt()
        self.assertEqual(self.hungry.armor, 1)
        self.assertEqual(HungryAnt.food_cost, 4)


    def test_DigestTest(self):
        self.hungry = HungryAnt()
        self.super_bee, self.wimpy_bee = Bee(1000), Bee(1)
        self.place = self.colony.places["tunnel_0_0"]
        self.place.add_insect(self.hungry)
        self.place.add_insect(self.super_bee)
        self.hungry.action(self.colony)         # super_bee is no match for HungryAnt!

        self.assertEqual(self.super_bee.armor, 0)


        self.place.add_insect(self.wimpy_bee)
        for _ in range(3):
            self.hungry.action(self.colony)     # digesting...not eating

        self.assertEqual(self.wimpy_bee.armor, 1)


        self.hungry.action(self.colony)         # back to eating!
        self.assertEqual(self.wimpy_bee.armor, 0)


    def test_WaitTest(self):
        self.hungry = HungryAnt()
        self.place = self.colony.places["tunnel_0_0"]
        self.place.add_insect(self.hungry)
        # Wait a few turns before adding Bee
        for _ in range(5):
            self.hungry.action(self.colony)  # shouldn't be digesting
        self.bee = Bee(3)
        self.place.add_insect(self.bee)
        self.hungry.action(self.colony)  # Eating time!
        self.assertEqual(self.bee.armor, 0)


        self.bee = Bee(3)
        self.place.add_insect(self.bee)
        for _ in range(3):
             self.hungry.action(self.colony)     # Should be digesting

        self.assertEqual(self.bee.armor, 3)


        self.hungry.action(self.colony)
        self.assertEqual(self.bee.armor, 0)


    def test_DigestTimeTest(self):
        self.very_hungry = HungryAnt()  # Add very hungry caterpi- um, ant
        self.very_hungry.time_to_digest = 0
        self.place = self.colony.places["tunnel_0_0"]
        self.place.add_insect(self.very_hungry)
        for _ in range(100):
            self.place.add_insect(Bee(3))
        for _ in range(100):
            self.very_hungry.action(self.colony)   # Eat all the bees!

        self.assertEqual(len(self.place.bees), 0)


    def test_DieTest(self):
        self.hungry = HungryAnt()
        self.place = self.colony.places["tunnel_0_0"]
        self.place.add_insect(self.hungry)
        self.place.add_insect(Bee(3))
        self.hungry.action(self.colony)
        self.assertEqual(len(self.place.bees), 0)


        self.bee = Bee(3)
        self.place.add_insect(self.bee)
        self.bee.action(self.colony) # Bee kills digesting ant

        self.assertTrue(self.place.ant is None)
        self.assertEqual(len(self.place.bees), 1)
