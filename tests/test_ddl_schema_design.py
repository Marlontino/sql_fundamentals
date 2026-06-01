# ============================================================
# Tests for the DDL / schema-design exercises.
#
# Each test builds a fresh in-memory DB, runs the learner's .sql, and
# verifies the resulting schema via introspection (table_info /
# foreign_keys / index_list), integrity-error probes, or a view query.
# Expected values were captured from verified reference solutions.
# ============================================================

# Imports / path setup
import unittest, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.harness import (build_db, run_sql_file, run_script_file, assert_result,
                        table_info, foreign_keys, index_list, expect_integrity_error)

EXDIR = os.path.join(os.path.dirname(__file__), '..', 'exercises', 'ddl_schema_design')


# Helpers
def ex(name):
    """Absolute path to an exercise .sql file."""
    return os.path.join(EXDIR, name)


def cols(info):
    """Reduce table_info dicts to (name, type, notnull, pk) tuples in column order."""
    return [(c["name"], c["type"], c["notnull"], c["pk"]) for c in info]


# Test suite
class TestDdlSchemaDesign(unittest.TestCase):
    def setUp(self):
        self.conn = build_db()

    def tearDown(self):
        self.conn.close()

    # 01 — CREATE TABLE with appropriate types
    def test_01_create_table(self):
        run_script_file(self.conn, ex("01_create_table.sql"))
        expected = [
            ("id", "INTEGER", 0, 1),
            ("name", "TEXT", 1, 0),
            ("country", "TEXT", 1, 0),
            ("rating", "REAL", 0, 0),
        ]
        self.assertEqual(cols(table_info(self.conn, "suppliers")), expected)

    # 02 — PK / FK / UNIQUE / CHECK constraints
    def test_02_constraints(self):
        run_script_file(self.conn, ex("02_constraints.sql"))

        # Column shape (incl. NOT NULL flags)
        expected_cols = [
            ("id", "INTEGER", 0, 1),
            ("product_id", "INTEGER", 1, 0),
            ("author", "TEXT", 1, 0),
            ("rating", "INTEGER", 1, 0),
        ]
        self.assertEqual(cols(table_info(self.conn, "reviews")), expected_cols)

        # FK points to products(id)
        fks = foreign_keys(self.conn, "reviews")
        self.assertEqual(len(fks), 1)
        self.assertEqual(fks[0]["table"], "products")
        self.assertEqual(fks[0]["from"], "product_id")
        self.assertEqual(fks[0]["to"], "id")

        # CHECK violation: rating out of 1..5
        with expect_integrity_error(self):
            self.conn.execute(
                "INSERT INTO reviews(id,product_id,author,rating) VALUES (100,1,'amy',6)")

        # FK violation: product_id 999 does not exist
        with expect_integrity_error(self):
            self.conn.execute(
                "INSERT INTO reviews(id,product_id,author,rating) VALUES (101,999,'amy',3)")

        # NOT NULL violation: author NULL
        with expect_integrity_error(self):
            self.conn.execute(
                "INSERT INTO reviews(id,product_id,author,rating) VALUES (102,1,NULL,3)")

        # UNIQUE violation: duplicate (product_id, author)
        self.conn.execute(
            "INSERT INTO reviews(id,product_id,author,rating) VALUES (200,2,'sam',4)")
        with expect_integrity_error(self):
            self.conn.execute(
                "INSERT INTO reviews(id,product_id,author,rating) VALUES (201,2,'sam',5)")

    # 03 — CREATE INDEX (plain + UNIQUE)
    def test_03_indexes(self):
        run_script_file(self.conn, ex("03_indexes.sql"))
        idx = {i["name"]: i["unique"] for i in index_list(self.conn, "events")}
        self.assertIn("idx_events_user", idx)
        self.assertEqual(idx["idx_events_user"], 0)
        self.assertIn("uq_events_kind_time", idx)
        self.assertEqual(idx["uq_events_kind_time"], 1)

    # 04 — CREATE VIEW
    def test_04_views(self):
        run_script_file(self.conn, ex("04_views.sql"))
        rows = self.conn.execute(
            "SELECT customer_id, order_count FROM customer_order_counts "
            "ORDER BY customer_id").fetchall()
        expected = [(1, 3), (2, 2), (3, 3), (4, 2), (5, 2), (6, 1), (7, 2)]
        assert_result(self, rows, expected, ordered=True)

    # 05 — transactions: COMMIT keeps, ROLLBACK discards
    def test_05_transactions(self):
        run_script_file(self.conn, ex("05_transactions.sql"))
        rows = self.conn.execute(
            "SELECT id, balance FROM accounts ORDER BY id").fetchall()
        expected = [(1, 70.0), (2, 30.0)]
        assert_result(self, rows, expected, ordered=True)


if __name__ == "__main__":
    unittest.main()
