from ants import *
import unittest

class TestExtraCredit(unittest.TestCase):
    def setUp(self):
        self.hive, self.layout = Hive(AssaultPlan()), dry_layout
        self.dimensions = (1, 9)
        self.colony = AntColony(None, self.hive, ant_types(), self.layout, self.dimensions)

    def test_status_parameter(self):
        slow = SlowThrower()
        stun = StunThrower()

        self.assertEqual(SlowThrower.food_cost, 4)
        self.assertEqual(StunThrower.food_cost, 6)
        self.assertEqual(slow.armor, 1)
        self.assertEqual(stun.armor, 1)

    def test_slow(self):
        slow = SlowThrower()
        bee = Bee(3)
        self.colony.places["tunnel_0_0"].add_insect(slow)
        self.colony.places["tunnel_0_4"].add_insect(bee)
        print('colony',self.colony)
        slow.action(self.colony)
        self.colony.time=1
        bee.action(self.colony)
        self.assertEqual(bee.place.name, 'tunnel_0_4') # SlowThrower should cause slowness on odd turns

        self.colony.time += 1
        bee.action(self.colony)
        self.assertEqual(bee.place.name, 'tunnel_0_3')# SlowThrower should cause slowness on odd turns

        for _ in range(3):
            self.colony.time += 1
            bee.action(self.colony)
        self.assertEqual(bee.place.name, 'tunnel_0_1')

    def test_stun(self):
        error_msg = "StunThrower doesn't stun for exactly one turn."
        stun = StunThrower()
        bee = Bee(3)
        self.colony.places["tunnel_0_0"].add_insect(stun)
        self.colony.places["tunnel_0_4"].add_insect(bee)
        stun.action(self.colony)
        bee.action(self.colony)
        self.assertEqual(bee.place.name,'tunnel_0_4') # StunThrower should stun for exactly one turn

        bee.action(self.colony)
        self.assertEqual(bee.place.name,'tunnel_0_3') # StunThrower should stun for exactly one turn


    def test_effect(self):
        stun = StunThrower()
        bee = Bee(3)
        stun_place = self.colony.places["tunnel_0_0"]
        bee_place = self.colony.places["tunnel_0_4"]
        stun_place.add_insect(stun)
        bee_place.add_insect(bee)
        for _ in range(4): # stun bee four times
            stun.action(self.colony)

        passed = True
        for _ in range(4):
            bee.action(self.colony)
            if bee.place.name != 'tunnel_0_4':
                passed = False

        self.assertTrue(passed)


    def test_multiple_stuns(self):

        stun1 = StunThrower()
        stun2 = StunThrower()
        bee1 = Bee(3)
        bee2 = Bee(3)

        self.colony.places["tunnel_0_0"].add_insect(stun1)
        self.colony.places["tunnel_0_1"].add_insect(bee1)
        self.colony.places["tunnel_0_2"].add_insect(stun2)
        self.colony.places["tunnel_0_3"].add_insect(bee2)

        stun1.action(self.colony)
        stun2.action(self.colony)
        bee1.action(self.colony)
        bee2.action(self.colony)

        self.assertEqual(bee1.place.name, 'tunnel_0_1')
        self.assertEqual(bee2.place.name, 'tunnel_0_3')

        bee1.action(self.colony)
        bee2.action(self.colony)

        self.assertEqual(bee1.place.name, 'tunnel_0_0')
        self.assertEqual(bee2.place.name, 'tunnel_0_2')


    def test_long_effect_stack(self):
        stun = StunThrower()
        slow = SlowThrower()
        bee = Bee(3)
        self.colony.places["tunnel_0_0"].add_insect(stun)
        self.colony.places["tunnel_0_1"].add_insect(slow)
        self.colony.places["tunnel_0_4"].add_insect(bee)
        for _ in range(3): # slow bee three times
            slow.action(self.colony)

        stun.action(self.colony) # stun bee once

        self.colony.time = 0
        bee.action(self.colony) # stunned
        self.assertEqual(bee.place.name, 'tunnel_0_4')

        self.colony.time = 1
        bee.action(self.colony) # slowed thrice
        self.assertEqual(bee.place.name, 'tunnel_0_4')

        self.colony.time = 2
        bee.action(self.colony) # slowed thrice
        self.assertEqual(bee.place.name, 'tunnel_0_3')

        self.colony.time = 3
        bee.action(self.colony) # slowed twice
        self.assertEqual(bee.place.name, 'tunnel_0_3')

        self.colony.time = 4
        bee.action(self.colony) # slowed twice
        self.assertEqual(bee.place.name, 'tunnel_0_2')

        self.colony.time = 5
        bee.action(self.colony) # slowed once
        self.assertEqual(bee.place.name, 'tunnel_0_2')

        self.colony.time = 6
        bee.action(self.colony) # slowed once
        self.assertEqual(bee.place.name, 'tunnel_0_1')

        self.colony.time = 7
        bee.action(self.colony) # status effects have worn off
        self.assertEqual(slow.armor, 0)
