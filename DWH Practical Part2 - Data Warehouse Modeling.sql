-- Databricks notebook source
-- MAGIC %md
-- MAGIC # ⭐ Building My First Star Schema — Full Walkthrough
-- MAGIC
-- MAGIC ## 🎯 What I Was Building
-- MAGIC
-- MAGIC Starting from the same `Orders` source table, I went further this time — instead of building one flat `core_sales` table, I split the warehouse's **core layer** into a proper **Star Schema**: 4 Dimension tables (`DimCustomers`, `DimProducts`, `DimRegion`, `DimDate`) surrounding 1 Fact table (`FactSales`).
-- MAGIC
-- MAGIC ```
-- MAGIC sales_new.Orders  →  stg_sales  →  trans_sales (view)  →  ⭐ FactSales + 4 Dim tables
-- MAGIC ```
-- MAGIC
-- MAGIC Staging and Transformation are unchanged from before — the real new work starts at the **Core layer**, where I'm now building a proper dimensional model instead of one flat table.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## 🗂️ Step 1 — Building Each Dimension Table
-- MAGIC
-- MAGIC Every dimension I built follows the **exact same repeatable pattern**, so once you understand one, you understand all four:
-- MAGIC
-- MAGIC ```
-- MAGIC 1. CREATE the physical table       (with a surrogate key column)
-- MAGIC 2. CREATE a view that:
-- MAGIC       - SELECTs DISTINCT natural-key rows from trans_sales
-- MAGIC       - Generates a surrogate key using row_number()
-- MAGIC 3. INSERT the view's output into the physical table
-- MAGIC ```
-- MAGIC
-- MAGIC ### 🧑 DimCustomers
-- MAGIC You listed the columns for this one:
-- MAGIC ```sql
-- MAGIC CustomerID INT,
-- MAGIC CustomerName VARCHAR(100),
-- MAGIC CustomerEmail VARCHAR(100),
-- MAGIC ```
-- MAGIC
-- MAGIC To follow the same pattern as your other three dimensions (and to make it actually joinable from the Fact table the way your `FactSales` code expects), this needs a **surrogate key column** and the same view + insert pattern:
-- MAGIC
-- MAGIC ```sql
-- MAGIC CREATE TABLE orderDWH.DimCustomers
-- MAGIC (
-- MAGIC   CustomerID INT,
-- MAGIC   CustomerName VARCHAR(100),
-- MAGIC   CustomerEmail VARCHAR(100),
-- MAGIC   DimCustomersKey INT
-- MAGIC );
-- MAGIC
-- MAGIC CREATE OR REPLACE VIEW orderDWH.view_DimCustomers
-- MAGIC AS
-- MAGIC SELECT T.*, row_number() OVER (ORDER BY T.CustomerID) AS DimCustomersKey FROM
-- MAGIC (
-- MAGIC   SELECT
-- MAGIC     DISTINCT(CustomerID) AS CustomerID,
-- MAGIC     CustomerName,
-- MAGIC     CustomerEmail
-- MAGIC   FROM
-- MAGIC     orderDWH.trans_sales
-- MAGIC ) AS T;
-- MAGIC
-- MAGIC INSERT INTO orderDWH.DimCustomers
-- MAGIC SELECT * FROM orderDWH.view_DimCustomers;
-- MAGIC ```
-- MAGIC
-- MAGIC **What's happening here, step by step:**
-- MAGIC 1. The inner `SELECT DISTINCT(CustomerID), CustomerName, CustomerEmail FROM trans_sales` pulls **one row per unique customer** out of your transactional-grain data (which has one row per order, so the same customer appears multiple times if they ordered more than once).
-- MAGIC 2. `row_number() OVER (ORDER BY CustomerID)` assigns a clean, sequential integer (1, 2, 3, ...) to each distinct customer — this is your **surrogate key**.
-- MAGIC 3. The `INSERT INTO ... SELECT * FROM view` materializes that view's result into the real physical table.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ### 📦 DimProducts
-- MAGIC ```sql
-- MAGIC CREATE TABLE orderDWH.DimProducts
-- MAGIC (
-- MAGIC   ProductID INT,
-- MAGIC   ProductName STRING,
-- MAGIC   ProductCategory STRING,
-- MAGIC   DimProductsKey INT 
-- MAGIC );
-- MAGIC
-- MAGIC CREATE OR REPLACE VIEW orderDWH.view_DimProducts
-- MAGIC AS 
-- MAGIC SELECT T.*, row_number() OVER (ORDER BY T.ProductID) AS DimCustomersKey FROM 
-- MAGIC (
-- MAGIC SELECT 
-- MAGIC   DISTINCT(ProductID) AS ProductID,
-- MAGIC   ProductName,
-- MAGIC   ProductCategory
-- MAGIC FROM 
-- MAGIC   orderDWH.trans_sales
-- MAGIC ) AS T;
-- MAGIC
-- MAGIC INSERT INTO orderdwh.DimProducts 
-- MAGIC SELECT * FROM orderdwh.view_DimProducts;
-- MAGIC ```
-- MAGIC
-- MAGIC Same exact pattern as `DimCustomers`, just for products: pull distinct `(ProductID, ProductName, ProductCategory)` combinations, generate a sequential surrogate key, load into the physical table.
-- MAGIC
-- MAGIC > ⚠️ **Small bug to flag:** in the view, the generated column is aliased `AS DimCustomersKey` — but this is the *products* view, and your `DimProducts` table's real column is `DimProductsKey`. This is almost certainly a copy-paste leftover from writing `DimCustomers` first. I'll cover the fix in the **Issues Found** section below.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ### 🌍 DimRegion
-- MAGIC ```sql
-- MAGIC CREATE OR REPLACE TABLE orderDWH.DimRegion 
-- MAGIC (
-- MAGIC   RegionID INT,
-- MAGIC   RegionName STRING,
-- MAGIC   Country STRING,
-- MAGIC   DimRegionKey INT
-- MAGIC );
-- MAGIC
-- MAGIC CREATE OR REPLACE VIEW orderDWH.view_DimRegion
-- MAGIC AS 
-- MAGIC SELECT T.*, row_number() OVER (ORDER BY T.RegionID) AS DimRegionKey FROM 
-- MAGIC (
-- MAGIC SELECT 
-- MAGIC   DISTINCT(RegionID) AS RegionID,
-- MAGIC   RegionName,
-- MAGIC   Country
-- MAGIC FROM 
-- MAGIC   orderDWH.trans_sales
-- MAGIC ) AS T;
-- MAGIC
-- MAGIC INSERT INTO orderdwh.DimRegion
-- MAGIC SELECT * FROM orderdwh.view_DimRegion;
-- MAGIC ```
-- MAGIC
-- MAGIC Same pattern again — distinct `(RegionID, RegionName, Country)` combinations, sequential surrogate key, load.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ### 📅 DimDate
-- MAGIC ```sql
-- MAGIC CREATE OR REPLACE TABLE orderDWH.DimDate
-- MAGIC (
-- MAGIC   OrderDate DATE,
-- MAGIC   DimDateKey INT
-- MAGIC );
-- MAGIC
-- MAGIC CREATE OR REPLACE VIEW orderDWH.view_DimDate
-- MAGIC AS 
-- MAGIC SELECT T.*, row_number() OVER (ORDER BY T.OrderDate) AS DimDateKey FROM 
-- MAGIC (
-- MAGIC SELECT 
-- MAGIC   DISTINCT(OrderDate) AS OrderDate
-- MAGIC FROM 
-- MAGIC   orderDWH.trans_sales
-- MAGIC ) AS T;
-- MAGIC
-- MAGIC INSERT INTO orderdwh.DimDate
-- MAGIC SELECT * FROM orderdwh.view_DimDate;
-- MAGIC ```
-- MAGIC
-- MAGIC Same pattern once more — every unique `OrderDate` gets a surrogate key. (I'll mention below how this dimension is usually made richer in real warehouses.)
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## 📈 Step 2 — Building the Fact Table
-- MAGIC
-- MAGIC ```sql
-- MAGIC CREATE TABLE orderDWH.FactSales
-- MAGIC (
-- MAGIC   OrderID INT,
-- MAGIC   Quantity DECIMAL,
-- MAGIC   UnitPrice DECIMAL,
-- MAGIC   TotalAmount DECIMAL,
-- MAGIC   DimProductsKey INT,
-- MAGIC   DimCustomersKeyu INT,
-- MAGIC   DimRegionKey INT,
-- MAGIC   DimDateKey INT
-- MAGIC );
-- MAGIC
-- MAGIC SELECT 
-- MAGIC   F.OrderID,
-- MAGIC   F.Quantity,
-- MAGIC   F.UnitPrice,
-- MAGIC   F.TotalAmount,
-- MAGIC   DC.DimCustomersKey,
-- MAGIC   DP.DimProductsKey,
-- MAGIC   DR.DimRegionKey,
-- MAGIC   DD.DimDateKey
-- MAGIC FROM  
-- MAGIC   orderDWH.trans_sales F 
-- MAGIC LEFT JOIN 
-- MAGIC   orderDWH.DimCustomers DC 
-- MAGIC   ON F.CustomerID = DC.CustomerID
-- MAGIC LEFT JOIN 
-- MAGIC   orderDWH.dimproducts DP 
-- MAGIC   ON F.ProductID = DP.ProductID
-- MAGIC LEFT JOIN 
-- MAGIC   orderDWH.DimRegion DR 
-- MAGIC   ON DR.Country = F.Country
-- MAGIC LEFT JOIN 
-- MAGIC   orderDWH.DimDate DD 
-- MAGIC   ON F.OrderDate = DD.OrderDate;
-- MAGIC ```
-- MAGIC
-- MAGIC **What's happening here — this is the most important part of the whole exercise:**
-- MAGIC
-- MAGIC 1. Start from `trans_sales` (the transactional-grain data — one row per order)
-- MAGIC 2. **`LEFT JOIN` to each dimension table**, matching on the **natural/business key** (`CustomerID`, `ProductID`, `Country`, `OrderDate`)
-- MAGIC 3. From each dimension, pull out **only its surrogate key** (`DimCustomersKey`, `DimProductsKey`, `DimRegionKey`, `DimDateKey`) — not the descriptive columns
-- MAGIC 4. The result: one row per order, but now with **short integer keys** pointing to each dimension instead of repeating long text values like `"Alice Johnson"` or `"North America"` directly in the fact table
-- MAGIC
-- MAGIC This is exactly what makes a fact table lightweight and fast — it stores **numbers and keys**, and leaves all the descriptive text in the (much smaller) dimension tables.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## 🔑 Core Concept: Surrogate Keys vs Natural Keys
-- MAGIC
-- MAGIC This is the single most important idea in your whole exercise, so it's worth being precise about it.
-- MAGIC
-- MAGIC | | Natural Key (a.k.a. Business Key) | Surrogate Key |
-- MAGIC |---|---|---|
-- MAGIC | **What it is** | An ID that already exists in the source system | A new, artificial ID generated *inside the warehouse* |
-- MAGIC | **Example** | `CustomerID = 101` (comes from the source app) | `DimCustomersKey = 1, 2, 3...` (generated by `row_number()`) |
-- MAGIC | **Meaning** | Has business meaning outside the warehouse | Has **no meaning** outside the warehouse — it's purely internal |
-- MAGIC | **Stability** | Could theoretically change or be reused by the source system | Never changes once assigned — 100% stable |
-- MAGIC | **Used for joins inside the warehouse?** | No (ideally) | **Yes — this is what Fact tables should join on** |
-- MAGIC
-- MAGIC **Why bother creating a surrogate key at all, if `CustomerID` already exists?**
-- MAGIC - If the source system ever **reuses or changes a `CustomerID`**, your warehouse history would silently corrupt if you relied on it directly.
-- MAGIC - Surrogate keys let you implement things like **SCD Type 2** later (the same real-world customer can have *multiple* surrogate key rows over time — one per historical version — while keeping one stable natural key).
-- MAGIC - Integer surrogate keys are **faster to join on** than text or composite natural keys.
-- MAGIC
-- MAGIC **In your code:** `row_number() OVER (ORDER BY CustomerID)` is exactly how a surrogate key gets generated — a clean, sequential, warehouse-only integer, separate from the original `CustomerID` from the source.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## 📏 Core Concept: Grain of the Fact Table
-- MAGIC
-- MAGIC **"Grain"** means: *what does one single row in the fact table actually represent?*
-- MAGIC
-- MAGIC In your `FactSales` table, the grain is: **one row = one order** (since your source `Orders` table already has one row per order/order-line).
-- MAGIC
-- MAGIC Defining the grain **before** building the fact table matters because every measure and every dimension key must make sense at that exact level — you wouldn't want to accidentally mix "one row per order" with "one row per order per day," for example, without meaning to.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## 🧩 Core Concept: Degenerate Dimension
-- MAGIC
-- MAGIC Look closely at your `FactSales` table — it kept `OrderID` directly, with **no `DimOrder` dimension table** built for it.
-- MAGIC
-- MAGIC This is intentional, and it's a real, named pattern: a **Degenerate Dimension**.
-- MAGIC
-- MAGIC > A degenerate dimension is a dimension-like attribute (usually an ID/reference number) that's kept **directly in the fact table** because it doesn't have any additional descriptive attributes worth putting in a separate dimension table — it's just useful for traceability (e.g., linking back to the original order in the source system, or displaying an order/invoice number in a report).
-- MAGIC
-- MAGIC You did this correctly without necessarily naming it — `OrderID` doesn't need its own dimension because there's nothing to describe about an Order ID beyond the ID itself; everything meaningful about the order (who, what, where, when) is already broken out into your four real dimensions.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## ✅ Star Schema Design Rules — Checklist
-- MAGIC
-- MAGIC Based on what you built, here are the actual rules you followed (and a few to double check):
-- MAGIC
-- MAGIC 1. **✅ Every dimension has a surrogate key** — generated inside the warehouse, not reused from the source.
-- MAGIC 2. **✅ Dimension tables hold descriptive/text attributes** — names, categories, countries.
-- MAGIC 3. **✅ The fact table holds numeric measures** — `Quantity`, `UnitPrice`, `TotalAmount`.
-- MAGIC 4. **✅ The fact table holds only foreign keys (surrogate keys) to dimensions** — not the descriptive text itself.
-- MAGIC 5. **✅ Dimension tables are built from `DISTINCT` values** — one row per unique entity, not one row per transaction.
-- MAGIC 6. **✅ `LEFT JOIN` (not `INNER JOIN`) from fact to dimension** — this is important: if a fact row's dimension value is somehow missing from the dimension table, `LEFT JOIN` keeps the fact row anyway (with a `NULL` key) instead of silently dropping it. Never lose fact data because of a join.
-- MAGIC 7. **✅ Grain is clearly defined** — one row per order, consistently.
-- MAGIC 8. **✅ A degenerate dimension (`OrderID`) is kept directly in the fact table** where a separate dimension wouldn't add value.
-- MAGIC 9. **⚠️ Join dimension tables on their true natural key, not a partial one** — see the `DimRegion` note below.
-- MAGIC 10. **⚠️ Column names must match exactly between the view, the table, and the fact table's join** — see Issues Found below.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## 🐛 Issues Found in the Code (Worth Fixing)
-- MAGIC
-- MAGIC ### 1. `DimProducts` view has a leftover naming bug
-- MAGIC ```sql
-- MAGIC -- Currently:
-- MAGIC SELECT T.*, row_number() OVER (ORDER BY T.ProductID) AS DimCustomersKey FROM (...)
-- MAGIC
-- MAGIC -- Should be:
-- MAGIC SELECT T.*, row_number() OVER (ORDER BY T.ProductID) AS DimProductsKey FROM (...)
-- MAGIC ```
-- MAGIC Since your `DimProducts` table's real column is `DimProductsKey`, the `INSERT INTO ... SELECT *` would fail or misalign unless the view's column is renamed to match.
-- MAGIC
-- MAGIC ### 2. `FactSales` table defines `DimCustomersKeyu` (typo) but the SELECT uses `DimCustomersKey`
-- MAGIC ```sql
-- MAGIC -- Table definition has a typo:
-- MAGIC DimCustomersKeyu INT,
-- MAGIC
-- MAGIC -- But the SELECT further down uses:
-- MAGIC DC.DimCustomersKey
-- MAGIC ```
-- MAGIC These two names don't match — this needs to be fixed to `DimCustomersKey` in the `CREATE TABLE` statement so the later insert aligns correctly.
-- MAGIC
-- MAGIC ### 3. Missing `INSERT INTO` before the final `SELECT`
-- MAGIC ```sql
-- MAGIC -- Currently just a standalone SELECT, so it returns results but doesn't save them anywhere:
-- MAGIC SELECT F.OrderID, ... FROM orderDWH.trans_sales F LEFT JOIN ...
-- MAGIC
-- MAGIC -- Should be:
-- MAGIC INSERT INTO orderDWH.FactSales
-- MAGIC SELECT F.OrderID, ... FROM orderDWH.trans_sales F LEFT JOIN ...
-- MAGIC ```
-- MAGIC Without `INSERT INTO orderDWH.FactSales`, this query just *displays* the joined result — it never actually populates the `FactSales` table.
-- MAGIC
-- MAGIC ### 4. `DimRegion` join uses only `Country`, not the full natural key
-- MAGIC ```sql
-- MAGIC LEFT JOIN orderDWH.DimRegion DR ON DR.Country = F.Country
-- MAGIC ```
-- MAGIC Your `DimRegion` dimension is built from the combination of `(RegionID, RegionName, Country)` — but the fact table only joins on `Country`. If two different regions ever shared the same country (unlikely here, but possible in real data), this join could match the wrong region or create duplicate rows. Safer to join on the true natural key:
-- MAGIC ```sql
-- MAGIC LEFT JOIN orderDWH.DimRegion DR ON DR.RegionID = F.RegionID
-- MAGIC ```
-- MAGIC
-- MAGIC ### 5. `DimDate` is currently very minimal
-- MAGIC Right now it only has `OrderDate` and `DimDateKey`. A production `DimDate` table is usually enriched with extra columns generated from the date itself — `Year`, `Month`, `MonthName`, `Quarter`, `DayOfWeek`, `IsWeekend` — so reports can group by "Q1 2024" or "February" without extra date logic in every query. Not a bug, just a natural next enhancement.
-- MAGIC
-- MAGIC ---
-- MAGIC
-- MAGIC ## 🧠 One-Sentence Summary
-- MAGIC
-- MAGIC You correctly built a real **Star Schema**: four dimension tables holding distinct descriptive data with warehouse-generated **surrogate keys**, and one fact table holding the transactional **measures** plus only the **foreign keys** back to each dimension — the small fixes above (matching key names exactly, joining on true natural keys, and adding the missing `INSERT INTO`) are exactly the kind of detail-level debugging real dimensional modeling work involves.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # Incremental Data Loading

-- COMMAND ----------

CREATE DATABASE IF NOT EXISTS sales_new;

-- COMMAND ----------

CREATE OR REPLACE TABLE sales_new.Orders (
    OrderID INT,
    OrderDate DATE,
    CustomerID INT,
    CustomerName VARCHAR(100),
    CustomerEmail VARCHAR(100),
    ProductID INT,
    ProductName VARCHAR(100),
    ProductCategory VARCHAR(50),
    RegionID INT,
    RegionName VARCHAR(50),
    Country VARCHAR(50),
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    TotalAmount DECIMAL(10,2)
);


-- COMMAND ----------

INSERT INTO sales_new.Orders (OrderID, OrderDate, CustomerID, CustomerName, CustomerEmail, ProductID, ProductName, ProductCategory, RegionID, RegionName, Country, Quantity, UnitPrice, TotalAmount) 
VALUES 
(1, '2024-02-01', 101, 'Alice Johnson', 'alice@example.com', 201, 'Laptop', 'Electronics', 301, 'North America', 'USA', 2, 800.00, 1600.00),
(2, '2024-02-02', 102, 'Bob Smith', 'bob@example.com', 202, 'Smartphone', 'Electronics', 302, 'Europe', 'Germany', 1, 500.00, 500.00),
(3, '2024-02-03', 103, 'Charlie Brown', 'charlie@example.com', 203, 'Tablet', 'Electronics', 303, 'Asia', 'India', 3, 300.00, 900.00),
(4, '2024-02-04', 101, 'Alice Johnson', 'alice@example.com', 204, 'Headphones', 'Accessories', 301, 'North America', 'USA', 1, 150.00, 150.00),
(5, '2024-02-05', 104, 'David Lee', 'david@example.com', 205, 'Gaming Console', 'Electronics', 302, 'Europe', 'France', 1, 400.00, 400.00),
(6, '2024-02-06', 102, 'Bob Smith', 'bob@example.com', 206, 'Smartwatch', 'Electronics', 303, 'Asia', 'China', 2, 200.00, 400.00),
(7, '2024-02-07', 105, 'Eve Adams', 'eve@example.com', 201, 'Laptop', 'Electronics', 301, 'North America', 'Canada', 1, 800.00, 800.00),
(8, '2024-02-08', 106, 'Frank Miller', 'frank@example.com', 207, 'Monitor', 'Accessories', 302, 'Europe', 'Italy', 2, 250.00, 500.00),
(9, '2024-02-09', 107, 'Grace White', 'grace@example.com', 208, 'Keyboard', 'Accessories', 303, 'Asia', 'Japan', 3, 100.00, 300.00),
(10, '2024-02-10', 104, 'David Lee', 'david@example.com', 209, 'Mouse', 'Accessories', 301, 'North America', 'USA', 1, 50.00, 50.00);


-- COMMAND ----------

SELECT * FROM sales_new.orders

-- COMMAND ----------

-- MAGIC %md
-- MAGIC # DATA WAREHOUSING

-- COMMAND ----------

CREATE DATABASE orderDWH

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Staging Layer

-- COMMAND ----------

CREATE OR REPLACE TABLE orderDWH.stg_sales 
AS 
SELECT * FROM sales_new.orders 

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Transformation

-- COMMAND ----------

CREATE VIEW orderDWH.trans_sales
AS
SELECT * FROM orderDWH.stg_sales WHERE Quantity IS NOT NULL 

-- COMMAND ----------

SELECT * FROM orderdwh.trans_sales

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### Core Layer 

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### DimCustomers

-- COMMAND ----------

CREATE OR REPLACE TABLE orderDWH.DimCustomers 
(
  CustomerID INT,
  CustomerName STRING,
  CustomerEmail STRING,
  DimCustomersKey INT
)

-- COMMAND ----------

CREATE OR REPLACE VIEW orderDWH.view_DimCustomers
AS 
SELECT T.*,row_number() over(ORDER BY T.CustomerID) as DimCustomersKey FROM 
(
SELECT 
  DISTINCT(CustomerID) as CustomerID,
  CustomerName,
  CustomerEmail
FROM 
  orderDWH.trans_sales
) AS T

-- COMMAND ----------

SELECT * FROM orderDWH.view_DimCustomers

-- COMMAND ----------

INSERT INTO orderdwh.DimCustomers 
SELECT * FROM orderdwh.view_DimCustomers

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### DimProducts

-- COMMAND ----------

CREATE TABLE orderDWH.DimProducts
(
  ProductID INT,
  ProductName STRING,
  ProductCategory STRING,
  DimProductsKey INT 
)

-- COMMAND ----------

CREATE OR REPLACE VIEW orderDWH.view_DimProducts
AS 
SELECT T.*,row_number() over(ORDER BY T.ProductID) as DimCustomersKey FROM 
(
SELECT 
  DISTINCT(ProductID) as ProductID,
  ProductName,
  ProductCategory
FROM 
  orderDWH.trans_sales
) AS T

-- COMMAND ----------

INSERT INTO orderdwh.DimProducts 
SELECT * FROM orderdwh.view_DimProducts

-- COMMAND ----------

SELECT * FROM orderdwh.DimProducts

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### DimRegion

-- COMMAND ----------

CREATE OR REPLACE TABLE orderDWH.DimRegion 
(
  RegionID INT,
  RegionName STRING,
  Country STRING,
  DimRegionKey INT
)

-- COMMAND ----------

CREATE OR REPLACE VIEW orderDWH.view_DimRegion
AS 
SELECT T.*,row_number() over(ORDER BY T.RegionID) as DimRegionKey FROM 
(
SELECT 
  DISTINCT(RegionID) as RegionID,
  RegionName,
  Country
FROM 
  orderDWH.trans_sales
) AS T

-- COMMAND ----------

INSERT INTO orderdwh.DimRegion
SELECT * FROM orderdwh.view_DimRegion

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ##### DimDate

-- COMMAND ----------

CREATE OR REPLACE TABLE orderDWH.DimDate
(
  OrderDate Date,
  DimDateKey INT
)

-- COMMAND ----------

CREATE OR REPLACE VIEW orderDWH.view_DimDate
AS 
SELECT T.*,row_number() over(ORDER BY T.OrderDate) as DimDateKey FROM 
(
SELECT 
  DISTINCT(OrderDate) as OrderDate
FROM 
  orderDWH.trans_sales
) AS T

-- COMMAND ----------

INSERT INTO orderdwh.DimDate
SELECT * FROM orderdwh.view_DimDate

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ### FACT TABLE

-- COMMAND ----------

CREATE TABLE orderDWH.FactSales
(
  OrderID INT,
  Quantity DECIMAL,
  UnitPrice DECIMAL,
  TotalAmount DECIMAL,
  DimProductsKey INT,
  DimCustomersKey INT,
  DimRegionKey INT,
  DimDateKey INT
)

-- COMMAND ----------

INSERT INTO orderDWH.FactSales
SELECT 
  F.OrderID,
  F.Quantity,
  F.UnitPrice,
  F.TotalAmount,
  DP.DimProductsKey,
  DC.DimCustomersKey,
  DR.DimRegionKey,
  DD.DimDateKey
FROM  
  orderDWH.trans_sales F 
LEFT JOIN 
  orderDWH.DimCustomers DC 
  ON F.CustomerID = DC.CustomerID
LEFT JOIN 
  orderDWH.DimProducts DP 
  ON F.ProductID = DP.ProductID
LEFT JOIN 
  orderDWH.DimRegion DR 
  ON DR.Country = F.Country
LEFT JOIN 
  orderDWH.DimDate DD 
  ON F.OrderDate = DD.OrderDate;

-- COMMAND ----------

-- DBTITLE 1,In Python
-- MAGIC %python
-- MAGIC
-- MAGIC from pyspark.sql.functions import *
-- MAGIC
-- MAGIC financemain = spark.read.table("orderdwh.trans_sales").alias("F")
-- MAGIC
-- MAGIC Customers = spark.read.table("orderdwh.DimCustomers").alias("DC")
-- MAGIC
-- MAGIC products = spark.read.table("orderdwh.dimproducts").alias("DP")
-- MAGIC
-- MAGIC Region = spark.read.table("orderdwh.DimRegion").alias("DR")
-- MAGIC
-- MAGIC Date = spark.read.table("orderdwh.DimDate").alias("DD")
-- MAGIC
-- MAGIC
-- MAGIC df_final_result = (financemain.join(Customers,col("F.CustomerID") == col("DC.CustomerID"),"left")
-- MAGIC     .join(products,col("F.ProductID") == col("DP.ProductID"),"left")
-- MAGIC     .join(Region,col("F.Country") == col("DR.Country"),"left")
-- MAGIC     .join(Date,col("F.OrderDate") == col("DD.OrderDate"),"left")
-- MAGIC     .selectExpr(
-- MAGIC         "F.OrderID",
-- MAGIC         "F.Quantity",
-- MAGIC         "F.UnitPrice",
-- MAGIC         "F.TotalAmount",
-- MAGIC         "DC.DimCustomersKey",
-- MAGIC         "DP.DimProductsKey",
-- MAGIC         "DR.DimRegionKey",
-- MAGIC         "DD.DimDateKey"))
-- MAGIC
-- MAGIC display(df_final_result)

-- COMMAND ----------

SELECT * FROM orderdwh.factsales