<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <title>Wyniki wyborów 2000</title>
  <link rel="stylesheet" type="text/css" href="{{ static('main.css') }}">
</head>
<body>

<div id="content">
  <div id="login">
    {% if error %}
      <span id="error">Wystąpił błąd przy logowaniu.</span>
    {% endif %}
    {% if request.user.is_authenticated() %}
      Zalogowano jako: {{ request.user.get_username() }}.
      <form action="{{ request.path }}" method="post">
        <input type="submit" value="Wyloguj się">
        <input type="hidden" name="type" value="logout">
        {{ csrf_input }}
      </form>
    {% else %}
      <form action="{{ request.path }}" method="post">
        Login: <input type="text" name="username">
        Hasło: <input type="text" name="password">
        <input type="submit" value="Login">
        <input type="hidden" name="type" value="login">
        {{ csrf_input }}
      </form>
      <a href="/register">Zarejestruj się</a>
    {% endif %}
  </div>
  <header id="title">
      Wybory prezydenckie 2000
  </header>
  <nav>
    Wyszukaj gminę po nazwie:
    <form action="/szukaj" method="get">
      <input type="text" name="q" value="">
      <input type="submit" value="Szukaj!">
    </form>
  </nav>
  <section id="candidates_section">
    {% if make_map %}
    <figure id="map">
      {% include 'mapka.html' %}
    </figure>
    {% endif %}
  <article id="candidates">
    <table class="candidates">
      <thead>
      <tr>
        <th>Nazwisko kandydata</th>
        <th>Zdobyte głosy</th>
        <th>Wynik (%)</th>
      </tr>
      </thead>
      <tbody>
      {% for c in candidates %}<tr>
        <td>{{ c.name }}</td>
        <td class="num">{{ c.votes }}</td>
        <td><div><div style="width:{{ c.votes_percent }}; background-color:{{ c.color }};">{{ c.votes_percent }}</div></div></td>
      </tr>{% endfor %}
      </tbody>
    </table>
  </article>
  </section>

  <section id="data_section">
    <table class="regions">
      <thead>
      <tr>
        <th>Nazwa jednostki</th>
        <th>Głosy ważne</th>
        {% for c in candidates %}<th class="thin">{{ c.name }}</th>{% endfor %}
      </tr>
      </thead>
      <tbody>
      {% for r in regions %}<tr>
        <td>
          {% if r.link %}
            <a href="{{ r.link }}">{{ r.name }}</a>
          {% else %}
          {{ r.name }}
          {% endif %}
        </td>
        <td class="num">{{ r.total }}</td>
        {% for v in r.candidate_votes %}<td class="num thin">{{ v }}</td>{% endfor %}
        <!--<td class="bars">
          {% for v in r.candidate_votes %}
            {% if r.total != 0 -%}
              {% set percents = ((v / r.total) * 100.0)|round(2) -%}
            {% else -%}
              {% set percents = (100.0 / r.candidate_votes|length)|round(2) -%}
            {% endif -%}
            <div class="cand_bar" style="width:{{ percents }}%; background-color:{{ ['black', 'red', 'green']|random }};"></div>
          {% endfor %}
        </td>-->
        {% if request.user.is_authenticated() and can_edit %}
          <td><a href="{{ r.edit_link }}">Edytuj</a></td>
        {% endif %}
      </tr>{% endfor %}
      </tbody>
    </table>
  </section>
</div>
</body>
</html>