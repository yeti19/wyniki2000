<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <title>Wyniki wyborów 2000</title>
  <link rel="stylesheet" type="text/css" href="{{ static }}/main.css">
</head>
<body>

<div id="content">
  <div id="login">
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
      <a href="register">Zarejestruj się</a>
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
  <h1>{{ message }}</h1>
</div>
</body>
</html>