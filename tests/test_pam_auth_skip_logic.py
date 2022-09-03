import sys
import unittest


class SkipLogic(object):
    """Implementation of the skip computational logic

    Table of skips (used to define the equations below)
    +-----------------------------------------++------------------------------+
    | INPUTS                                  || SKIPS                        |
    | duo_local | duo | caching | krb5 | ldap || caching | krb5 | unix | ldap |
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     0     |  0  |    0    |   0  |   0  ||   (0)   |  (2) |   1  |  (1) |
    |     0     |  0  |    0    |   0  |   1  ||   (0)   |  (3) |   2  |   1  |
    |     0     |  0  |    0    |   1  |   0  ||   (0)   |   2  |   1  |  (1) |
    |     0     |  0  |    0    |   1  |   1  ||   (0)   |   3  |   2  |   1  |
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     0     |  0  |    1    |   0  |   0  ||   (0)   |  (4) |   3  |  (3) |
    |     0     |  0  |    1    |   0  |   1  ||    2    |  (5) |   4  |   3  |
    |     0     |  0  |    1    |   1  |   0  ||    2    |   4  |   3  |  (3) |
    |     0     |  0  |    1    |   1  |   1  ||    2    |   5  |   4  |   3  |
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     1     |  0  |    0    |   0  |   0  ||   (0)   |  (4) |  (1) |  (1) |
    |     1     |  0  |    0    |   0  |   1  ||   (0)   |  (5) |  (2) |  (1) |
    |     1     |  0  |    0    |   1  |   0  ||   (0)   |  (4) |  (1) |  (1) |
    |     1     |  0  |    0    |   1  |   1  ||   (0)   |  (5) |  (2) |  (1) |
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     1     |  0  |    1    |   0  |   0  ||   (2)   |  (6) |  (3) |  (3) |
    |     1     |  0  |    1    |   0  |   1  ||   (2)   |  (7) |  (4) |  (3) |
    |     1     |  0  |    1    |   1  |   0  ||   (2)   |  (6) |  (3) |  (3) |
    |     1     |  0  |    1    |   1  |   1  ||   (2)   |  (7) |  (4) |  (3) |
    +-----------+-----+---------+------+------++---------+------+------+------+
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     0     |  1  |    0    |   0  |   0  ||   (0)   |  (1) |   2  |  (0) |
    |     0     |  1  |    0    |   0  |   1  ||   (0)   |  (2) |   3  |   0  |
    |     0     |  1  |    0    |   1  |   0  ||   (0)   |   1  |   2  |  (0) |
    |     0     |  1  |    0    |   1  |   1  ||   (0)   |   2  |   3  |   0  |
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     0     |  1  |    1    |   0  |   0  ||   (0)   |  (3) |   4  |  (2) |
    |     0     |  1  |    1    |   0  |   1  ||    3    |  (4) |   5  |   2  |
    |     0     |  1  |    1    |   1  |   0  ||    3    |   3  |   4  |  (2) |
    |     0     |  1  |    1    |   1  |   1  ||    3    |   4  |   5  |   2  |
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     1     |  1  |    0    |   0  |   0  ||   (0)   |  (1) |   0  |  (0) |
    |     1     |  1  |    0    |   0  |   1  ||   (0)   |  (2) |   1  |   0  |
    |     1     |  1  |    0    |   1  |   0  ||   (0)   |   1  |   0  |  (0) |
    |     1     |  1  |    0    |   1  |   1  ||   (0)   |   2  |   1  |   0  |
    +-----------+-----+---------+------+------++---------+------+------+------+
    |     1     |  1  |    1    |   0  |   0  ||   (0)   |  (3) |   2  |  (2) |
    |     1     |  1  |    1    |   0  |   1  ||    3    |  (4) |   3  |   2  |
    |     1     |  1  |    1    |   1  |   0  ||    3    |   3  |   2  |  (2) |
    |     1     |  1  |    1    |   1  |   1  ||    3    |   4  |   3  |   2  |
    +-----------+-----+---------+------+------++---------+------+------+------+
    """

    def __init__(self, duo_local, duo, caching, krb5, ldap):
        self.duo_local = duo_local
        self.duo = duo
        self.caching = caching
        self.krb5 = krb5
        self.ldap = ldap

        self.caching_skips = 0
        self.krb5_skips = 0
        self.unix_skips = 0
        self.ldap_skips = 0
        if caching == 1:
            if krb5 == 1 or ldap == 1:
                self.caching_skips = 2 + duo
        self.ldap_skips = self.caching_skips + (1 - duo) - (duo * caching)
        self.unix_skips = (1 + ldap) + (2 * caching) + duo - (2 * duo_local * duo)
        self.krb5_skips = self.unix_skips + 1 + (-2 * duo) + (2 * duo_local)

    def value(self, entry):
        field = '{}_skips'.format(entry)
        value = getattr(self, field)
        dontcare = '({})'.format(value)
        if self.duo_local == 1 and self.duo == 0:
            return dontcare
        if entry == 'caching':
            if self.caching == 0:
                return dontcare
            else:
                if self.krb5 == 0 and self.ldap == 0:
                    return dontcare
        elif entry == 'krb5':
            if self.krb5 == 0:
                return dontcare
        elif entry == 'ldap':
            if self.ldap == 0:
                return dontcare
        return value


