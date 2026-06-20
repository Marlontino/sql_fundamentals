-- ============================================================
-- Exercise: Each order's previous order date (customer 3)
-- Problem: For customer 3's orders, in date order, show each order alongside
--          the date of that customer's PREVIOUS order. The earliest order has
--          no previous order, so its prev_order_date is NULL.
-- Expected columns (in order): order_id, order_date, prev_order_date
-- Ordering: order_date ASC
-- Concepts: LAG, LEAD
--
-- LAG and LEAD peek at OTHER rows relative to the current row within the
-- window's order:
--   LAG(col)  -> value from the PRECEDING row (NULL past the first row)
--   LEAD(col) -> value from the FOLLOWING row (NULL past the last row)
-- Here you want the prior order's date:
--   LAG(order_date) OVER (ORDER BY order_date)
-- Remember to filter to customer_id = 3.
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT id, order_date, LAG(order_date) OVER (ORDER BY order_date) AS prev_order_date
FROM orders
WHERE customer_id = 3
ORDER BY order_date ASC;
