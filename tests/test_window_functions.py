import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_sql_file, assert_result

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'window_functions')


class TestWindowFunctions(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - ROW_NUMBER / RANK / DENSE_RANK across the whole company
    def test_01_row_number_rank(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '01_row_number_rank.sql'))
        expected = [
            ('Diana', 180000.0, 1), ('Fiona', 150000.0, 2), ('Evan', 140000.0, 3),
            ('Laura', 120000.0, 4), ('George', 110000.0, 5), ('Hannah', 105000.0, 6),
            ('Julia', 98000.0, 7), ('Ian', 95000.0, 8), ('Kevin', 85000.0, 9),
            ('Mike', 75000.0, 10),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 02 - PARTITION BY: ranking restarts per department
    def test_02_partition_by(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '02_partition_by.sql'))
        expected = [
            (1, 'Diana', 180000.0, 1), (1, 'Evan', 140000.0, 2), (1, 'George', 110000.0, 3),
            (1, 'Hannah', 105000.0, 4), (1, 'Kevin', 85000.0, 5),
            (2, 'Fiona', 150000.0, 1), (2, 'Julia', 98000.0, 2), (2, 'Ian', 95000.0, 3),
            (3, 'Laura', 120000.0, 1), (3, 'Mike', 75000.0, 2),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 03 - LAG: previous order's date (customer 3)
    def test_03_lag_lead(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '03_lag_lead.sql'))
        expected = [
            (4, '2023-03-05', None),
            (5, '2023-03-18', '2023-03-05'),
            (6, '2023-04-02', '2023-03-18'),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 04 - Windowed SUM running total (customer 1)
    def test_04_running_totals(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '04_running_totals.sql'))
        expected = [
            (1, '2023-01-10', 1540.0, 1540.0),
            (2, '2023-02-15', 105.0, 1645.0),
            (15, '2023-09-03', 120.0, 1765.0),
        ]
        assert_result(self, rows, expected, ordered=True)


if __name__ == '__main__':
    unittest.main()
