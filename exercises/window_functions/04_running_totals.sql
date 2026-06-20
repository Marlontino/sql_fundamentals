-- ============================================================
-- Exercise: Running total of order values (customer 1)
-- Problem: For customer 1's orders, in date order, return each order's total
--          value and a cumulative running total of those values over time.
--          order_total = SUM(quantity * unit_price) over that order's items.
--          running_total = cumulative sum of order_total up to and including
--          the current order, ordered by order_date.
-- Expected columns (in order): order_id, order_date, order_total, running_total
-- Ordering: order_date ASC
-- Concepts: windowed SUM, running total, frame clause
--
-- A windowed SUM with an ORDER BY (and a frame ending at the current row)
-- accumulates as it walks the rows -- a running total:
--   SUM(order_total) OVER (
--     ORDER BY order_date
--     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
-- The frame clause says "from the first row up to this row". (With ORDER BY,
-- that frame is the default, so it can be omitted -- but being explicit makes
-- the intent clear.)
--
-- Hint: first compute one row per order with its order_total (a CTE or derived
-- table that JOINs orders to order_items, filters customer_id = 1, and GROUPs
-- BY the order), then apply the windowed SUM over those per-order rows.
-- ============================================================
-- TODO: replace the placeholder below with your query
WITH order_totals AS (
    SELECT
        o.id AS order_id,
        o.order_date,
        SUM(oi.quantity * oi.unit_price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    WHERE o.customer_id = 1
    GROUP BY o.id, o.order_date
)
SELECT
    order_id,
    order_date,
    order_total,
    SUM(order_total) OVER (
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM order_totals
ORDER BY order_date ASC;