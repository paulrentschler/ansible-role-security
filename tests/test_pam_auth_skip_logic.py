import sys
import unittest


class SkipLogic(object):
    """Implementation of the skip computational logic

    Table of skips (used to define the equations below)
    +------+-----------------------------------------------++------------------------------------+  # NOQA
    |      | INPUTS                                        || SKIPS                              |
    | TEST | duo_local | duo | caching | krb5 | ldap | sss || caching | krb5 | unix | ldap | sss |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |    1 |     0     |  0  |    0    |   0  |   0  |  0  ||   (0)   |  (2) |   1  |  (1) | (1) |
    |    2 |     0     |  0  |    0    |   0  |   0  |  1  ||   (0)   |  (3) |   2  |  (2) |  1  |
    |    3 |     0     |  0  |    0    |   0  |   1  |  0  ||   (0)   |  (3) |   2  |   1  | (1) |
    |    4 |     0     |  0  |    0    |   0  |   1  |  1  ||   (0)   |  (4) |   3  |   2  |  1  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |    5 |     0     |  0  |    0    |   1  |   0  |  0  ||   (0)   |   2  |   1  |  (1) | (1) |
    |    6 |     0     |  0  |    0    |   1  |   0  |  1  ||   (0)   |   3  |   2  |  (2) |  1  |
    |    7 |     0     |  0  |    0    |   1  |   1  |  0  ||   (0)   |   3  |   2  |   1  | (1) |
    |    8 |     0     |  0  |    0    |   1  |   1  |  1  ||   (0)   |   4  |   3  |   2  |  1  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |    9 |     0     |  0  |    1    |   0  |   0  |  0  ||   (0)   |  (2) |   1  |  (1) | (1) |
    |   10 |     0     |  0  |    1    |   0  |   0  |  1  ||    2    |  (5) |   4  |  (4) |  3  |
    |   11 |     0     |  0  |    1    |   0  |   1  |  0  ||    2    |  (5) |   4  |   3  | (3) |
    |   12 |     0     |  0  |    1    |   0  |   1  |  1  ||    2    |  (6) |   5  |   4  |  3  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   13 |     0     |  0  |    1    |   1  |   0  |  0  ||    2    |   4  |   3  |  (3) | (3) |
    |   14 |     0     |  0  |    1    |   1  |   0  |  1  ||    2    |   5  |   4  |  (4) |  3  |
    |   15 |     0     |  0  |    1    |   1  |   1  |  0  ||    2    |   5  |   4  |   3  | (3) |
    |   16 |     0     |  0  |    1    |   1  |   1  |  1  ||    2    |   6  |   5  |   4  |  3  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+

    +------+-----------------------------------------------++------------------------------------+
    |      | INPUTS                                        || SKIPS                              |
    | TEST | duo_local | duo | caching | krb5 | ldap | sss || caching | krb5 | unix | ldap | sss |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   17 |     1     |  0  |    0    |   0  |   0  |  0  ||   (0)   |  (4) |  (1) |  (1) | (1) |
    |   18 |     1     |  0  |    0    |   0  |   0  |  1  ||   (0)   |  (5) |  (2) |  (2) | (1) |
    |   19 |     1     |  0  |    0    |   0  |   1  |  0  ||   (0)   |  (5) |  (2) |  (1) | (1) |
    |   20 |     1     |  0  |    0    |   0  |   1  |  1  ||   (0)   |  (6) |  (3) |  (2) | (1) |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   21 |     1     |  0  |    0    |   1  |   0  |  0  ||   (0)   |  (4) |  (1) |  (1) | (1) |
    |   22 |     1     |  0  |    0    |   1  |   0  |  1  ||   (0)   |  (5) |  (2) |  (2) | (1) |
    |   23 |     1     |  0  |    0    |   1  |   1  |  0  ||   (0)   |  (5) |  (2) |  (1) | (1) |
    |   24 |     1     |  0  |    0    |   1  |   1  |  1  ||   (0)   |  (6) |  (3) |  (2) | (1) |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   25 |     1     |  0  |    1    |   0  |   0  |  0  ||   (0)   |  (4) |  (1) |  (1) | (1) |
    |   26 |     1     |  0  |    1    |   0  |   0  |  1  ||   (2)   |  (7) |  (4) |  (4) | (3) |
    |   27 |     1     |  0  |    1    |   0  |   1  |  0  ||   (2)   |  (7) |  (4) |  (3) | (3) |
    |   28 |     1     |  0  |    1    |   0  |   1  |  1  ||   (2)   |  (8) |  (5) |  (4) | (3) |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   29 |     1     |  0  |    1    |   1  |   0  |  0  ||   (2)   |  (6) |  (3) |  (3) | (3) |
    |   30 |     1     |  0  |    1    |   1  |   0  |  1  ||   (2)   |  (7) |  (4) |  (4) | (3) |
    |   31 |     1     |  0  |    1    |   1  |   1  |  0  ||   (2)   |  (7) |  (4) |  (3) | (3) |
    |   32 |     1     |  0  |    1    |   1  |   1  |  1  ||   (2)   |  (8) |  (5) |  (4) | (3) |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+

    +------+-----------------------------------------------++------------------------------------+
    |      | INPUTS                                        || SKIPS                              |
    | TEST | duo_local | duo | caching | krb5 | ldap | sss || caching | krb5 | unix | ldap | sss |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   33 |     0     |  1  |    0    |   0  |   0  |  0  ||   (0)   |  (2) |   3  |  (1) | (1) |
    |   34 |     0     |  1  |    0    |   0  |   0  |  1  ||   (0)   |  (3) |   4  |  (2) |  1  |
    |   35 |     0     |  1  |    0    |   0  |   1  |  0  ||   (0)   |  (3) |   4  |   1  | (1) |
    |   36 |     0     |  1  |    0    |   0  |   1  |  1  ||   (0)   |  (4) |   5  |   2  |  1  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   37 |     0     |  1  |    0    |   1  |   0  |  0  ||   (0)   |   2  |   3  |  (1) | (1) |
    |   38 |     0     |  1  |    0    |   1  |   0  |  1  ||   (0)   |   3  |   4  |  (2) |  1  |
    |   39 |     0     |  1  |    0    |   1  |   1  |  0  ||   (0)   |   3  |   4  |   1  | (1) |
    |   40 |     0     |  1  |    0    |   1  |   1  |  1  ||   (0)   |   4  |   5  |   2  |  1  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   41 |     0     |  1  |    1    |   0  |   0  |  0  ||   (0)   |  (2) |   3  |  (1) | (1) |
    |   42 |     0     |  1  |    1    |   0  |   0  |  1  ||    4    |  (5) |   6  |  (4) |  3  |
    |   43 |     0     |  1  |    1    |   0  |   1  |  0  ||    4    |  (5) |   6  |   3  | (3) |
    |   44 |     0     |  1  |    1    |   0  |   1  |  1  ||    4    |  (6) |   7  |   4  |  3  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   45 |     0     |  1  |    1    |   1  |   0  |  0  ||    4    |   4  |   5  |  (3) | (3) |
    |   46 |     0     |  1  |    1    |   1  |   0  |  1  ||    4    |   5  |   6  |  (4) |  3  |
    |   47 |     0     |  1  |    1    |   1  |   1  |  0  ||    4    |   5  |   6  |   3  | (3) |
    |   48 |     0     |  1  |    1    |   1  |   1  |  1  ||    4    |   6  |   7  |   4  |  3  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+

    +------+-----------------------------------------------++------------------------------------+
    |      | INPUTS                                        || SKIPS                              |
    | TEST | duo_local | duo | caching | krb5 | ldap | sss || caching | krb5 | unix | ldap | sss |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   49 |     1     |  1  |    0    |   0  |   0  |  0  ||   (0)   |  (2) |   1  |  (1) | (1) |
    |   50 |     1     |  1  |    0    |   0  |   0  |  1  ||   (0)   |  (3) |   2  |  (2) |  1  |
    |   51 |     1     |  1  |    0    |   0  |   1  |  0  ||   (0)   |  (3) |   2  |   1  | (1) |
    |   52 |     1     |  1  |    0    |   0  |   1  |  1  ||   (0)   |  (4) |   3  |   2  |  1  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   53 |     1     |  1  |    0    |   1  |   0  |  0  ||   (0)   |   2  |   1  |  (1) | (1) |
    |   54 |     1     |  1  |    0    |   1  |   0  |  1  ||   (0)   |   3  |   2  |  (2) |  1  |
    |   55 |     1     |  1  |    0    |   1  |   1  |  0  ||   (0)   |   3  |   2  |   1  | (1) |
    |   56 |     1     |  1  |    0    |   1  |   1  |  1  ||   (0)   |   4  |   3  |   2  |  1  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   57 |     1     |  1  |    1    |   0  |   0  |  0  ||   (0)   |  (2) |   1  |  (1) | (1) |
    |   58 |     1     |  1  |    1    |   0  |   0  |  1  ||    4    |  (5) |   4  |  (4) |  3  |
    |   59 |     1     |  1  |    1    |   0  |   1  |  0  ||    4    |  (5) |   4  |   3  | (3) |
    |   60 |     1     |  1  |    1    |   0  |   1  |  1  ||    4    |  (6) |   5  |   4  |  3  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
    |   61 |     1     |  1  |    1    |   1  |   0  |  0  ||    4    |   4  |   3  |  (3) | (3) |
    |   62 |     1     |  1  |    1    |   1  |   0  |  1  ||    4    |   5  |   4  |  (4) |  3  |
    |   63 |     1     |  1  |    1    |   1  |   1  |  0  ||    4    |   5  |   4  |   3  | (3) |
    |   64 |     1     |  1  |    1    |   1  |   1  |  1  ||    4    |   6  |   5  |   4  |  3  |
    +------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+
        * Numbers in () are computed values that are not needed/not used.
        * TEST column provides a number that references the unit test below.
        * TESTs 17-32 are ignored because those situations cannot occur as
            as it is impossible to have duo_local without duo.
    """

    def __init__(self, duo_local, duo, caching, krb5, ldap, sss):
        self.duo_local = duo_local
        self.duo = duo
        self.caching = caching
        self.krb5 = krb5
        self.ldap = ldap
        self.sss = sss

        self.caching_skips = 0
        self.krb5_skips = 0
        self.unix_skips = 0
        self.ldap_skips = 0
        self.sss_skips = 0
        if caching == 1:
            if krb5 == 1 or ldap == 1 or sss == 1:
                self.caching_skips = 2 + (2 * duo)
            else:
                caching = 0
        self.sss_skips = 1 + (2 * caching)
        self.ldap_skips = 1 + (2 * caching) + (1 * sss)
        self.unix_skips = (1 + ldap) + (1 * sss) + (2 * caching) + (2 * duo) - (2 * duo_local * duo)  # NOQA
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
                if self.krb5 == 0 and self.ldap == 0 and self.sss == 0:
                    return dontcare
        elif entry == 'krb5':
            if self.krb5 == 0:
                return dontcare
        elif entry == 'ldap':
            if self.ldap == 0:
                return dontcare
        elif entry == 'sss':
            if self.sss == 0:
                return dontcare
        return value


