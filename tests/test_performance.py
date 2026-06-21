import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import build_db, run_script_file

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'performance')


# Helper
def query_plan(conn, sql):
    """Return the EXPLAIN QUERY PLAN output as a single newline-joined string.

    SQLite's plan output is a small set of rows; for these exercises we only
    need substring matching ('SCAN', 'SEARCH', the index name), so flattening
    to one string is enough.
    """
    rows = conn.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
    return "\n".join(str(r) for r in rows)


class TestPerformance(unittest.TestCase):
    # Fresh in-memory DB per test
    def setUp(self): self.conn = build_db()
    def tearDown(self): self.conn.close()

    # 01 - no index on user_id: plan must SCAN
    def test_01_explain_query_plan(self):
        run_script_file(self.conn, os.path.join(EXDIR, '01_explain_query_plan.sql'))
        plan = query_plan(self.conn, "SELECT * FROM events_log WHERE user_id = 42")
        self.assertIn('SCAN', plan,
                      f"expected a SCAN (no index on user_id), got plan:\n{plan}")
        n = self.conn.execute(
            "SELECT COUNT(*) FROM events_log WHERE user_id = 42").fetchone()[0]
        self.assertEqual(n, 3)

    # 02 - with idx_events_log_user the plan must SEARCH that index
    def test_02_index_impact(self):
        run_script_file(self.conn, os.path.join(EXDIR, '02_index_impact.sql'))
        plan = query_plan(self.conn, "SELECT * FROM events_log WHERE user_id = 42")
        self.assertIn('SEARCH', plan,
                      f"expected a SEARCH using idx_events_log_user, got plan:\n{plan}")
        self.assertIn('idx_events_log_user', plan,
                      f"expected the plan to name idx_events_log_user, got:\n{plan}")
        n = self.conn.execute(
            "SELECT COUNT(*) FROM events_log WHERE user_id = 42").fetchone()[0]
        self.assertEqual(n, 3)


if __name__ == '__main__':
    unittest.main()
