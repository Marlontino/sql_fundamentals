-- ============================================================
-- Exercise: Select basics
-- Problem: Return every product's id, name, and a computed
--          price_with_tax = ROUND(price * 1.1, 2) (10% tax).
-- Expected columns (in order): id, name, price_with_tax
-- Ordering: id ASC
-- Concepts: SELECT, column alias, arithmetic
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT id, name, ROUND(price * 1.1, 2) AS price_with_tax
FROM products
ORDER BY id ASC;
