-- ============================================================
-- Exercise: Set operations
-- Problem: Return the customer_ids that appear in BOTH sets:
--            * customers with at least one 'completed' order
--            * customers with at least one 'shipped'   order
--          i.e. INTERSECT the two id sets.
-- Expected columns (in order): customer_id
-- Ordering: customer_id ASC
-- Concepts: INTERSECT
--   (SQLite also supports UNION (distinct), UNION ALL (keeps dupes),
--    and EXCEPT (set difference) -- all combine two SELECTs that have
--    the same column count/types.)
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT customer_id 
FROM orders 
WHERE status = 'completed'

INTERSECT

SELECT customer_id 
FROM orders 
WHERE status = 'shipped'

ORDER BY customer_id ASC;