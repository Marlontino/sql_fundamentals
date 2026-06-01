-- ============================================================
-- Deterministic seed data for sql_fundamentals
--
-- Every value here is fixed so the test suite can assert exact rows.
-- Notable shapes worth knowing while authoring/solving:
--   * customer Heidi (id 8) has NO orders   -> LEFT JOIN / NOT EXISTS
--   * employees.manager_id is a hierarchy rooted at Diana (id 1)
--                                            -> recursive CTE
--   * departments split 5 / 3 / 2 by headcount -> window ranking
-- ============================================================

-- Catalog
INSERT INTO categories (id,name) VALUES (1,'Electronics'),(2,'Books'),(3,'Clothing'),(4,'Home'),(5,'Toys');
INSERT INTO products (id,name,category_id,price) VALUES
 (1,'Laptop',1,1200.00),(2,'Headphones',1,150.00),(3,'Python Book',2,40.00),(4,'SQL Book',2,35.00),(5,'T-Shirt',3,20.00),
 (6,'Jeans',3,60.00),(7,'Coffee Maker',4,80.00),(8,'Desk Lamp',4,45.00),(9,'Action Figure',5,25.00),(10,'Board Game',5,30.00);

-- Customers
INSERT INTO customers (id,name,country,signup_date) VALUES
 (1,'Alice','USA','2022-01-15'),(2,'Bob','USA','2022-03-22'),(3,'Carol','Canada','2021-11-05'),(4,'Dave','UK','2022-06-30'),
 (5,'Eve','Canada','2023-02-14'),(6,'Frank','USA','2023-05-01'),(7,'Grace','Australia','2021-08-19'),(8,'Heidi','UK','2023-07-07');

-- Orders
INSERT INTO orders (id,customer_id,order_date,status) VALUES
 (1,1,'2023-01-10','completed'),(2,1,'2023-02-15','completed'),(3,2,'2023-01-20','shipped'),(4,3,'2023-03-05','completed'),
 (5,3,'2023-03-18','completed'),(6,3,'2023-04-02','pending'),(7,4,'2023-02-28','cancelled'),(8,5,'2023-05-10','completed'),
 (9,5,'2023-05-22','shipped'),(10,6,'2023-06-01','completed'),(11,7,'2023-01-05','completed'),(12,7,'2023-07-15','pending'),
 (13,2,'2023-08-01','completed'),(14,4,'2023-08-20','completed'),(15,1,'2023-09-03','shipped');

-- Order line items
INSERT INTO order_items (id,order_id,product_id,quantity,unit_price) VALUES
 (1,1,1,1,1200.00),(2,1,2,2,150.00),(3,1,3,1,40.00),(4,2,3,1,40.00),(5,2,4,1,35.00),(6,2,10,1,30.00),(7,3,5,3,20.00),
 (8,3,6,1,60.00),(9,4,1,1,1200.00),(10,4,7,1,80.00),(11,4,8,2,45.00),(12,4,2,1,150.00),(13,5,9,4,25.00),(14,6,10,2,30.00),
 (15,7,2,1,150.00),(16,8,3,2,40.00),(17,8,4,2,35.00),(18,8,5,1,20.00),(19,9,6,1,60.00),(20,10,7,1,80.00),(21,10,8,1,45.00),
 (22,10,10,2,30.00),(23,11,1,2,1200.00),(24,12,5,5,20.00),(25,13,10,3,30.00),(26,13,9,1,25.00),(27,13,4,2,35.00),
 (28,14,2,1,150.00),(29,14,3,1,40.00),(30,15,6,2,60.00);

-- HR: departments and a self-referencing employee hierarchy
INSERT INTO departments (id,name) VALUES (1,'Engineering'),(2,'Sales'),(3,'Marketing');
INSERT INTO employees (id,name,manager_id,department_id,salary,hire_date) VALUES
 (1,'Diana',NULL,1,180000.00,'2018-03-01'),(2,'Evan',1,1,140000.00,'2019-05-10'),(3,'Fiona',1,2,150000.00,'2019-07-20'),
 (4,'George',2,1,110000.00,'2020-02-15'),(5,'Hannah',2,1,105000.00,'2020-08-01'),(6,'Ian',3,2,95000.00,'2021-01-11'),
 (7,'Julia',3,2,98000.00,'2021-03-30'),(8,'Kevin',4,1,85000.00,'2022-06-01'),(9,'Laura',1,3,120000.00,'2019-09-09'),
 (10,'Mike',9,3,75000.00,'2022-11-20');
