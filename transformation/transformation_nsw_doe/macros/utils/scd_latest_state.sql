{%- macro scd_latest_state(source='base', max_column='_task_instance') -%}

, max_task_instance AS (
    SELECT MAX({{ max_column }}) AS max_column_value
    FROM {{ source }}
    WHERE RIGHT( {{ max_column }}, 8) = (

                                SELECT MAX(RIGHT( {{ max_column }}, 8))
                                FROM {{ source }} )

), filtered AS (

    SELECT *
    FROM {{ source }}
    WHERE {{ max_column }} = (

                            SELECT max_column_value
                            FROM max_task_instance

                            )

)

SELECT *
FROM filtered

{%- endmacro -%}
