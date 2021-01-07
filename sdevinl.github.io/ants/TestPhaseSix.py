from ants import *
import unittest

class TestProblemEleven1(unittest.TestCase):
    def setUp(self):
        self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

    def test_bodyguardAntParamTest(self):
        self.bodyguard = BodyguardAnt()
        self.assertEqual(BodyguardAnt.food_cost, 4)
        self.assertEqual(self.bodyguard.armor, 2)

    def test_containerAttributes(self):
        self.bodyguard = BodyguardAnt()
        self.assertEqual(self.bodyguard.ant, None)
        self.assertTrue(self.bodyguard.container)
        self.test_ant = Ant()
        self.assertFalse(self.test_ant.container)

    def test_contain_ant(self):
        self.bodyguard = BodyguardAnt()
        self.bodyguard2 = BodyguardAnt()
        self.test_ant = Ant()
        self.test_ant2 = Ant()

        self.assertFalse(self.bodyguard.can_contain(self.bodyguard2))
        self.assertTrue(self.bodyguard.can_contain(self.test_ant))
        self.assertFalse(self.test_ant.can_contain(self.bodyguard))

        self.bodyguard.contain_ant(self.test_ant)
        self.assertTrue(self.bodyguard.ant is self.test_ant)
        self.assertFalse(self.bodyguard.can_contain(self.test_ant2))


    def test_placingAntsTest(self):
        self.colony.food = 0
        self.bodyguard0 = BodyguardAnt()
        self.harvester0 = HarvesterAnt()
        self.place0 = self.colony.places['tunnel_0_0']
        # Add bodyguard before harvester
        self.place0.add_insect(self.bodyguard0)
        self.place0.add_insect(self.harvester0)

        self.assertTrue(self.place0.ant is self.bodyguard0)
        self.assertTrue(self.bodyguard0.ant is self.harvester0)


        self.bodyguard0.action(self.colony)

        self.assertEqual(self.colony.food, 1)
        self.bodyguard0.reduce_armor(self.bodyguard0.armor)

        self.assertTrue(self.place0.ant is self.harvester0)


        self.bodyguard1 = BodyguardAnt()
        self.harvester1 = HarvesterAnt()
        self.place1 = self.colony.places['tunnel_0_1']
        # Add harvester before bodyguard
        self.place1.add_insect(self.harvester1)
        self.place1.add_insect(self.bodyguard1)

        self.assertTrue(self.place1.ant is self.bodyguard1)
        self.assertTrue(self.bodyguard1.ant is self.harvester1)
        self.bodyguard1.action(self.colony)
        self.assertEqual(self.colony.food, 2)
        self.bodyguard1.reduce_armor(self.bodyguard1.armor)
        self.assertTrue(self.place1.ant is self.harvester1)


    def test_removingAntsTest(self):
        self.bodyguard = BodyguardAnt()
        self.test_ant = Ant()
        self.place = Place('Test')
        self.place.add_insect(self.bodyguard)
        self.place.add_insect(self.test_ant)
        self.place.remove_insect(self.test_ant)
        self.assertEqual(self.bodyguard.ant, None)
        self.assertEqual(self.test_ant.place, None)


    def test_placementOfAntsTest(self):
        self.bodyguard0 = BodyguardAnt()
        self.bodyguard1 = BodyguardAnt()
        self.harvester0 = HarvesterAnt()
        self.harvester1 = HarvesterAnt()
        self.place0 = self.colony.places['tunnel_0_0']
        self.place1 = self.colony.places['tunnel_0_1']
        self.place0.add_insect(self.bodyguard0)
        self.place0.add_insect(self.harvester0)
        self.colony.food = 0
        self.bodyguard0.action(self.colony)
        self.assertEqual(self.colony.food, 1)


        for ant in [BodyguardAnt(), HarvesterAnt()]:
            try:
            	self.place0.add_insect(ant)
            except AssertionError:
            	self.assertTrue(self.place0.ant is self.bodyguard0, 'Bodyguard was kicked out by {0}'.format(ant))
            	self.assertTrue(self.bodyguard0.ant is self.harvester0, 'Contained ant was kicked out by {0}'.format(ant))
            	continue

            self.assertTrue(False, 'No AssertionError raised when adding')

        self.place1.add_insect(self.harvester1)
        self.place1.add_insect(self.bodyguard1)
        self.bodyguard1.action(self.colony)
        self.assertEqual(self.colony.food, 2)


        for ant in [BodyguardAnt(), HarvesterAnt()]:
            try:
            	self.place1.add_insect(ant)
            except AssertionError:
                self.assertTrue(self.place1.ant is self.bodyguard1,'Bodyguard was kicked out by {0}'.format(ant))
                self.assertTrue(self.bodyguard1.ant is self.harvester1, 'Contained ant was kicked out by {0}'.format(ant))
                continue

            self.assertTrue(False, 'No AssertionError raised when adding {0}'.format(ant))

        self.bodyguard0.reduce_armor(self.bodyguard0.armor)
        self.assertTrue(self.place0.ant is self.harvester0)



    def test_removingAntsTest2(self):
        self.bodyguard = BodyguardAnt()
        self.test_ant = Ant()
        self.place = Place('Test')
        self.place.add_insect(self.bodyguard)
        self.place.add_insect(self.test_ant)
        self.place.remove_insect(self.test_ant)

        self.assertTrue(self.bodyguard.ant is None)
        self.place.remove_insect(self.bodyguard)
        self.assertTrue(self.place.ant is None)



