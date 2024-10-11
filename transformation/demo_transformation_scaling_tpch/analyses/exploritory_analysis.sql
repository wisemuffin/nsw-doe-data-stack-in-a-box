-- Build a query to generate a query
SELECT
    'SELECT ''' || table_name || ''' AS table_name, COUNT(*) AS row_count FROM tpch.' || table_name || ' UNION ALL '
FROM
    information_schema.tables
WHERE 1=1
{# AND table_schema = 'main'  #}
AND
    table_type = 'BASE TABLE'

-- After running this, copy the result, remove the last 'UNION ALL', and run the final query


SELECT 'dim__date' AS table_name, COUNT(*) AS row_count FROM tpch.dim__date UNION ALL
SELECT 'fct__order' AS table_name, COUNT(*) AS row_count FROM tpch.fct__order UNION ALL
SELECT 'fct__order_item' AS table_name, COUNT(*) AS row_count FROM tpch.fct__order_item UNION ALL
SELECT 'lineitem' AS table_name, COUNT(*) AS row_count FROM tpch.lineitem UNION ALL
SELECT 'nation' AS table_name, COUNT(*) AS row_count FROM tpch.nation UNION ALL
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM tpch.orders UNION ALL
SELECT 'part' AS table_name, COUNT(*) AS row_count FROM tpch.part UNION ALL
SELECT 'partsupp' AS table_name, COUNT(*) AS row_count FROM tpch.partsupp UNION ALL
SELECT 'prep__order_item' AS table_name, COUNT(*) AS row_count FROM tpch.prep__order_item UNION ALL
SELECT 'region' AS table_name, COUNT(*) AS row_count FROM tpch.region UNION ALL
SELECT 'supplier' AS table_name, COUNT(*) AS row_count FROM tpch.supplier
