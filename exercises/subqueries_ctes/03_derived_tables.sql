-- ============================================================
-- Exercise: Derived table (subquery in FROM)
-- Problem: Build a derived table of per-order totals
--          (order_id, total = SUM(quantity * unit_price) grouped by order_id),
--          then return order_id and total for orders whose total > 500.
-- Expected columns (in order): order_id, total
-- Ordering: total DESC, order_id ASC
-- Concepts: derived table (subquery in FROM), GROUP BY
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT order_id, SUM(quantity * unit_price) AS total
FROM (
    SELECT order_id, quantity, unit_price
    FROM order_items
) AS oi
GROUP BY order_id
HAVING SUM(quantity * unit_price) > 500
ORDER BY total DESC, order_id ASC;
