# sql_fundamentals

Learn SQL the way you'd learn anything that sticks: by writing it. Each
exercise is a **documented `.sql` stub** you fill in, and a **Python `unittest`
suite encodes the expected result** so the test stays red until your query is
correct. The tests *are* the spec.

This mirrors a scaffold + tests-as-spec model: nothing here ships a reference
solution. You write the SQL; the suite tells you when it's right.

## Tech & constraints

- **Engine:** SQLite via Python's standard-library `sqlite3` — zero
  dependencies, nothing to install.
- **Tests:** the stdlib `unittest` framework (not pytest).
- **Database:** a compact e-commerce + HR schema, rebuilt fresh in memory for
  every test from [`db/schema.sql`](db/schema.sql) and
  [`db/seed.sql`](db/seed.sql). The seed is deterministic so tests can assert
  exact rows.

## How to run

From the **repo root**:

```
python -m unittest discover
```

Run a single topic:

```
python -m unittest tests.test_core_querying
```

See the full curriculum index any time:

```
python main.py
```

### What "passing" looks like

- `tests/test_harness.py` **passes out of the box** — it confirms the database
  builds and the seed loaded the expected row counts. If it fails, the problem
  is in `db/`, not in your answer.
- Every **exercise test fails initially**. That's the intended starting state:
  each `.sql` stub contains a placeholder (`SELECT NULL AS todo;`) that returns
  the wrong rows on purpose. Replace it with a real query and the test goes
  green.

## How to work an exercise

1. Open the `.sql` file under `exercises/<topic>/`.
2. Read the comment header: it states the problem, the **expected columns in
   order**, the **required ordering** (if any), and the concepts in play.
3. Replace the `SELECT NULL AS todo;` placeholder with your query.
4. Run that topic's tests. Iterate until green.

A note on ordering: tests that specify an `ORDER BY` in the header are compared
*ordered* — your row order must match. Tests with no required ordering compare
as sets, so you don't have to sort.

## Suggested order

Work the topics top to bottom. Within a topic, the files are numbered in the
order to attempt them.

1. **`core_querying/`** — `SELECT`, `WHERE`, `ORDER BY`/`LIMIT`/`DISTINCT`,
   aggregates, `GROUP BY`/`HAVING`, joins, set operations.
2. **`subqueries_ctes/`** — scalar subqueries, `IN`/`EXISTS` (incl.
   correlated), derived tables, CTEs, and a recursive CTE over the employee
   hierarchy.
3. **`window_functions/`** — `ROW_NUMBER`/`RANK`, `PARTITION BY`, `LAG`/`LEAD`,
   running totals.
4. **`ddl_schema_design/`** — `CREATE TABLE`, constraints (PK/FK/UNIQUE/CHECK),
   indexes, views, transactions. These exercises create **new** tables so they
   don't collide with the seeded schema.

New to SQL or rusty? Read [`SQL_PRIMER.md`](SQL_PRIMER.md) first — it's a
"lesson zero" covering the relational model, logical query order, `NULL`
three-valued logic, a JOIN cheat sheet, index intuition, and normalization.

## Layout

```
sql_fundamentals/
├── README.md          # you are here
├── SQL_PRIMER.md      # lesson zero
├── main.py            # prints the curriculum index + run instructions
├── db/
│   ├── schema.sql     # table definitions
│   ├── seed.sql       # deterministic seed data
│   └── harness.py     # build_db / run_sql_file / assert_result / DDL helpers
├── exercises/         # plain .sql stubs grouped by topic (not a Python package)
│   ├── core_querying/
│   ├── subqueries_ctes/
│   ├── window_functions/
│   └── ddl_schema_design/
└── tests/             # one test module per topic
```
