# 🏛️ Data Warehouse — The Ultimate Guide
![Data Warehousing](https://img.shields.io/badge/Data-Warehousing-E25A1C?style=for-the-badge&logo=databricks&logoColor=white)
![Dimensional Modeling](https://img.shields.io/badge/Dimensional-Modeling-blue?style=for-the-badge)
![Star Schema](https://img.shields.io/badge/Star-Schema-9cf?style=for-the-badge)
![SCD](https://img.shields.io/badge/Slowly%20Changing-Dimensions-brightgreen?style=for-the-badge)
![Incremental Loading](https://img.shields.io/badge/Incremental-Loading-orange?style=for-the-badge)
![Fact & Dim Tables](https://img.shields.io/badge/Fact%20%26%20Dimension-Tables-blueviolet?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-Databricks-success?style=for-the-badge)

---

## 📌 Section Overview

This repository is **theory-to-practice, end to end**: it starts at the whiteboard level (*what even is a data warehouse, and why does a business need one?*), works down through the formal discipline of **data modeling** (Conceptual → Logical → Physical), lands on the industry-standard **dimensional modeling** approach (Star Schema, Fact & Dimension tables), and then proves every one of those ideas out with **real, hands-on SQL** — building an actual incremental pipeline and an actual Star Schema from scratch, bugs and all.

> Most people can define "ETL" in an interview. This repo goes further — it's the difference between reciting the definition of a Star Schema and having actually built one, staged the data, hit a real copy-paste bug in a `row_number()` alias, and fixed it.

---

## 🎯 Aim & Objectives

- Understand **what a Data Warehouse is** (the destination) versus **Data Warehousing** (the end-to-end process) — and why organizations need a dedicated analytical system separate from operational databases
- Master **OLTP vs OLAP** — the fundamental split between systems that *run* the business and systems that *analyze* it
- Understand the **three levels of Data Modeling** — Conceptual → Logical → Physical — and how each adds precision until you reach real, deployable SQL
- Master **Dimensional Modeling**: Fact tables vs Dimension tables, Star Schema vs Snowflake Schema, and exactly when to reach for each
- Understand the **different types of Fact tables** (Transaction, Periodic Snapshot, Accumulating Snapshot) and **Dimension tables** (Conformed, Role-Playing, Junk, Degenerate)
- Master **Slowly Changing Dimensions (SCD)** — Type 1, Type 2, and Type 3 — and know precisely which one to reach for based on whether history needs to be preserved
- Understand **Incremental Loading** — Full Load vs Incremental Load, Change Data Capture (CDC), and the Staging → Transformation → Core pipeline pattern
- Apply every one of these concepts hands-on: build a real Staging/Core pipeline, implement CDC with a timestamp filter, build a full Star Schema with surrogate keys, and implement SCD Type 1 with a `MERGE`

---

## 🧰 Tech Stack & Concepts

| Concept | Purpose |
|---|---|
| Data Warehouse vs Data Warehousing | The destination system vs. the complete process/architecture around it |
| OLTP vs OLAP | Transactional systems (run the business) vs. analytical systems (analyze the business) |
| Data Modeling (Conceptual/Logical/Physical) | Progressive levels of precision from business concept to deployable SQL |
| Dimensional Modeling | Fact & Dimension tables, purpose-built for fast analytical queries |
| Star Schema & Snowflake Schema | Denormalized vs. normalized dimension structures around a fact table |
| Types of Fact Tables | Transaction, Periodic Snapshot, Accumulating Snapshot |
| Types of Dimension Tables | Conformed, Role-Playing, Junk, Degenerate |
| Surrogate Keys vs Natural Keys | Warehouse-generated stable IDs vs. source-system business IDs |
| Slowly Changing Dimensions (SCD) | Type 1 (overwrite), Type 2 (new row/history), Type 3 (new column) |
| Incremental Loading & CDC | Loading only new/changed data instead of reprocessing everything |
| Staging → Transformation → Core | The standard layered pipeline pattern in a real warehouse |
| Databricks SQL & PySpark | The engine used to implement every concept above with real tables, views, and `MERGE` statements |

---

## 🏗️ Learning Architecture

```
Foundations
   └── What is a Data Warehouse? Why does it exist? OLTP vs OLAP
        ↓
Formal Design Discipline
   └── Data Modeling: Conceptual → Logical → Physical
        ↓
The Warehouse-Specific Modeling Style
   └── Dimensional Modeling: Fact Tables, Dimension Tables, Star vs Snowflake Schema
        ↓
Going Deeper on Table Design
   └── Types of Fact Tables (Transaction/Snapshot/Accumulating)
   └── Types of Dimension Tables (Conformed/Role-Playing/Junk/Degenerate)
        ↓
Handling Change Over Time
   └── Slowly Changing Dimensions: Type 1, Type 2, Type 3
        ↓
Getting Data In, The Right Way
   └── Full Load vs Incremental Load, CDC, Staging vs Core
        ↓
Proof of Mastery — Hands-On Practicals
   └── Practical 1: Building a real Incremental Loading pipeline (Staging → Core)
   └── Practical 2: Building a real Star Schema (4 Dims + 1 Fact, with surrogate keys)
   └── Practical 3: Implementing SCD Type 1 with a Delta `MERGE`
```

---

## 🧩 Notebook-by-Notebook Breakdown

| # | Notebook | Core Concept |
|---|---|---|
| 1 | Data Warehousing Theory | The complete conceptual foundation — DWH definition, OLTP vs OLAP, architecture, ETL/ELT, medallion architecture, governance, and 55 sections covering the entire discipline end to end |
| 2 | Data Modeling Theory | Conceptual → Logical → Physical modeling, dimensional modeling, Fact vs Dimension tables, Star vs Snowflake schema |
| 3 | Types of Fact & Dim Table Theory | The three fact table types (Transaction, Periodic Snapshot, Accumulating Snapshot) and four dimension table types (Conformed, Role-Playing, Junk, Degenerate) |
| 4 | SCD Types Theory | Slowly Changing Dimensions — Type 1 (overwrite), Type 2 (new row), Type 3 (new column), and how to decide between them |
| 5 | DWH Practical Part 1 — Incremental Loading | Hands-on: built a source table, a 3-layer warehouse (Staging → Transformation → Core), implemented timestamp-based CDC, and proved out incremental `INSERT` vs. full reload |
| 6 | DWH Practical Part 2 — Data Warehouse Modeling | Hands-on: built a full Star Schema from scratch — `DimCustomers`, `DimProducts`, `DimRegion`, `DimDate` + `FactSales`, using `row_number()`-generated surrogate keys and multi-way `LEFT JOIN`s |
| 7 | DWH Practical 3 — Implementing SCD Type 1 | Hands-on: built a `DimProducts` table and applied SCD Type 1 logic using a Delta Lake `MERGE ... WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT` |

---

## 📖 Detailed Learnings

### 🏛️ 1. Data Warehousing Theory — The Complete Foundation
**Focus:** Building the full mental model of *why* data warehouses exist and *how* the discipline of data warehousing works, from first principles to interview-ready answers.

- Defined a **Data Warehouse** as the centralized, integrated analytical repository — and drew the clear line between it and **Data Warehousing**, the full end-to-end process (extract, ingest, clean, transform, integrate, govern, serve)
- Mastered the **four classic characteristics** of a traditional warehouse: Subject-Oriented, Integrated, Time-Variant, and Non-Volatile
- Deep-dived **OLTP vs OLAP** — transactional systems built for fast, frequent, small operations (`MySQL`, `PostgreSQL`) versus analytical systems built for large, complex, historical queries (`Snowflake`, `BigQuery`, `Redshift`)
- Traced the full **warehouse architecture**: Data Sources → Ingestion → Raw/Staging → Clean/Validate → Transform → Warehouse → BI/Reports/Analytics
- Compared **ETL vs ELT**, understood the **Staging Area** and the **Raw → Clean → Curated** layering pattern (a precursor to the **Medallion Architecture** — Bronze/Silver/Gold)
- Covered **Data Warehouse vs Data Lake vs Lakehouse**, **MPP (Massively Parallel Processing)** and why it matters for warehouse performance, **Partition Pruning**, **Data Quality**, **Data Governance**, **Data Security**, **Metadata**, and **Data Lineage**
- Studied **Data Marts** vs. the **Enterprise Data Warehouse**, walked an **end-to-end retail example**, and traced **what actually happens when a BI user runs a query**
- Closed with a full set of **interview-ready answers** for the most commonly asked warehousing questions (What is a DWH? ETL vs ELT? Star Schema? DWH vs Data Lake?)

```text
Source Systems → ETL/ELT → Data Warehouse → Reports / Dashboards / Analytics
```
**Takeaway:** This notebook is the theoretical backbone of the whole repo — every practical exercise below is a direct, hands-on execution of a concept introduced here (Staging/Core comes straight from Section 13–14; the Star Schema comes straight from Sections 15–19; SCD comes straight from Sections 23–26).

---

### 🧩 2. Data Modeling Theory — Conceptual → Logical → Physical
**Focus:** Understanding data modeling as a *formal discipline* — not just "designing tables," but a deliberate, progressively more detailed process.

- Learned the **three levels of data modeling** as a funnel of increasing precision:
  - **Conceptual** — business entities and relationships only (`Customer places Order`), understandable by non-technical stakeholders, zero technical detail
  - **Logical** — real attributes, generic data types, and explicit **PK/FK** relationships, but still technology-agnostic
  - **Physical** — the final, database-specific blueprint: exact data types, constraints, indexes — this is what actually becomes a `CREATE TABLE` statement
- Compared all three side-by-side across audience, detail level, and "can you actually run it as SQL?"
- Introduced **Dimensional Modeling** as the specialized modeling style used specifically inside data warehouses — because a warehouse's job (answering big aggregate questions fast) is fundamentally different from an OLTP database's job (fast small reads/writes)
- Mastered the **Fact vs Dimension** decision rule: *"Is this a number I'd `SUM()`/`AVG()`/`COUNT()`, or a label I'd filter/group by?"* — numbers go in the Fact table, descriptive context goes in Dimension tables
- Compared **Star Schema** (flat, denormalized dimensions, fewer joins, faster, some redundancy) against **Snowflake Schema** (normalized dimensions broken into sub-tables, less redundancy, more joins, better data integrity) — and when each is the right call

```sql
SELECT p.ProductCategory, SUM(f.TotalAmount) AS total_sales
FROM fact_sales f
JOIN dim_product p  ON f.ProductKey  = p.ProductKey
JOIN dim_customer c ON f.CustomerKey = c.CustomerKey
JOIN dim_date d      ON f.DateKey     = d.DateKey
WHERE c.Country = 'USA' AND d.Quarter = 'Q1' AND d.Year = 2024
GROUP BY p.ProductCategory;
```
**Takeaway:** Conceptual → Logical → Physical is the discipline that keeps a warehouse design honest at every stage; Dimensional Modeling (and specifically the Star Schema) is *why* that discipline produces something an analyst can actually query quickly.

---

### 🥇🥈🥉 3. Types of Fact & Dimension Tables — Going Deeper
**Focus:** Not every Fact or Dimension table works the same way — this notebook builds directly on top of the Star Schema already implemented (`FactSales` + 4 dims) and classifies the *specific patterns* real warehouses use.

**Fact Table Types:**
- **Transaction (Granular) Fact Table** — one row per individual event, maximum detail, fastest-growing, most flexible for aggregation (exactly the `FactSales` table built in the practicals)
- **Periodic Snapshot Fact Table** — captures the *state* of something at a fixed interval (daily inventory, monthly balances) — a new row lands every period **even if nothing changed**, which is what makes trend analysis fast without replaying every transaction
- **Accumulating Snapshot Fact Table** — tracks a process with a defined start and end (order → shipped → delivered); uniquely, **the same row gets updated repeatedly** as the process moves through milestones, instead of new rows being appended

**Dimension Table Types:**
- **Conformed Dimension** — the same shared dimension (`DimDate`, `DimCustomer`) used consistently across multiple fact tables, so nothing drifts into duplicate/inconsistent versions
- **Role-Playing Dimension** — one physical dimension table (`DimDate`) joined multiple times in the *same* fact table under different aliases (`OrderDate`, `ShippedDate`, `DeliveredDate`) — no need for three near-identical date tables
- **Junk Dimension** — several small, low-cardinality flags (`IsGift`, `PaymentMethod`, `OrderChannel`) bundled into one tidy dimension instead of cluttering the fact table with loose columns
- **Degenerate Dimension** — an identifier (like `OrderID`) that lives directly inside the fact table because it has no descriptive attributes that would justify a dedicated dimension table of its own — recognized directly from the `FactSales` table already built

```sql
SELECT f.OrderID
FROM FactSales f
JOIN DimDate od ON f.OrderDateKey     = od.DimDateKey   -- "Date" playing Order Date
JOIN DimDate sd ON f.ShippedDateKey   = sd.DimDateKey   -- "Date" playing Ship Date
JOIN DimDate dd ON f.DeliveredDateKey = dd.DimDateKey   -- "Date" playing Delivery Date
```
**Takeaway:** Picking the right *type* of Fact or Dimension table is what separates a warehouse that merely "works" from one that's actually intentional — the rule of thumb: identify the grain first (event, snapshot, or process), then classify each attribute (shared? multi-role? a small flag? just an ID?).

---

### 🕰️ 4. SCD Types Theory — Handling Change Over Time
**Focus:** The core question every dimension eventually forces you to answer: *when a value changes, do I overwrite it, or keep the history?*

- **SCD Type 1 (Overwrite)** — the old value is simply replaced; no history kept. Best for corrections/typos where the old value has zero business value (e.g., fixing a misspelled email)
- **SCD Type 2 (New Row)** — the old row is expired (`IsActive = 'N'`, `EndTime` set) and a brand-new row is inserted for the updated version; full history preserved. This is **the industry standard** for anything where "what was true as of date X" matters (address history, price history, job title history)
- **SCD Type 3 (New Column)** — a `PreviousValue` column captures just the one-step-back value while the main column updates to current; simple, but only ever remembers a single prior version — anything before that is lost
- Built the full **side-by-side comparison** (history kept? table growth? complexity? can you answer "what was true on date X"?) and a clean **decision framework**: *"If this value changes, do I ever need to know what it used to be? No → Type 1. Yes, fully → Type 2. Only the last step → Type 3."*

```sql
-- SCD Type 2 pattern
MERGE INTO DimCustomers trg USING src ON trg.CustomerID = src.CustomerID AND trg.IsActive = 'Y'
WHEN MATCHED AND src.City <> trg.City THEN UPDATE SET trg.EndTime = current_timestamp(), trg.IsActive = 'N';

MERGE INTO DimCustomers trg USING src ON trg.CustomerID = src.CustomerID AND trg.IsActive = 'Y'
WHEN NOT MATCHED THEN INSERT *;
```
**Takeaway:** Real warehouses use a *mix* — critical dimensions get Type 2, minor corrective fields get Type 1, and Type 3 shows up only in narrow before/after comparison cases. Knowing which one a business requirement actually calls for is a genuinely senior-level skill.

---

### 🏗️ 5. Practical 1 — Building a Real Incremental Loading Pipeline
**Focus:** Proving, with actual running SQL, that a warehouse doesn't need to reload everything every time — hands-on Staging → Transformation → Core, plus a real CDC filter.

- Built a **source system table** (`sales.Orders`, 10 rows) to represent an operational app generating daily orders
- Built the warehouse as **three explicit layers**: `stg_sales` (raw landing copy), `trans_sales` (a *view* applying a business rule — drop rows with `NULL Quantity`), and `core_sales` (the permanent, trusted table analysts actually query)
- Proved the **incremental mechanism end to end**: inserted 5 new rows into the source, then re-populated staging using `WHERE OrderDate > '2024-02-10'` — **this one filter is timestamp-based CDC in action**
- Correctly recognized that the **transformation view needed zero changes** — since it's a view, it automatically re-evaluates against whatever staging currently holds; the incremental behavior lives entirely in staging's CDC filter
- Used `INSERT INTO core_sales` (append) instead of `CREATE OR REPLACE TABLE ... AS SELECT` (which would have destroyed the previous batch) — the exact mechanical difference between an incremental load and a full load
- Self-diagnosed the pipeline's own rough edges like a production engineer would: staging is replaced rather than `TRUNCATE`d, the CDC cutoff date is hardcoded instead of pulled from a **watermark control table**, and reusing `OrderID`s 1–5 for "new" rows actually calls for a `MERGE`/upsert rather than a plain `INSERT` if those are meant to be updates

```sql
-- The CDC filter — the entire incremental mechanism in one WHERE clause
CREATE OR REPLACE TABLE salesDWH.stg_sales AS
SELECT * FROM sales.Orders WHERE OrderDate > '2024-02-10';

-- Append, don't replace — this is what makes it incremental
INSERT INTO salesDWH.core_sales
SELECT * FROM salesDWH.trans_sales;
```
**Takeaway:** This notebook turns "CDC" and "incremental loading" from buzzwords into something concretely understood — a `WHERE` filter in staging plus an `INSERT` instead of a rebuild into core, with the judgment to know exactly what a production version would need on top (watermarks, `TRUNCATE`, `MERGE`).

---

### ⭐ 6. Practical 2 — Building a Real Star Schema
**Focus:** Going from a single flat `core_sales` table to a genuine dimensional model — 4 Dimension tables and 1 Fact table, built with the exact repeatable pattern used in every production warehouse.

- Built **`DimCustomers`, `DimProducts`, `DimRegion`, and `DimDate`**, each following the same three-step recipe: (1) create the physical table with a surrogate key column, (2) create a view that pulls `DISTINCT` natural-key rows and generates a surrogate key via `row_number() OVER (ORDER BY ...)`, (3) `INSERT` the view's output into the physical table
- Built **`FactSales`** by starting from `trans_sales` (the transactional-grain data) and `LEFT JOIN`ing to every dimension **on the natural key**, pulling out only each dimension's **surrogate key** — this is exactly what keeps a fact table lightweight: short integer keys instead of repeated text like `"Alice Johnson"` or `"North America"`
- Internalized **Surrogate Keys vs Natural Keys**: a `CustomerID` from the source system can theoretically be reused or changed, but a warehouse-generated `DimCustomersKey` never changes once assigned — which is exactly what makes SCD Type 2 possible later
- Defined the **grain** of `FactSales` explicitly — one row = one order — and recognized `OrderID` sitting directly in the fact table as a **Degenerate Dimension** (an identifier with no separate descriptive attributes worth its own table)
- Also implemented the **same join logic in PySpark**, using `.alias()` and `.selectExpr()` to mirror the SQL `LEFT JOIN` chain — proving the concept translates cleanly between SQL and DataFrame APIs

```sql
INSERT INTO orderDWH.FactSales
SELECT F.OrderID, F.Quantity, F.UnitPrice, F.TotalAmount,
       DP.DimProductsKey, DC.DimCustomersKey, DR.DimRegionKey, DD.DimDateKey
FROM orderDWH.trans_sales F
LEFT JOIN orderDWH.DimCustomers DC ON F.CustomerID = DC.CustomerID
LEFT JOIN orderDWH.DimProducts  DP ON F.ProductID  = DP.ProductID
LEFT JOIN orderDWH.DimRegion    DR ON DR.Country   = F.Country
LEFT JOIN orderDWH.DimDate      DD ON F.OrderDate  = DD.OrderDate;
```
**Takeaway:** This is the theory of Star Schemas made real — and real code comes with real bugs (a copy-pasted `AS DimCustomersKey` alias inside the `DimProducts` view was caught and understood, not just fixed blindly), which is exactly the kind of detail-oriented debugging a working data engineer needs.

---

### 🔁 7. Practical 3 — Implementing SCD Type 1
**Focus:** Taking the SCD Type 1 theory and applying it directly against the `DimProducts` table from the Star Schema practical, using Delta Lake's `MERGE` syntax.

- Rebuilt `DimProducts` from a filtered view of `sales_new.orders` and loaded it with an initial batch
- Inserted new order rows into the source to simulate new/changed product data arriving
- Implemented the **SCD Type 1 overwrite pattern** with a Delta `MERGE`: matched rows get **updated in place** (`WHEN MATCHED THEN UPDATE SET *`), unmatched rows get **inserted** (`WHEN NOT MATCHED THEN INSERT *`) — no old-value history is retained, which is exactly the Type 1 contract
- This is the direct, hands-on counterpart to the `MERGE` pattern introduced in the SCD Theory notebook — proving the overwrite strategy with a real running `MERGE INTO` statement rather than just reading about it

```sql
MERGE INTO sales_new.DimProducts AS trg
USING sales_new.view_DimProducts AS src
ON trg.ProductID = src.ProductID
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
```
**Takeaway:** SCD Type 1 is the simplest of the three strategies, but implementing it correctly via `MERGE` (rather than a manual `DELETE` + `INSERT`) is exactly how it's done in real Delta Lake / Databricks pipelines — a small notebook that closes the loop between "I read about SCD" and "I ran a `MERGE` that does SCD."

---

## 🧠 Skills Demonstrated — Full Mastery Checklist

| Data Warehousing Domain | Demonstrated Through |
|---|---|
| ✅ Warehouse Fundamentals | DWH vs Data Warehousing, OLTP vs OLAP, ETL vs ELT, Medallion Architecture, full 55-section theory notebook |
| ✅ Formal Data Modeling | Conceptual → Logical → Physical modeling, applied down to real `CREATE TABLE` statements |
| ✅ Dimensional Modeling | Fact vs Dimension tables, Star vs Snowflake Schema, and *when* to choose each |
| ✅ Advanced Table Design | Transaction/Periodic/Accumulating fact tables; Conformed/Role-Playing/Junk/Degenerate dimensions |
| ✅ Change Management | All three SCD types (Theory) — implemented live with a Delta `MERGE` (Practical 3) |
| ✅ Real Pipeline Engineering | A working Staging → Transformation → Core pipeline with timestamp-based CDC (Practical 1) |
| ✅ Star Schema From Scratch | 4 Dimension tables + 1 Fact table, surrogate keys via `row_number()`, multi-way `LEFT JOIN`s in both SQL and PySpark (Practical 2) |
| ✅ Self-Debugging & Production Judgment | Caught a real copy-paste alias bug; identified missing `TRUNCATE`, missing watermark table, and `INSERT` vs `MERGE` semantics unprompted |

> **In short:** this repo isn't just "I read about data warehouses" — it's proof of having gone from the whiteboard definition of a Data Warehouse all the way down to writing the exact `MERGE` statement that implements SCD Type 1 on a real Delta table, catching your own bugs along the way. **This person has mastered data warehousing — from theory to a working, dimensionally-modeled, incrementally-loaded warehouse.**

---

## ▶️ How to Run

### Prerequisites
- Databricks Workspace with a running cluster (Delta Lake enabled)
- No external datasets required — every practical creates its own source data via `INSERT INTO ... VALUES`

### Steps
1. Import each `.py` / `.sql` notebook into your Databricks workspace
2. Run in this order for the cleanest learning path:
   - `Data Warehousing Theory.py` → `Data Modeling Theory.py` → `Types of Fact and Dim Table Theory.py` → `SCD Types Theory.py`
   - `DWH Practical Part1 - Incremental Loading.py` → `DWH Practical Part2 - Data Warehouse Modeling.sql` → `DWH Practical 3 - Implementing SCD Type 1.sql`
3. Each practical creates its own databases (`sales`, `salesDWH`, `orderDWH`, `sales_new`) — safe to run independently in a fresh workspace
4. Use `SELECT * FROM <table>` after each `COMMAND` cell to see the data evolve exactly as described in the write-ups above

---

## 📂 Repository Structure

```
Data-Warehouse-Ultimate-Guide/
├── Data_Warehousing_Theory.py                       → Full DWH foundation: OLTP/OLAP, architecture, ETL/ELT, Medallion, governance (55 sections)
├── Data_Modeling_Theory.py                          → Conceptual/Logical/Physical modeling + Dimensional Modeling + Star/Snowflake
├── Types_of_Fact_and_Dim_Table_Theory.py             → Transaction/Snapshot/Accumulating facts + Conformed/Role-Playing/Junk/Degenerate dims
├── SCD_Types_Theory.py                               → SCD Type 1, Type 2, Type 3 — theory and decision framework
├── DWH_Practical_Part1_-_Incremental_Loading.py      → Hands-on: Staging → Transformation → Core pipeline with timestamp-based CDC
├── DWH_Practical_Part2_-_Data_Warehouse_Modeling.sql → Hands-on: Full Star Schema build — 4 Dims + FactSales with surrogate keys
└── DWH_Practical_3_-_Implementing_SCD_Type_1.sql     → Hands-on: SCD Type 1 via Delta Lake MERGE
```
