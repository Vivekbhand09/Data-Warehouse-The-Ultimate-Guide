-- Databricks notebook source
-- MAGIC %md
-- MAGIC ## SCD TYPE - 1

-- COMMAND ----------

SELECT * FROM sales_new.orders

-- COMMAND ----------

CREATE OR REPLACE VIEW sales_new.view_DimProducts
AS
SELECT DISTINCT(ProductID) as ProductID, ProductName, ProductCategory
FROM sales_new.orders
WHERE OrderDate > '2024-02-10'

-- COMMAND ----------

CREATE OR REPLACE TABLE sales_new.DimProducts 
(
  ProductID INT,
  ProductName STRING,
  ProductCategory STRING 
)

-- COMMAND ----------

INSERT INTO sales_new.DimProducts
SELECT ProductID, ProductName, ProductCategory FROM sales_new.view_DimProducts

-- COMMAND ----------

SELECT * FROM sales_new.DimProducts

-- COMMAND ----------

INSERT INTO sales_new.Orders (OrderID, OrderDate, CustomerID, CustomerName, CustomerEmail, ProductID, ProductName, ProductCategory, RegionID, RegionName, Country, Quantity, UnitPrice, TotalAmount) 
VALUES 
(1, '2024-02-11', 101, 'Alice Johnson', 'alice@example.com', 201, 'Gaming Laptop', 'Electronics', 301, 'North America', 'USA', 2, 800.00, 1600.00),
(2, '2024-02-12', 102, 'Bob Smith', 'bob@example.com', 230, 'Airpods', 'Electronics', 302, 'Europe', 'Germany', 1, 500.00, 500.00)

-- COMMAND ----------

SELECT * FROM sales_new.view_DimProducts

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## MERGE - SCD TYPE - 1

-- COMMAND ----------

MERGE INTO sales_new.DimProducts AS trg 
USING sales_new.view_DimPrOducts AS src 
ON trg.ProductID = src.ProductID 
WHEN MATCHED THEN UPDATE SET * 
WHEN NOT MATCHED THEN INSERT *

-- COMMAND ----------

SELECT * FROM sales_new.DimProducts

-- COMMAND ----------

