"""Smoke test for the harness itself.

Unlike the exercise tests, this one PASSES out of the box: it proves the
database builds and the deterministic seed loaded the expected row counts.
If this fails, something is wrong with db/ rather than with a learner answer.
"""

import os
import sys
import unittest

# Make `from db.harness import ...` work when run via `unittest discover`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.harness import build_db, foreign_keys, table_info


class TestHarness(unittest.TestCase):
    def setUp(self):
        self.conn = build_db()

    def tearDown(self):
        self.conn.close()

    # Seed row counts (deterministic — see db/seed.sql)
    def test_seed_row_counts(self):
        expected = {
            "categories": 5,
            "products": 10,
            "customers": 8,
            "orders": 15,
            "order_items": 30,
            "departments": 3,
            "employees": 10,
        }
        for table, count in expected.items():
            with self.subTest(table=table):
                (actual,) = self.conn.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()
                self.assertEqual(actual, count)

    # Foreign keys are enforced (PRAGMA foreign_keys = ON)
    def test_foreign_keys_enforced(self):
        with self.assertRaises(Exception):
            self.conn.execute(
                "INSERT INTO products (id,name,category_id,price) "
                "VALUES (999,'Ghost',999,1.0)"
            )

    # Schema introspection helpers return sane data
    def test_introspection_helpers(self):
        cols = {c["name"] for c in table_info(self.conn, "orders")}
        self.assertEqual(cols, {"id", "customer_id", "order_date", "status"})
        fks = foreign_keys(self.conn, "order_items")
        referenced = {fk["table"] for fk in fks}
        self.assertEqual(referenced, {"orders", "products"})


if __name__ == "__main__":
    unittest.main()
