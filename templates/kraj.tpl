# block content:
    {% wykres %}
    {% tabelka %}
    <ul>
    {% for kand in kandydaci %}
        <li>{{ kand.nazwa }} - {{ kand.glosy }}</li>
    {% endfor %}
    </ul>
    {% mapka %}
# endblock