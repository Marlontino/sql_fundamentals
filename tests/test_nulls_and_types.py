import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_sql_file, assert_result

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'nulls_and_types')


class TestNullsAndTypes(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - IS NULL vs '= NULL': employees with no manager
    def test_01_is_null_vs_equals(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '01_is_null_vs_equals.sql'))
        expected = [(1, 'Diana')]
        assert_result(self, rows, expected, ordered=True)

    # 02 - COALESCE: substitute 0 for NULL manager_id
    def test_02_coalesce_nullif(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '02_coalesce_nullif.sql'))
        expected = [
            (1, 'Diana', 0), (2, 'Evan', 1), (3, 'Fiona', 1),
            (4, 'George', 2), (5, 'Hannah', 2), (6, 'Ian', 3),
            (7, 'Julia', 3), (8, 'Kevin', 4), (9, 'Laura', 1),
            (10, 'Mike', 9),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 03 - COUNT(*) vs COUNT(col): NULLs are skipped by COUNT(col)
    def test_03_nulls_in_aggregates(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '03_nulls_in_aggregates.sql'))
        expected = [(10, 9)]
        assert_result(self, rows, expected, ordered=True)

    # 04 - CAST + strftime: signup year as an integer
    def test_04_cast_and_dates(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '04_cast_and_dates.sql'))
        expected = [
            (1, 'Alice', 2022), (2, 'Bob', 2022), (3, 'Carol', 2021),
            (4, 'Dave', 2022), (5, 'Eve', 2023), (6, 'Frank', 2023),
            (7, 'Grace', 2021), (8, 'Heidi', 2023),
        ]
        assert_result(self, rows, expected, ordered=True)


if __name__ == '__main__':
    unittest.main()
