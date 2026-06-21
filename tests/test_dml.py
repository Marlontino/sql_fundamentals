import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_script_file, assert_result

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'dml')


class TestDml(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - CREATE + multi-row INSERT into staff
    def test_01_insert_basic(self):
        run_script_file(self.conn, os.path.join(EXDIR, '01_insert_basic.sql'))
        rows = self.conn.execute(
            "SELECT id, name, role FROM staff ORDER BY id").fetchall()
        expected = [
            (1, 'Alice', 'engineer'),
            (2, 'Bob',   'designer'),
            (3, 'Carol', 'engineer'),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 02 - UPDATE ... SET ... WHERE: 10% discount on price > 50
    def test_02_update_filtered(self):
        run_script_file(self.conn, os.path.join(EXDIR, '02_update_filtered.sql'))
        rows = self.conn.execute(
            "SELECT id, name, price FROM widgets ORDER BY id").fetchall()
        expected = [
            (1, 'small',  10.0),
            (2, 'medium', 50.0),
            (3, 'large',  90.0),
            (4, 'xl',     180.0),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 03 - DELETE ... WHERE: remove rows with status='cancelled'
    def test_03_delete_filtered(self):
        run_script_file(self.conn, os.path.join(EXDIR, '03_delete_filtered.sql'))
        rows = self.conn.execute(
            "SELECT id, status FROM order_log ORDER BY id").fetchall()
        expected = [
            (1, 'completed'),
            (3, 'completed'),
            (5, 'pending'),
        ]
        assert_result(self, rows, expected, ordered=True)

    # 04 - INSERT ... ON CONFLICT DO UPDATE: page-view counters
    def test_04_upsert(self):
        run_script_file(self.conn, os.path.join(EXDIR, '04_upsert.sql'))
        rows = self.conn.execute(
            "SELECT page, views FROM page_counters ORDER BY page").fetchall()
        expected = [
            ('about', 1),
            ('home',  3),
        ]
        assert_result(self, rows, expected, ordered=True)


if __name__ == '__main__':
    unittest.main()
