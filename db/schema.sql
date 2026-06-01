-- ============================================================
-- Practice database schema for sql_fundamentals
--
-- A compact e-commerce + HR domain. Loaded into a fresh in-memory
-- SQLite database by db/harness.py before every test.
-- ============================================================

-- Lookup / catalog tables
CREATE TABLE categories (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    id           INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    category_id  INTEGER NOT NULL REFERENCES categories(id),
    price        REAL    NOT NULL
);

-- Customers and their orders
CREATE TABLE customers (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    country      TEXT NOT NULL,
    signup_date  TEXT NOT NULL          -- ISO-8601 'YYYY-MM-DD'
);

CREATE TABLE orders (
    id           INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(id),
    order_date   TEXT    NOT NULL,      -- ISO-8601 'YYYY-MM-DD'
    status       TEXT    NOT NULL       -- 'completed' | 'shipped' | 'pending' | 'cancelled'
);

CREATE TABLE order_items (
    id          INTEGER PRIMARY KEY,
    order_id    INTEGER NOT NULL REFERENCES orders(id),
    product_id  INTEGER NOT NULL REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    unit_price  REAL    NOT NULL        -- price charged at order time
);

-- HR side: a self-referencing management hierarchy
CREATE TABLE departments (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE employees (
    id             INTEGER PRIMARY KEY,
    name           TEXT    NOT NULL,
    manager_id     INTEGER REFERENCES employees(id),   -- NULL for the top of the org
    department_id  INTEGER NOT NULL REFERENCES departments(id),
    salary         REAL    NOT NULL,
    hire_date      TEXT    NOT NULL                     -- ISO-8601 'YYYY-MM-DD'
);