def output_logic_table():
    """Outputs the truth table shown above

    Loops through all the possible input combinations and uses the
    SkipLogic() class to determine the outputs
    """
    print('+------+-----------------------------------------------++------------------------------------+')  # NOQA
    print('|      | INPUTS                                        || SKIPS                              |')  # NOQA
    print('| TEST | duo_local | duo | caching | krb5 | ldap | sss || caching | krb5 | unix | ldap | sss |')  # NOQA
    print('+------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+')  # NOQA
    test_count = 1
    for duo in (0, 1):
        for duo_local in (0, 1):
            for caching in (0, 1):
                for krb5 in (0, 1):
                    for ldap in (0, 1):
                        for sss in (0, 1):
                            x = SkipLogic(
                                duo_local,
                                duo,
                                caching,
                                krb5,
                                ldap,
                                sss,
                            )
                            print('| {:>4} |{:^11}|{:^5}|{:^9}|   {}  |   {}  |  {}  ||{:^9}|  {:^3} |  {:^3} |  {:^3} | {:^3} |'.format(  # NOQA
                                test_count,
                                duo_local,
                                duo,
                                caching,
                                krb5,
                                ldap,
                                sss,
                                x.value('caching'),
                                x.value('krb5'),
                                x.value('unix'),
                                x.value('ldap'),
                                x.value('sss'),
                            ))
                            test_count += 1
                    print('+------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+')  # NOQA
            print('+------+-----------+-----+---------+------+------+-----++---------+------+------+------+-----+')  # NOQA