class TestProblemEleven2(unittest.TestCase):
	def setUp(self):
		self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
		self.dimensions = (1, 9)
		self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

	def test_1(self):
		self.bodyguard = BodyguardAnt()
		self.bodyguard.action(self.colony)   # Action without contained ant should not error

	def test_bodyguardPerformsThrower1(self):
		self.bodyguard = BodyguardAnt()
		self.thrower = ThrowerAnt()
		self.bee = Bee(2)
		# Place bodyguard before thrower
		self.colony.places["tunnel_0_0"].add_insect(self.bodyguard)
		self.colony.places["tunnel_0_0"].add_insect(self.thrower)
		self.colony.places["tunnel_0_3"].add_insect(self.bee)
		self.bodyguard.action(self.colony)
		self.assertEqual(self.bee.armor, 1)


	def test_bodyguardPerformsThrower2(self):
		self.bodyguard = BodyguardAnt()
		self.thrower = ThrowerAnt()
		self.bee = Bee(2)
		# Place thrower before bodyguard
		self.colony.places["tunnel_0_0"].add_insect(self.thrower)
		self.colony.places["tunnel_0_0"].add_insect(self.bodyguard)
		self.colony.places["tunnel_0_3"].add_insect(self.bee)
		self.bodyguard.action(self.colony)
		self.assertEqual(self.bee.armor, 1)


	def test_removingBodyguardNotAntTest(self):
		self.place = self.colony.places['tunnel_0_0']
		self.bodyguard = BodyguardAnt()
		self.test_ant = Ant(1)
		self.place.add_insect(self.bodyguard)
		self.place.add_insect(self.test_ant)
		self.colony.remove_ant('tunnel_0_0')
		self.assertTrue(self.place.ant is self.test_ant)

	def test_bodyguardedAntTest(self):
		self.test_ant = Ant()
		def new_action(colony):
			self.test_ant.armor += 9000
		self.test_ant.action = new_action
		self.place = self.colony.places['tunnel_0_0']
		self.bodyguard = BodyguardAnt()
		self.place.add_insect(self.test_ant)
		self.place.add_insect(self.bodyguard)
		self.place.ant.action(self.colony)
		self.assertEqual(self.place.ant.ant.armor, 9001)


	def test_constructContainerTest(self):
		self.ant = ThrowerAnt()
		self.ant.container = True
		self.ant.ant = None
		self.assertTrue(self.ant.can_contain(ThrowerAnt()))


	def test_containerTest(self):
		self.bodyguard = BodyguardAnt()
		self.mod_guard = BodyguardAnt()
		self.mod_guard.container = False
		self.assertTrue(self.bodyguard.can_contain(self.mod_guard))


