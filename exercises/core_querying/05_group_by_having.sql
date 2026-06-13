-- ============================================================
-- Exercise: GROUP BY with HAVING
-- Problem: Return customers who have placed MORE THAN 2 orders.
--          Show their name and order_count (number of orders).
--          HAVING filters on the aggregate; WHERE cannot.
-- Expected columns (in order): name, order_count
-- Ordering: order_count DESC, name ASC
-- Concepts: GROUP BY, HAVING, COUNT
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT c.name, COUNT(*) AS order_count
FROM customers c
JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
HAVING COUNT(*) > 2
ORDER BY COUNT(*) DESC, c.name ASC;
