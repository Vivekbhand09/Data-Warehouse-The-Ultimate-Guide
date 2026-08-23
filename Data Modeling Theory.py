# Databricks notebook source
# MAGIC %md
# MAGIC # 🧩 Data Modeling — Complete Beginner's Guide
# MAGIC
# MAGIC ## 🧠 What Is Data Modeling?
# MAGIC
# MAGIC **Data modeling** is the process of deciding **how data will be organized, structured, and related** before you actually build any tables.
# MAGIC
# MAGIC Think of it like an architect's blueprint for a house. Before anyone pours concrete, the architect decides: how many rooms, where the walls go, where the plumbing runs. **Data modeling is that blueprint, but for a database or data warehouse.**
# MAGIC
# MAGIC Without a proper model, you end up with:
# MAGIC - Duplicate data scattered everywhere
# MAGIC - No clear relationships between tables
# MAGIC - Slow, confusing queries
# MAGIC - A warehouse nobody trusts
# MAGIC
# MAGIC A good data model answers: *"What data do I have, how does it relate to other data, and how should it actually be stored?"*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🪜 The Three Levels of Data Modeling
# MAGIC
# MAGIC Data modeling isn't done in one shot — it happens in **three progressively more detailed stages**:
# MAGIC
# MAGIC ```
# MAGIC CONCEPTUAL MODEL  →  LOGICAL MODEL  →  PHYSICAL MODEL
# MAGIC    (What?)              (How, in detail?)      (How, in the actual database?)
# MAGIC ```
# MAGIC
# MAGIC Each stage takes the previous one and adds more precision, until you finally have something you can run `CREATE TABLE` with.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 1️⃣ Conceptual Data Model — "What are the big things, and how do they relate?"
# MAGIC
# MAGIC **Purpose:** A high-level, business-friendly picture. No technical details at all — no data types, no keys, nothing a database cares about. This is meant to be understood by **business people**, not just engineers.
# MAGIC
# MAGIC **What it captures:**
# MAGIC - The major **entities** (things) in the business
# MAGIC - How those entities **relate** to each other
# MAGIC
# MAGIC **Simple Example — Sales Business:**
# MAGIC
# MAGIC ```
# MAGIC Customer  ──places──▶  Order  ──contains──▶  Product
# MAGIC                           │
# MAGIC                           ▼
# MAGIC                         Region
# MAGIC ```
# MAGIC
# MAGIC That's it. No columns, no data types — just: "A Customer places Orders. Orders contain Products. Orders happen in a Region." A business stakeholder with zero technical background can look at this and understand the business.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 2️⃣ Logical Data Model — "What exact fields does each thing have, and how are they connected?"
# MAGIC
# MAGIC **Purpose:** Add real structure — attributes (columns), data types (in a generic sense, not database-specific), and precise relationships (primary keys / foreign keys) — but still **not tied to any specific database technology**.
# MAGIC
# MAGIC **What it captures:**
# MAGIC - Every entity becomes a **table** (conceptually)
# MAGIC - Every attribute of that entity becomes a **column**
# MAGIC - Relationships become explicit **primary key → foreign key** links
# MAGIC
# MAGIC **Simple Example — Same Sales Business, More Detail:**
# MAGIC
# MAGIC ```
# MAGIC Customer                    Order                       Product
# MAGIC ─────────                   ─────────                   ─────────
# MAGIC CustomerID (PK)             OrderID (PK)                ProductID (PK)
# MAGIC CustomerName                OrderDate                    ProductName
# MAGIC CustomerEmail                CustomerID (FK)             ProductCategory
# MAGIC                              ProductID (FK)               UnitPrice
# MAGIC                              Quantity
# MAGIC                              RegionID (FK)
# MAGIC
# MAGIC Region
# MAGIC ─────────
# MAGIC RegionID (PK)
# MAGIC RegionName
# MAGIC Country
# MAGIC ```
# MAGIC
# MAGIC Now we know exactly what fields exist and how tables connect (`Order.CustomerID` links to `Customer.CustomerID`, etc.) — but we still haven't decided things like "will this be a VARCHAR(100) or VARCHAR(255) in MySQL?" That comes next.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 3️⃣ Physical Data Model — "How does this actually get built in the real database?"
# MAGIC
# MAGIC **Purpose:** The final, technology-specific blueprint — the one that becomes real `CREATE TABLE` statements. This includes exact data types, constraints, indexes, partitioning, and naming conventions specific to the database engine you're using (e.g., Databricks, PostgreSQL, Snowflake).
# MAGIC
# MAGIC **Simple Example — Now It's Real SQL:**
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE sales.Customer (
# MAGIC     CustomerID INT PRIMARY KEY,
# MAGIC     CustomerName VARCHAR(100),
# MAGIC     CustomerEmail VARCHAR(100)
# MAGIC );
# MAGIC
# MAGIC CREATE TABLE sales.Orders (
# MAGIC     OrderID INT PRIMARY KEY,
# MAGIC     OrderDate DATE,
# MAGIC     CustomerID INT REFERENCES sales.Customer(CustomerID),
# MAGIC     ProductID INT REFERENCES sales.Product(ProductID),
# MAGIC     RegionID INT REFERENCES sales.Region(RegionID),
# MAGIC     Quantity INT,
# MAGIC     UnitPrice DECIMAL(10,2)
# MAGIC );
# MAGIC ```
# MAGIC
# MAGIC This is what actually gets deployed. It has real data types (`DECIMAL(10,2)` for money, `DATE` for dates), real primary keys, and real foreign key constraints enforced by the database engine.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Side-by-Side Comparison
# MAGIC
# MAGIC | | Conceptual | Logical | Physical |
# MAGIC |---|---|---|---|
# MAGIC | **Audience** | Business stakeholders | Data architects / analysts | Database engineers / developers |
# MAGIC | **Detail level** | Very high-level | Detailed, but tech-agnostic | Fully technical, database-specific |
# MAGIC | **Has data types?** | ❌ No | ⚠️ Generic types only | ✅ Exact types (VARCHAR(100), INT, etc.) |
# MAGIC | **Has keys/constraints?** | ❌ No | ✅ PK/FK relationships | ✅ Enforced PK/FK, indexes, constraints |
# MAGIC | **Can you run it as SQL?** | ❌ No | ❌ No | ✅ Yes |
# MAGIC | **Question it answers** | "What exists?" | "What fields, and how connected?" | "How is this actually built?" |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🌟 Dimensional Data Modeling
# MAGIC
# MAGIC Once you get into **data warehousing** specifically (as opposed to a regular transactional database), there's a special, very popular style of logical/physical modeling called **Dimensional Modeling**.
# MAGIC
# MAGIC ### Why a Different Model for Warehousing?
# MAGIC
# MAGIC A normal transactional database (like the `sales.Orders` table you'd use for an app) is optimized for **fast, small read/write operations** — inserting one order, updating one customer.
# MAGIC
# MAGIC A data warehouse is optimized for a completely different job: **answering big analytical questions** — "What were total sales by region last quarter?" "Which product category grew the fastest?"
# MAGIC
# MAGIC Dimensional modeling restructures data specifically to make those big aggregate questions **fast and intuitive** to query. It does this by splitting data into two types of tables: **Fact tables** and **Dimension tables**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📈 Fact Tables — "The Things That Happened (The Numbers)"
# MAGIC
# MAGIC A **Fact table** stores **measurable, numeric events** — things that happened, and how much/many.
# MAGIC
# MAGIC **Characteristics:**
# MAGIC - Contains **numbers you can add up, average, or count** (measures)
# MAGIC - Contains **foreign keys** pointing to dimension tables (for context)
# MAGIC - Usually the **largest** table in the warehouse (grows with every transaction)
# MAGIC - One row = one event (e.g., one line item in one order)
# MAGIC
# MAGIC **Simple Example — `fact_sales`:**
# MAGIC
# MAGIC | OrderID | DateKey | CustomerKey | ProductKey | RegionKey | Quantity | UnitPrice | TotalAmount |
# MAGIC |---|---|---|---|---|---|---|---|
# MAGIC | 1 | 20240201 | 101 | 201 | 301 | 2 | 800.00 | 1600.00 |
# MAGIC | 2 | 20240202 | 102 | 202 | 302 | 1 | 500.00 | 500.00 |
# MAGIC
# MAGIC Notice: `Quantity`, `UnitPrice`, `TotalAmount` are **numbers you'd aggregate** — `SUM(TotalAmount)`, `AVG(UnitPrice)`. Everything else (`DateKey`, `CustomerKey`, `ProductKey`, `RegionKey`) is just a **pointer** to a dimension table for more detail.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🗂️ Dimension Tables — "The Context Around the Fact (The Descriptions)"
# MAGIC
# MAGIC A **Dimension table** stores **descriptive, contextual attributes** — the "who, what, where, when" that gives meaning to the numbers in the fact table.
# MAGIC
# MAGIC **Characteristics:**
# MAGIC - Contains **text/descriptive attributes**, not measures you'd sum up
# MAGIC - Much **smaller** than fact tables (a company might have millions of orders, but only thousands of customers)
# MAGIC - Used to **filter, group, and label** fact data in reports
# MAGIC - One row = one entity (one customer, one product, one date)
# MAGIC
# MAGIC **Simple Example — `dim_customer`:**
# MAGIC
# MAGIC | CustomerKey | CustomerName | CustomerEmail | Country |
# MAGIC |---|---|---|---|
# MAGIC | 101 | Alice Johnson | alice@example.com | USA |
# MAGIC | 102 | Bob Smith | bob@example.com | Germany |
# MAGIC
# MAGIC **Simple Example — `dim_product`:**
# MAGIC
# MAGIC | ProductKey | ProductName | ProductCategory |
# MAGIC |---|---|---|
# MAGIC | 201 | Laptop | Electronics |
# MAGIC | 202 | Smartphone | Electronics |
# MAGIC
# MAGIC **Simple Example — `dim_date`:**
# MAGIC
# MAGIC | DateKey | Date | Month | Quarter | Year |
# MAGIC |---|---|---|---|---|
# MAGIC | 20240201 | 2024-02-01 | February | Q1 | 2024 |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ⭐ Putting Them Together — The Star Schema
# MAGIC
# MAGIC When you connect **one fact table** to **multiple dimension tables**, the diagram literally looks like a star:
# MAGIC
# MAGIC ```
# MAGIC               dim_date
# MAGIC                  │
# MAGIC                  │
# MAGIC dim_customer ── fact_sales ── dim_product
# MAGIC                  │
# MAGIC                  │
# MAGIC               dim_region
# MAGIC ```
# MAGIC
# MAGIC This shape — one fact table in the center, dimension tables radiating out around it — is called a **Star Schema**, the most common pattern in dimensional modeling.
# MAGIC
# MAGIC ### Why This Structure Is So Powerful
# MAGIC
# MAGIC Now a business question like:
# MAGIC
# MAGIC > "What's the total sales amount by product category, for customers in the USA, in Q1 2024?"
# MAGIC
# MAGIC ...becomes a simple, fast query:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT
# MAGIC     p.ProductCategory,
# MAGIC     SUM(f.TotalAmount) AS total_sales
# MAGIC FROM fact_sales f
# MAGIC JOIN dim_product p  ON f.ProductKey = p.ProductKey
# MAGIC JOIN dim_customer c ON f.CustomerKey = c.CustomerKey
# MAGIC JOIN dim_date d      ON f.DateKey = d.DateKey
# MAGIC WHERE c.Country = 'USA' AND d.Quarter = 'Q1' AND d.Year = 2024
# MAGIC GROUP BY p.ProductCategory;
# MAGIC ```
# MAGIC
# MAGIC Each dimension table lets you **filter and group** by a different angle (product, customer, time, region), while the fact table supplies the **numbers** being summed. This is exactly why dimensional modeling exists — it makes analytical questions like this fast and natural to write.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🤔 Fact vs Dimension — Quick Decision Guide
# MAGIC
# MAGIC Ask yourself: **"Is this a number I'd want to add up, or a label I'd want to filter/group by?"**
# MAGIC
# MAGIC | If it's... | It belongs in... | Example |
# MAGIC |---|---|---|
# MAGIC | A number you'd `SUM()`, `AVG()`, or `COUNT()` | **Fact table** | `Quantity`, `UnitPrice`, `TotalAmount` |
# MAGIC | A descriptive attribute you'd filter or group by | **Dimension table** | `CustomerName`, `ProductCategory`, `Country`, `Month` |
# MAGIC | A foreign key connecting the two | **Fact table** (as a key pointing to the dimension) | `CustomerKey`, `ProductKey`, `DateKey` |
# MAGIC
# MAGIC **Simple rule of thumb:**
# MAGIC > If it answers **"how much/how many"** → Fact.
# MAGIC > If it answers **"who, what, where, when, which category"** → Dimension.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 When to Use What
# MAGIC
# MAGIC | Scenario | Use |
# MAGIC |---|---|
# MAGIC | Designing a new app's database (orders, users, transactions) | Regular normalized **logical/physical model** (not dimensional) |
# MAGIC | Building a reporting/analytics warehouse | **Dimensional model** (Star Schema) |
# MAGIC | Explaining the system to a business stakeholder | **Conceptual model** |
# MAGIC | Handing off table structure to a database developer | **Logical model** |
# MAGIC | Actually writing `CREATE TABLE` scripts | **Physical model** |
# MAGIC | Want fast aggregate queries (totals, averages, trends) across many angles | **Fact + Dimension tables (Star Schema)** |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Quick Summary
# MAGIC
# MAGIC - **Data modeling** = deciding how data is structured before building it — moving from a big-picture idea to an actual database.
# MAGIC - **Conceptual → Logical → Physical** = three levels of increasing detail: *what exists* → *what fields and relationships* → *actual database-ready SQL*.
# MAGIC - **Dimensional modeling** is a specialized approach used specifically in data warehouses to make analytical (aggregate) queries fast and intuitive.
# MAGIC - **Fact tables** hold the numbers/measures (and foreign keys to dimensions) — they answer "how much/how many."
# MAGIC - **Dimension tables** hold the descriptive context (who, what, where, when) — they answer "which one, described how."
# MAGIC - Together, one fact table surrounded by its dimension tables forms a **Star Schema** — the standard shape of a modern analytical data warehouse.

# COMMAND ----------

# MAGIC %md
# MAGIC # ⭐ Fact vs Dimension Tables & Star vs Snowflake Schema
# MAGIC
# MAGIC ## 📊 Fact Table vs Dimension Table — Complete Comparison
# MAGIC
# MAGIC | Aspect | Fact Table | Dimension Table |
# MAGIC |---|---|---|
# MAGIC | **What it stores** | Measurable, numeric business events (measures) | Descriptive, contextual attributes (who/what/where/when) |
# MAGIC | **Core question it answers** | "How much? How many?" | "Which one? Described how?" |
# MAGIC | **Example columns** | `Quantity`, `UnitPrice`, `TotalAmount`, `Discount` | `CustomerName`, `ProductCategory`, `Country`, `MonthName` |
# MAGIC | **Row represents** | One event / transaction (e.g., one order line item) | One entity (e.g., one customer, one product, one date) |
# MAGIC | **Table size** | Very large — grows with every transaction (millions/billions of rows) | Much smaller — grows slowly (thousands, maybe millions of rows) |
# MAGIC | **Growth pattern** | Grows continuously and rapidly over time | Relatively static; changes occasionally (new customer, new product) |
# MAGIC | **Key structure** | Contains **foreign keys** pointing to every related dimension | Has its own **primary key** (surrogate key), referenced by fact tables |
# MAGIC | **Data type of columns** | Mostly numeric (measures) + keys (integers) | Mostly text/descriptive (strings, dates, categories) |
# MAGIC | **Used for** | Aggregation — `SUM()`, `AVG()`, `COUNT()`, `MIN()`, `MAX()` | Filtering and grouping — `WHERE`, `GROUP BY` |
# MAGIC | **Granularity** | Defined at the most detailed transactional level (the "grain") | Defined at the entity level — one row per unique entity |
# MAGIC | **Update frequency** | Insert-heavy — mostly new rows added (append) | Occasionally updated (e.g., customer changes address) — this is where **SCD** (Slowly Changing Dimensions) comes in |
# MAGIC | **Position in Star Schema** | Sits in the **center** | Surrounds the fact table, radiating outward |
# MAGIC | **Typical examples** | `fact_sales`, `fact_orders`, `fact_payments` | `dim_customer`, `dim_product`, `dim_date`, `dim_region` |
# MAGIC | **Joins required to be useful** | Needs dimension tables to give the numbers meaning | Can be queried alone, or joined to enrich fact data |
# MAGIC | **Normalization level** | Usually not normalized further — kept flat and wide | Can be kept flat (Star) or normalized further (Snowflake) |
# MAGIC
# MAGIC ### 🧠 The One-Line Way to Remember It
# MAGIC > **Fact table = the numbers. Dimension table = the descriptions that explain those numbers.**
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ⭐ Star Schema — The Simple, Denormalized Shape
# MAGIC
# MAGIC ### What It Is
# MAGIC A **Star Schema** connects **one central fact table** directly to **multiple dimension tables** — each dimension table is flat (not broken down further), so the diagram looks like a star with the fact table at the center.
# MAGIC
# MAGIC ```
# MAGIC                 dim_date
# MAGIC                    │
# MAGIC                    │
# MAGIC    dim_customer ── fact_sales ── dim_product
# MAGIC                    │
# MAGIC                    │
# MAGIC                 dim_region
# MAGIC ```
# MAGIC
# MAGIC ### Key Trait: Denormalized Dimensions
# MAGIC In a Star Schema, each dimension table holds **all** its related attributes directly in one flat table — even if some of that data is technically repetitive.
# MAGIC
# MAGIC **Example — `dim_product` in a Star Schema:**
# MAGIC
# MAGIC | ProductKey | ProductName | ProductCategory | CategoryDescription |
# MAGIC |---|---|---|---|
# MAGIC | 201 | Laptop | Electronics | Devices and gadgets |
# MAGIC | 202 | Smartphone | Electronics | Devices and gadgets |
# MAGIC
# MAGIC Notice `CategoryDescription` repeats for every product in the same category — that's **denormalization**, and it's intentional.
# MAGIC
# MAGIC ### Why Use Star Schema
# MAGIC - ✅ **Fewer joins** — a query only needs to join the fact table directly to each dimension, one hop each
# MAGIC - ✅ **Simpler to write queries** — very intuitive for analysts and BI tools (Power BI, Tableau) to navigate
# MAGIC - ✅ **Faster read performance** — fewer joins generally means faster aggregate queries
# MAGIC - ❌ **Some data redundancy** — the same category info repeats across many product rows
# MAGIC
# MAGIC **When to use it:** This is the **default, most common choice** for data warehouses — especially when query speed and simplicity for reporting matter more than saving a small amount of storage space.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ❄️ Snowflake Schema — The Normalized Shape
# MAGIC
# MAGIC ### What It Is
# MAGIC A **Snowflake Schema** takes a Star Schema and **breaks the dimension tables down further** into additional related sub-tables — removing repeated/redundant data by normalizing dimensions, the same way you'd normalize a regular transactional database.
# MAGIC
# MAGIC ```
# MAGIC                     dim_date
# MAGIC                        │
# MAGIC                        │
# MAGIC dim_customer ──   fact_sales   ── dim_product ── dim_category
# MAGIC                        │
# MAGIC                        │
# MAGIC                    dim_region ── dim_country
# MAGIC ```
# MAGIC
# MAGIC Notice `dim_product` no longer holds `CategoryDescription` directly — it just holds a `CategoryKey`, pointing to a separate `dim_category` table.
# MAGIC
# MAGIC ### Key Trait: Normalized Dimensions
# MAGIC
# MAGIC **Example — Same Product Info, Now Snowflaked:**
# MAGIC
# MAGIC `dim_product`
# MAGIC
# MAGIC | ProductKey | ProductName | CategoryKey |
# MAGIC |---|---|---|
# MAGIC | 201 | Laptop | 501 |
# MAGIC | 202 | Smartphone | 501 |
# MAGIC
# MAGIC `dim_category`
# MAGIC
# MAGIC | CategoryKey | ProductCategory | CategoryDescription |
# MAGIC |---|---|---|
# MAGIC | 501 | Electronics | Devices and gadgets |
# MAGIC
# MAGIC Now `CategoryDescription` is stored **only once**, in its own table — no repetition.
# MAGIC
# MAGIC ### Why Use Snowflake Schema
# MAGIC - ✅ **Less data redundancy** — each piece of information is stored exactly once
# MAGIC - ✅ **Easier to maintain** — updating "Electronics" category description happens in one place, not thousands of rows
# MAGIC - ✅ **Better data integrity** — normalized structure enforces consistency
# MAGIC - ❌ **More joins required** — a single report might now need to join fact → dim_product → dim_category (multiple hops)
# MAGIC - ❌ **More complex queries** — harder for analysts/BI tools to navigate intuitively
# MAGIC - ❌ **Can be slower** — more joins generally means more query overhead
# MAGIC
# MAGIC **When to use it:** When **storage efficiency and data integrity** matter more than raw query simplicity/speed — often in very large-scale warehouses with dimensions that have deep hierarchies (e.g., Category → Subcategory → Sub-subcategory) and where update consistency is critical.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🥊 Star vs Snowflake — Side-by-Side
# MAGIC
# MAGIC | Aspect | Star Schema | Snowflake Schema |
# MAGIC |---|---|---|
# MAGIC | **Dimension structure** | Flat, denormalized | Broken into related sub-tables, normalized |
# MAGIC | **Number of joins** | Fewer (fact → dimension, one hop) | More (fact → dimension → sub-dimension) |
# MAGIC | **Query complexity** | Simple, intuitive | More complex |
# MAGIC | **Query performance** | Generally faster | Generally slower (more joins) |
# MAGIC | **Data redundancy** | Higher (repeated attributes) | Lower (each value stored once) |
# MAGIC | **Storage usage** | Slightly higher | Slightly lower |
# MAGIC | **Ease of maintenance** | Harder to update shared values (must update every repeated row) | Easier (update once, in the sub-table) |
# MAGIC | **Best for** | Most BI/reporting use cases, simpler analytics | Very large dimensions, deep hierarchies, storage-sensitive systems |
# MAGIC | **Industry popularity** | Much more common | Used more selectively |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Quick Summary
# MAGIC
# MAGIC - **Fact tables** hold the measurable numbers (and foreign keys); **dimension tables** hold the descriptive context that gives those numbers meaning.
# MAGIC - **Star Schema** = fact table + flat, denormalized dimension tables → simple, fast, fewer joins, some redundancy. The default choice for most warehouses.
# MAGIC - **Snowflake Schema** = fact table + normalized, multi-level dimension tables → less redundancy, better data integrity, but more joins and query complexity.
# MAGIC - **Rule of thumb:** Start with a Star Schema unless you have a specific reason (huge dimension tables, strict storage/consistency requirements) to snowflake it.