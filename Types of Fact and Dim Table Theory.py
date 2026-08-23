# Databricks notebook source
# MAGIC %md
# MAGIC # 📊 Types of Fact Tables & Types of Dimension Tables — Complete Guide
# MAGIC
# MAGIC This builds directly on the Star Schema you already implemented (`FactSales` + `DimProducts`, `DimCustomers`, `DimRegion`, `DimDate`). Not every fact table or dimension table works the same way — there are specific **types**, each solving a different reporting problem.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC # 🧾 Part 1 — Types of Fact Tables
# MAGIC
# MAGIC Fact tables differ based on **what kind of event they're recording**, and **how often a row gets added or changed**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 1️⃣ Transaction (Granular) Fact Table
# MAGIC
# MAGIC ### What It Is
# MAGIC Records **one row per individual business event/transaction**, at the most detailed level possible — this is the "grain" concept from before, taken to its most precise level. This is exactly the type of fact table you already built (`FactSales`).
# MAGIC
# MAGIC ### Simple Example
# MAGIC
# MAGIC | OrderID | DimProductsKey | DimCustomersKey | Quantity | UnitPrice | TotalAmount |
# MAGIC |---|---|---|---|---|---|
# MAGIC | 1 | 201 | 101 | 2 | 800.00 | 1600.00 |
# MAGIC | 2 | 202 | 102 | 1 | 500.00 | 500.00 |
# MAGIC | 3 | 203 | 103 | 3 | 300.00 | 900.00 |
# MAGIC
# MAGIC Every single order line is its own row. If a customer places 5 orders, there are 5 rows.
# MAGIC
# MAGIC ### Characteristics
# MAGIC - **Grain:** One row = one transaction/event
# MAGIC - **Growth:** Grows very fast — every new sale, click, or transaction adds a new row
# MAGIC - **Size:** Usually the **largest** fact table type in a warehouse
# MAGIC - **Data:** Highly detailed — can answer almost any question by aggregating up
# MAGIC
# MAGIC ### When to Use It
# MAGIC Use this whenever you need the **finest possible detail** — e.g., "show me every individual sale," or when you need flexibility to aggregate data in many different, unpredictable ways later (by day, by product, by customer, by region — all from the same table).
# MAGIC
# MAGIC **Real-world examples:** Sales transactions, website clicks, individual bank transactions, order line items (exactly what you built).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 2️⃣ Periodic Snapshot Fact Table
# MAGIC
# MAGIC ### What It Is
# MAGIC Instead of recording every individual event, this captures the **state of something at a regular, fixed interval** — e.g., every day, every week, every month — like taking a photograph of a value at that specific point in time.
# MAGIC
# MAGIC ### Simple Example — Daily Inventory Snapshot
# MAGIC
# MAGIC | SnapshotDate | DimProductsKey | UnitsInStock | UnitsOnOrder |
# MAGIC |---|---|---|---|
# MAGIC | 2024-02-01 | 201 | 500 | 100 |
# MAGIC | 2024-02-02 | 201 | 480 | 100 |
# MAGIC | 2024-02-03 | 201 | 460 | 50 |
# MAGIC
# MAGIC Notice: this **isn't** "every time inventory changed" — it's "what did inventory look like at the end of each day," captured once per day, every day, regardless of how many individual inventory transactions happened underneath.
# MAGIC
# MAGIC ### Characteristics
# MAGIC - **Grain:** One row per entity, per fixed time interval (e.g., per product per day)
# MAGIC - **Growth:** Predictable — grows by a fixed amount each period (number of entities × 1, every day)
# MAGIC - **Purpose:** Tracks **trends over time** for things that have a "balance" or "status," not just discrete events
# MAGIC - Even if **nothing changed**, a new row is still recorded for that period (that's what makes it a true "snapshot")
# MAGIC
# MAGIC ### When to Use It
# MAGIC Use this when you need to track **how a value trends over time** — account balances, inventory levels, subscriber counts — where the *transaction* fact table alone would make trend analysis very slow and complicated (you'd have to replay and sum up every transaction just to know "what was the balance on this date").
# MAGIC
# MAGIC **Real-world examples:** Daily bank account balances, monthly inventory levels, weekly website active-user counts.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 3️⃣ Accumulating Snapshot Fact Table
# MAGIC
# MAGIC ### What It Is
# MAGIC Tracks a **process or workflow that has a defined beginning and end**, with multiple milestone stages in between. Unlike the other two types, **the same row gets updated repeatedly** as the process moves through each stage — it "accumulates" the full lifecycle in one row.
# MAGIC
# MAGIC ### Simple Example — Order Fulfillment Process
# MAGIC
# MAGIC | OrderID | OrderDate | ShippedDate | DeliveredDate | DaysToShip | DaysToDeliver |
# MAGIC |---|---|---|---|---|---|
# MAGIC | 1 | 2024-02-01 | 2024-02-02 | 2024-02-05 | 1 | 3 |
# MAGIC | 2 | 2024-02-02 | NULL | NULL | NULL | NULL |
# MAGIC
# MAGIC Order 1 has completed its whole journey — every milestone is filled in. Order 2 has only just been placed — as it moves through shipping and delivery, **this same row gets updated** (not a new row inserted) to fill in `ShippedDate`, then later `DeliveredDate`.
# MAGIC
# MAGIC ### Characteristics
# MAGIC - **Grain:** One row per process instance (e.g., one row per order, tracking its entire lifecycle)
# MAGIC - **Growth:** Rows get **updated in place**, not just appended — this is the key difference from the other two types
# MAGIC - **Purpose:** Measures how long a process takes to move between stages (lead time, cycle time, bottlenecks)
# MAGIC
# MAGIC ### When to Use It
# MAGIC Use this when you're analyzing a **multi-step process/pipeline** and care about the time between stages — order fulfillment, loan approval workflows, support ticket resolution, hiring pipelines (application → interview → offer → hire).
# MAGIC
# MAGIC **Real-world examples:** Order-to-delivery pipeline, insurance claim processing, manufacturing production stages.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📊 Fact Table Types — Side-by-Side
# MAGIC
# MAGIC | Aspect | Transaction (Granular) | Periodic Snapshot | Accumulating Snapshot |
# MAGIC |---|---|---|---|
# MAGIC | **Grain** | One row per event | One row per entity per fixed interval | One row per process instance |
# MAGIC | **New rows added when...** | Every new transaction happens | Every fixed time period (regardless of activity) | Every new process starts |
# MAGIC | **Existing rows updated?** | Rarely (append-only) | Rarely (append-only) | **Yes — updated repeatedly** as the process progresses |
# MAGIC | **Growth rate** | Fast, unpredictable volume | Steady, predictable volume | Slow — bounded by number of active processes |
# MAGIC | **Best for** | Maximum detail, flexible aggregation | Trend analysis of a "point-in-time balance" | Measuring process duration/bottlenecks |
# MAGIC | **Example** | Every sale, every click | Daily account balance, monthly inventory | Order fulfillment, loan approval pipeline |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC # 🗂️ Part 2 — Types of Dimension Tables
# MAGIC
# MAGIC Just like fact tables, dimension tables come in different flavors depending on **how they're used or shared** across the warehouse.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 1️⃣ Conformed Dimension
# MAGIC
# MAGIC ### What It Is
# MAGIC A dimension table that is **shared and reused identically across multiple fact tables** — same structure, same keys, same meaning — everywhere it's used in the warehouse.
# MAGIC
# MAGIC ### Simple Example
# MAGIC Your `DimDate` and `DimCustomers` tables are perfect examples of conformed dimensions. If your warehouse later adds a `FactReturns` table (tracking product returns) alongside your existing `FactSales`, **both** fact tables would join to the exact same `DimDate` and `DimCustomers` tables — not separate, duplicate versions of them.
# MAGIC
# MAGIC ```
# MAGIC FactSales    ──┐
# MAGIC                 ├──▶ DimDate (shared, conformed)
# MAGIC FactReturns  ──┘
# MAGIC ```
# MAGIC
# MAGIC ### Characteristics
# MAGIC - Ensures **consistency** — "March 2024" means the exact same thing whether you're looking at sales or returns
# MAGIC - Built and maintained **once**, referenced by many fact tables
# MAGIC - Prevents duplicate, slightly-different versions of the same dimension from creeping into the warehouse
# MAGIC
# MAGIC ### When to Use It
# MAGIC Whenever a dimension (like Date, Customer, Product, Region) will be relevant to **more than one fact table** — which, in a real warehouse, is almost always the case. This is less a "special type you opt into" and more a **best practice you should default to** for shared dimensions like Date and Customer.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 2️⃣ Role-Playing Dimension
# MAGIC
# MAGIC ### What It Is
# MAGIC The **same physical dimension table** is used **multiple times in the same fact table**, each time representing a different "role" or context.
# MAGIC
# MAGIC ### Simple Example
# MAGIC Imagine your `FactSales` needed to track not just `OrderDate`, but also `ShippedDate` and `DeliveredDate` — three different dates, but all of them are genuinely just... dates. You don't need three separate physical date tables (`DimOrderDate`, `DimShippedDate`, `DimDeliveredDate`) — you reuse the **same** `DimDate` table three times, joined via three different foreign keys:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT f.OrderID
# MAGIC FROM FactSales f
# MAGIC JOIN DimDate od ON f.OrderDateKey = od.DimDateKey       -- "Date" playing the role of Order Date
# MAGIC JOIN DimDate sd ON f.ShippedDateKey = sd.DimDateKey     -- "Date" playing the role of Ship Date
# MAGIC JOIN DimDate dd ON f.DeliveredDateKey = dd.DimDateKey   -- "Date" playing the role of Delivery Date
# MAGIC ```
# MAGIC
# MAGIC The underlying table (`DimDate`) is physically **one table** — it's just being "played" in three different roles within the same query, usually given a different alias each time (`od`, `sd`, `dd` above).
# MAGIC
# MAGIC ### Characteristics
# MAGIC - Saves you from creating near-duplicate dimension tables that hold identical structure/data
# MAGIC - Requires clear **aliasing** in queries so it's obvious which "role" each join represents
# MAGIC - Very common with `DimDate`, but can apply to any dimension used in multiple contexts (e.g., `DimEmployee` used as both "Salesperson" and "Manager" on the same fact row)
# MAGIC
# MAGIC ### When to Use It
# MAGIC Whenever a fact table needs to reference the **same type of dimension multiple times for different purposes** — most commonly dates (order date vs. ship date vs. delivery date), but also applies to things like "billing address" vs. "shipping address" both pointing to the same `DimAddress` table.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 3️⃣ Junk Dimension
# MAGIC
# MAGIC ### What It Is
# MAGIC A single dimension table created by **grouping together several small, low-cardinality, unrelated flags/indicators** that don't deserve their own separate dimension tables — instead of scattering them as loose columns on the fact table.
# MAGIC
# MAGIC ### Simple Example
# MAGIC Imagine your orders also had a few small yes/no or short-code flags: `IsGift` (Y/N), `PaymentMethod` (Cash/Card/UPI), `OrderChannel` (Online/In-Store). Rather than adding three raw columns directly onto `FactSales`, or creating three tiny separate dimension tables for each, you combine them into **one small "junk" dimension**:
# MAGIC
# MAGIC `DimOrderFlags`
# MAGIC
# MAGIC | DimOrderFlagsKey | IsGift | PaymentMethod | OrderChannel |
# MAGIC |---|---|---|---|
# MAGIC | 1 | Y | Card | Online |
# MAGIC | 2 | N | Cash | In-Store |
# MAGIC | 3 | N | Card | Online |
# MAGIC | 4 | Y | UPI | Online |
# MAGIC
# MAGIC `FactSales` then just stores a single `DimOrderFlagsKey`, instead of three separate raw flag columns cluttering the fact table.
# MAGIC
# MAGIC ### Characteristics
# MAGIC - Keeps the **fact table clean** — one key instead of several miscellaneous flag columns
# MAGIC - Typically has a **small number of rows** — since it's just every unique *combination* of the flag values (not one row per transaction)
# MAGIC - Combines otherwise-meaningless-on-their-own attributes into a tidy, queryable group
# MAGIC
# MAGIC ### When to Use It
# MAGIC When you have several **small, low-cardinality flags or indicator columns** (yes/no fields, short codes, statuses) that are related to a transaction but don't naturally belong to any of your existing "real" dimensions (Customer, Product, Region, Date) and aren't significant enough to warrant their own dedicated dimension table each.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 4️⃣ Degenerate Dimension
# MAGIC
# MAGIC ### What It Is
# MAGIC A dimension-like attribute that's **kept directly inside the fact table itself**, rather than being broken out into its own separate dimension table — because it has **no additional descriptive attributes** to justify one.
# MAGIC
# MAGIC ### Simple Example
# MAGIC Look at your own `FactSales` table — it directly stores `OrderID`:
# MAGIC
# MAGIC ```sql
# MAGIC CREATE TABLE orderDWH.FactSales
# MAGIC (
# MAGIC   OrderID INT,       -- 👈 this is a degenerate dimension
# MAGIC   Quantity DECIMAL,
# MAGIC   ...
# MAGIC )
# MAGIC ```
# MAGIC
# MAGIC `OrderID` is clearly identifying/descriptive information (it identifies which order this line belongs to) — which normally sounds like "dimension" territory. But there's no separate `DimOrders` table with extra `OrderID` attributes (like an order status, order source, etc.) — it's just the raw identifier itself, sitting directly in the fact table. That makes it a **degenerate dimension**.
# MAGIC
# MAGIC ### Characteristics
# MAGIC - Looks like a dimension key, but has **no dimension table behind it**
# MAGIC - Usually an **identifier/reference number** from the source system (order number, invoice number, ticket number)
# MAGIC - Kept in the fact table simply because creating a whole separate one-column dimension table for it would be wasteful
# MAGIC
# MAGIC ### When to Use It
# MAGIC Whenever you have an identifier that's useful to keep (e.g., for tracing back to the source system, grouping line items that belong to the same order) but that has **no additional attributes worth modeling** as a full dimension table. If that identifier *does* start needing descriptive attributes (like an `OrderStatus` or `OrderSource`), it may be time to promote it into a real dimension table instead.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📊 Dimension Table Types — Side-by-Side
# MAGIC
# MAGIC | Aspect | Conformed | Role-Playing | Junk | Degenerate |
# MAGIC |---|---|---|---|---|
# MAGIC | **What it solves** | Consistency across multiple fact tables | Reusing one dimension for multiple purposes in the same fact table | Tidying up several small unrelated flags | Handling an identifier with no real descriptive attributes |
# MAGIC | **Physical tables** | One shared table, used by many facts | One physical table, joined multiple times per query | One small combined table | No separate table — lives in the fact table |
# MAGIC | **Typical size** | Varies (often large, e.g., DimCustomer) | Same as the base dimension (e.g., DimDate) | Small (one row per unique flag combination) | N/A — it's just a column |
# MAGIC | **Example** | `DimDate`, `DimCustomer` shared across `FactSales` & `FactReturns` | `DimDate` reused as OrderDate/ShipDate/DeliveredDate | `DimOrderFlags` (IsGift, PaymentMethod, Channel) | `OrderID` sitting directly in `FactSales` |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Quick Summary
# MAGIC
# MAGIC **Fact Table Types:**
# MAGIC - **Transaction/Granular** → one row per individual event; maximum detail; your `FactSales` is this type.
# MAGIC - **Periodic Snapshot** → one row per entity per fixed time interval; great for tracking balances/trends over time.
# MAGIC - **Accumulating Snapshot** → one row per process instance, updated as it moves through stages; great for measuring process duration.
# MAGIC
# MAGIC **Dimension Table Types:**
# MAGIC - **Conformed** → the same dimension shared consistently across multiple fact tables.
# MAGIC - **Role-Playing** → the same physical dimension table reused multiple times in one fact table for different purposes (most often `DimDate`).
# MAGIC - **Junk** → several small, unrelated flags/indicators bundled into one tidy dimension instead of cluttering the fact table.
# MAGIC - **Degenerate** → an identifier kept directly in the fact table because it has no meaningful attributes to justify its own dimension table.
# MAGIC
# MAGIC **Rule of thumb for choosing:** Start by identifying your **grain** (transaction, snapshot, or process) to pick the right fact table type — then look at each attribute and ask *"does this belong in a shared dimension, does it play multiple roles, is it a small flag, or is it just an ID with nothing more to say?"* to pick the right dimension table type.