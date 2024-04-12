{%- macro dbt_audit(cte_ref, created_by, updated_by, created_date, updated_date) -%}

    SELECT
      *,
      '{{ created_by }}'::VARCHAR       AS _audit__created_by,
      '{{ updated_by }}'::VARCHAR       AS _audit__updated_by,
      '{{ created_date }}'::DATE        AS _audit__model_created_date,
      '{{ updated_date }}'::DATE        AS _audit__model_updated_date,
      get_current_timestamp()               AS _audit__dbt_updated_at,

    {% if execute %}

        {% if not flags.FULL_REFRESH and config.get('materialized') == "incremental" %}

            {%- set source_relation = adapter.get_relation(
                database=target.database,
                schema=this.schema,
                identifier=this.table,
                ) -%}      

            {% if source_relation != None %}

                {% set min_created_date %}
                    SELECT LEAST(MIN(dbt_created_at), get_current_timestamp()) AS min_ts 
                    FROM {{ this }}
                {% endset %}

                {% set results = run_query(min_created_date) %}

                '{{results.columns[0].values()[0]}}'::TIMESTAMP AS _audit__dbt_created_at

            {% else %}

                get_current_timestamp()               AS _audit__dbt_created_at

            {% endif %}

        {% else %}

            get_current_timestamp()               AS _audit__dbt_created_at

        {% endif %}
    
    {% endif %}

    FROM {{ cte_ref }}

{%- endmacro -%}
