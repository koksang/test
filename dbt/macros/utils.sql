{% macro generate_schema_name(custom_schema_name, node) -%}

    {% if node.fqn[1:-1] | length == 0 %}
        {%- set default_schema = target.schema | trim | lower -%}
    {% else %}
        {%- set default_schema = node.fqn[1:-1] | join('__') | trim | lower -%}
    {% endif %}

    {%- if custom_schema_name is none -%}
        {{ default_schema | lower }}
    {%- else -%}
        {{ custom_schema_name | lower }}

    {%- endif -%}

{%- endmacro %}