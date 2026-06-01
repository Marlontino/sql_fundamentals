# SQL Primer — Lesson Zero

A refresher on the ideas the exercises lean on. Skim it once before you start,
and come back to it when a problem references a concept you want to nail down.
Everything here is true for SQLite (the engine these exercises run on); most of
it is true for any SQL database.

---

## 1. The relational model

A **relation** is a table: a set of **rows** (tuples), each with the same named
**columns** (attributes). Two ideas do most of the work:

- **A table is conceptually a *set* of rows.** There's no inherent order, and
  no row numbers — if you want order, you ask for it with `ORDER BY`. If you
  want a guaranteed-unique handle on a row, that's what a **primary key** is.
- **Relationships are expressed by *values*, not pointers.** An `order` doesn't
  contain its customer; it stores a `customer_id` that *equals* some
  `customers.id`. That stored reference is a **foreign key**. You reconstruct
  the relationship at query time with a **join**.

The practice schema (see [`db/schema.sql`](db/schema.sql)):

```
categories ──< products ──< order_items >── orders >── customers
                                                  
departments ──< employees ──┐
                  ^         │  (employees.manager_id -> employees.id,
                  └─────────┘   a self-reference: the org hierarchy)
```

`──<` means "one-to-many": one category has many products; one order has many
order_items; one customer has many orders. `employees.manager_id` points back
into `employees`, so the table references *itself* — that's what makes the
recursive-CTE exercise possible.

---

## 2. Logical query processing order

You *write* a query in one order but the database *evaluates* the clauses in
another. Knowing the logical order explains almost every "why can't I do that
here?" question:

| Step | Clause      | What it does                                            |
|------|-------------|---------------------------------------------------------|
| 1    | `FROM` / `JOIN` | Pick the tables and combine them into rows.         |
| 2    | `WHERE`     | Keep rows matching a condition (before grouping).       |
| 3    | `GROUP BY`  | Collapse rows into one row per group.                   |
| 4    | `HAVING`    | Keep groups matching a condition (after grouping).      |
| 5    | `SELECT`    | Choose/compute the output columns; assign aliases.      |
| 6    | `DISTINCT`  | Remove duplicate output rows.                           |
| 7    | `ORDER BY`  | Sort the result.                                        |
| 8    | `LIMIT`     | Take the first N rows.                                  |

Consequences worth memorizing:

- **`WHERE` runs before `GROUP BY`**, so it filters individual rows. To filter
  on an aggregate (e.g. "groups with `COUNT(*) > 3`"), you need **`HAVING`**,
  which runs after grouping.
