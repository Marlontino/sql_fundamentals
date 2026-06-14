-- ============================================================
-- Exercise: Correlated NOT EXISTS
-- Problem: Return the id and name of every customer who has NEVER placed
--          an order. Use a correlated NOT EXISTS subquery (a subquery that
--          references the outer customer row).
-- Expected columns (in order): id, name
-- Ordering: id ASC
-- Concepts: NOT EXISTS, correlated subquery
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT id, name
FROM customers
WHERE NOT EXISTS (
    SELECT 1
    FROM orders
    WHERE orders.customer_id = customers.id
);
