from ants import *
from unittest import TestCase

class TestProblemFive(TestCase):
    def setUp(self):
        self.hive, self.layout = Hive(AssaultPlan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)


    def test_nearest_bee(self):
        thrower = ThrowerAnt()
        self.colony.places['tunnel_0_0'].add_insect(thrower)
        place = self.colony.places['tunnel_0_0']
        near_bee = Bee(2)
        far_bee = Bee(2)
        self.colony.places["tunnel_0_3"].add_insect(near_bee)
        self.colony.places["tunnel_0_6"].add_insect(far_bee)
        self.hive = self.colony.hive
        self.assertIsNot(thrower.nearest_bee(self.hive), far_bee)
        self.assertIs(thrower.nearest_bee(self.hive), near_bee)

        thrower.action(self.colony)    # Attack!
        self.assertEqual(near_bee.armor, 1)
        self.assertIs(thrower.place, place)


    def test_nearest_bee_not_in_hive(self):
        thrower = ThrowerAnt()
        self.colony.places["tunnel_0_0"].add_insect(thrower)
        self.hive = self.colony.hive
        bee = Bee(2)
        self.hive.add_insect(bee)      # Adding a bee to the self.hive

        self.assertIsNot(thrower.nearest_bee(self.hive), bee)

        thrower.action(self.colony)    # Attempt to attack
        self.assertEqual(bee.armor, 2)


    def test_attacks_on_own_square(self):
        # Test that ThrowerAnt attacks bees on its own square

        thrower = ThrowerAnt()
        self.colony.places['tunnel_0_0'].add_insect(thrower)
        near_bee = Bee(2)
        self.colony.places["tunnel_0_0"].add_insect(near_bee)

        self.assertIs(thrower.nearest_bee(self.colony.hive), near_bee)

        thrower.action(self.colony)   # Attack!
        self.assertEqual(near_bee.armor, 1)           # should do 1 damage


    def test_attacks_at_end_of_tunnel(self):
        # Test that ThrowerAnt attacks bees at end of tunnel

        thrower = ThrowerAnt()
        self.colony.places['tunnel_0_0'].add_insect(thrower)
        near_bee = Bee(2)
        self.colony.places["tunnel_0_8"].add_insect(near_bee)

        self.assertIs(thrower.nearest_bee(self.colony.hive), near_bee)

        thrower.action(self.colony)   # Attack!
        self.assertEqual(near_bee.armor, 1)           # should do 1 damage


    def test_choose_random_target(self):
        # Testing ThrowerAnt chooses a random target

        thrower = ThrowerAnt()
        self.colony.places["tunnel_0_0"].add_insect(thrower)
        bee1 = Bee(1001)
        bee2 = Bee(1001)
        self.colony.places["tunnel_0_3"].add_insect(bee1)
        self.colony.places["tunnel_0_3"].add_insect(bee2)

        # Throw 1000 times. The first bee should take ~1000*1/2 = ~500 damage,
        # and have ~501 remaining.
        for _ in range(1000):
            thrower.action(self.colony)

        # Test if damage to bee1 is within 6 standard deviations (~95 damage)
        # If bees are chosen uniformly, this is true 99.9999998% of the time.
        def dmg_within_tolerance():
            return abs(bee1.armor-501) < 95
        self.assertTrue(dmg_within_tolerance())



