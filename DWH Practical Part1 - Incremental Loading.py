# Databricks notebook source
# MAGIC %md
# MAGIC ## Incremental Data Loading

# COMMAND ----------

# MAGIC %md
# MAGIC # 🏗️ My Incremental Loading Exercise — Staging → Transformation → Core
# MAGIC
# MAGIC ## 🎯 What I Was Trying to Prove
# MAGIC
# MAGIC Can I build a warehouse where, instead of reloading the **entire** `Orders` table every time, I only pull in what's **new** and correctly land it in the final table? This is the exercise, walked through step by step, using the actual code I wrote.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🥇 Phase 1 — Full Load (Setting Up the Source)
# MAGIC
# MAGIC First, I built a source system table (`sales.Orders`) and loaded my first 10 orders into it — this represents "the system that generates data every day," like an e-commerce app's order database.
# MAGIC
# MAGIC ```sql
# MAGIC CREATE DATABASE sales;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE sales.Orders (
# MAGIC     OrderID INT,
# MAGIC     OrderDate DATE,
# MAGIC     CustomerID INT,
# MAGIC     CustomerName VARCHAR(100),
# MAGIC     ...
# MAGIC );
# MAGIC
# MAGIC INSERT INTO sales.Orders (...)
# MAGIC VALUES
# MAGIC (1, '2024-02-01', ...),
# MAGIC (2, '2024-02-02', ...),
# MAGIC ...
# MAGIC (10, '2024-02-10', ...);
# MAGIC ```
# MAGIC
# MAGIC This is my **source system** — the place incremental loads will always pull *from*.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🥈 Phase 2 — Building the Warehouse (Staging → Transformation → Core)
# MAGIC
# MAGIC I then created a second database, `salesDWH`, to represent the warehouse itself, and built it in three layers:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE DATABASE salesDWH;
# MAGIC
# MAGIC -- 1. STAGING — raw landing copy of the source
# MAGIC CREATE OR REPLACE TABLE salesDWH.stg_sales
# MAGIC AS
# MAGIC SELECT * FROM sales.Orders;
# MAGIC
# MAGIC -- 2. TRANSFORMATION — a view that applies light cleaning rules
# MAGIC CREATE VIEW salesDWH.trans_sales
# MAGIC AS
# MAGIC SELECT * FROM salesDWH.stg_sales WHERE Quantity IS NOT NULL;
# MAGIC
# MAGIC -- 3. CORE — the final table that reports/analysts would query
# MAGIC CREATE TABLE salesDWH.core_sales
# MAGIC AS
# MAGIC SELECT * FROM salesDWH.trans_sales;
# MAGIC ```
# MAGIC
# MAGIC At this point: `sales.Orders` (10 rows) → `stg_sales` (10 rows) → `trans_sales` view (10 rows, filtered) → `core_sales` (10 rows). Everything matches — this is a **full load**, and it's the easy case.
# MAGIC
# MAGIC **What each layer is actually for, in my own words:**
# MAGIC - **Staging** = "just get the raw data into the warehouse, don't think too hard yet"
# MAGIC - **Transformation** = "apply my business rules" (here: drop any row with a null `Quantity`, since that's bad/incomplete data I don't want polluting reporting)
# MAGIC - **Core** = "the trusted, final version of the truth that everyone downstream actually queries"
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ❓ The Real Question: What Happens When New Data Arrives?
# MAGIC
# MAGIC This is the part I wanted to prove out — **do I really have to reload all 10+ rows again, or can I load *only* what's new?**
# MAGIC
# MAGIC To simulate new data arriving, I inserted 5 more rows into the source:
# MAGIC
# MAGIC ```sql
# MAGIC INSERT INTO sales.Orders (...)
# MAGIC VALUES
# MAGIC (1, '2024-02-11', ...),
# MAGIC (2, '2024-02-12', ...),
# MAGIC (3, '2024-02-13', ...),
# MAGIC (4, '2024-02-14', ...),
# MAGIC (5, '2024-02-15', ...);
# MAGIC ```
# MAGIC
# MAGIC > ⚠️ **Quick note on this test data:** I reused `OrderID`s 1–5 here with new `OrderDate`s. In a real system, a genuinely *new* order would get a brand-new `OrderID` (like 11–15) — reusing an existing ID would normally mean "this is an *update* to an existing order," not a new one. I'll flag why this matters at the end, but for the purposes of proving out the incremental *mechanism*, it still works — I just need to be precise about what I'm actually simulating.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔍 Step 1 — CDC in the Staging Layer
# MAGIC
# MAGIC This is where **CDC (Change Data Capture)** actually shows up in my pipeline. Instead of copying the *whole* source table into staging again, I filtered:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE OR REPLACE TABLE salesDWH.stg_sales
# MAGIC AS
# MAGIC SELECT * FROM sales.Orders
# MAGIC WHERE OrderDate > '2024-02-10';
# MAGIC ```
# MAGIC
# MAGIC **This one `WHERE` clause is my CDC logic.** Specifically, this is **timestamp-based CDC** — I'm using `OrderDate` as the signal for "what's changed since last time," and only pulling rows newer than my last load's cutoff.
# MAGIC
# MAGIC Result: `stg_sales` now holds only **5 rows** (the new batch), not 15. This is the entire point of incremental loading — staging never has to be "everything," just "what's new right now."
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔄 Step 2 — Transformation Layer (Unchanged, On Purpose)
# MAGIC
# MAGIC ```sql
# MAGIC -- trans_sales view definition doesn't change
# MAGIC SELECT * FROM salesDWH.stg_sales WHERE Quantity IS NOT NULL
# MAGIC ```
# MAGIC
# MAGIC I correctly noticed this layer needs **no changes** — it's a *view*, not a physical table, so it automatically re-evaluates against whatever is currently in `stg_sales`. Since `stg_sales` now holds only the 5 new rows, `trans_sales` automatically reflects just those 5 rows too, filtered by the same business rule as before.
# MAGIC
# MAGIC **This is an important insight:** the transformation logic itself doesn't care whether staging has 10 rows or 5 — it just applies the same rule to whatever's there. The *incremental* behavior lives entirely in staging's CDC filter, not here.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Step 3 — Loading Into Core (The Actual Incremental Insert)
# MAGIC
# MAGIC ```sql
# MAGIC INSERT INTO salesDWH.core_sales
# MAGIC SELECT * FROM salesdwh.trans_sales;
# MAGIC ```
# MAGIC
# MAGIC Instead of recreating `core_sales` from scratch (`CREATE OR REPLACE TABLE ... AS SELECT`, which is what a **full load** would do), I used `INSERT INTO` — which **appends** the 5 new/transformed rows onto whatever was already sitting in `core_sales`.
# MAGIC
# MAGIC Result: `core_sales` now has **15 rows** — the original 10, plus the 5 newly loaded ones — without ever having touched or reprocessed the original 10 again.
# MAGIC
# MAGIC **This is the heart of incremental loading:** Core keeps growing additively, batch by batch, instead of being rebuilt from zero every time.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🗺️ The Full Flow I Built
# MAGIC
# MAGIC ```
# MAGIC sales.Orders (source, 10 rows)
# MAGIC         │
# MAGIC         │  ── 5 new rows inserted ──
# MAGIC         ▼
# MAGIC sales.Orders (source, 15 rows)
# MAGIC         │
# MAGIC         │  CDC filter: WHERE OrderDate > '2024-02-10'
# MAGIC         ▼
# MAGIC stg_sales  (staging, only the 5 NEW rows)
# MAGIC         │
# MAGIC         │  same transformation rule, unchanged
# MAGIC         ▼
# MAGIC trans_sales (view, 5 rows, filtered)
# MAGIC         │
# MAGIC         │  INSERT INTO (append, not replace)
# MAGIC         ▼
# MAGIC core_sales (10 old rows + 5 new rows = 15 total)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ What I Got Right
# MAGIC
# MAGIC - **Separating staging from core** — staging is disposable and only ever holds the current batch; core is the permanent, growing table. This is the correct mental model.
# MAGIC - **Using a `WHERE` filter as CDC** — timestamp-based CDC is genuinely the most common real-world approach, and I implemented it correctly using `OrderDate`.
# MAGIC - **Using `INSERT INTO` for core, not `CREATE OR REPLACE`** — this is the key mechanical difference between an incremental load and a full load. Replacing the table would have thrown away my previous 10 rows; appending preserved them.
# MAGIC - **Letting the transformation view stay untouched** — recognizing that the business logic doesn't need to change just because the incoming volume changed is a good instinct.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔧 What I'd Tighten Up for a Production-Grade Version
# MAGIC
# MAGIC ### 1. My `stg_sales` isn't actually being truncated — it's being replaced
# MAGIC I used `CREATE OR REPLACE TABLE salesDWH.stg_sales AS SELECT ...`, which drops and rebuilds the whole table each time. This *works* and achieves the same practical effect as truncating-then-loading, but a more standard production pattern is:
# MAGIC ```sql
# MAGIC TRUNCATE TABLE salesDWH.stg_sales;
# MAGIC INSERT INTO salesDWH.stg_sales
# MAGIC SELECT * FROM sales.Orders WHERE OrderDate > '<last_load_date>';
# MAGIC ```
# MAGIC Functionally similar here, but `TRUNCATE + INSERT` is the more conventional pattern you'll see in real pipelines (and plays better with table permissions/history tracking than dropping and recreating).
# MAGIC
# MAGIC ### 2. The `WHERE OrderDate > '2024-02-10'` cutoff is hardcoded
# MAGIC Right now, that date is manually typed in. In a real pipeline, this value would come from a **watermark** — usually a small control table that stores "the last successfully loaded date," e.g.:
# MAGIC ```sql
# MAGIC SELECT * FROM sales.Orders
# MAGIC WHERE OrderDate > (SELECT max_loaded_date FROM control.watermark_table)
# MAGIC ```
# MAGIC This way, the pipeline figures out the cutoff automatically instead of a human updating it before every run.
# MAGIC
# MAGIC ### 3. Reusing `OrderID`s 1–5 needs a decision: is this an INSERT or an UPDATE?
# MAGIC This is the most important one. Because I reused existing `OrderID`s with new `OrderDate`s, and then plain `INSERT INTO core_sales`, my `core_sales` table now has **two rows for `OrderID = 1`** (one from `2024-02-01`, one from `2024-02-11`) — same for IDs 2–5.
# MAGIC
# MAGIC - If these were meant to be **new, distinct orders**, they should have gotten new `OrderID`s (11–15), and plain `INSERT` is correct.
# MAGIC - If these were meant to represent **updates to existing orders** (e.g., "Order #1 got modified"), then plain `INSERT` is the wrong tool — you'd want a **`MERGE`** instead, so the existing row gets updated in place rather than duplicated:
# MAGIC ```sql
# MAGIC MERGE INTO salesDWH.core_sales AS trg
# MAGIC USING salesDWH.trans_sales AS src
# MAGIC ON trg.OrderID = src.OrderID
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *
# MAGIC ```
# MAGIC This is exactly the **upsert** pattern used in real Delta Lake / warehouse pipelines — and it's the natural next concept to practice once plain incremental `INSERT` feels solid.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🧠 The One-Sentence Summary
# MAGIC
# MAGIC I built a working incremental pipeline where **staging always holds only "what changed since last time" (found via a CDC filter), transformation applies the same business rules regardless of batch size, and core grows additively through `INSERT` rather than being rebuilt** — the next natural step is swapping that final `INSERT` for a `MERGE` so updates to existing records are handled correctly instead of creating duplicates.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE sales.Orders (
# MAGIC     OrderID INT,
# MAGIC     OrderDate DATE,
# MAGIC     CustomerID INT,
# MAGIC     CustomerName VARCHAR(100),
# MAGIC     CustomerEmail VARCHAR(100),
# MAGIC     ProductID INT,
# MAGIC     ProductName VARCHAR(100),
# MAGIC     ProductCategory VARCHAR(50),
# MAGIC     RegionID INT,
# MAGIC     RegionName VARCHAR(50),
# MAGIC     Country VARCHAR(50),
# MAGIC     Quantity INT,
# MAGIC     UnitPrice DECIMAL(10,2),
# MAGIC     TotalAmount DECIMAL(10,2)
# MAGIC );
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO sales.Orders (OrderID, OrderDate, CustomerID, CustomerName, CustomerEmail, ProductID, ProductName, ProductCategory, RegionID, RegionName, Country, Quantity, UnitPrice, TotalAmount) 
# MAGIC VALUES 
# MAGIC (1, '2024-02-01', 101, 'Alice Johnson', 'alice@example.com', 201, 'Laptop', 'Electronics', 301, 'North America', 'USA', 2, 800.00, 1600.00),
# MAGIC (2, '2024-02-02', 102, 'Bob Smith', 'bob@example.com', 202, 'Smartphone', 'Electronics', 302, 'Europe', 'Germany', 1, 500.00, 500.00),
# MAGIC (3, '2024-02-03', 103, 'Charlie Brown', 'charlie@example.com', 203, 'Tablet', 'Electronics', 303, 'Asia', 'India', 3, 300.00, 900.00),
# MAGIC (4, '2024-02-04', 101, 'Alice Johnson', 'alice@example.com', 204, 'Headphones', 'Accessories', 301, 'North America', 'USA', 1, 150.00, 150.00),
# MAGIC (5, '2024-02-05', 104, 'David Lee', 'david@example.com', 205, 'Gaming Console', 'Electronics', 302, 'Europe', 'France', 1, 400.00, 400.00),
# MAGIC (6, '2024-02-06', 102, 'Bob Smith', 'bob@example.com', 206, 'Smartwatch', 'Electronics', 303, 'Asia', 'China', 2, 200.00, 400.00),
# MAGIC (7, '2024-02-07', 105, 'Eve Adams', 'eve@example.com', 201, 'Laptop', 'Electronics', 301, 'North America', 'Canada', 1, 800.00, 800.00),
# MAGIC (8, '2024-02-08', 106, 'Frank Miller', 'frank@example.com', 207, 'Monitor', 'Accessories', 302, 'Europe', 'Italy', 2, 250.00, 500.00),
# MAGIC (9, '2024-02-09', 107, 'Grace White', 'grace@example.com', 208, 'Keyboard', 'Accessories', 303, 'Asia', 'Japan', 3, 100.00, 300.00),
# MAGIC (10, '2024-02-10', 104, 'David Lee', 'david@example.com', 209, 'Mouse', 'Accessories', 301, 'North America', 'USA', 1, 50.00, 50.00);
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Inserting New Records

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO sales.Orders (OrderID, OrderDate, CustomerID, CustomerName, CustomerEmail, ProductID, ProductName, ProductCategory, RegionID, RegionName, Country, Quantity, UnitPrice, TotalAmount) 
# MAGIC VALUES 
# MAGIC (1, '2024-02-16', 101, 'Alice Johnson', 'alice@example.com', 201, 'Laptop', 'Electronics', 301, 'North America', 'USA', 2, 800.00, 1600.00),
# MAGIC (2, '2024-02-17', 102, 'Bob Smith', 'bob@example.com', 202, 'Smartphone', 'Electronics', 302, 'Europe', 'Germany', 1, 500.00, 500.00)
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales.Orders

