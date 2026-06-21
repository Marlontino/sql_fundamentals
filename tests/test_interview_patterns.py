import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_sql_file, assert_result

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'interview_patterns')


class TestInterviewPatterns(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - top 2 per group via windowed rank in a subquery
    def test_01_top_n_per_group(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '01_top_n_per_group.sql'))
        expected = [
            (1, 'Diana', 180000.0),
            (1, 'Evan', 140000.0),
            (2, 'Fiona', 150000.0),
            (2, 'Julia', 98000.0),
            (3, 'Laura', 120000.0),
            (3, 'Mike', 75000.0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 02 - gaps-and-islands: ROW_NUMBER trick to collapse runs
    def test_02_gaps_and_islands(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '02_gaps_and_islands.sql'))
        expected = [
            (1, 2, 2),
            (15, 15, 1),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 03 - sessionization: LAG -> gap flag -> running sum
    def test_03_sessionization(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '03_sessionization.sql'))
        expected = [
            (1, '2023-01-10', 1),
            (2, '2023-02-15', 2),
            (15, '2023-09-03', 3),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 04 - cohort retention: yearly cohort size + how many ever ordered
    def test_04_cohort_retention(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '04_cohort_retention.sql'))
        expected = [
            ('2021', 2, 2),
            ('2022', 3, 3),
            ('2023', 3, 2),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 05 - pivot statuses to columns with SUM(CASE ...)
    def test_05_pivot_with_case(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '05_pivot_with_case.sql'))
        expected = [
            (1, 2, 1, 0, 0),
            (2, 1, 1, 0, 0),
            (3, 2, 0, 1, 0),
            (4, 1, 0, 0, 1),
            (5, 1, 1, 0, 0),
            (6, 1, 0, 0, 0),
            (7, 1, 0, 1, 0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 06 - median order value via ROW_NUMBER + COUNT trick
    def test_06_median_percentile(self):
        rows = run_sql_file(self.conn, os.path.join(EXDIR, '06_median_percentile.sql'))
        expected = [
            (1, 120.0),
            (2, 152.5),
            (3, 100.0),
            (4, 170.0),
            (5, 115.0),
            (6, 185.0),
            (7, 1250.0),
        ]
        assert_result(self, rows, expected, ordered=True)


if __name__ == '__main__':
    unittest.main()
