<%inherit file="layout.mako"/>

<%block name="head">
<script type="text/javascript" src="${request.static_url('kensaku:static/js/search.js')}"></script>
</%block>

<%block name="title">Search</%block>

<form>
    <input name="q" id="q" value="${ args.get("q", "") }" />
</form>

<div id="results">

</div>

