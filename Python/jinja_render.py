from jinja2 import Template

render_jinja = """
{% set myList=[1,2,3,4,5,6] %}
{% set displayCount = 0 %}
{% for x in myList %}
{% set displayCount = x %}
{% if displayCount <= 3 %}
Under or Equal to 3
{% else %}
Above 3
{% endif %}
{% endfor %}
"""

template = Template(render_jinja)
print template.render()