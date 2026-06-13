-- ============================================================
-- Exercise: Self join with LEFT JOIN
-- Problem: Return each employee's name and their manager's name.
--          The top of the org (manager_id IS NULL) must still appear,
--          with a NULL manager -- so join employees to itself with a
--          LEFT JOIN on e.manager_id = m.id.
-- Expected columns (in order): employee, manager
-- Ordering: employee id ASC
-- Concepts: self join, LEFT JOIN, NULL
-- ============================================================
-- TODO: replace the placeholder below with your query
SELECT e.name as employee_name, m.name as manager_name
FROM employees e 
LEFT JOIN employees m ON e.manager_id = m.id
ORDER BY e.id ASC;

