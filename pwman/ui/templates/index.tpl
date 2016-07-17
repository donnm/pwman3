<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>Pwman3 Web</title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <link rel="stylesheet" href="/static/css/milligram.css">
	<link rel="stylesheet" href="/static/css/style.css">
    </head>


<main class="wrapper">
  <nav class="navigation">
  <section class="container">
    <a class="navigation-title" href="https://pwman3.github.io/">
    <img class="img" src="https://openclipart.org/download/190821/Cles-de-serrure-lock-keys.svg" height="30" alt="pwman3" title="pwman3">
    <h1 class="title">Pwman3</h1>
    </a>
    <span class="auth">
    <form class="auth-form">
      <button id="auth-btn" class="button">Auth</button>
      <input id="pwd-input" class="navigation-button" type="password" name="auth-pwd" placeholder="Password" style="display: none;" >
      <input id="show" class="button-primary navigation-button" style="display:none;" value="Submit" type="submit">
    </form>
    </span>
  </section>
  </nav>
</main>

<script type="text/javascript">
$("#auth-btn").click(function () {
   $("#pwd-input").show('fast');
   $("#show").show('fast');
});

$("#auth-btn").click(function () {
   $("#auth-btn").hide(1000);
});
</script>
</html>
