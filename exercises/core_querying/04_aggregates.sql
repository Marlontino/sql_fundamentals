-- ============================================================
-- Exercise: Aggregates over joined tables
-- Problem: Return each customer's id, name, and total_spent, where
--          total_spent = SUM(quantity * unit_price) across every line
--          item in all of that customer's orders.
--          (Customers with no orders are excluded by the inner join.)
-- Expected columns (in order): customer_id, name, total_spent
-- Ordering: total_spent DESC, customer_id ASC
-- Concepts: JOIN, SUM, GROUP BY, ORDER BY
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT c.id AS customer_id, c.name, SUM(oi.quantity * oi.unit_price) AS total_spent
FROM customers c
JOIN orders o ON c.id = o.customer_id
JOIN order_items oi ON o.id = oi.order_id
GROUP BY c.id, c.name
ORDER BY total_spent DESC, customer_id ASC;                  