.. Reference: https://stackoverflow.com/questions/48074094/use-sphinx-autosummary-recursively-to-generate-api-documentation

{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% block methods %}
   {% block attributes %}

   .. HACK -- the point here is that we don't want this to appear in the output, but the autosummary should still generate the pages.

   {% if attributes %}
      .. autosummary::
         :toctree:
      {% for item in all_attributes %}
         {%- if not item.startswith('_') %}
         {{ name }}.{{ item }}
         {%- endif -%}
      {%- endfor %}
   {% endif %}
   {% endblock %}

   .. HACK -- the point here is that we don't want this to appear in the output, but the autosummary should still generate the pages.

   {% if methods %}
      .. autosummary::
         :toctree:
      {% for item in all_methods %}
         {%- if not item.startswith('_') or item in ['__call__'] %}
         {{ name }}.{{ item }}
         {%- endif -%}
      {%- endfor %}
   {% endif %}
   {% endblock %}