{% macro add_audit_columns() %}
        get_current_timestamp() AS _load_timestamp,
        '{{ invocation_id }}' AS _dbt_process_id
{% endmacro %}