def output_logic_table():
    print('+-----------------------------------------++------------------------------+')  # NOQA
    print('| INPUTS                                  || SKIPS                        |')  # NOQA
    print('| duo_local | duo | caching | krb5 | ldap || caching | krb5 | unix | ldap |')  # NOQA
    print('+-----------+-----+---------+------+------++---------+------+------+------+')  # NOQA
    for duo in (0, 1):
        for duo_local in (0, 1):
            for caching in (0, 1):
                for krb5 in (0, 1):
                    for ldap in (0, 1):
                        x = SkipLogic(duo_local, duo, caching, krb5, ldap)
                        print('|{:^11}|{:^5}|{:^9}|   {}  |   {}  ||{:^9}|  {:^3} |  {:^3} |  {:^3} |'.format(  # NOQA
                            duo_local,
                            duo,
                            caching,
                            krb5,
                            ldap,
                            x.value('caching'),
                            x.value('krb5'),
                            x.value('unix'),
                            x.value('ldap'),
                        ))
                print('+-----------+-----+---------+------+------++---------+------+------+------+')  # NOQA
        print('+-----------+-----+---------+------+------++---------+------+------+------+')  # NOQA


class TestPamAuthSkipLogic(unittest.TestCase):

    def test__no_local__no_duo__no_caching__no_krb__no_ldap(self):
        x = SkipLogic(0, 0, 0, 0, 0)
        self.assertEqual(x.unix_skips, 1)

    def test__no_local__no_duo__no_caching__no_krb__ldap(self):
        x = SkipLogic(0, 0, 0, 0, 1)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.ldap_skips, 1)

    def test__no_local__no_duo__no_caching__krb__no_ldap(self):
        x = SkipLogic(0, 0, 0, 1, 0)
        self.assertEqual(x.krb5_skips, 2)
        self.assertEqual(x.unix_skips, 1)

    def test__no_local__no_duo__no_caching__krb__ldap(self):
        x = SkipLogic(0, 0, 0, 1, 1)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.ldap_skips, 1)


    def test__no_local__no_duo__caching__no_krb__no_ldap(self):
        x = SkipLogic(0, 0, 1, 0, 0)
        self.assertEqual(x.unix_skips, 3)

    def test__no_local__no_duo__caching__no_krb__ldap(self):
        x = SkipLogic(0, 0, 1, 0, 1)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 3)

    def test__no_local__no_duo__caching__krb__no_ldap(self):
        x = SkipLogic(0, 0, 1, 1, 0)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 3)

    def test__no_local__no_duo__caching__krb__ldap(self):
        x = SkipLogic(0, 0, 1, 1, 1)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.krb5_skips, 5)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 3)


    def test__no_local__duo__no_caching__no_krb__no_ldap(self):
        x = SkipLogic(0, 1, 0, 0, 0)
        self.assertEqual(x.unix_skips, 2)

    def test__no_local__duo__no_caching__no_krb__ldap(self):
        x = SkipLogic(0, 1, 0, 0, 1)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 0)

    def test__no_local__duo__no_caching__krb__no_ldap(self):
        x = SkipLogic(0, 1, 0, 1, 0)
        self.assertEqual(x.krb5_skips, 1)
        self.assertEqual(x.unix_skips, 2)

    def test__no_local__duo__no_caching__krb__ldap(self):
        x = SkipLogic(0, 1, 0, 1, 1)
        self.assertEqual(x.krb5_skips, 2)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 0)


    def test__no_local__duo__caching__no_krb__no_ldap(self):
        x = SkipLogic(0, 1, 1, 0, 0)
        self.assertEqual(x.unix_skips, 4)

    def test__no_local__duo__caching__no_krb__ldap(self):
        x = SkipLogic(0, 1, 1, 0, 1)
        self.assertEqual(x.caching_skips, 3)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 2)

    def test__no_local__duo__caching__krb__no_ldap(self):
        x = SkipLogic(0, 1, 1, 1, 0)
        self.assertEqual(x.caching_skips, 3)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 4)

    def test__no_local__duo__caching__krb__ldap(self):
        x = SkipLogic(0, 1, 1, 1, 1)
        self.assertEqual(x.caching_skips, 3)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 2)


    def test__local__duo__no_caching__no_krb__no_ldap(self):
        x = SkipLogic(1, 1, 0, 0, 0)
        self.assertEqual(x.unix_skips, 0)

    def test__local__duo__no_caching__no_krb__ldap(self):
        x = SkipLogic(1, 1, 0, 0, 1)
        self.assertEqual(x.unix_skips, 1)
        self.assertEqual(x.ldap_skips, 0)

    def test__local__duo__no_caching__krb__no_ldap(self):
        x = SkipLogic(1, 1, 0, 1, 0)
        self.assertEqual(x.krb5_skips, 1)
        self.assertEqual(x.unix_skips, 0)

    def test__local__duo__no_caching__krb__ldap(self):
        x = SkipLogic(1, 1, 0, 1, 1)
        self.assertEqual(x.krb5_skips, 2)
        self.assertEqual(x.unix_skips, 1)
        self.assertEqual(x.ldap_skips, 0)


    def test__local__duo__caching__no_krb__no_ldap(self):
        x = SkipLogic(1, 1, 1, 0, 0)
        self.assertEqual(x.unix_skips, 2)

    def test__local__duo__caching__no_krb__ldap(self):
        x = SkipLogic(1, 1, 1, 0, 1)
        self.assertEqual(x.caching_skips, 3)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 2)

    def test__local__duo__caching__krb__no_ldap(self):
        x = SkipLogic(1, 1, 1, 1, 0)
        self.assertEqual(x.caching_skips, 3)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 2)

    def test__local__duo__caching__krb__ldap(self):
        x = SkipLogic(1, 1, 1, 1, 1)
        self.assertEqual(x.caching_skips, 3)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 2)


if __name__ == '__main__':
    done = False
    try:
        if sys.argv[1].lower() == 'table':
            output_logic_table()
            done = True
    except (AttributeError, IndexError, TypeError):
        pass
    if not done:
        unittest.main()