- **`SELECT` aliases aren't visible to `WHERE`, `GROUP BY`, or `HAVING`** in
  standard SQL, because those run first. (SQLite is lenient and often lets you
  use a select-alias in `GROUP BY`/`HAVING`/`ORDER BY`, but don't rely on it.)
- **`ORDER BY` runs last**, so it *can* use select-list aliases and even output
  column positions (`ORDER BY 2`).

---

## 3. `NULL` and three-valued logic

`NULL` means "unknown / no value." It is **not** zero and **not** the empty
string. Comparisons against it don't return true or false — they return a third
truth value, **unknown**:

```sql
NULL = NULL      -- unknown (NOT true!)
NULL = 5         -- unknown
5 <> NULL        -- unknown
```

`WHERE` keeps a row only when its condition is **true** — `unknown` rows are
dropped. That's why you must test for null with the dedicated operators:

```sql
WHERE manager_id IS NULL        -- correct
WHERE manager_id = NULL         -- never matches anything
```

Other consequences:

- **Aggregates skip `NULL`.** `COUNT(col)` counts non-null values; `COUNT(*)`
  counts rows. `AVG`, `SUM`, etc. ignore nulls.
- **`NOT IN (subquery)` is a trap** when the subquery can return a `NULL`: the
  whole expression can collapse to `unknown` and match no rows. Prefer
  `NOT EXISTS` for "rows with no match."
- Boolean logic is three-valued: `true AND unknown = unknown`,
  `true OR unknown = true`, `NOT unknown = unknown`.

In the seed data, `employees.manager_id` is `NULL` for Diana (the org's root) —
the one place a null lives in the data.

---

## 4. JOIN cheat sheet

A join combines rows from two tables on a condition (usually FK = PK).

- **`INNER JOIN`** — rows that match on **both** sides. Non-matching rows from
  either side are dropped.
  ```sql
  SELECT o.id, c.name
  FROM orders o
  JOIN customers c ON c.id = o.customer_id;
  ```
- **`LEFT JOIN`** (left outer) — **every** left row, plus matching right rows;
  where there's no match, the right columns come back `NULL`. This is how you
  find "rows with no related rows":
  ```sql
  SELECT c.name
  FROM customers c
  LEFT JOIN orders o ON o.customer_id = c.id
  WHERE o.id IS NULL;        -- customers who never ordered (e.g. Heidi)
  ```
- **`SELF JOIN`** — join a table to itself with aliases; used for hierarchies
  and row-to-row comparisons:
  ```sql
  SELECT e.name AS employee, m.name AS manager
  FROM employees e
  LEFT JOIN employees m ON m.id = e.manager_id;
  ```
- **`CROSS JOIN`** — every combination (Cartesian product). Rarely what you
  want; usually a sign of a missing `ON` condition.

SQLite has no `RIGHT JOIN` or `FULL OUTER JOIN` in older versions; swap the
table order and use `LEFT JOIN`. **Join vs. filter:** put the relationship in
`ON`; put row selection in `WHERE`. For inner joins they're interchangeable;
for outer joins the distinction matters (a condition on the right table in
`WHERE` quietly turns a `LEFT JOIN` back into an inner one).

---

## 5. Aggregation vs. window functions

Both compute over multiple rows, but they differ in *what comes back*:

- **`GROUP BY` + aggregate** collapses each group into **one** row:
  ```sql
  SELECT category_id, COUNT(*) FROM products GROUP BY category_id;
  ```
- A **window function** computes across a set of rows (the "window") but
  **keeps every row**:
  ```sql
  SELECT name, salary,
         RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rk
  FROM employees;
  ```
  `PARTITION BY` is "group by for windows"; `ORDER BY` inside `OVER(...)`
  defines the ordering the function sees (essential for `RANK`, `ROW_NUMBER`,
  `LAG`/`LEAD`, and running totals).

`ROW_NUMBER` always gives distinct 1,2,3…; `RANK` leaves gaps after ties
(1,1,3); `DENSE_RANK` doesn't (1,1,2).

---

## 6. Index intuition

An **index** is a sorted side-structure (a B-tree) on one or more columns. It
lets the engine find matching rows without scanning the whole table — the
database equivalent of a book's index versus reading cover to cover.

- Helps `WHERE col = ?`, `WHERE col > ?`, joins on the column, and `ORDER BY`
  on the column.
- **Primary keys and `UNIQUE` columns are indexed automatically.**
- Not free: each index must be updated on every `INSERT`/`UPDATE`/`DELETE`, and
  it takes space. Index the columns you filter/join on, not every column.
- A **composite index** on `(a, b)` helps queries that filter on `a` alone or
  `a` and `b`, but generally not `b` alone (think phone book: sorted by last
  then first name).

Use `PRAGMA index_list(table)` to see a table's indexes (the DDL exercises do
exactly this).

---

## 7. Normalization (1NF / 2NF / 3NF)

Normalization removes redundancy so a fact lives in exactly one place. The
first three normal forms, in plain terms:

- **1NF — atomic values.** Each cell holds a single value; no repeating groups
  or comma-separated lists in a column. One row per entity, columns are
  single-valued.
- **2NF — no partial-key dependencies.** (Only relevant with a *composite*
  primary key.) Every non-key column must depend on the **whole** key, not just
  part of it. If `order_items` were keyed on `(order_id, product_id)`, storing
  the product's *name* there would violate 2NF — name depends only on
  `product_id`, so it belongs in `products`.
- **3NF — no transitive dependencies.** Non-key columns must depend on the key
  and nothing but the key. Storing a `category_name` on `products` (when
  `products` already has `category_id`) violates 3NF: `category_name` depends
  on `category_id`, not on the product. Keep it in `categories`.

The practice schema is already normalized — that's why `products` stores
`category_id` (not a category name) and `order_items` stores its own
`unit_price` (the price *at order time*, a genuine fact about the line item,
distinct from the product's current `price`).

---

### Quick reference

```sql
-- skeleton of a full query, in the order you write it
SELECT   col, AGG(col) AS a          -- 5: choose/compute output
FROM     t1 JOIN t2 ON t2.fk = t1.id -- 1: sources
WHERE    row_condition               -- 2: filter rows
GROUP BY col                         -- 3: form groups
HAVING   AGG(col) > 0                -- 4: filter groups
ORDER BY a DESC                      -- 7: sort
LIMIT    10;                         -- 8: take top N
```

Now open [`README.md`](README.md) for how to run the tests, and start with
`exercises/core_querying/01_select_basics.sql`.