class TestProblemTwelve1(unittest.TestCase):
    def setUp(self):
        self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

    def test_TankAnt_parameters(self):
        self.assertEqual(TankAnt.food_cost, 6)
        self.assertEqual(TankAnt.damage, 1)
        self.assertTrue(TankAnt.container)

        tank = TankAnt()
        self.assertEqual(tank.armor, 2)


    def test_TankAnt_action(self):
        tank = TankAnt()
        place = self.colony.places['tunnel_0_1']
        place.add_insect(tank)
        for _ in range(3):
            place.add_insect(Bee(3))
        tank.action(self.colony)
        self.assertEqual([bee.armor for bee in place.bees], [2, 2, 2])

    def test_tank_ant_container(self):
        tank = TankAnt()
        thrower = ThrowerAnt()
        place = self.colony.places['tunnel_0_1']
        place.add_insect(thrower)
        place.add_insect(tank)
        self.assertTrue(place.ant is tank)
        bee = Bee(3)
        place.add_insect(bee)
        tank.action(self.colony)   # Both ants attack bee
        self.assertEqual(bee.armor, 1)


class TestProblemTwelve2(unittest.TestCase):
    def setUp(self):
        self.hive, self.layout = Hive(make_test_assault_plan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

    def test_tank_ant_action(self):
        tank = TankAnt()
        place = self.colony.places['tunnel_0_1']
        place.add_insect(tank)
        for _ in range(3):
            place.add_insect(Bee(1))
        tank.action(self.colony)
        self.assertEqual(len(place.bees), 0)


    def test_placement_of_ants(self):
        tank0 = TankAnt()
        tank1 = TankAnt()
        harvester0 = HarvesterAnt()
        harvester1 = HarvesterAnt()
        place0 = self.colony.places['tunnel_0_0']
        place1 = self.colony.places['tunnel_0_1']
        # Add tank before harvester
        place0.add_insect(tank0)
        place0.add_insect(harvester0)
        self.colony.food = 0
        tank0.action(self.colony)
        self.assertEqual(self.colony.food, 1)
        for ant in [TankAnt(), HarvesterAnt()]:
            try:
                place0.add_insect(ant)
            except AssertionError:
                self.assertIs(place0.ant, tank0,
                    'Tank was kicked out by {0}'.format(ant))
                self.assertIs(tank0.ant, harvester0,
                    'Contained ant was kicked out by {0}'.format(ant))
                continue
            self.assertTrue(False, 'No AssertionError raised when adding {0}'.format(ant))


        # Add harvester before tank
        place1.add_insect(harvester1)
        place1.add_insect(tank1)
        tank1.action(self.colony)
        self.assertEqual(self.colony.food, 2)
        for ant in [TankAnt(), HarvesterAnt()]:
            try:
                place1.add_insect(ant)
            except AssertionError:
                self.assertIs(place1.ant, tank1,
                    'Tank was kicked out by {0}'.format(ant))
                self.assertIs(tank1.ant, harvester1,
                    'Contained ant was kicked out by {0}'.format(ant))
                continue
            self.assertTrue(False, 'No AssertionError raised when adding {0}'.format(ant))

        tank0.reduce_armor(tank0.armor)
        self.assertIs(place0.ant, harvester0)


    def test_remove_ants(self):
        tank = TankAnt()
        test_ant = Ant()
        place = Place('Test')
        place.add_insect(tank)
        place.add_insect(test_ant)
        place.remove_insect(test_ant)
        self.assertIs(tank.ant, None)
        self.assertIs(test_ant.place, None)
        place.remove_insect(tank)
        self.assertIs(place.ant, None)
        self.assertIs(tank.place, None)


    def test_without_contained(self):
        tank = TankAnt()
        place = Place('Test')
        place.add_insect(tank)
        tank.action(self.colony) # Action without contained ant should not error

    """ @ Project 2 Team Emaulate below and also look at Yelp Maps testers """
class TestProblemThirteen1(unittest.TestCase):
    """ This method runs once and is essntially stuff
    that happens before each unit test. This is a method that we override and is
    part of the JUnit Framework """

    """ https://docs.python.org/2/library/unittest.html """

    """ To run test: python3 -m unittest TestPhaseSix.TestProblemThirteen1 """
    def setUp(self):
        import ants, importlib
        self.ants_pack = ants
        importlib.reload(self.ants_pack)
        self.hive = self.ants_pack.Hive(self.ants_pack.make_test_assault_plan())
        self.dimensions = (2, 9)
        self.colony = self.ants_pack.AntColony(None, self.hive, self.ants_pack.ant_types(), self.ants_pack.dry_layout, self.dimensions)
        self.ants_pack.bees_win = lambda: None

    def test_QueenAnt_parameters(self):
        self.assertEqual(QueenAnt.food_cost, 7)



    def test_QueenAnt_placement(self):
        self.queen = self.ants_pack.QueenAnt()
        self.impostor = self.ants_pack.QueenAnt()
        self.front_ant, self.back_ant = self.ants_pack.ThrowerAnt(), self.ants_pack.ThrowerAnt()
        self.tunnel = [self.colony.places['tunnel_0_{0}'.format(i)] for i in range(9)]
        self.tunnel[1].add_insect(self.back_ant)
        self.tunnel[7].add_insect(self.front_ant)
        self.tunnel[4].add_insect(self.impostor)
        self.impostor.action(self.colony)

        self.assertEqual(self.impostor.armor, 0) # Impostors must die!
        self.assertTrue(self.tunnel[4].ant is None)
        self.assertEqual(self.back_ant.damage, 1)# Ants should not be buffed

        self.assertEqual(self.front_ant.damage, 1)


        self.tunnel[4].add_insect(self.queen)
        self.queen.action(self.colony)
        self.assertEqual(self.queen.armor, 1) # Long live the Queen!
        self.assertEqual(self.back_ant.damage, 2) # Ants behind queen should be buffed

        self.assertEqual(self.front_ant.damage, 1)


    def test_RemovalTest(self):
        self.queen = self.ants_pack.QueenAnt()

        self.impostor = self.ants_pack.QueenAnt()

        self.place = self.colony.places['tunnel_0_2']
        self.place.add_insect(self.impostor)
        self.place.remove_insect(self.impostor)
        self.assertTrue(self.place.ant is None) # Impostors can be removed
        self.place.add_insect(self.queen)
        self.place.remove_insect(self.queen)

        self.assertTrue(self.place.ant is self.queen) # True queen cannot be removed


    def test_QueenAntSwim(self):
        self.queen = QueenAnt()
        self.water = Water('Water')
        self.water.add_insect(self.queen)
        self.assertEqual(self.queen.armor, 1)

    def test_DamageMultiplierTest(self):
        self.queen_tunnel, self.side_tunnel = [[self.colony.places['tunnel_{0}_{1}'.format(i, j)] for j in range(9)] for i in range(2)]
        self.queen = self.ants_pack.QueenAnt()
        self.back = self.ants_pack.ThrowerAnt()
        self.front = self.ants_pack.ThrowerAnt()
        self.guard = self.ants_pack.BodyguardAnt()
        self.guarded = self.ants_pack.ThrowerAnt()
        self.side = self.ants_pack.ThrowerAnt()
        self.bee = self.ants_pack.Bee(10)
        self.side_bee = self.ants_pack.Bee(10)
        self.queen_tunnel[0].add_insect(self.back)
        self.queen_tunnel[1].add_insect(self.guard)
        self.queen_tunnel[1].add_insect(self.guarded)
        self.queen_tunnel[2].add_insect(self.queen)
        self.queen_tunnel[3].add_insect(self.front)
        self.side_tunnel[0].add_insect(self.side)
        self.queen_tunnel[4].add_insect(self.bee)
        self.side_tunnel[4].add_insect(self.side_bee)
        self.queen.action(self.colony)
        self.assertEqual(self.bee.armor, 9)

        self.back.action(self.colony)
        self.assertEqual(self.bee.armor, 7)


        self.front.action(self.colony)
        self.assertEqual(self.bee.armor, 6)

        self.guard.action(self.colony)
        self.assertEqual(self.bee.armor, 4)


        self.side.action(self.colony)
        self.assertEqual(self.side_bee.armor, 9)



class TestProblemThirteen2(unittest.TestCase):


    """ https://docs.python.org/2/library/unittest.html """

    """ To run test: python3 -m unittest TestPhaseSix.TestProblemThirteen2 """

    def setUp(self):
        import ants, importlib
        self.ants_pack = ants
        importlib.reload(self.ants_pack)
        self.hive= self.ants_pack.Hive(self.ants_pack.make_test_assault_plan())
        self.dimensions = (2, 9)
        self.colony = self.ants_pack.AntColony(None, self.hive, self.ants_pack.ant_types(), self.ants_pack.dry_layout, self.dimensions)

    def test_GameOverTest(self):
        self.queen = self.ants_pack.QueenAnt()
        self.impostor = self.ants_pack.QueenAnt()
        self.tunnel = [self.colony.places['tunnel_0_{0}'.format(i)] for i in range(9)]
        self.tunnel[4].add_insect(self.queen)
        self.tunnel[6].add_insect(self.impostor)
        self.bee = Bee(3)
        self.tunnel[6].add_insect(self.bee)     # Bee in place with impostor
        self.bee.action(self.colony)            # Game should not end

        self.bee.move_to(self.tunnel[4])        # Bee moved to place with true queen
        try:
            self.bee.action(self.colony)            # Game should end
        except self.ants_pack.BeesWinException:
            pass

    def test_NoBuffTest(self):
        self.queen = self.ants_pack.QueenAnt()
        self.colony.places['tunnel_0_2'].add_insect(self.queen)
        self.queen.action(self.colony)
        # Attack a bee
        self.bee = self.ants_pack.Bee(3)
        self.colony.places['tunnel_0_4'].add_insect(self.bee)
        self.queen.action(self.colony)
        self.assertEqual(self.bee.armor, 2) # Queen should still hit the bee


    def test_QueenActionTest(self):
        self.queen = self.ants_pack.QueenAnt()
        self.impostor = self.ants_pack.QueenAnt()
        self.bee = self.ants_pack.Bee(10)
        self.ant = self.ants_pack.ThrowerAnt()
        self.colony.places['tunnel_0_0'].add_insect(self.ant)
        self.colony.places['tunnel_0_1'].add_insect(self.queen)
        self.colony.places['tunnel_0_2'].add_insect(self.impostor)
        self.colony.places['tunnel_0_4'].add_insect(self.bee)

        self.impostor.action(self.colony)
        self.assertEqual(self.bee.armor, 10)   # Impostor should not damage bee

        self.assertEqual(self.ant.damage, 1)  # Impostor should not double damage
        self.queen.action(self.colony)
        self.assertEqual(self.bee.armor, 9)   # Queen should damage bee
        self.assertEqual(self.ant.damage, 2)  # Queen should double damage

        self.ant.action(self.colony)


        self.assertEqual(self.bee.armor, 7) # If failed, ThrowerAnt has incorrect damage

        self.assertEqual(self.queen.armor, 1)   # Long live the Queen


        self.assertEqual(self.impostor.armor, 0)  # Short-lived impostor


    def test_DamageDoublingTest(self):
        self.queen_tunnel, self.side_tunnel = [[self.colony.places['tunnel_{0}_{1}'.format(i, j)] for j in range(9)] for i in range(2)]
        self.queen = self.ants_pack.QueenAnt()
        self.queen_tunnel[7].add_insect(self.queen)
        # Turn 0
        self.thrower = self.ants_pack.ThrowerAnt()
        self.fire = self.ants_pack.FireAnt()
        self.ninja = self.ants_pack.NinjaAnt()
        self.side = self.ants_pack.ThrowerAnt()
        self.front = self.ants_pack.NinjaAnt()
        self.queen_tunnel[0].add_insect(self.thrower)
        self.queen_tunnel[1].add_insect(self.fire)
        self.queen_tunnel[2].add_insect(self.ninja)
        self.queen_tunnel[8].add_insect(self.front)
        self.side_tunnel[0].add_insect(self.side)
        self.buffed_ants = [self.thrower, self.fire, self.ninja]
        self.old_dmgs = [ant.damage for ant in self.buffed_ants]
        self.queen.action(self.colony)
        for ant, dmg in zip(self.buffed_ants, self.old_dmgs):
            self.assertEqual(ant.damage, dmg * 2, "Failed Damage Doubling Test #1: {0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2))
        for ant in [self.side, self.front]:
            self.assertEqual(ant.damage, dmg, "Failed Damage Doubling Test #2: {0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg))

        self.assertEqual(self.queen.damage, 1, "QueenAnt damage was modified to {0}".format(ant.damage))

        # Turn 1
        self.tank = self.ants_pack.TankAnt()
        self.guard = self.ants_pack.BodyguardAnt()
        self.queen_tank = self.ants_pack.TankAnt()
        self.queen_tunnel[6].add_insect(self.tank)          # Not protecting an ant
        self.queen_tunnel[1].add_insect(self.guard)         # Guarding FireAnt
        self.queen_tunnel[7].add_insect(self.queen_tank)    # Guarding QueenAnt
        self.buffed_ants.extend([self.tank, self.guard])
        self.old_dmgs.extend([ant.damage for ant in [self.tank, self.guard, self.queen_tank]])
        self.queen.action(self.colony)
        for ant, dmg in zip(self.buffed_ants, self.old_dmgs):
            self.assertEqual(ant.damage, dmg * 2, "Failed Damage Doubling Test #3: {0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2))
        # Turn 2
        self.thrower1 = self.ants_pack.ThrowerAnt()
        self.thrower2 = self.ants_pack.ThrowerAnt()
        self.queen_tunnel[6].add_insect(self.thrower1)      # Add thrower1 in TankAnt
        self.queen_tunnel[5].add_insect(self.thrower2)
        self.buffed_ants.extend([self.thrower1, self.thrower2])
        self.old_dmgs.extend([ant.damage for ant in [self.thrower1, self.thrower2]])
        self.queen.action(self.colony)
        for ant, dmg in zip(self.buffed_ants, self.old_dmgs):
            self.assertEqual(ant.damage, dmg * 2, "Failed Damage Doubling Test #4: {0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2))
        # Turn 3
        self.tank.reduce_armor(self.tank.armor)             # Expose thrower1
        self.queen.action(self.colony)
        for ant, dmg in zip(self.buffed_ants, self.old_dmgs):
            self.assertEqual(ant.damage, dmg * 2, "Failed Damage Doubling Test #5: {0}'s damage is {1}, but should be {2}".format(ant, ant.damage, dmg * 2))

    def test_ContainerTest(self):
        self.queen = self.ants_pack.QueenAnt()
        self.impostor = self.ants_pack.QueenAnt()
        self.container = self.ants_pack.TankAnt()
        self.colony.places['tunnel_0_3'].add_insect(self.container)
        self.colony.places['tunnel_0_3'].add_insect(self.impostor)
        self.impostor.action(self.colony)
        print(self.container)
        print(self.colony.places['tunnel_0_3'].ant)
        self.assertTrue(self.colony.places['tunnel_0_3'].ant is self.container)
        self.assertTrue(self.container.place is self.colony.places['tunnel_0_3'])
        self.assertTrue(self.container.ant is None)
        self.assertTrue(self.impostor.place is None)
        self.colony.places['tunnel_0_3'].add_insect(self.queen)
        self.colony.places['tunnel_0_3'].remove_insect(self.queen)

        self.assertTrue(self.container.ant is self.queen)
        self.assertTrue(self.queen.place is self.colony.places['tunnel_0_3'])
        self.assertEqual(self.queen.action(self.colony), None)
