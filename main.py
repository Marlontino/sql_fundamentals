"""sql_fundamentals — curriculum index and run instructions.

Run me to see the full exercise list and how to work through it:

    python main.py
"""

# Curriculum definition
CURRICULUM = [
    (
        "core_querying",
        "The bread and butter of SELECT: shaping, filtering, and combining rows.",
        [
            ("01_select_basics.sql", "Projection, column aliases, computed columns"),
            ("02_filtering.sql", "WHERE, IN, BETWEEN, LIKE, IS NULL"),
            ("03_sorting_limiting.sql", "ORDER BY, LIMIT, DISTINCT"),
            ("04_aggregates.sql", "COUNT, SUM, AVG, MIN, MAX"),
            ("05_group_by_having.sql", "GROUP BY and filtering groups with HAVING"),
            ("06_joins.sql", "INNER / LEFT / self joins"),
            ("07_set_operations.sql", "UNION, UNION ALL, INTERSECT, EXCEPT"),
        ],
    ),
    (
        "subqueries_ctes",
        "Composing queries out of other queries.",
        [
            ("01_scalar_subquery.sql", "Subqueries that return a single value"),
            ("02_in_exists.sql", "IN / EXISTS, including correlated subqueries"),
            ("03_derived_tables.sql", "Subqueries in the FROM clause"),
            ("04_cte_basics.sql", "Naming subqueries with WITH"),
            ("05_recursive_cte.sql", "Walking the employee hierarchy recursively"),
        ],
    ),
    (
        "window_functions",
        "Per-row calculations over a window of related rows.",
        [
            ("01_row_number_rank.sql", "ROW_NUMBER, RANK, DENSE_RANK"),
            ("02_partition_by.sql", "PARTITION BY to compute within groups"),
            ("03_lag_lead.sql", "LAG / LEAD to reach neighboring rows"),
            ("04_running_totals.sql", "Running totals with windowed SUM"),
        ],
    ),
    (
        "ddl_schema_design",
        "Designing schemas: tables, constraints, indexes, views, transactions.",
        [
            ("01_create_table.sql", "CREATE TABLE with appropriate column types"),
            ("02_constraints.sql", "PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK"),
            ("03_indexes.sql", "CREATE INDEX for lookups"),
            ("04_views.sql", "CREATE VIEW to encapsulate a query"),
            ("05_transactions.sql", "BEGIN / COMMIT / ROLLBACK"),
        ],
    ),
]


# Rendering
def print_index():
    print("=" * 64)
    print(" sql_fundamentals - SQL practice via scaffold + tests-as-spec")
    print("=" * 64)
    print()
    print("Each exercise is a .sql stub under exercises/<topic>/. Open it,")
    print("read the problem in the comment header, and replace the placeholder")
    print("query. A unittest in tests/ encodes the expected result, so the test")
    print("stays RED until your query is correct.")
    print()

    n = 0
    for topic, blurb, items in CURRICULUM:
        print(f"  {topic}/")
        print(f"    {blurb}")
        for filename, desc in items:
            n += 1
            print(f"      - {filename:<26} {desc}")
        print()

    print(f"Total: {n} exercises across {len(CURRICULUM)} topics.")
    print()
    print("-" * 64)
    print(" How to run the tests")
    print("-" * 64)
    print("  From the repo root:")
    print()
    print("      python -m unittest discover")
    print()
    print("  Run a single topic's tests:")
    print()
    print("      python -m unittest tests.test_core_querying")
    print()
    print("  tests/test_harness.py passes out of the box (it checks the DB")
    print("  builds and the seed loaded). Every exercise test fails until you")
    print("  solve the matching .sql file.")
    print()
    print("  Suggested order: work the topics top-to-bottom as listed above.")
    print("  Read SQL_PRIMER.md first if you want a refresher on the model.")


if __name__ == "__main__":
    print_index()
