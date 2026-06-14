-- ============================================================
-- Exercise: Scalar subquery in SELECT
-- Problem: For each product, return its id, name, price, and how far its
--          price is from the average price across ALL products,
--          as diff_from_avg = ROUND(price - (average price), 2).
-- Expected columns (in order): id, name, price, diff_from_avg
-- Ordering: id ASC
-- Concepts: scalar subquery in SELECT
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT 
    id, 
    name, 
    price, 
    ROUND(price - (SELECT AVG(price) FROM products), 2) AS diff_from_avg
FROM products
ORDER BY id ASC;
