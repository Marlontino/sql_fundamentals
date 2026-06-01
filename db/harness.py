"""Test harness for sql_fundamentals.

Every test builds a *fresh* in-memory database in setUp, runs a learner's
.sql file against it, and compares the result to a baked-in expected set.

Public API
----------
DB lifecycle:
    build_db()                         -> fresh in-memory connection (schema + seed)

Running learner files:
    run_sql_file(conn, path)           -> list[tuple]   (a single SELECT)
    run_script_file(conn, path)        -> None          (multi-statement DDL/DML)

Assertion:
    assert_result(test, actual, expected, ordered=False)

DDL introspection helpers (for ddl_schema_design):
    table_info(conn, table)            -> list of column-info dicts
    foreign_keys(conn, table)          -> list of FK-info dicts
    index_list(conn, table)            -> list of index-info dicts
    expect_integrity_error(test)       -> context manager (fails if no IntegrityError)
"""

import os
import sqlite3
from contextlib import contextmanager

# Paths
_HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(_HERE, "schema.sql")
SEED_PATH = os.path.join(_HERE, "seed.sql")


# DB lifecycle
def build_db():
    """Return a fresh in-memory SQLite connection with schema + seed loaded.

    Foreign-key enforcement is turned ON (it is OFF by default in SQLite),
    so FK violations raise sqlite3.IntegrityError as learners expect.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    return conn


# Running learner files
def run_sql_file(conn, path):
    """Execute a learner .sql file holding a single SELECT; return list[tuple].

    Use this for query exercises. The file is expected to contain one
    statement that produces rows.
    """
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    cur = conn.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return [tuple(r) for r in rows]


def run_script_file(conn, path):
    """Execute a learner .sql file containing multiple statements (DDL/DML).

    Use this for schema-design exercises that CREATE tables, insert rows,
    run transactions, etc. Returns None; introspect the resulting schema
    with the helpers below.
    """
    with open(path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()


# Assertion
def _sort_key(row):
    """Stable, type-agnostic ordering key for unordered comparison.

    repr() gives a deterministic string across mixed types (None, int, float,
    str) without raising on cross-type '<' comparisons under Python 3.
    """
    return repr(row)


def assert_result(testcase, actual, expected, ordered=False):
    """Compare two result sets of rows (lists of tuples).

    ordered=False (default): compare as multisets by sorting both sides on a
    repr-based key, so problems that don't specify an ORDER BY are not
    over-constrained. ordered=True: compare row-for-row in the given order.
    """
    actual = [tuple(r) for r in actual]
    expected = [tuple(r) for r in expected]
    if ordered:
        testcase.assertEqual(actual, expected)
    else:
        testcase.assertEqual(
            sorted(actual, key=_sort_key),
            sorted(expected, key=_sort_key),
        )


# DDL introspection helpers
def table_info(conn, table):
    """Return PRAGMA table_info(table) rows as a list of dicts.

    Keys: cid, name, type, notnull, dflt_value, pk.
    """
    cur = conn.execute(f"PRAGMA table_info({table});")
    cols = [
        {
            "cid": cid,
            "name": name,
            "type": ctype,
            "notnull": notnull,
            "dflt_value": dflt,
            "pk": pk,
        }
        for (cid, name, ctype, notnull, dflt, pk) in cur.fetchall()
    ]
    cur.close()
    return cols


def foreign_keys(conn, table):
    """Return PRAGMA foreign_key_list(table) rows as a list of dicts.

    Keys: id, seq, table (referenced), from, to, on_update, on_delete, match.
    """
    cur = conn.execute(f"PRAGMA foreign_key_list({table});")
    fks = [
        {
            "id": fid,
            "seq": seq,
            "table": ref_table,
            "from": from_col,
            "to": to_col,
            "on_update": on_update,
            "on_delete": on_delete,
            "match": match,
        }
        for (fid, seq, ref_table, from_col, to_col, on_update, on_delete, match)
        in cur.fetchall()
    ]
    cur.close()
    return fks


def index_list(conn, table):
    """Return PRAGMA index_list(table) rows as a list of dicts.

    Keys: seq, name, unique, origin, partial.
    """
    cur = conn.execute(f"PRAGMA index_list({table});")
    idxs = [
        {
            "seq": seq,
            "name": name,
            "unique": unique,
            "origin": origin,
            "partial": partial,
        }
        for (seq, name, unique, origin, partial) in cur.fetchall()
    ]
    cur.close()
    return idxs


@contextmanager
def expect_integrity_error(testcase):
    """Context manager asserting the wrapped block raises sqlite3.IntegrityError.

    Fails the test if the block completes without raising (e.g. a CHECK / FK /
    UNIQUE / NOT NULL constraint the learner forgot to declare).
    """
    try:
        yield
    except sqlite3.IntegrityError:
        return
    testcase.fail("expected sqlite3.IntegrityError, but no exception was raised")