class TestProblemSix1(TestCase):
    def setUp(self):
        self.hive, self.layout = Hive(AssaultPlan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)


    def test_long_short_thrower_parameters(self):
        # Testing Long/ShortThrower parameters
        self.assertEqual(ShortThrower.food_cost, 2)
        self.assertEqual(LongThrower.food_cost, 2)

        short_t = ShortThrower()
        long_t = LongThrower()
        self.assertEqual(short_t.armor, 1)
        self.assertEqual(long_t.armor, 1)


    def test_longthrower_hit(self):
        # Test LongThrower Hit

        ant = LongThrower()
        in_range = Bee(2)
        self.colony.places['tunnel_0_0'].add_insect(ant)
        self.colony.places["tunnel_0_5"].add_insect(in_range)
        ant.action(self.colony)
        self.assertEqual(in_range.armor, 1)


    def test_longthrower_miss(self):
        # Testing LongThrower miss

        ant = LongThrower()
        out_of_range = Bee(2)
        self.colony.places["tunnel_0_0"].add_insect(ant)
        self.colony.places["tunnel_0_4"].add_insect(out_of_range)
        ant.action(self.colony)
        self.assertEqual(out_of_range.armor, 2)


    def test_longthrower_targets_farther(self):
        # Testing LongThrower targets farther one

        ant = LongThrower()
        out_of_range = Bee(2)
        in_range = Bee(2)
        self.colony.places["tunnel_0_0"].add_insect(ant)
        self.colony.places["tunnel_0_4"].add_insect(out_of_range)
        self.colony.places["tunnel_0_5"].add_insect(in_range)
        ant.action(self.colony)
        self.assertEqual(out_of_range.armor, 2)

        self.assertEqual(in_range.armor, 1)


    def test_shortthrower_hit(self):
        # Test ShortThrower hit

        ant = ShortThrower()
        in_range = Bee(2)
        self.colony.places['tunnel_0_0'].add_insect(ant)
        self.colony.places["tunnel_0_3"].add_insect(in_range)
        ant.action(self.colony)
        self.assertEqual(in_range.armor, 1)


    def test_shortthrower_miss(self):
        # Testing ShortThrower miss

        ant = ShortThrower()
        out_of_range = Bee(2)
        self.colony.places["tunnel_0_0"].add_insect(ant)
        self.colony.places["tunnel_0_4"].add_insect(out_of_range)
        ant.action(self.colony)
        self.assertEqual(out_of_range.armor, 2)


    def test_longthrower_ignore_outside_range(self):
        # Testing LongThrower ignores bees outside range

        thrower = LongThrower()
        self.colony.places["tunnel_0_0"].add_insect(thrower)
        bee1 = Bee(1001)
        bee2 = Bee(1001)
        self.colony.places["tunnel_0_4"].add_insect(bee1)
        self.colony.places["tunnel_0_5"].add_insect(bee2)
        thrower.action(self.colony)
        self.assertEqual(bee1.armor, 1001)
        self.assertEqual(bee2.armor, 1000)


    def test_longthrower_attacks_nearest(self):
        # Testing LongThrower attacks nearest bee in range

        thrower = LongThrower()
        self.colony.places["tunnel_0_0"].add_insect(thrower)
        bee1 = Bee(1001)
        bee2 = Bee(1001)
        self.colony.places["tunnel_0_5"].add_insect(bee1)
        self.colony.places["tunnel_0_6"].add_insect(bee2)
        thrower.action(self.colony)
        self.assertEqual(bee1.armor, 1000)
        self.assertEqual(bee2.armor, 1001)


    def test_max_range_looked_up_in_instance(self):
        # Testing if max_range is looked up in the instance

        ant = ShortThrower()
        ant.max_range = 10   # Buff the ant's range
        self.colony.places["tunnel_0_0"].add_insect(ant)
        bee = Bee(2)
        self.colony.places["tunnel_0_6"].add_insect(bee)
        ant.action(self.colony)
        self.assertEqual(bee.armor, 1)



class TestProblemSix2(TestCase):

    def setUp(self):
        self.hive, self.layout = Hive(AssaultPlan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

    def tearDown(self):
        ThrowerAnt.action = self.old_thrower_action
        ThrowerAnt.throw_at = self.old_throw_at


    def test_long_inheritance_thrower_ant(self):
        # Testing LongThrower Inheritance from ThrowerAnt

        def new_action(self, colony):
            raise NotImplementedError()

        def new_throw_at(self, target):
            raise NotImplementedError()

        self.old_thrower_action = ThrowerAnt.action
        self.old_throw_at = ThrowerAnt.throw_at

        ThrowerAnt.action = new_action
        test_long = LongThrower()
        passed = 0
        try:
            test_long.action(self.colony)
        except NotImplementedError:
            passed += 1
        ThrowerAnt.action = self.old_thrower_action
        ThrowerAnt.throw_at = new_throw_at
        test_long = LongThrower()
        try:
            test_long.throw_at(Bee(1))
        except NotImplementedError:
            passed += 1
        ThrowerAnt.throw_at = self.old_throw_at

        self.assertEqual(passed, 2)



    def test_short_inheritance(self):
        # Testing ShortThrower Inheritance from ThrowerAnt
        def new_action(self, colony):
            raise NotImplementedError()
        def new_throw_at(self, target):
            raise NotImplementedError()
        self.old_thrower_action = ThrowerAnt.action
        self.old_throw_at = ThrowerAnt.throw_at

        ThrowerAnt.action = new_action
        test_short = ShortThrower()
        passed = 0
        try:
            test_short.action(self.colony)
        except NotImplementedError:
            passed += 1

        ThrowerAnt.action = self.old_thrower_action
        ThrowerAnt.throw_at = new_throw_at
        test_short = ShortThrower()
        try:
            test_short.throw_at(Bee(1))
        except NotImplementedError:
            passed += 1

        ThrowerAnt.throw_at = self.old_throw_at
        self.assertEqual(passed, 2)
