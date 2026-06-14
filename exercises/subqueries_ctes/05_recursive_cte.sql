-- ============================================================
-- Exercise: Recursive CTE over the employee hierarchy
-- Problem: Using a recursive CTE rooted at the top manager
--          (manager_id IS NULL), return id, name, and level for every
--          employee. The root is level 1, their direct reports are level 2,
--          and so on down the org chart.
-- Expected columns (in order): id, name, level
-- Ordering: level ASC, id ASC
-- Concepts: recursive CTE, WITH RECURSIVE
-- ============================================================
-- TODO: replace the placeholder below with your query
WITH RECURSIVE employee_hierarchy AS (
    -- Anchor member: start with the top manager (manager_id IS NULL)
    SELECT
        id,
        name,
        1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive member: join employees to the CTE to find direct reports
    SELECT
        e.id,
        e.name,
        eh.level + 1 AS level
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT id, name, level
FROM employee_hierarchy
ORDER BY level ASC, id ASC;
