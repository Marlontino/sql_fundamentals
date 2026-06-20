-- ============================================================
-- Exercise: Rank employees by salary within their department
-- Problem: Within each department, rank employees by salary (highest = 1).
--          The ranking RESTARTS at 1 for every department.
-- Expected columns (in order): department_id, name, salary, dept_rank
-- Ordering: department_id ASC, dept_rank ASC
-- Concepts: PARTITION BY, RANK
--
-- PARTITION BY splits the rows into independent groups; the window function
-- is computed separately within each group (much like GROUP BY, but without
-- collapsing rows). The ranking counter resets at the start of each partition:
--   RANK() OVER (PARTITION BY department_id ORDER BY salary DESC)
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT department_id, name, salary,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dept_rank
FROM employees 
ORDER BY department_id ASC, dept_rank ASC;
