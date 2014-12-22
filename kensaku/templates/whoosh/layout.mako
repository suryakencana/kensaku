<!doctype html>
<html>
    <head>
        <title>${self.title()}</title>
        <link rel=stylesheet type=text/css href="${request.static_url('kensaku:static/css/bootstrap.min.css')}">
        <link rel=stylesheet type=text/css href="${request.static_url('kensaku:static/css/style.css')}">
        <script src="${request.static_url('kensaku:static/js/jquery-1.9.1.min.js') }"></script>
        <script src="${request.static_url('kensaku:static/js/bootstrap.min.js') }"></script>
        <%block name="head"/>
        <script>
        <%block name="js"/>
        </script>
    </head>
    <body>
        <div class="container">
            <h1><%block name="title"/></h1>

            ${self.body()}
        </div>
    </body>
</html>
