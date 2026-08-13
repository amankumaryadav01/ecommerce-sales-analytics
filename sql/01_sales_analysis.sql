-- ============================================================
-- E-COMMERCE SALES ANALYTICS
-- SQL SALES ANALYSIS
-- ============================================================


-- ============================================================
-- 1. TOTAL REVENUE
-- ============================================================

SELECT
    SUM(Revenue) AS total_revenue
FROM online_retail_cleaned;


-- ============================================================
-- 2. TOTAL SALES REVENUE
-- ============================================================

SELECT
    SUM(Revenue) AS sales_revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale';


-- ============================================================
-- 3. TOTAL RETURN VALUE
-- ============================================================

SELECT
    SUM(Revenue) AS return_value
FROM online_retail_cleaned
WHERE TransactionType = 'Return';


-- ============================================================
-- 4. SALES VS RETURNS
-- ============================================================

SELECT
    TransactionType,
    COUNT(*) AS transactions,
    SUM(Revenue) AS revenue,
    AVG(Revenue) AS average_revenue
FROM online_retail_cleaned
GROUP BY TransactionType
ORDER BY revenue DESC;


-- ============================================================
-- 5. MONTHLY REVENUE
-- ============================================================

SELECT
    DATE_TRUNC('month', InvoiceDate) AS month,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
GROUP BY DATE_TRUNC('month', InvoiceDate)
ORDER BY month;


-- ============================================================
-- 6. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    StockCode,
    Description,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY StockCode, Description
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 7. TOP 10 PRODUCTS BY QUANTITY SOLD
-- ============================================================

SELECT
    StockCode,
    Description,
    SUM(Quantity) AS quantity_sold
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY StockCode, Description
ORDER BY quantity_sold DESC
LIMIT 10;


-- ============================================================
-- 8. TOP 10 COUNTRIES BY REVENUE
-- ============================================================

SELECT
    Country,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY Country
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 9. TOP 10 COUNTRIES BY NUMBER OF ORDERS
-- ============================================================

SELECT
    Country,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY Country
ORDER BY orders DESC
LIMIT 10;


-- ============================================================
-- 10. AVERAGE ORDER VALUE
-- ============================================================

SELECT
    AVG(order_value) AS average_order_value
FROM (
    SELECT
        InvoiceNo,
        SUM(Revenue) AS order_value
    FROM online_retail_cleaned
    WHERE TransactionType = 'Sale'
    GROUP BY InvoiceNo
) orders;


-- ============================================================
-- 11. TOP 10 CUSTOMERS BY REVENUE
-- ============================================================

SELECT
    CustomerID,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
  AND CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 12. CUSTOMER ORDER COUNT
-- ============================================================

SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS total_orders
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
  AND CustomerID IS NOT NULL
GROUP BY CustomerID
ORDER BY total_orders DESC
LIMIT 10;


-- ============================================================
-- 13. MONTHLY ORDERS
-- ============================================================

SELECT
    DATE_TRUNC('month', InvoiceDate) AS month,
    COUNT(DISTINCT InvoiceNo) AS orders
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY DATE_TRUNC('month', InvoiceDate)
ORDER BY month;


-- ============================================================
-- 14. MONTHLY QUANTITY SOLD
-- ============================================================

SELECT
    DATE_TRUNC('month', InvoiceDate) AS month,
    SUM(Quantity) AS quantity_sold
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY DATE_TRUNC('month', InvoiceDate)
ORDER BY month;


-- ============================================================
-- 15. REVENUE BY COUNTRY WITH ORDERS
-- ============================================================

SELECT
    Country,
    COUNT(DISTINCT InvoiceNo) AS orders,
    SUM(Quantity) AS quantity_sold,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY Country
ORDER BY revenue DESC;


-- ============================================================
-- 16. TOP 10 PRODUCTS BY AVERAGE REVENUE PER TRANSACTION
-- ============================================================

SELECT
    StockCode,
    Description,
    AVG(Revenue) AS average_revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY StockCode, Description
HAVING COUNT(*) >= 10
ORDER BY average_revenue DESC
LIMIT 10;


-- ============================================================
-- 17. RETURN RATE BY COUNTRY
-- ============================================================

SELECT
    Country,
    COUNT(CASE
        WHEN TransactionType = 'Return' THEN 1
    END) AS returns,
    COUNT(CASE
        WHEN TransactionType = 'Sale' THEN 1
    END) AS sales,
    ROUND(
        100.0 * COUNT(CASE
            WHEN TransactionType = 'Return' THEN 1
        END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS return_rate_percent
FROM online_retail_cleaned
GROUP BY Country
ORDER BY return_rate_percent DESC;


-- ============================================================
-- 18. DAILY REVENUE
-- ============================================================

SELECT
    DATE(InvoiceDate) AS sale_date,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY DATE(InvoiceDate)
ORDER BY sale_date;


-- ============================================================
-- 19. BEST REVENUE MONTH
-- ============================================================

SELECT
    DATE_TRUNC('month', InvoiceDate) AS month,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY DATE_TRUNC('month', InvoiceDate)
ORDER BY revenue DESC
LIMIT 1;


-- ============================================================
-- 20. WORST REVENUE MONTH
-- ============================================================

SELECT
    DATE_TRUNC('month', InvoiceDate) AS month,
    SUM(Revenue) AS revenue
FROM online_retail_cleaned
WHERE TransactionType = 'Sale'
GROUP BY DATE_TRUNC('month', InvoiceDate)
ORDER BY revenue ASC
LIMIT 1;


-- ============================================================
-- END OF SQL ANALYSIS
-- ============================================================