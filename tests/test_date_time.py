import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_sql_file, assert_result

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'date_time')


class TestDateTime(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - half-open date range filtering: January 2023 orders
    def test_01_date_filtering(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '01_date_filtering.sql'))
        expected = [
            (11, 7, '2023-01-05'),
            (1, 1, '2023-01-10'),
            (3, 2, '2023-01-20'),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 02 - bucket orders by month via strftime + GROUP BY
    def test_02_date_truncation(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '02_date_truncation.sql'))
        expected = [
            ('2023-01', 3), ('2023-02', 2), ('2023-03', 2),
            ('2023-04', 1), ('2023-05', 2), ('2023-06', 1),
            ('2023-07', 1), ('2023-08', 2), ('2023-09', 1),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 03 - tenure days between hire_date and 2024-01-01 via julianday
    def test_03_date_arithmetic(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '03_date_arithmetic.sql'))
        expected = [
            (1, 'Diana', 2132), (2, 'Evan', 1697), (3, 'Fiona', 1626),
            (4, 'George', 1416), (5, 'Hannah', 1248), (6, 'Ian', 1085),
            (7, 'Julia', 1007), (8, 'Kevin', 579), (9, 'Laura', 1575),
            (10, 'Mike', 407),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 04 - CASE-based bucketing of signup dates
    def test_04_age_buckets(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '04_age_buckets.sql'))
        expected = [
            (1, 'Alice', '2022'), (2, 'Bob', '2022'), (3, 'Carol', 'pre_2022'),
            (4, 'Dave', '2022'), (5, 'Eve', '2023_plus'), (6, 'Frank', '2023_plus'),
            (7, 'Grace', 'pre_2022'), (8, 'Heidi', '2023_plus'),
        ]
        assert_result(self, rows, expected, ordered=True)


if __name__ == '__main__':
    unittest.main()
