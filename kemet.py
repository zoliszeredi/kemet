import unittest


class Modifier(object):
    def __init__(self, strength=0, damage=0, protection=0):
        self.strength = strength
        self.damage = damage
        self.protection = protection

    def __repr__(self):
        return u'{}(strength={}, damage={}, protection={})'.format(
            self.__class__.__name__,
            self.strength, self.damage, self.protection
        )

    def __eq__(self, other):
        return (self.strength == other.strength and
                self.damage == other.damage and
                self.protection == other.protection)

    def __add__(self, other):
        return self.__class__(strength=self.strength + other.strength,
                              damage=self.damage + other.damage,
                              protection=self.protection + other.protection)


class BattleCard(Modifier):
    pass


class DivineInterventionCard(Modifier):
    pass


class Troop(Modifier):
    pass


class BattlePack(object):
    default = (
        {'strength': 2, 'damage': 0, 'protection': 2},
        {'strength': 3, 'damage': 0, 'protection': 1},
        {'strength': 1, 'damage': 3, 'protection': 0},
        {'strength': 2, 'damage': 2, 'protection': 1},
        {'strength': 3, 'damage': 2, 'protection': 0},
        {'strength': 4, 'damage': 1, 'protection': 0},
    )

    def __init__(self):
        self.cards = {BattleCard(**card_attributes)
                      for card_attributes in self.default}

    def __iter__(self):
        return iter(self.cards)

    def __repr__(self):
        return repr(self.cards)


def battle(attacker, defender):
    total_attacker = sum(attacker, Modifier())
    total_defender = sum(defender, Modifier())
    return (total_attacker.strength > total_defender.strength,
            max(total_defender.damage - total_attacker.protection, 0),
            max(total_attacker.damage - total_defender.protection, 0))


class BattleTest(unittest.TestCase):
    def test_fight(self):
        attacker = [BattleCard(3, 2, 1),
                    Troop(5)]
        defender = [BattleCard(2, 0, 1),
                    Troop(5),
                    DivineInterventionCard(1, 0, 0)]
        outcome = battle(attacker=attacker, defender=defender)
        self.assertTupleEqual(outcome, (False, 0, 1))


class BattlePackTest(unittest.TestCase):
    def test_init(self):
        self.assertEqual(len(set(BattlePack())), 6)

    def test_repr(self):
        pack = BattlePack()
        self.assertEqual(repr(pack), repr(pack.cards))


class ModifierTest(unittest.TestCase):
    def test_representation(self):
        self.assertEqual(u'{card}'.format(card=Modifier(4, 1, 0)),
                         'Modifier(strength=4, damage=1, protection=0)')

    def test_init(self):
        mod = Modifier(strength=2, damage=2, protection=1)
        self.assertEqual((mod.strength, mod.damage, mod.protection),
                         (2, 2, 1))

    def test_add(self):
        self.assertEqual(Modifier(strength=3, damage=2, protection=1) +
                         Modifier(strength=2, damage=1, protection=0),
                         Modifier(strength=5, damage=3, protection=1))

