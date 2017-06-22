<html>
<head>
  <meta charset="utf-8">
  <title>Wyniki wyborów 2000</title>
  <link rel="stylesheet" type="text/css" href="{{ static }}/main.css">
</head>
<body>
<div id="content">
  <form action="{{ request.path }}" method="post">
    {{ form.as_p() }}
    {{ csrf_input }}
    <input type="submit" value="Submit">
  </form>
</div>
</body>
</html>