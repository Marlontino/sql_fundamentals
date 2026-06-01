# Test suite for the subqueries_ctes exercises.
# Each expected set was captured by running a verified reference query
# against a fresh build_db(); all five problems specify an ORDER BY, so
# every comparison uses ordered=True.

import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_sql_file, assert_result

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'subqueries_ctes')


class TestSubqueriesCtes(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - scalar subquery in SELECT
    def test_01_scalar_subquery(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '01_scalar_subquery.sql'))
        expected = [
            (1, 'Laptop', 1200.0, 1031.5),
            (2, 'Headphones', 150.0, -18.5),
            (3, 'Python Book', 40.0, -128.5),
            (4, 'SQL Book', 35.0, -133.5),
            (5, 'T-Shirt', 20.0, -148.5),
            (6, 'Jeans', 60.0, -108.5),
            (7, 'Coffee Maker', 80.0, -88.5),
            (8, 'Desk Lamp', 45.0, -123.5),
            (9, 'Action Figure', 25.0, -143.5),
            (10, 'Board Game', 30.0, -138.5),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 02 - correlated NOT EXISTS
    def test_02_in_exists(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '02_in_exists.sql'))
        expected = [
            (8, 'Heidi'),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 03 - derived table (subquery in FROM)
    def test_03_derived_tables(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '03_derived_tables.sql'))
        expected = [
            (11, 2400.0),
            (1, 1540.0),
            (4, 1520.0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 04 - CTE with aggregate over the CTE
    def test_04_cte_basics(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '04_cte_basics.sql'))
        expected = [
            ('Grace', 2500.0),
            ('Alice', 1765.0),
            ('Carol', 1680.0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 05 - recursive CTE over the employee hierarchy
    def test_05_recursive_cte(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '05_recursive_cte.sql'))
        expected = [
            (1, 'Diana', 1),
            (2, 'Evan', 2),
            (3, 'Fiona', 2),
            (9, 'Laura', 2),
            (4, 'George', 3),
            (5, 'Hannah', 3),
            (6, 'Ian', 3),
            (7, 'Julia', 3),
            (10, 'Mike', 3),
            (8, 'Kevin', 4),
        ]
        assert_result(self, rows, expected, ordered=True)


if __name__ == '__main__':
    unittest.main()
