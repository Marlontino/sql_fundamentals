-- ============================================================
-- Exercise: Filtering rows with WHERE
-- Problem: Return id, name, salary of employees who match ALL of:
--            * department_id IN (1, 2)
--            * salary BETWEEN 90000 AND 150000 (inclusive)
--            * name LIKE '%a%'   (contains a lowercase 'a')
--            * manager_id IS NOT NULL
-- Expected columns (in order): id, name, salary
-- Ordering: salary DESC, id ASC
-- Concepts: WHERE, IN, BETWEEN, LIKE, IS NOT NULL
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT id, name, salary
FROM employees
WHERE department_id IN (1, 2)
  AND salary BETWEEN 90000 AND 150000
  AND name LIKE '%a%'
  AND manager_id IS NOT NULL
ORDER BY salary DESC, id ASC;
