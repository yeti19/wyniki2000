<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <title>Wyniki wyborów 2000</title>
  <link rel="stylesheet" type="text/css" href="{{ static }}/main.css">
</head>
<body>
  <div id="content">
    <form action="/" method="post">
      <div>Login: <input id="username" maxlength="30" name="username" type="text"></div>
      <div>Hasło: <input id="password" name="password" type="password"></div>
      <div><input type="submit" value="Zarejestruj się!"></div>
      <input type="hidden" name="type" value="register">
      {{ csrf_input }}
    </form>
  </div>
</body>
</html>