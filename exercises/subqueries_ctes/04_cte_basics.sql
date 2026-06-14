-- ============================================================
-- Exercise: CTE (WITH) with an aggregate over the CTE
-- Problem: Using a CTE that computes total_spent per customer
--          (SUM(quantity * unit_price) over customers -> orders -> order_items),
--          return name and total_spent for customers whose total_spent is
--          strictly greater than the average customer total_spent
--          (averaged over the CTE rows).
-- Expected columns (in order): name, total_spent
-- Ordering: total_spent DESC, name ASC
-- Concepts: CTE (WITH), aggregate over a CTE
-- ============================================================
-- TODO: replace the placeholder below with your query
WITH customer_spending AS (
    SELECT
        c.id AS customer_id,
        c.name AS name,
        SUM(oi.quantity * oi.unit_price) AS total_spent
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    JOIN order_items oi ON o.id = oi.order_id
    GROUP BY c.id, c.name
)
SELECT name, total_spent
FROM customer_spending
WHERE total_spent > (SELECT AVG(total_spent) FROM customer_spending)
ORDER BY total_spent DESC, name ASC;    