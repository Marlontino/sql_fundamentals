# Core querying exercises: tests-as-spec
# Each test runs a learner .sql file and compares to baked, verified rows.
import unittest, os, sys

# Make the repo root importable so `db.harness` resolves
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_sql_file, assert_result

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'core_querying')


class TestCoreQuerying(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - projection / aliases / computed column
    def test_01_select_basics(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '01_select_basics.sql'))
        expected = [
            (1, 'Laptop', 1320.0), (2, 'Headphones', 165.0), (3, 'Python Book', 44.0),
            (4, 'SQL Book', 38.5), (5, 'T-Shirt', 22.0), (6, 'Jeans', 66.0),
            (7, 'Coffee Maker', 88.0), (8, 'Desk Lamp', 49.5),
            (9, 'Action Figure', 27.5), (10, 'Board Game', 33.0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 02 - WHERE / IN / BETWEEN / LIKE / IS NOT NULL
    def test_02_filtering(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '02_filtering.sql'))
        expected = [
            (3, 'Fiona', 150000.0), (2, 'Evan', 140000.0), (5, 'Hannah', 105000.0),
            (7, 'Julia', 98000.0), (6, 'Ian', 95000.0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 03 - DISTINCT / ORDER BY / LIMIT
    def test_03_sorting_limiting(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '03_sorting_limiting.sql'))
        expected = [(1200.0,), (150.0,), (80.0,), (60.0,), (45.0,)]
        assert_result(self, rows, expected, ordered=True)

    # 04 - JOIN / SUM / GROUP BY
    def test_04_aggregates(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '04_aggregates.sql'))
        expected = [
            (7, 'Grace', 2500.0), (1, 'Alice', 1765.0), (3, 'Carol', 1680.0),
            (4, 'Dave', 340.0), (2, 'Bob', 305.0), (5, 'Eve', 230.0),
            (6, 'Frank', 185.0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 05 - GROUP BY / HAVING / COUNT
    def test_05_group_by_having(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '05_group_by_having.sql'))
        expected = [('Alice', 3), ('Carol', 3)]
        assert_result(self, rows, expected, ordered=True)

    # 06 - self LEFT JOIN / NULL
    def test_06_joins(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '06_joins.sql'))
        expected = [
            ('Diana', None), ('Evan', 'Diana'), ('Fiona', 'Diana'),
            ('George', 'Evan'), ('Hannah', 'Evan'), ('Ian', 'Fiona'),
            ('Julia', 'Fiona'), ('Kevin', 'George'), ('Laura', 'Diana'),
            ('Mike', 'Laura'),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 07 - INTERSECT
    def test_07_set_operations(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '07_set_operations.sql'))
        expected = [(1,), (2,), (5,)]
        assert_result(self, rows, expected, ordered=True)


if __name__ == '__main__':
    unittest.main()
