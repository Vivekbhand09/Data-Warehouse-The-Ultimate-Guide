# Databricks notebook source
# MAGIC %md
# MAGIC # 🕰️ Slowly Changing Dimensions (SCD) — Complete Guide
# MAGIC
# MAGIC ## 🧠 What Is SCD?
# MAGIC
# MAGIC **Slowly Changing Dimension (SCD)** is a technique for handling changes to dimension data **over time** in a data warehouse.
# MAGIC
# MAGIC Think about your `DimCustomers` table. A customer's name, email, or address doesn't change every day — but it *does* change occasionally (a customer moves cities, updates their email, gets married and changes their name). That's exactly what "slowly changing" means: not static, but not constantly changing either.
# MAGIC
# MAGIC The core question SCD answers is:
# MAGIC
# MAGIC > **When a dimension record changes, what do we do — overwrite it, or keep the history?**
# MAGIC
# MAGIC Different SCD **types** give different answers to that question, and each is used for a different business need.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🤔 Why Does This Even Matter?
# MAGIC
# MAGIC Imagine `DimCustomers` today:
# MAGIC
# MAGIC | CustomerID | CustomerName | City |
# MAGIC |---|---|---|
# MAGIC | 101 | Alice Johnson | New York |
# MAGIC
# MAGIC Now Alice moves to Chicago. If we just run:
# MAGIC
# MAGIC ```sql
# MAGIC UPDATE DimCustomers SET City = 'Chicago' WHERE CustomerID = 101;
# MAGIC ```
# MAGIC
# MAGIC The table now says:
# MAGIC
# MAGIC | CustomerID | CustomerName | City |
# MAGIC |---|---|---|
# MAGIC | 101 | Alice Johnson | Chicago |
# MAGIC
# MAGIC **Problem:** Every past sale linked to Alice — even ones from when she genuinely lived in New York — now *reports* as if she lived in Chicago. Any historical report ("total sales by city, last year") becomes **wrong**, because history got silently rewritten.
# MAGIC
# MAGIC This is exactly the problem SCD types are designed to solve — each one is a different strategy for handling that update.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🥇 SCD Type 1 — Overwrite (No History Kept)
# MAGIC
# MAGIC ### What Happens
# MAGIC The old value is simply **replaced** with the new value. No history is kept — the record just reflects the latest, current truth.
# MAGIC
# MAGIC ### Simple Example
# MAGIC
# MAGIC **Before:**
# MAGIC
# MAGIC | CustomerID | CustomerName | City |
# MAGIC |---|---|---|
# MAGIC | 101 | Alice Johnson | New York |
# MAGIC
# MAGIC Alice moves to Chicago →
# MAGIC
# MAGIC **After:**
# MAGIC
# MAGIC | CustomerID | CustomerName | City |
# MAGIC |---|---|---|
# MAGIC | 101 | Alice Johnson | Chicago |
# MAGIC
# MAGIC The old value (`New York`) is **gone**. There is no way to know from this table alone that Alice ever lived in New York.
# MAGIC
# MAGIC ### How It's Implemented
# MAGIC A simple `UPDATE`, or a Delta Lake `MERGE` with `WHEN MATCHED THEN UPDATE SET *`:
# MAGIC
# MAGIC ```sql
# MAGIC MERGE INTO DimCustomers trg
# MAGIC USING src ON trg.CustomerID = src.CustomerID
# MAGIC WHEN MATCHED THEN UPDATE SET trg.City = src.City
# MAGIC WHEN NOT MATCHED THEN INSERT *;
# MAGIC ```
# MAGIC
# MAGIC ### When to Use It
# MAGIC Use SCD Type 1 when the **old value has no business or reporting value** — it was simply wrong, outdated, or a correction. Good example: fixing a typo in a customer's email address. Nobody needs to know "this customer's email used to be misspelled."
# MAGIC
# MAGIC **Trade-off:** Simple and cheap to implement, but you **permanently lose history**.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🥈 SCD Type 2 — Add a New Row (Full History Preserved)
# MAGIC
# MAGIC ### What Happens
# MAGIC Instead of overwriting, the **old row is kept and marked as inactive/expired**, and a **brand-new row** is inserted with the updated values. Both versions now exist side by side.
# MAGIC
# MAGIC This requires a few extra tracking columns: `StartTime` (when this version became active), `EndTime` (when it stopped being active), and `IsActive` (a simple flag for "is this the current version?").
# MAGIC
# MAGIC ### Simple Example
# MAGIC
# MAGIC **Before:**
# MAGIC
# MAGIC | CustomerID | CustomerName | City | StartTime | EndTime | IsActive |
# MAGIC |---|---|---|---|---|---|
# MAGIC | 101 | Alice Johnson | New York | 2023-01-01 | 3000-01-01 | Y |
# MAGIC
# MAGIC Alice moves to Chicago on `2024-02-10` →
# MAGIC
# MAGIC **After:**
# MAGIC
# MAGIC | CustomerID | CustomerName | City | StartTime | EndTime | IsActive |
# MAGIC |---|---|---|---|---|---|
# MAGIC | 101 | Alice Johnson | New York | 2023-01-01 | 2024-02-10 | **N** |
# MAGIC | 101 | Alice Johnson | Chicago | 2024-02-10 | 3000-01-01 | **Y** |
# MAGIC
# MAGIC Now there are **two rows for the same customer** — the old (now expired) version, and the new (current) version. Nothing was deleted; history is fully intact.
# MAGIC
# MAGIC ### How It's Implemented
# MAGIC Two-step `MERGE`, exactly like the pattern you built earlier:
# MAGIC
# MAGIC ```sql
# MAGIC -- MERGE 1: Expire the old active row if anything changed
# MAGIC MERGE INTO DimCustomers trg
# MAGIC USING src ON trg.CustomerID = src.CustomerID AND trg.IsActive = 'Y'
# MAGIC WHEN MATCHED AND src.City <> trg.City
# MAGIC THEN UPDATE SET trg.EndTime = current_timestamp(), trg.IsActive = 'N';
# MAGIC
# MAGIC -- MERGE 2: Insert the new active row
# MAGIC MERGE INTO DimCustomers trg
# MAGIC USING src ON trg.CustomerID = src.CustomerID AND trg.IsActive = 'Y'
# MAGIC WHEN NOT MATCHED THEN INSERT *;
# MAGIC ```
# MAGIC
# MAGIC ### When to Use It
# MAGIC Use SCD Type 2 when **preserving history is essential** — this is the most commonly used SCD type in real data warehouses. Anytime you need to correctly answer "what was true *as of* a specific point in time," Type 2 is the answer.
# MAGIC
# MAGIC **Trade-off:** Preserves full history and enables accurate historical reporting, but the dimension table grows over time (multiple rows per entity), and every query needs to be aware of `IsActive` / date ranges to get the "current" version correctly.
# MAGIC
# MAGIC **Real-world examples:** Customer address history, product price history, employee job title/department history.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🥉 SCD Type 3 — Add a New Column (Limited History: Just "Previous" and "Current")
# MAGIC
# MAGIC ### What Happens
# MAGIC Instead of a new row, a **new column** is added to store the *previous* value, while the main column is updated to the *current* value. This keeps **only one level of history** — the immediately previous value, not the full timeline.
# MAGIC
# MAGIC ### Simple Example
# MAGIC
# MAGIC **Before:**
# MAGIC
# MAGIC | CustomerID | CustomerName | CurrentCity |
# MAGIC |---|---|---|
# MAGIC | 101 | Alice Johnson | New York |
# MAGIC
# MAGIC Alice moves to Chicago →
# MAGIC
# MAGIC **After:**
# MAGIC
# MAGIC | CustomerID | CustomerName | CurrentCity | PreviousCity |
# MAGIC |---|---|---|---|
# MAGIC | 101 | Alice Johnson | **Chicago** | **New York** |
# MAGIC
# MAGIC If Alice moves again later, to Boston, `PreviousCity` would simply get overwritten to "Chicago" — the original "New York" value is now lost forever, since Type 3 only ever remembers **one step back**.
# MAGIC
# MAGIC ### How It's Implemented
# MAGIC A simple `UPDATE` that shifts the current value into the "previous" column before overwriting:
# MAGIC
# MAGIC ```sql
# MAGIC UPDATE DimCustomers
# MAGIC SET PreviousCity = CurrentCity,
# MAGIC     CurrentCity = 'Chicago'
# MAGIC WHERE CustomerID = 101;
# MAGIC ```
# MAGIC
# MAGIC ### When to Use It
# MAGIC Use SCD Type 3 when you only need to compare **"before vs. after"** for a specific known attribute — not a full timeline. It's useful for very specific, limited comparison needs, like "how many customers changed their preferred payment method last quarter?" — where only the immediate before/after matters.
# MAGIC
# MAGIC **Trade-off:** Much simpler and more compact than Type 2 (no extra rows), but only preserves **one previous value** — anything before that is lost. Rarely used compared to Type 1 and Type 2 because most real business needs require full history, not just one step back.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📊 SCD Types — Side-by-Side Comparison
# MAGIC
# MAGIC | Aspect | Type 1 (Overwrite) | Type 2 (New Row) | Type 3 (New Column) |
# MAGIC |---|---|---|---|
# MAGIC | **History kept?** | ❌ None | ✅ Full history | ⚠️ Only the immediately previous value |
# MAGIC | **How it's stored** | Same row, value replaced | New row added, old row marked inactive | Same row, new column added |
# MAGIC | **Table grows over time?** | No | Yes (more rows over time) | No (fixed extra columns) |
# MAGIC | **Complexity to implement** | Very simple | Moderate (needs Start/End/Active tracking) | Simple, but limited |
# MAGIC | **Can answer "what was true on date X"?** | ❌ No | ✅ Yes | ⚠️ Only for the last change |
# MAGIC | **Best for** | Correcting errors/typos, values where history is irrelevant | Tracking meaningful business changes over time (address, price, job title) | Simple before/after comparisons |
# MAGIC | **Most commonly used in practice** | Common for minor/corrective fields | ⭐ **The industry standard** for real historical tracking | Rare — used only for specific narrow needs |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 How to Decide Which Type to Use
# MAGIC
# MAGIC Ask yourself: **"If this value changes, do I ever need to know what it used to be?"**
# MAGIC
# MAGIC | Question | Answer | Use |
# MAGIC |---|---|---|
# MAGIC | "No — the old value was wrong or irrelevant" | Just fix it | **Type 1** |
# MAGIC | "Yes — I need to know the full history and when each version was true" | Track everything | **Type 2** |
# MAGIC | "Only sort of — I just want to compare the current value to the last one" | One-step-back comparison | **Type 3** |
# MAGIC
# MAGIC **In practice:** Most real-world data warehouses use a **mix** — critical dimensions like `DimCustomer` and `DimProduct` (price history) usually get **Type 2**, while minor corrective fields get **Type 1**, and **Type 3** shows up only occasionally for very specific comparison needs.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ✅ Quick Summary
# MAGIC
# MAGIC - **SCD (Slowly Changing Dimension)** = the strategy for handling changes to dimension data over time in a data warehouse.
# MAGIC - **Type 1 (Overwrite)** — replace the old value, no history kept. Use for corrections/irrelevant history.
# MAGIC - **Type 2 (New Row)** — keep the old row (marked inactive) and insert a new row for the change. Full history preserved. The most widely used type in real warehouses.
# MAGIC - **Type 3 (New Column)** — add a "previous value" column alongside the "current value" column. Only remembers one step back.
# MAGIC - The right choice always comes down to one question: **do you need to preserve history, and if so, how much of it?**