class TestPamAuthSkipLogic(unittest.TestCase):
    """Automated unit tests to verify the outputs of SkipLogic"""

    def test__no_local__no_duo__no_caching__no_krb__no_ldap__no_sss(self):
        """TEST 1"""
        x = SkipLogic(0, 0, 0, 0, 0, 0)
        self.assertEqual(x.unix_skips, 1)

    def test__no_local__no_duo__no_caching__no_krb__no_ldap__sss(self):
        """TEST 2"""
        x = SkipLogic(0, 0, 0, 0, 0, 1)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__no_duo__no_caching__no_krb__ldap__no_sss(self):
        """TEST 3"""
        x = SkipLogic(0, 0, 0, 0, 1, 0)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.ldap_skips, 1)

    def test__no_local__no_duo__no_caching__no_krb__ldap__sss(self):
        """TEST 4"""
        x = SkipLogic(0, 0, 0, 0, 1, 1)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__no_duo__no_caching__krb__no_ldap__no_sss(self):
        """TEST 5"""
        x = SkipLogic(0, 0, 0, 1, 0, 0)
        self.assertEqual(x.krb5_skips, 2)
        self.assertEqual(x.unix_skips, 1)

    def test__no_local__no_duo__no_caching__krb__no_ldap__sss(self):
        """TEST 6"""
        x = SkipLogic(0, 0, 0, 1, 0, 1)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__no_duo__no_caching__krb__ldap__no_sss(self):
        """TEST 7"""
        x = SkipLogic(0, 0, 0, 1, 1, 0)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.ldap_skips, 1)

    def test__no_local__no_duo__no_caching__krb__ldap__sss(self):
        """TEST 8"""
        x = SkipLogic(0, 0, 0, 1, 1, 1)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__no_duo__caching__no_krb__no_ldap__no_sss(self):
        """TEST 9"""
        x = SkipLogic(0, 0, 1, 0, 0, 0)
        self.assertEqual(x.unix_skips, 1)

    def test__no_local__no_duo__caching__no_krb__no_ldap__sss(self):
        """TEST 10"""
        x = SkipLogic(0, 0, 1, 0, 0, 1)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__no_local__no_duo__caching__no_krb__ldap__no_sss(self):
        """TEST 11"""
        x = SkipLogic(0, 0, 1, 0, 1, 0)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 3)

    def test__no_local__no_duo__caching__no_krb__ldap__sss(self):
        """TEST 12"""
        x = SkipLogic(0, 0, 1, 0, 1, 1)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__no_local__no_duo__caching__krb__no_ldap__no_sss(self):
        """TEST 13"""
        x = SkipLogic(0, 0, 1, 1, 0, 0)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 3)

    def test__no_local__no_duo__caching__krb__no_ldap__sss(self):
        """TEST 14"""
        x = SkipLogic(0, 0, 1, 1, 0, 1)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.krb5_skips, 5)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__no_local__no_duo__caching__krb__ldap__no_sss(self):
        """TEST 15"""
        x = SkipLogic(0, 0, 1, 1, 1, 0)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.krb5_skips, 5)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 3)

    def test__no_local__no_duo__caching__krb__ldap__sss(self):
        """TEST 16"""
        x = SkipLogic(0, 0, 1, 1, 1, 1)
        self.assertEqual(x.caching_skips, 2)
        self.assertEqual(x.krb5_skips, 6)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__no_local__duo__no_caching__no_krb__no_ldap__no_sss(self):
        """TEST 33"""
        x = SkipLogic(0, 1, 0, 0, 0, 0)
        self.assertEqual(x.unix_skips, 3)

    def test__no_local__duo__no_caching__no_krb__no_ldap__sss(self):
        """TEST 34"""
        x = SkipLogic(0, 1, 0, 0, 0, 1)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__duo__no_caching__no_krb__ldap__no_sss(self):
        """TEST 35"""
        x = SkipLogic(0, 1, 0, 0, 1, 0)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 1)

    def test__no_local__duo__no_caching__no_krb__ldap__sss(self):
        """TEST 36"""
        x = SkipLogic(0, 1, 0, 0, 1, 1)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__duo__no_caching__krb__no_ldap__no_sss(self):
        """TEST 37"""
        x = SkipLogic(0, 1, 0, 1, 0, 0)
        self.assertEqual(x.krb5_skips, 2)
        self.assertEqual(x.unix_skips, 3)

    def test__no_local__duo__no_caching__krb__no_ldap__sss(self):
        """TEST 38"""
        x = SkipLogic(0, 1, 0, 1, 0, 1)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__duo__no_caching__krb__ldap__no_sss(self):
        """TEST 39"""
        x = SkipLogic(0, 1, 0, 1, 1, 0)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 1)

    def test__no_local__duo__no_caching__krb__ldap__sss(self):
        """TEST 40"""
        x = SkipLogic(0, 1, 0, 1, 1, 1)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__no_local__duo__caching__no_krb__no_ldap__no_sss(self):
        """TEST 41"""
        x = SkipLogic(0, 1, 1, 0, 0, 0)
        self.assertEqual(x.unix_skips, 3)

    def test__no_local__duo__caching__no_krb__no_ldap__sss(self):
        """TEST 42"""
        x = SkipLogic(0, 1, 1, 0, 0, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.unix_skips, 6)
        self.assertEqual(x.sss_skips, 3)

    def test__no_local__duo__caching__no_krb__ldap__no_sss(self):
        """TEST 43"""
        x = SkipLogic(0, 1, 1, 0, 1, 0)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.unix_skips, 6)
        self.assertEqual(x.ldap_skips, 3)

    def test__no_local__duo__caching__no_krb__ldap__sss(self):
        """TEST 44"""
        x = SkipLogic(0, 1, 1, 0, 1, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.unix_skips, 7)
        self.assertEqual(x.ldap_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__no_local__duo__caching__krb__no_ldap__no_sss(self):
        """TEST 45"""
        x = SkipLogic(0, 1, 1, 1, 0, 0)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 5)

    def test__no_local__duo__caching__krb__no_ldap__sss(self):
        """TEST 46"""
        x = SkipLogic(0, 1, 1, 1, 0, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 5)
        self.assertEqual(x.unix_skips, 6)
        self.assertEqual(x.sss_skips, 3)

    def test__no_local__duo__caching__krb__ldap__no_sss(self):
        """TEST 47"""
        x = SkipLogic(0, 1, 1, 1, 1, 0)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 5)
        self.assertEqual(x.unix_skips, 6)
        self.assertEqual(x.ldap_skips, 3)

    def test__no_local__duo__caching__krb__ldap__sss(self):
        """TEST 48"""
        x = SkipLogic(0, 1, 1, 1, 1, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 6)
        self.assertEqual(x.unix_skips, 7)
        self.assertEqual(x.ldap_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__local__duo__no_caching__no_krb__no_ldap__no_sss(self):
        """TEST 49"""
        x = SkipLogic(1, 1, 0, 0, 0, 0)
        self.assertEqual(x.unix_skips, 1)

    def test__local__duo__no_caching__no_krb__no_ldap__sss(self):
        """TEST 50"""
        x = SkipLogic(1, 1, 0, 0, 0, 1)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__local__duo__no_caching__no_krb__ldap__no_sss(self):
        """TEST 51"""
        x = SkipLogic(1, 1, 0, 0, 1, 0)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.ldap_skips, 1)

    def test__local__duo__no_caching__no_krb__ldap__sss(self):
        """TEST 52"""
        x = SkipLogic(1, 1, 0, 0, 1, 1)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__local__duo__no_caching__krb__no_ldap__no_sss(self):
        """TEST 53"""
        x = SkipLogic(1, 1, 0, 1, 0, 0)
        self.assertEqual(x.krb5_skips, 2)
        self.assertEqual(x.unix_skips, 1)

    def test__local__duo__no_caching__krb__no_ldap__sss(self):
        """TEST 54"""
        x = SkipLogic(1, 1, 0, 1, 0, 1)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__local__duo__no_caching__krb__ldap__no_sss(self):
        """TEST 55"""
        x = SkipLogic(1, 1, 0, 1, 1, 0)
        self.assertEqual(x.krb5_skips, 3)
        self.assertEqual(x.unix_skips, 2)
        self.assertEqual(x.ldap_skips, 1)

    def test__local__duo__no_caching__krb__ldap__sss(self):
        """TEST 56"""
        x = SkipLogic(1, 1, 0, 1, 1, 1)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 3)
        self.assertEqual(x.ldap_skips, 2)
        self.assertEqual(x.sss_skips, 1)

    def test__local__duo__caching__no_krb__no_ldap__no_sss(self):
        """TEST 57"""
        x = SkipLogic(1, 1, 1, 0, 0, 0)
        self.assertEqual(x.unix_skips, 1)

    def test__local__duo__caching__no_krb__no_ldap__sss(self):
        """TEST 58"""
        x = SkipLogic(1, 1, 1, 0, 0, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__local__duo__caching__no_krb__ldap__no_sss(self):
        """TEST 59"""
        x = SkipLogic(1, 1, 1, 0, 1, 0)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 3)

    def test__local__duo__caching__no_krb__ldap__sss(self):
        """TEST 60"""
        x = SkipLogic(1, 1, 1, 0, 1, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__local__duo__caching__krb__no_ldap__no_sss(self):
        """TEST 61"""
        x = SkipLogic(1, 1, 1, 1, 0, 0)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 4)
        self.assertEqual(x.unix_skips, 3)

    def test__local__duo__caching__krb__no_ldap__sss(self):
        """TEST 62"""
        x = SkipLogic(1, 1, 1, 1, 0, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 5)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.sss_skips, 3)

    def test__local__duo__caching__krb__ldap__no_sss(self):
        """TEST 63"""
        x = SkipLogic(1, 1, 1, 1, 1, 0)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 5)
        self.assertEqual(x.unix_skips, 4)
        self.assertEqual(x.ldap_skips, 3)

    def test__local__duo__caching__krb__ldap__sss(self):
        """TEST 64"""
        x = SkipLogic(1, 1, 1, 1, 1, 1)
        self.assertEqual(x.caching_skips, 4)
        self.assertEqual(x.krb5_skips, 6)
        self.assertEqual(x.unix_skips, 5)
        self.assertEqual(x.ldap_skips, 4)
        self.assertEqual(x.sss_skips, 3)


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
