/*  -------------------------------------------------------------------------------------------------------
    clean up tables
------------------------------------------------------------------------------------------------------- */
DECLARE @DropSQL NVARCHAR(MAX) = ''

-- Generate a list of tables to drop using dynamic SQL
SELECT @DropSQL = @DropSQL + 'DROP TABLE ' + QUOTENAME(schemas.name) + '.' + QUOTENAME(tables.name) + ';
'
FROM sys.schemas
LEFT JOIN sys.tables ON schemas.schema_id = tables.schema_id
WHERE schemas.name LIKE 'dbt_%'
  AND tables.name IS NOT NULL

-- Execute the dynamic SQL to drop tables
EXEC sp_executesql @DropSQL
go

/*  -------------------------------------------------------------------------------------------------------
    clean up views
------------------------------------------------------------------------------------------------------- */

DECLARE @DropSQL NVARCHAR(MAX) = ''

-- Generate a list of tables to drop using dynamic SQL
SELECT @DropSQL = @DropSQL + 'DROP VIEW ' + QUOTENAME(schemas.name) + '.' + QUOTENAME(views.name) + ';
'
FROM sys.schemas
LEFT JOIN sys.views ON schemas.schema_id = views.schema_id
WHERE schemas.name LIKE 'dbt_%'
  AND views.name IS NOT NULL

-- Execute the dynamic SQL to drop tables
EXEC sp_executesql @DropSQL
go

/*  -------------------------------------------------------------------------------------------------------
    clean up schemas
------------------------------------------------------------------------------------------------------- */

DECLARE @DropSQL NVARCHAR(MAX) = ''

-- Generate a list of schemas to drop using dynamic SQL
SELECT @DropSQL = @DropSQL + 'DROP SCHEMA ' + QUOTENAME(schemas.name) + ';
'
FROM sys.schemas
WHERE schemas.name LIKE 'dbt_%'

-- Execute the dynamic SQL to drop schemas
EXEC sp_executesql @DropSQL
