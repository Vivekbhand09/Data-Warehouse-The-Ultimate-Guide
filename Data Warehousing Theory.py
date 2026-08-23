# Databricks notebook source
# MAGIC %md
# MAGIC # Data Warehouse and Data Warehousing --- Complete Guide
# MAGIC
# MAGIC ## 1. What is a Data Warehouse?
# MAGIC
# MAGIC A **Data Warehouse (DWH)** is a centralized system used to collect,
# MAGIC integrate, store, organize, and analyze data from multiple sources.
# MAGIC
# MAGIC Its main purpose is to provide reliable, historical, integrated data
# MAGIC for:
# MAGIC
# MAGIC -   Reporting
# MAGIC -   Business Intelligence (BI)
# MAGIC -   Analytics
# MAGIC -   Trend analysis
# MAGIC -   Decision-making
# MAGIC
# MAGIC Simple architecture:
# MAGIC
# MAGIC ``` text
# MAGIC Source Systems
# MAGIC      |
# MAGIC      +---- Database
# MAGIC      +---- API
# MAGIC      +---- CSV / JSON
# MAGIC      +---- CRM / ERP
# MAGIC      |
# MAGIC      v
# MAGIC ETL / ELT
# MAGIC      |
# MAGIC      v
# MAGIC Data Warehouse
# MAGIC      |
# MAGIC      +---- Reports
# MAGIC      +---- Dashboards
# MAGIC      +---- Analytics
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC ## 2. Why Do We Need a Data Warehouse?
# MAGIC
# MAGIC Organizations usually have many operational systems:
# MAGIC
# MAGIC ``` text
# MAGIC E-commerce System
# MAGIC        |
# MAGIC Customer Database
# MAGIC        |
# MAGIC Payment System
# MAGIC        |
# MAGIC Inventory System
# MAGIC        |
# MAGIC CRM
# MAGIC ```
# MAGIC
# MAGIC The data may have different formats, structures, and definitions.
# MAGIC
# MAGIC Problems without a warehouse:
# MAGIC
# MAGIC -   Data is scattered across systems.
# MAGIC -   Historical analysis is difficult.
# MAGIC -   Different systems may use different definitions.
# MAGIC -   Large analytical queries can affect production databases.
# MAGIC -   Reporting becomes complicated.
# MAGIC -   Data quality and governance become harder to manage.
# MAGIC
# MAGIC A data warehouse brings data together into a centralized analytical
# MAGIC environment.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC ## 3. Example
# MAGIC
# MAGIC Suppose a retail company has:
# MAGIC
# MAGIC ``` text
# MAGIC MySQL       → Customers
# MAGIC PostgreSQL  → Orders
# MAGIC CSV         → Products
# MAGIC API         → Payments
# MAGIC CRM         → Customer interactions
# MAGIC ```
# MAGIC
# MAGIC A pipeline can integrate them:
# MAGIC
# MAGIC ``` text
# MAGIC MySQL --------PostgreSQL ----CSV ------------> ETL / ELT ---> Data Warehouse
# MAGIC API ------------/
# MAGIC CRM ------------/
# MAGIC ```
# MAGIC
# MAGIC Now an analyst can ask:
# MAGIC
# MAGIC ``` text
# MAGIC What were total sales by product category,
# MAGIC country, and month?
# MAGIC ```
# MAGIC
# MAGIC from one analytical environment.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 4. Data Warehouse vs Data Warehousing
# MAGIC
# MAGIC These terms are related but different.
# MAGIC
# MAGIC ## Data Warehouse
# MAGIC
# MAGIC The **actual analytical repository/system** where integrated data is
# MAGIC stored.
# MAGIC
# MAGIC ## Data Warehousing
# MAGIC
# MAGIC The **complete process, architecture, and practices** used to:
# MAGIC
# MAGIC -   Extract data
# MAGIC -   Ingest data
# MAGIC -   Clean data
# MAGIC -   Transform data
# MAGIC -   Integrate data
# MAGIC -   Store data
# MAGIC -   Govern data
# MAGIC -   Serve data for analytics
# MAGIC
# MAGIC Easy way to remember:
# MAGIC
# MAGIC ``` text
# MAGIC Data Warehouse
# MAGIC = The destination / analytical repository
# MAGIC
# MAGIC Data Warehousing
# MAGIC = The complete process and architecture around it
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 5. Characteristics of a Traditional Data Warehouse
# MAGIC
# MAGIC Classic data warehouse concepts describe four major characteristics.
# MAGIC
# MAGIC ## Subject-Oriented
# MAGIC
# MAGIC Data is organized around business subjects:
# MAGIC
# MAGIC ``` text
# MAGIC Customers
# MAGIC Products
# MAGIC Sales
# MAGIC Orders
# MAGIC Payments
# MAGIC ```
# MAGIC
# MAGIC ## Integrated
# MAGIC
# MAGIC Data from different systems is standardized.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC System A → USA
# MAGIC System B → US
# MAGIC System C → United States
# MAGIC ```
# MAGIC
# MAGIC The warehouse can standardize these to:
# MAGIC
# MAGIC ``` text
# MAGIC USA
# MAGIC ```
# MAGIC
# MAGIC ## Time-Variant
# MAGIC
# MAGIC A warehouse generally maintains historical information.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Product Price
# MAGIC
# MAGIC 2024 → $100
# MAGIC 2025 → $110
# MAGIC 2026 → $125
# MAGIC ```
# MAGIC
# MAGIC This allows historical analysis.
# MAGIC
# MAGIC ## Non-Volatile
# MAGIC
# MAGIC Traditional warehouse data is primarily used for analytical reads and
# MAGIC controlled loads rather than constant transactional updates.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 6. OLTP vs OLAP
# MAGIC
# MAGIC This is one of the most important data warehousing concepts.
# MAGIC
# MAGIC ## OLTP
# MAGIC
# MAGIC **OLTP = Online Transaction Processing**
# MAGIC
# MAGIC Used for day-to-day operations.
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Place an order
# MAGIC Make a payment
# MAGIC Create a customer
# MAGIC Update inventory
# MAGIC Book a ticket
# MAGIC ```
# MAGIC
# MAGIC Typical systems include:
# MAGIC
# MAGIC ``` text
# MAGIC MySQL
# MAGIC PostgreSQL
# MAGIC Oracle
# MAGIC SQL Server
# MAGIC ```
# MAGIC
# MAGIC ## OLAP
# MAGIC
# MAGIC **OLAP = Online Analytical Processing**
# MAGIC
# MAGIC Used for analysis.
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Total sales by month
# MAGIC Sales by country
# MAGIC Top-selling products
# MAGIC Customer lifetime value
# MAGIC Year-over-year growth
# MAGIC ```
# MAGIC
# MAGIC A data warehouse is primarily designed for OLAP workloads.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC ## OLTP vs OLAP
# MAGIC
# MAGIC   Feature        OLTP                       OLAP / Data Warehouse
# MAGIC   -------------- -------------------------- --------------------------
# MAGIC   Purpose        Transactions               Analytics
# MAGIC   Data           Operational/current        Historical + integrated
# MAGIC   Queries        Small and frequent         Large and complex
# MAGIC   Operations     INSERT / UPDATE / DELETE   Mostly analytical reads
# MAGIC   Users          Applications/end users     Analysts/BI/data teams
# MAGIC   Optimization   Transaction speed          Analytical query speed
# MAGIC   History        Usually limited            Usually extensive
# MAGIC   Example        Place an order             Analyze 5 years of sales
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 7. Typical Data Warehouse Architecture
# MAGIC
# MAGIC ``` text
# MAGIC                     DATA SOURCES
# MAGIC                          |
# MAGIC         +----------------+----------------+
# MAGIC         |                |                |
# MAGIC        DB               API             Files
# MAGIC         |                |                |
# MAGIC         +----------------+----------------+
# MAGIC                          |
# MAGIC                          v
# MAGIC                   DATA INGESTION
# MAGIC                          |
# MAGIC                          v
# MAGIC                   RAW / STAGING
# MAGIC                          |
# MAGIC                          v
# MAGIC                 CLEAN + VALIDATE
# MAGIC                          |
# MAGIC                          v
# MAGIC                     TRANSFORM
# MAGIC                          |
# MAGIC                          v
# MAGIC                  DATA WAREHOUSE
# MAGIC                          |
# MAGIC              +-----------+-----------+
# MAGIC              |           |           |
# MAGIC              v           v           v
# MAGIC             BI        Reports     Analytics
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 8. Data Sources
# MAGIC
# MAGIC Data warehouses can receive data from:
# MAGIC
# MAGIC ### Databases
# MAGIC
# MAGIC ``` text
# MAGIC MySQL
# MAGIC PostgreSQL
# MAGIC Oracle
# MAGIC SQL Server
# MAGIC ```
# MAGIC
# MAGIC ### Files
# MAGIC
# MAGIC ``` text
# MAGIC CSV
# MAGIC JSON
# MAGIC Parquet
# MAGIC XML
# MAGIC Excel
# MAGIC ```
# MAGIC
# MAGIC ### Applications
# MAGIC
# MAGIC ``` text
# MAGIC CRM
# MAGIC ERP
# MAGIC E-commerce
# MAGIC Marketing systems
# MAGIC Payment systems
# MAGIC ```
# MAGIC
# MAGIC ### APIs
# MAGIC
# MAGIC ``` text
# MAGIC REST APIs
# MAGIC SaaS APIs
# MAGIC Third-party services
# MAGIC ```
# MAGIC
# MAGIC ### Streaming Systems
# MAGIC
# MAGIC ``` text
# MAGIC Kafka
# MAGIC Event Hubs
# MAGIC Kinesis
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 9. Data Ingestion
# MAGIC
# MAGIC **Data ingestion** is the process of moving data from source systems
# MAGIC into the analytical platform.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC MySQL
# MAGIC   |
# MAGIC   v
# MAGIC Ingestion
# MAGIC   |
# MAGIC   v
# MAGIC Raw Storage
# MAGIC ```
# MAGIC
# MAGIC Or:
# MAGIC
# MAGIC ``` text
# MAGIC API
# MAGIC  |
# MAGIC  v
# MAGIC Ingestion Pipeline
# MAGIC  |
# MAGIC  v
# MAGIC Data Warehouse
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 10. ETL
# MAGIC
# MAGIC **ETL = Extract, Transform, Load**
# MAGIC
# MAGIC ``` text
# MAGIC Extract
# MAGIC    |
# MAGIC    v
# MAGIC Transform
# MAGIC    |
# MAGIC    v
# MAGIC Load
# MAGIC ```
# MAGIC
# MAGIC ### Extract
# MAGIC
# MAGIC Read data from sources.
# MAGIC
# MAGIC ``` text
# MAGIC Database
# MAGIC CSV
# MAGIC API
# MAGIC CRM
# MAGIC ```
# MAGIC
# MAGIC ### Transform
# MAGIC
# MAGIC Clean and modify data.
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Remove duplicates
# MAGIC Convert data types
# MAGIC Handle nulls
# MAGIC Standardize values
# MAGIC Join data
# MAGIC Calculate columns
# MAGIC ```
# MAGIC
# MAGIC ### Load
# MAGIC
# MAGIC Load transformed data into the warehouse.
# MAGIC
# MAGIC ``` text
# MAGIC Source
# MAGIC   |
# MAGIC Extract
# MAGIC   |
# MAGIC Transform
# MAGIC   |
# MAGIC Load
# MAGIC   |
# MAGIC Warehouse
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 11. ELT
# MAGIC
# MAGIC **ELT = Extract, Load, Transform**
# MAGIC
# MAGIC ``` text
# MAGIC Extract
# MAGIC    |
# MAGIC    v
# MAGIC Load
# MAGIC    |
# MAGIC    v
# MAGIC Transform
# MAGIC ```
# MAGIC
# MAGIC Raw data is loaded first, and transformations are performed inside the
# MAGIC target analytical platform.
# MAGIC
# MAGIC This is common in modern cloud data platforms because they provide
# MAGIC scalable compute.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 12. ETL vs ELT
# MAGIC
# MAGIC   -----------------------------------------------------------------------
# MAGIC   ETL                                 ELT
# MAGIC   ----------------------------------- -----------------------------------
# MAGIC   Extract                             Extract
# MAGIC
# MAGIC   Transform before loading            Load before transforming
# MAGIC
# MAGIC   Load transformed data               Transform in target platform
# MAGIC
# MAGIC   Traditional approach                Common modern approach
# MAGIC
# MAGIC   External ETL engine often used      Warehouse/lakehouse often performs
# MAGIC                                       transformations
# MAGIC   -----------------------------------------------------------------------
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 13. Staging Area
# MAGIC
# MAGIC A **staging area** is an intermediate location where source data can be
# MAGIC stored before final transformation and loading.
# MAGIC
# MAGIC ``` text
# MAGIC Source
# MAGIC   |
# MAGIC   v
# MAGIC Staging
# MAGIC   |
# MAGIC   v
# MAGIC Validation / Cleaning
# MAGIC   |
# MAGIC   v
# MAGIC Warehouse
# MAGIC ```
# MAGIC
# MAGIC Staging can help with:
# MAGIC
# MAGIC -   Raw ingestion
# MAGIC -   Validation
# MAGIC -   Error handling
# MAGIC -   Reprocessing
# MAGIC -   Decoupling source systems from transformations
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 14. Raw, Clean, and Curated Layers
# MAGIC
# MAGIC A common architecture is:
# MAGIC
# MAGIC ``` text
# MAGIC Raw
# MAGIC  |
# MAGIC  v
# MAGIC Clean
# MAGIC  |
# MAGIC  v
# MAGIC Curated
# MAGIC ```
# MAGIC
# MAGIC ### Raw
# MAGIC
# MAGIC Data close to the source.
# MAGIC
# MAGIC ``` text
# MAGIC Raw orders
# MAGIC Raw customers
# MAGIC Raw API responses
# MAGIC ```
# MAGIC
# MAGIC ### Clean
# MAGIC
# MAGIC Data that has been standardized and validated.
# MAGIC
# MAGIC ``` text
# MAGIC Correct data types
# MAGIC Duplicates handled
# MAGIC Standardized values
# MAGIC Null handling
# MAGIC ```
# MAGIC
# MAGIC ### Curated
# MAGIC
# MAGIC Business-ready data.
# MAGIC
# MAGIC ``` text
# MAGIC Sales summary
# MAGIC Customer dimension
# MAGIC Product dimension
# MAGIC Monthly revenue
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 15. Fact Tables
# MAGIC
# MAGIC A **fact table** stores measurable business events.
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Sales
# MAGIC Orders
# MAGIC Payments
# MAGIC Shipments
# MAGIC Transactions
# MAGIC ```
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC fact_sales
# MAGIC
# MAGIC sale_id
# MAGIC customer_id
# MAGIC product_id
# MAGIC date_id
# MAGIC quantity
# MAGIC sales_amount
# MAGIC discount
# MAGIC ```
# MAGIC
# MAGIC Typical measures include:
# MAGIC
# MAGIC ``` text
# MAGIC quantity
# MAGIC sales_amount
# MAGIC discount
# MAGIC cost
# MAGIC profit
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 16. Dimension Tables
# MAGIC
# MAGIC A **dimension table** stores descriptive information about business
# MAGIC entities.
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Customer
# MAGIC Product
# MAGIC Date
# MAGIC Store
# MAGIC Location
# MAGIC ```
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC dim_customer
# MAGIC
# MAGIC customer_id
# MAGIC customer_name
# MAGIC city
# MAGIC country
# MAGIC segment
# MAGIC ```
# MAGIC
# MAGIC A fact table tells us **what happened**.
# MAGIC
# MAGIC A dimension tells us **who, what, where, or when** it happened.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 17. Star Schema
# MAGIC
# MAGIC A star schema contains a central fact table surrounded by dimension
# MAGIC tables.
# MAGIC
# MAGIC ``` text
# MAGIC                  dim_customer
# MAGIC                       |
# MAGIC                       |
# MAGIC dim_product ---- fact_sales ---- dim_date
# MAGIC                       |
# MAGIC                       |
# MAGIC                   dim_store
# MAGIC ```
# MAGIC
# MAGIC The fact table contains measurements and foreign keys.
# MAGIC
# MAGIC Dimensions provide descriptive context.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 18. Snowflake Schema
# MAGIC
# MAGIC A snowflake schema normalizes dimensions into additional tables.
# MAGIC
# MAGIC ``` text
# MAGIC                  dim_customer
# MAGIC                       |
# MAGIC                   dim_city
# MAGIC                       |
# MAGIC                  dim_country
# MAGIC
# MAGIC dim_product ---- fact_sales ---- dim_date
# MAGIC ```
# MAGIC
# MAGIC Compared with star schema, it usually has more normalized dimensions and
# MAGIC therefore potentially more joins.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 19. Star vs Snowflake
# MAGIC
# MAGIC   Feature            Star Schema         Snowflake Schema
# MAGIC   ------------------ ------------------- -----------------------------------
# MAGIC   Dimensions         More denormalized   More normalized
# MAGIC   Joins              Usually fewer       Usually more
# MAGIC   Query simplicity   Easier              More complex
# MAGIC   Redundancy         Higher              Lower
# MAGIC   BI usage           Very common         Used when normalization is useful
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 20. Measures and Dimensions
# MAGIC
# MAGIC A **measure** is a value that can be aggregated.
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Sales Amount
# MAGIC Quantity
# MAGIC Profit
# MAGIC Discount
# MAGIC Cost
# MAGIC ```
# MAGIC
# MAGIC A **dimension attribute** describes the context.
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Product Category
# MAGIC Country
# MAGIC Customer
# MAGIC Month
# MAGIC Store
# MAGIC ```
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` sql
# MAGIC SELECT
# MAGIC     product_category,
# MAGIC     SUM(sales_amount)
# MAGIC FROM fact_sales
# MAGIC GROUP BY product_category;
# MAGIC ```
# MAGIC
# MAGIC Here:
# MAGIC
# MAGIC ``` text
# MAGIC product_category = Dimension
# MAGIC
# MAGIC sales_amount = Measure
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 21. Surrogate Key
# MAGIC
# MAGIC A **surrogate key** is a warehouse-generated identifier.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC customer_sk = 101
# MAGIC ```
# MAGIC
# MAGIC while the source system may use:
# MAGIC
# MAGIC ``` text
# MAGIC customer_id = CUST001
# MAGIC ```
# MAGIC
# MAGIC Surrogate keys are useful for:
# MAGIC
# MAGIC -   Managing historical dimension versions
# MAGIC -   Integrating multiple sources
# MAGIC -   Avoiding dependence on source-system identifiers
# MAGIC -   Simplifying dimensional relationships
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 22. Natural Key vs Surrogate Key
# MAGIC
# MAGIC ### Natural Key
# MAGIC
# MAGIC Comes from the business/source system.
# MAGIC
# MAGIC ``` text
# MAGIC customer_id = CUST001
# MAGIC ```
# MAGIC
# MAGIC ### Surrogate Key
# MAGIC
# MAGIC Generated by the warehouse.
# MAGIC
# MAGIC ``` text
# MAGIC customer_sk = 101
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 23. Slowly Changing Dimensions
# MAGIC
# MAGIC Dimension attributes can change over time.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Customer 101
# MAGIC City = Mumbai
# MAGIC ```
# MAGIC
# MAGIC Later:
# MAGIC
# MAGIC ``` text
# MAGIC City = Delhi
# MAGIC ```
# MAGIC
# MAGIC The warehouse needs a strategy for handling the change.
# MAGIC
# MAGIC This is called **Slowly Changing Dimension (SCD)**.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 24. SCD Type 1
# MAGIC
# MAGIC Type 1 overwrites the old value.
# MAGIC
# MAGIC Before:
# MAGIC
# MAGIC ``` text
# MAGIC Customer 101 → Mumbai
# MAGIC ```
# MAGIC
# MAGIC After:
# MAGIC
# MAGIC ``` text
# MAGIC Customer 101 → Delhi
# MAGIC ```
# MAGIC
# MAGIC The old value is not retained.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 25. SCD Type 2
# MAGIC
# MAGIC Type 2 preserves history by creating a new version.
# MAGIC
# MAGIC Before:
# MAGIC
# MAGIC ``` text
# MAGIC Customer 101 | Mumbai | 2025-01-01 | 9999-12-31 | Y
# MAGIC ```
# MAGIC
# MAGIC After the customer moves:
# MAGIC
# MAGIC ``` text
# MAGIC Customer 101 | Mumbai | 2025-01-01 | 2026-05-10 | N
# MAGIC Customer 101 | Delhi  | 2026-05-10 | 9999-12-31 | Y
# MAGIC ```
# MAGIC
# MAGIC Now historical reporting can determine which city was valid at a
# MAGIC particular time.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 26. Why SCD Type 2 Is Important
# MAGIC
# MAGIC Without history:
# MAGIC
# MAGIC ``` text
# MAGIC Customer → Delhi
# MAGIC ```
# MAGIC
# MAGIC You may not know that the customer was previously in Mumbai.
# MAGIC
# MAGIC With SCD Type 2:
# MAGIC
# MAGIC ``` text
# MAGIC 2025 → Mumbai
# MAGIC 2026 → Delhi
# MAGIC ```
# MAGIC
# MAGIC This supports historical reporting and trend analysis.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 27. Full Load vs Incremental Load
# MAGIC
# MAGIC ## Full Load
# MAGIC
# MAGIC Load all source data.
# MAGIC
# MAGIC ``` text
# MAGIC Source
# MAGIC   |
# MAGIC   v
# MAGIC Read everything
# MAGIC   |
# MAGIC   v
# MAGIC Warehouse
# MAGIC ```
# MAGIC
# MAGIC Useful for:
# MAGIC
# MAGIC -   Initial loads
# MAGIC -   Small datasets
# MAGIC -   Full rebuilds
# MAGIC
# MAGIC ## Incremental Load
# MAGIC
# MAGIC Load only new or changed records.
# MAGIC
# MAGIC ``` text
# MAGIC Existing Warehouse
# MAGIC        +
# MAGIC New/Changed Records
# MAGIC        |
# MAGIC        v
# MAGIC Updated Warehouse
# MAGIC ```
# MAGIC
# MAGIC This is generally more efficient for large datasets.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 28. CDC
# MAGIC
# MAGIC **CDC = Change Data Capture**
# MAGIC
# MAGIC CDC captures changes in source systems.
# MAGIC
# MAGIC Typical changes:
# MAGIC
# MAGIC ``` text
# MAGIC INSERT
# MAGIC UPDATE
# MAGIC DELETE
# MAGIC ```
# MAGIC
# MAGIC Instead of extracting the entire source repeatedly:
# MAGIC
# MAGIC ``` text
# MAGIC Source Database
# MAGIC       |
# MAGIC       v
# MAGIC      CDC
# MAGIC       |
# MAGIC       v
# MAGIC Only changed records
# MAGIC       |
# MAGIC       v
# MAGIC Warehouse
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 29. Batch vs Streaming
# MAGIC
# MAGIC ## Batch
# MAGIC
# MAGIC Process data periodically.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Every night at 2 AM
# MAGIC ```
# MAGIC
# MAGIC ``` text
# MAGIC Source
# MAGIC   |
# MAGIC   v
# MAGIC Daily Batch
# MAGIC   |
# MAGIC   v
# MAGIC Warehouse
# MAGIC ```
# MAGIC
# MAGIC ## Streaming
# MAGIC
# MAGIC Process events continuously or near real time.
# MAGIC
# MAGIC ``` text
# MAGIC Event
# MAGIC   |
# MAGIC   v
# MAGIC Streaming Pipeline
# MAGIC   |
# MAGIC   v
# MAGIC Processing
# MAGIC   |
# MAGIC   v
# MAGIC Analytics
# MAGIC ```
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Fraud detection
# MAGIC Real-time dashboards
# MAGIC IoT monitoring
# MAGIC Clickstream analytics
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 30. Data Warehouse vs Data Lake
# MAGIC
# MAGIC ## Data Warehouse
# MAGIC
# MAGIC Primarily designed for curated analytical data.
# MAGIC
# MAGIC ``` text
# MAGIC Structured
# MAGIC    |
# MAGIC Cleaned
# MAGIC    |
# MAGIC Business-ready
# MAGIC ```
# MAGIC
# MAGIC ## Data Lake
# MAGIC
# MAGIC Can store large volumes of raw data in many formats.
# MAGIC
# MAGIC ``` text
# MAGIC CSV
# MAGIC JSON
# MAGIC Parquet
# MAGIC Logs
# MAGIC Images
# MAGIC Video
# MAGIC ```
# MAGIC
# MAGIC Simple memory trick:
# MAGIC
# MAGIC ``` text
# MAGIC Data Lake
# MAGIC = Flexible/raw large-scale storage
# MAGIC
# MAGIC Data Warehouse
# MAGIC = Curated analytical storage
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 31. Data Lakehouse
# MAGIC
# MAGIC A **Data Lakehouse** combines many capabilities of data lakes and data
# MAGIC warehouses.
# MAGIC
# MAGIC ``` text
# MAGIC Data Lake
# MAGIC     +
# MAGIC Warehouse capabilities
# MAGIC     |
# MAGIC     v
# MAGIC Lakehouse
# MAGIC ```
# MAGIC
# MAGIC Typical capabilities can include:
# MAGIC
# MAGIC -   Object storage
# MAGIC -   ACID transactions
# MAGIC -   Schema enforcement
# MAGIC -   Time travel
# MAGIC -   SQL analytics
# MAGIC -   BI
# MAGIC -   Data engineering
# MAGIC -   Machine learning
# MAGIC -   Governance
# MAGIC
# MAGIC Examples of lakehouse technologies include:
# MAGIC
# MAGIC ``` text
# MAGIC Delta Lake
# MAGIC Apache Iceberg
# MAGIC Apache Hudi
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 32. Data Warehouse vs Data Lake vs Lakehouse
# MAGIC
# MAGIC   Feature                Data Warehouse       Data Lake      Data Lakehouse
# MAGIC   ---------------------- -------------------- -------------- ----------------
# MAGIC   Raw data               Limited              Strong         Strong
# MAGIC   Structured analytics   Strong               Possible       Strong
# MAGIC   BI                     Strong               Possible       Strong
# MAGIC   ACID tables            Platform-dependent   Not inherent   Strong
# MAGIC   ML/Data Science        Possible             Strong         Strong
# MAGIC   Object storage         Not required         Strong         Strong
# MAGIC   Curated data           Strong               Possible       Strong
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 33. MPP
# MAGIC
# MAGIC Many analytical systems use **MPP**.
# MAGIC
# MAGIC **MPP = Massively Parallel Processing**
# MAGIC
# MAGIC Instead of one machine processing everything, the workload is
# MAGIC distributed.
# MAGIC
# MAGIC ``` text
# MAGIC                 Query
# MAGIC                   |
# MAGIC        +----------+----------+
# MAGIC        |          |          |
# MAGIC        v          v          v
# MAGIC     Node 1      Node 2     Node 3
# MAGIC        |          |          |
# MAGIC        v          v          v
# MAGIC    Partition   Partition  Partition
# MAGIC        \          |          /
# MAGIC         +---------+---------+
# MAGIC                   |
# MAGIC                 Result
# MAGIC ```
# MAGIC
# MAGIC This allows large analytical workloads to execute in parallel.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 34. Why Parallel Processing Matters
# MAGIC
# MAGIC Suppose the system has 1 TB of data.
# MAGIC
# MAGIC Instead of:
# MAGIC
# MAGIC ``` text
# MAGIC One machine
# MAGIC     |
# MAGIC     v
# MAGIC 1 TB
# MAGIC ```
# MAGIC
# MAGIC the workload can be distributed:
# MAGIC
# MAGIC ``` text
# MAGIC Node 1 → 250 GB
# MAGIC Node 2 → 250 GB
# MAGIC Node 3 → 250 GB
# MAGIC Node 4 → 250 GB
# MAGIC ```
# MAGIC
# MAGIC The nodes can process their portions in parallel.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 35. Data Warehouse Performance
# MAGIC
# MAGIC Common techniques include:
# MAGIC
# MAGIC ## Partitioning
# MAGIC
# MAGIC Divide data into logical partitions.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC sales/
# MAGIC   year=2024/
# MAGIC   year=2025/
# MAGIC   year=2026/
# MAGIC ```
# MAGIC
# MAGIC A query for 2026 may only need the 2026 partition.
# MAGIC
# MAGIC ## Clustering / Sorting
# MAGIC
# MAGIC Organize data around frequently queried columns.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC customer_id
# MAGIC order_date
# MAGIC ```
# MAGIC
# MAGIC The exact implementation depends on the platform.
# MAGIC
# MAGIC ## Materialized Views
# MAGIC
# MAGIC Precompute and store expensive query results.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Monthly Sales
# MAGIC ```
# MAGIC
# MAGIC Instead of recalculating a costly aggregation for every request.
# MAGIC
# MAGIC ## Query Optimization
# MAGIC
# MAGIC Warehouses may use:
# MAGIC
# MAGIC ``` text
# MAGIC Predicate pushdown
# MAGIC Column pruning
# MAGIC Partition pruning
# MAGIC Join optimization
# MAGIC Data skipping
# MAGIC Caching
# MAGIC Parallel execution
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 36. Partition Pruning
# MAGIC
# MAGIC Suppose data is partitioned by year:
# MAGIC
# MAGIC ``` text
# MAGIC year=2024
# MAGIC year=2025
# MAGIC year=2026
# MAGIC ```
# MAGIC
# MAGIC Query:
# MAGIC
# MAGIC ``` sql
# MAGIC SELECT *
# MAGIC FROM sales
# MAGIC WHERE year = 2026;
# MAGIC ```
# MAGIC
# MAGIC The engine may only read:
# MAGIC
# MAGIC ``` text
# MAGIC year=2026
# MAGIC ```
# MAGIC
# MAGIC instead of scanning all years.
# MAGIC
# MAGIC ``` text
# MAGIC 2024 → Skip
# MAGIC 2025 → Skip
# MAGIC 2026 → Read
# MAGIC ```
# MAGIC
# MAGIC This reduces data scanned and can improve performance.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 37. Data Quality
# MAGIC
# MAGIC Data warehouses need strong data quality.
# MAGIC
# MAGIC Common checks:
# MAGIC
# MAGIC ### Null checks
# MAGIC
# MAGIC ``` text
# MAGIC customer_id should not be NULL
# MAGIC ```
# MAGIC
# MAGIC ### Duplicate checks
# MAGIC
# MAGIC ``` text
# MAGIC customer_id should be unique
# MAGIC ```
# MAGIC
# MAGIC ### Data type checks
# MAGIC
# MAGIC ``` text
# MAGIC price should be numeric
# MAGIC ```
# MAGIC
# MAGIC ### Referential integrity
# MAGIC
# MAGIC ``` text
# MAGIC fact_sales.product_id
# MAGIC        |
# MAGIC        v
# MAGIC must exist in dim_product
# MAGIC ```
# MAGIC
# MAGIC ### Business rules
# MAGIC
# MAGIC ``` text
# MAGIC quantity > 0
# MAGIC sales_amount >= 0
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 38. Data Governance
# MAGIC
# MAGIC **Data governance** defines how data is managed and controlled.
# MAGIC
# MAGIC It includes:
# MAGIC
# MAGIC ``` text
# MAGIC Data ownership
# MAGIC Data quality
# MAGIC Security
# MAGIC Privacy
# MAGIC Access control
# MAGIC Compliance
# MAGIC Metadata
# MAGIC Lineage
# MAGIC Retention
# MAGIC ```
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Analyst
# MAGIC   |
# MAGIC   v
# MAGIC Can access sales data
# MAGIC
# MAGIC Finance
# MAGIC   |
# MAGIC   v
# MAGIC Can access financial details
# MAGIC
# MAGIC Regional Manager
# MAGIC   |
# MAGIC   v
# MAGIC Can access only permitted regions
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 39. Data Security
# MAGIC
# MAGIC A data warehouse can use:
# MAGIC
# MAGIC -   Role-based access control
# MAGIC -   Row-level security
# MAGIC -   Column-level security
# MAGIC -   Data masking
# MAGIC -   Encryption
# MAGIC -   Auditing
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Admin
# MAGIC   ↓
# MAGIC Full customer email
# MAGIC
# MAGIC Analyst
# MAGIC   ↓
# MAGIC Masked customer email
# MAGIC ```
# MAGIC
# MAGIC Row-level security can also restrict:
# MAGIC
# MAGIC ``` text
# MAGIC User A → India rows
# MAGIC User B → USA rows
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 40. Metadata
# MAGIC
# MAGIC **Metadata means data about data.**
# MAGIC
# MAGIC Examples:
# MAGIC
# MAGIC ``` text
# MAGIC Table name
# MAGIC Column name
# MAGIC Data type
# MAGIC Description
# MAGIC Owner
# MAGIC Source
# MAGIC Last updated time
# MAGIC Lineage
# MAGIC ```
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Table: fact_sales
# MAGIC
# MAGIC Column: sales_amount
# MAGIC Type: DECIMAL
# MAGIC Source: ERP
# MAGIC Description: Total sales amount
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 41. Data Lineage
# MAGIC
# MAGIC Data lineage tells us where data came from and how it was transformed.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC ERP
# MAGIC  |
# MAGIC  v
# MAGIC Raw Orders
# MAGIC  |
# MAGIC  v
# MAGIC Clean Orders
# MAGIC  |
# MAGIC  v
# MAGIC fact_sales
# MAGIC  |
# MAGIC  v
# MAGIC Sales Dashboard
# MAGIC ```
# MAGIC
# MAGIC If a dashboard has an incorrect number, lineage helps trace the data
# MAGIC backward.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 42. Data Mart
# MAGIC
# MAGIC A **Data Mart** is a smaller analytical store focused on a particular
# MAGIC business area.
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC Enterprise Data Warehouse
# MAGIC           |
# MAGIC      +----+----+----+
# MAGIC      |         |    |
# MAGIC      v         v    v
# MAGIC    Sales      HR  Finance
# MAGIC    Mart       Mart  Mart
# MAGIC ```
# MAGIC
# MAGIC A sales mart may contain:
# MAGIC
# MAGIC ``` text
# MAGIC Sales
# MAGIC Products
# MAGIC Customers
# MAGIC Revenue
# MAGIC Orders
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 43. Enterprise Data Warehouse
# MAGIC
# MAGIC An **Enterprise Data Warehouse (EDW)** is a centralized warehouse
# MAGIC designed to support multiple areas of an organization.
# MAGIC
# MAGIC ``` text
# MAGIC                   EDW
# MAGIC                    |
# MAGIC        +-----------+-----------+
# MAGIC        |           |           |
# MAGIC       Sales        HR       Finance
# MAGIC        |           |           |
# MAGIC       BI          BI          BI
# MAGIC ```
# MAGIC
# MAGIC The goal is to provide a consistent enterprise-wide view of data.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 44. Medallion Architecture
# MAGIC
# MAGIC A common modern data architecture is:
# MAGIC
# MAGIC ``` text
# MAGIC Bronze
# MAGIC    |
# MAGIC    v
# MAGIC Silver
# MAGIC    |
# MAGIC    v
# MAGIC Gold
# MAGIC ```
# MAGIC
# MAGIC ### Bronze
# MAGIC
# MAGIC Raw/source-like data.
# MAGIC
# MAGIC ### Silver
# MAGIC
# MAGIC Cleaned, validated, standardized data.
# MAGIC
# MAGIC ### Gold
# MAGIC
# MAGIC Business-ready data such as:
# MAGIC
# MAGIC ``` text
# MAGIC KPIs
# MAGIC Aggregations
# MAGIC Fact tables
# MAGIC Dimension tables
# MAGIC BI datasets
# MAGIC ```
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` text
# MAGIC CSV
# MAGIC  |
# MAGIC  v
# MAGIC Bronze
# MAGIC  |
# MAGIC  v
# MAGIC Clean Orders
# MAGIC  |
# MAGIC  v
# MAGIC Silver
# MAGIC  |
# MAGIC  v
# MAGIC Monthly Sales
# MAGIC  |
# MAGIC  v
# MAGIC Gold
# MAGIC  |
# MAGIC  v
# MAGIC Dashboard
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 45. End-to-End Retail Example
# MAGIC
# MAGIC Suppose a retail company has:
# MAGIC
# MAGIC ``` text
# MAGIC customers.csv
# MAGIC products.csv
# MAGIC orders.csv
# MAGIC payments.csv
# MAGIC ```
# MAGIC
# MAGIC ## Step 1 --- Ingestion
# MAGIC
# MAGIC ``` text
# MAGIC Files
# MAGIC   |
# MAGIC   v
# MAGIC Raw Storage
# MAGIC ```
# MAGIC
# MAGIC ## Step 2 --- Cleaning
# MAGIC
# MAGIC ``` text
# MAGIC Remove duplicates
# MAGIC Handle nulls
# MAGIC Correct data types
# MAGIC Standardize values
# MAGIC ```
# MAGIC
# MAGIC ## Step 3 --- Transformation
# MAGIC
# MAGIC Create:
# MAGIC
# MAGIC ``` text
# MAGIC dim_customer
# MAGIC dim_product
# MAGIC dim_date
# MAGIC fact_sales
# MAGIC ```
# MAGIC
# MAGIC ## Step 4 --- Load
# MAGIC
# MAGIC ``` text
# MAGIC Data Warehouse
# MAGIC ```
# MAGIC
# MAGIC ## Step 5 --- BI
# MAGIC
# MAGIC Dashboards can show:
# MAGIC
# MAGIC ``` text
# MAGIC Total Revenue
# MAGIC Monthly Sales
# MAGIC Top Products
# MAGIC Sales by Country
# MAGIC Customer Segments
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 46. Example Warehouse Data Model
# MAGIC
# MAGIC ### dim_customer
# MAGIC
# MAGIC ``` text
# MAGIC customer_sk
# MAGIC customer_id
# MAGIC customer_name
# MAGIC city
# MAGIC country
# MAGIC start_date
# MAGIC end_date
# MAGIC is_active
# MAGIC ```
# MAGIC
# MAGIC ### dim_product
# MAGIC
# MAGIC ``` text
# MAGIC product_sk
# MAGIC product_id
# MAGIC product_name
# MAGIC category
# MAGIC price
# MAGIC ```
# MAGIC
# MAGIC ### dim_date
# MAGIC
# MAGIC ``` text
# MAGIC date_sk
# MAGIC date
# MAGIC day
# MAGIC month
# MAGIC quarter
# MAGIC year
# MAGIC ```
# MAGIC
# MAGIC ### fact_sales
# MAGIC
# MAGIC ``` text
# MAGIC sales_id
# MAGIC customer_sk
# MAGIC product_sk
# MAGIC date_sk
# MAGIC quantity
# MAGIC sales_amount
# MAGIC discount
# MAGIC ```
# MAGIC
# MAGIC Relationship:
# MAGIC
# MAGIC ``` text
# MAGIC                  dim_customer
# MAGIC                       |
# MAGIC                       |
# MAGIC dim_product ---- fact_sales ---- dim_date
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 47. What Happens When a BI User Runs a Query?
# MAGIC
# MAGIC Example:
# MAGIC
# MAGIC ``` sql
# MAGIC SELECT
# MAGIC     d.year,
# MAGIC     p.category,
# MAGIC     SUM(f.sales_amount)
# MAGIC FROM fact_sales f
# MAGIC JOIN dim_date d
# MAGIC     ON f.date_sk = d.date_sk
# MAGIC JOIN dim_product p
# MAGIC     ON f.product_sk = p.product_sk
# MAGIC GROUP BY
# MAGIC     d.year,
# MAGIC     p.category;
# MAGIC ```
# MAGIC
# MAGIC Simplified flow:
# MAGIC
# MAGIC ``` text
# MAGIC BI Dashboard
# MAGIC       |
# MAGIC       v
# MAGIC SQL Query
# MAGIC       |
# MAGIC       v
# MAGIC Query Optimizer
# MAGIC       |
# MAGIC       v
# MAGIC Scan Relevant Data
# MAGIC       |
# MAGIC       v
# MAGIC Join
# MAGIC       |
# MAGIC       v
# MAGIC Aggregate
# MAGIC       |
# MAGIC       v
# MAGIC Result
# MAGIC       |
# MAGIC       v
# MAGIC Dashboard
# MAGIC ```
# MAGIC
# MAGIC The warehouse is designed to efficiently perform this kind of analytical
# MAGIC query.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 48. Data Warehouse vs Operational Database
# MAGIC
# MAGIC An operational database is optimized for transactions:
# MAGIC
# MAGIC ``` text
# MAGIC Customer places order
# MAGIC         |
# MAGIC         v
# MAGIC INSERT order
# MAGIC         |
# MAGIC         v
# MAGIC UPDATE inventory
# MAGIC ```
# MAGIC
# MAGIC A warehouse is optimized for analysis:
# MAGIC
# MAGIC ``` text
# MAGIC Analyze 5 years of sales
# MAGIC         |
# MAGIC         v
# MAGIC JOIN millions/billions of rows
# MAGIC         |
# MAGIC         v
# MAGIC GROUP BY month/product/region
# MAGIC         |
# MAGIC         v
# MAGIC Business Report
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 49. Benefits of a Data Warehouse
# MAGIC
# MAGIC ## Centralized Data
# MAGIC
# MAGIC Data from many systems can be accessed centrally.
# MAGIC
# MAGIC ## Historical Analysis
# MAGIC
# MAGIC Historical data can be retained for trends and comparisons.
# MAGIC
# MAGIC ## Better Reporting
# MAGIC
# MAGIC Provides consistent data for BI and reporting.
# MAGIC
# MAGIC ## Improved Analytical Performance
# MAGIC
# MAGIC Designed for complex analytical queries.
# MAGIC
# MAGIC ## Data Integration
# MAGIC
# MAGIC Combines multiple source systems.
# MAGIC
# MAGIC ## Data Quality
# MAGIC
# MAGIC Transformation and validation can standardize information.
# MAGIC
# MAGIC ## Governance
# MAGIC
# MAGIC Security, lineage, metadata, and access policies can be managed.
# MAGIC
# MAGIC ## Better Decision Making
# MAGIC
# MAGIC Provides trusted information for business decisions.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 50. Limitations / Challenges
# MAGIC
# MAGIC Depending on the architecture, challenges can include:
# MAGIC
# MAGIC -   ETL/ELT pipeline complexity
# MAGIC -   Data modeling complexity
# MAGIC -   Data quality issues
# MAGIC -   Cost management
# MAGIC -   Historical backfills
# MAGIC -   Schema changes
# MAGIC -   CDC complexity
# MAGIC -   Governance
# MAGIC -   Security
# MAGIC -   Integrating rapidly changing sources
# MAGIC -   Managing very large datasets
# MAGIC
# MAGIC Modern lakehouse and cloud architectures address some of these
# MAGIC challenges.
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 51. Complete Data Warehousing Pipeline
# MAGIC
# MAGIC ``` text
# MAGIC                          SOURCE SYSTEMS
# MAGIC                               |
# MAGIC               +---------------+---------------+
# MAGIC               |               |               |
# MAGIC              DB              API             Files
# MAGIC               |               |               |
# MAGIC               +---------------+---------------+
# MAGIC                               |
# MAGIC                               v
# MAGIC                          INGESTION
# MAGIC                               |
# MAGIC                               v
# MAGIC                         RAW / STAGING
# MAGIC                               |
# MAGIC                               v
# MAGIC                       DATA VALIDATION
# MAGIC                               |
# MAGIC                               v
# MAGIC                          TRANSFORM
# MAGIC                               |
# MAGIC                     +---------+---------+
# MAGIC                     |                   |
# MAGIC                     v                   v
# MAGIC               DIMENSION TABLES     FACT TABLES
# MAGIC                     |                   |
# MAGIC                     +---------+---------+
# MAGIC                               |
# MAGIC                               v
# MAGIC                        DATA WAREHOUSE
# MAGIC                               |
# MAGIC               +---------------+---------------+
# MAGIC               |               |               |
# MAGIC               v               v               v
# MAGIC              BI            Reports        Analytics
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 52. Most Important Concepts to Remember
# MAGIC
# MAGIC ``` text
# MAGIC Data Warehouse
# MAGIC     ↓
# MAGIC Centralized analytical repository
# MAGIC
# MAGIC Data Warehousing
# MAGIC     ↓
# MAGIC Complete process + architecture for building and using the warehouse
# MAGIC
# MAGIC OLTP
# MAGIC     ↓
# MAGIC Day-to-day transactions
# MAGIC
# MAGIC OLAP
# MAGIC     ↓
# MAGIC Analytics and reporting
# MAGIC
# MAGIC ETL
# MAGIC     ↓
# MAGIC Extract → Transform → Load
# MAGIC
# MAGIC ELT
# MAGIC     ↓
# MAGIC Extract → Load → Transform
# MAGIC
# MAGIC Fact Table
# MAGIC     ↓
# MAGIC Business events + measures
# MAGIC
# MAGIC Dimension Table
# MAGIC     ↓
# MAGIC Descriptive information
# MAGIC
# MAGIC Star Schema
# MAGIC     ↓
# MAGIC Fact surrounded by dimensions
# MAGIC
# MAGIC Snowflake Schema
# MAGIC     ↓
# MAGIC Normalized dimensions
# MAGIC
# MAGIC SCD Type 1
# MAGIC     ↓
# MAGIC Overwrite old value
# MAGIC
# MAGIC SCD Type 2
# MAGIC     ↓
# MAGIC Preserve historical versions
# MAGIC
# MAGIC CDC
# MAGIC     ↓
# MAGIC Capture source changes
# MAGIC
# MAGIC Partitioning
# MAGIC     ↓
# MAGIC Divide data for efficient access
# MAGIC
# MAGIC MPP
# MAGIC     ↓
# MAGIC Parallel processing across nodes
# MAGIC
# MAGIC Data Lake
# MAGIC     ↓
# MAGIC Flexible/raw large-scale storage
# MAGIC
# MAGIC Lakehouse
# MAGIC     ↓
# MAGIC Lake storage + warehouse-style analytical capabilities
# MAGIC ```
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 53. Interview Answer --- What is a Data Warehouse?
# MAGIC
# MAGIC > **A data warehouse is a centralized analytical data repository that
# MAGIC > integrates data from multiple source systems and stores structured,
# MAGIC > historical, and business-ready data for reporting, analytics, and
# MAGIC > decision-making. It is optimized for OLAP workloads such as large
# MAGIC > aggregations, joins, and historical analysis rather than day-to-day
# MAGIC > transactional processing.**
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 54. Interview Answer --- What is Data Warehousing?
# MAGIC
# MAGIC > **Data warehousing is the complete process and architecture used to
# MAGIC > collect data from multiple sources, ingest it, clean and transform it,
# MAGIC > integrate it, store it in analytical structures such as fact and
# MAGIC > dimension tables, and make it available for reporting and analytics.**
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 55. Interview Answer --- ETL vs ELT
# MAGIC
# MAGIC > **ETL means Extract, Transform, Load, where data is transformed before
# MAGIC > loading into the target system. ELT means Extract, Load, Transform,
# MAGIC > where raw data is first loaded into the target platform and
# MAGIC > transformations are performed there. ELT is common in modern cloud
# MAGIC > data platforms because they provide scalable compute for
# MAGIC > transformations.**
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 56. Interview Answer --- Star Schema
# MAGIC
# MAGIC > **A star schema is a dimensional modeling approach where a central
# MAGIC > fact table contains business events and measures, while surrounding
# MAGIC > dimension tables contain descriptive information such as customer,
# MAGIC > product, and date.**
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 57. Interview Answer --- Data Warehouse vs Data Lake
# MAGIC
# MAGIC > **A data warehouse is primarily designed for curated, structured
# MAGIC > analytical data and BI reporting, while a data lake is designed to
# MAGIC > store large volumes of raw data in different formats. A warehouse
# MAGIC > emphasizes business-ready analytics, while a lake provides flexibility
# MAGIC > for raw storage, data engineering, and data science. A lakehouse
# MAGIC > combines capabilities of both.**
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 58. Interview Answer --- Why Do We Need a Data Warehouse?
# MAGIC
# MAGIC > **We need a data warehouse to integrate data from multiple operational
# MAGIC > systems into a centralized, consistent, historical repository
# MAGIC > optimized for analytics. It separates analytical workloads from
# MAGIC > transactional systems and enables reliable reporting, trend analysis,
# MAGIC > business intelligence, and decision-making.**
# MAGIC
# MAGIC ------------------------------------------------------------------------
# MAGIC
# MAGIC # 59. Final Mental Model
# MAGIC
# MAGIC ``` text
# MAGIC SOURCE SYSTEMS
# MAGIC       |
# MAGIC       v
# MAGIC INGESTION
# MAGIC       |
# MAGIC       v
# MAGIC RAW / STAGING
# MAGIC       |
# MAGIC       v
# MAGIC CLEAN + VALIDATE
# MAGIC       |
# MAGIC       v
# MAGIC TRANSFORM
# MAGIC       |
# MAGIC       v
# MAGIC FACT + DIMENSION TABLES
# MAGIC       |
# MAGIC       v
# MAGIC DATA WAREHOUSE
# MAGIC       |
# MAGIC       +---- BI
# MAGIC       +---- Reports
# MAGIC       +---- Dashboards
# MAGIC       +---- Analytics
# MAGIC       +---- Decision Making
# MAGIC ```
# MAGIC
# MAGIC ## Final Definition
# MAGIC
# MAGIC ``` text
# MAGIC DATA WAREHOUSE
# MAGIC
# MAGIC A centralized analytical system where data from multiple sources
# MAGIC is integrated, cleaned, organized, and stored historically so that
# MAGIC businesses can efficiently perform reporting, analytics, and
# MAGIC decision-making.
# MAGIC
# MAGIC DATA WAREHOUSING
# MAGIC
# MAGIC The complete process and architecture of extracting, ingesting,
# MAGIC transforming, integrating, storing, governing, and serving data
# MAGIC for analytical use.
# MAGIC ```
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Difference Between Database and Data Warehouse
# MAGIC
# MAGIC | Feature | Database | Data Warehouse |
# MAGIC |---|---|---|
# MAGIC | **Purpose** | Used for day-to-day operations and transactions | Used for reporting, analytics, and decision-making |
# MAGIC | **Main Workload** | OLTP (Online Transaction Processing) | OLAP (Online Analytical Processing) |
# MAGIC | **Data Type** | Mostly current/operational data | Historical + integrated data |
# MAGIC | **Operations** | Frequent INSERT, UPDATE, DELETE | Mostly SELECT and analytical queries |
# MAGIC | **Query Type** | Simple and short queries | Complex queries with JOIN, GROUP BY, aggregations, etc. |
# MAGIC | **Data Volume** | Usually smaller compared to analytical warehouses | Designed to handle very large volumes of data |
# MAGIC | **Performance Optimization** | Optimized for fast transactions | Optimized for analytical queries |
# MAGIC | **Users** | Applications, customers, operational users | Data analysts, BI teams, data scientists, management |
# MAGIC | **Data Sources** | Usually one application/system | Multiple sources such as DBs, APIs, files, CRM, ERP, etc. |
# MAGIC | **Historical Data** | Usually limited | Stores large amounts of historical data |
# MAGIC | **Schema** | Usually normalized | Often uses dimensional models such as Star/Snowflake schema |
# MAGIC | **Example Tables** | `customers`, `orders`, `payments` | `fact_sales`, `dim_customer`, `dim_product` |
# MAGIC | **Data Updates** | Continuous and frequent | Usually batch or incremental loads |
# MAGIC | **Transactions** | Strongly focused on ACID transactions | Primarily focused on analytical processing |
# MAGIC | **Example** | MySQL, PostgreSQL, Oracle | Snowflake, Amazon Redshift, Google BigQuery, Azure Synapse |
# MAGIC | **Example Query** | Get a customer's current order | Calculate total sales by country for the last 5 years |
# MAGIC | **Primary Goal** | Run the business | Analyze the business |
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # 📦 Incremental Loading in Data Warehousing — Explained Simply
# MAGIC
# MAGIC ## 🧠 The Core Idea
# MAGIC
# MAGIC Every day, new data arrives — new orders, new customers, updated prices. A data warehouse needs to absorb this new data **without reprocessing everything from scratch** every single time.
# MAGIC
# MAGIC There are two ways to load data:
# MAGIC
# MAGIC | Full Load | Incremental Load |
# MAGIC |---|---|
# MAGIC | Reload **everything**, every time | Load only what's **new or changed** since last time |
# MAGIC | Simple, but slow and wasteful as data grows | Efficient, but requires more careful design |
# MAGIC | Fine for small, static datasets | The standard approach for real production warehouses |
# MAGIC
# MAGIC **Incremental Loading** means: *"Only bring in the rows that are new or have changed since the last time I loaded data — don't touch what hasn't changed."*
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🤔 Why Not Just Reload Everything Every Time?
# MAGIC
# MAGIC Imagine a `orders` table with **500 million rows**. If only 10,000 new orders came in today, reloading all 500 million rows just to get those 10,000 is:
# MAGIC
# MAGIC - ❌ Slow (hours instead of minutes)
# MAGIC - ❌ Expensive (more compute, more I/O)
# MAGIC - ❌ Risky (higher chance of failure on a huge job vs a small one)
# MAGIC - ❌ Unnecessary — 99.998% of that data didn't even change
# MAGIC
# MAGIC **Incremental loading fixes this** by identifying and moving only the delta (the difference) — the new/changed rows.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔍 How Do We Know What's "New or Changed"? → CDC
# MAGIC
# MAGIC **CDC = Change Data Capture**
# MAGIC
# MAGIC CDC is the general term for *"how do we detect that something changed in the source system?"*
# MAGIC
# MAGIC There are a few common ways to implement CDC:
# MAGIC
# MAGIC ### 1. Timestamp-Based CDC (most common, simplest)
# MAGIC The source table has a column like `modified_date` or `updated_at`. Each incremental run just asks:
# MAGIC
# MAGIC ```sql
# MAGIC SELECT * FROM source_table
# MAGIC WHERE modified_date > '<last_load_timestamp>'
# MAGIC ```
# MAGIC
# MAGIC This grabs only rows that changed after the last time you loaded data.
# MAGIC
# MAGIC **Limitation:** If a row is deleted, there's no "delete timestamp" — the row just disappears, and this method won't detect it.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 2. Log-Based CDC (used in real production systems)
# MAGIC Databases keep an internal **transaction log** (e.g., MySQL's binlog, PostgreSQL's WAL) that records every insert, update, and delete as it happens — in order, with full detail.
# MAGIC
# MAGIC Tools like **Debezium**, **Databricks Delta Live Tables CDC**, or cloud-native CDC services **read this log directly**, so they capture:
# MAGIC - ✅ Inserts
# MAGIC - ✅ Updates
# MAGIC - ✅ **Deletes** (this is the big win over timestamp-based CDC)
# MAGIC
# MAGIC This is more powerful but more complex to set up — it needs access to the database's internal log, not just a query.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 3. Trigger-Based CDC (older approach)
# MAGIC Database triggers fire on every `INSERT`/`UPDATE`/`DELETE` and write the change into a separate "audit" or "change" table. Rarely used today because it adds overhead directly to the source database — log-based CDC is the modern replacement.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 4. Snapshot Comparison (fallback when nothing else is available)
# MAGIC If the source system has **no timestamp column and no accessible log**, you can:
# MAGIC 1. Take a full snapshot of the source data today
# MAGIC 2. Compare it against yesterday's snapshot
# MAGIC 3. Whatever rows differ = the changes
# MAGIC
# MAGIC This works but is expensive (you're essentially still reading everything) — used only when CDC isn't otherwise possible.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🏗️ Staging vs Core — Where Does the Data Actually Go?
# MAGIC
# MAGIC A typical data warehouse pipeline has (at least) two layers:
# MAGIC
# MAGIC ```
# MAGIC Source System
# MAGIC       │
# MAGIC       ▼
# MAGIC ┌──────────────┐
# MAGIC │   STAGING    │   ← raw landing zone for incremental data
# MAGIC └──────────────┘
# MAGIC       │
# MAGIC       ▼
# MAGIC ┌──────────────┐
# MAGIC │     CORE     │   ← the real, permanent, historical warehouse table
# MAGIC └──────────────┘
# MAGIC ```
# MAGIC
# MAGIC ### Staging Table
# MAGIC - A **temporary landing area** for the data pulled in during *this specific run*
# MAGIC - Holds only the **latest batch** of new/changed records (not the full history)
# MAGIC - Structurally similar to the source, minimal transformation
# MAGIC - Think of it as: *"the inbox where today's mail lands before you file it away"*
# MAGIC
# MAGIC ### Core Table
# MAGIC - The **permanent, trusted warehouse table** — the actual "single source of truth"
# MAGIC - Contains the **full historical dataset**, built up over time
# MAGIC - This is what reports, dashboards, and analysts actually query
# MAGIC - Data gets here through a controlled process (usually a `MERGE`/`UPSERT`) that takes what's in Staging and correctly applies it to Core
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🧹 Why Do We Truncate the Staging Table?
# MAGIC
# MAGIC **`TRUNCATE`** means: wipe the table completely empty, instantly, before the next load.
# MAGIC
# MAGIC ### The Core Reason
# MAGIC Staging is meant to hold **only the current batch** — not a growing pile of every batch ever loaded. If you don't clear it out, here's what goes wrong:
# MAGIC
# MAGIC | Problem | Why It Happens |
# MAGIC |---|---|
# MAGIC | **Duplicate processing** | Old batch data is still sitting there; next run might process it again |
# MAGIC | **Incorrect MERGE results** | The `MERGE INTO Core FROM Staging` step would apply *stale* rows from previous runs, not just today's changes |
# MAGIC | **Uncontrolled growth** | Staging would keep growing forever, becoming just as big as Core — defeating the whole purpose of incremental loading |
# MAGIC | **Ambiguous state** | You can no longer tell "is this row from today's batch or last week's?" |
# MAGIC
# MAGIC ### The Correct Pattern
# MAGIC ```
# MAGIC 1. TRUNCATE staging table          → make sure it's empty
# MAGIC 2. Load only new/changed rows      → from source into staging (using CDC)
# MAGIC 3. MERGE staging → core            → apply changes into the permanent table
# MAGIC 4. (Next run repeats from step 1)  → staging is disposable, core is permanent
# MAGIC ```
# MAGIC
# MAGIC **Simple analogy:**
# MAGIC Think of Staging as a **whiteboard** you use every morning to jot down today's to-do list, and Core as your **permanent notebook** where completed tasks get written down for good.
# MAGIC - If you don't erase the whiteboard each morning, yesterday's notes get mixed in with today's — and you might copy the same task into your notebook twice.
# MAGIC - Erasing (truncating) the whiteboard before writing today's list keeps things clean and prevents duplicate or stale entries from bleeding into your permanent notebook.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔄 Putting It All Together — The Full Incremental Flow
# MAGIC
# MAGIC ```
# MAGIC 1. CDC detects what changed in the source
# MAGIC       (timestamp filter, log-based CDC, etc.)
# MAGIC               │
# MAGIC               ▼
# MAGIC 2. TRUNCATE the staging table
# MAGIC       (clear out last run's leftovers)
# MAGIC               │
# MAGIC               ▼
# MAGIC 3. Load only the new/changed rows into staging
# MAGIC               │
# MAGIC               ▼
# MAGIC 4. MERGE staging into core
# MAGIC       - Matched rows  → UPDATE
# MAGIC       - New rows      → INSERT
# MAGIC       - (Sometimes)   → mark as deleted if using log-based CDC
# MAGIC               │
# MAGIC               ▼
# MAGIC 5. Core table now reflects the latest, correct, full history
# MAGIC               │
# MAGIC               ▼
# MAGIC    (Repeat tomorrow — staging starts empty again)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Quick Summary
# MAGIC
# MAGIC - **Incremental Loading** = only move what's new or changed, instead of reprocessing everything.
# MAGIC - **CDC (Change Data Capture)** = the technique used to *detect* what changed — commonly via timestamps, or more robustly via database transaction logs (which also catch deletes).
# MAGIC - **Staging** = a temporary, disposable landing zone for just the current batch of changes.
# MAGIC - **Core** = the permanent warehouse table holding the full trusted history — built up incrementally via `MERGE` from staging.
# MAGIC - **Why truncate staging** = to guarantee staging only ever holds *this run's* data, preventing duplicate processing, stale merges, and uncontrolled growth.
# MAGIC