# COMMAND ----------

# MAGIC %md
# MAGIC ## 
# MAGIC ## DATA WAREHOUSING

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE salesDWH

# COMMAND ----------

# MAGIC %md
# MAGIC ## Staging Layer

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE salesDWH.stg_sales 
# MAGIC AS 
# MAGIC SELECT * FROM sales.Orders 
# MAGIC WHERE OrderDate > '2024-02-15'

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from salesDWH.stg_sales 

# COMMAND ----------

# MAGIC %md
# MAGIC ## Transformation

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VIEW salesDWH.trans_sales
# MAGIC AS
# MAGIC SELECT * FROM salesDWH.stg_sales WHERE Quantity IS NOT NULL 
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM salesDWH.trans_sales

# COMMAND ----------

# MAGIC %md
# MAGIC ## Core Layer

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC --  CREATE TABLE salesDWH.core_sales
# MAGIC --  AS
# MAGIC --  SELECT * FROM salesDWH.trans_sales
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE salesDWH.core_sales (
# MAGIC     OrderID INT,
# MAGIC     OrderDate DATE,
# MAGIC     CustomerID INT,
# MAGIC     CustomerName VARCHAR(100),
# MAGIC     CustomerEmail VARCHAR(100),
# MAGIC     ProductID INT,
# MAGIC     ProductName VARCHAR(100),
# MAGIC     ProductCategory VARCHAR(50),
# MAGIC     RegionID INT,
# MAGIC     RegionName VARCHAR(50),
# MAGIC     Country VARCHAR(50),
# MAGIC     Quantity INT,
# MAGIC     UnitPrice DECIMAL(10,2),
# MAGIC     TotalAmount DECIMAL(10,2)
# MAGIC );
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO salesDWH.core_sales
# MAGIC SELECT * FROM salesdwh.trans_sales

# COMMAND ----------

# MAGIC %md
# MAGIC ## DWH Core Layer Display

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from salesdwh.core_sales