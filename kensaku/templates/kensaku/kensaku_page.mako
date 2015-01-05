<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Kensaku | Ikhram</title>
    <meta name="description" content="A lightweight autocomplete plugin for jQuery.">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link type="text/css" rel="stylesheet" href="${request.static_url('kensaku:static/kensaku/css/bootstrap.min.css')}" />
    <link type="text/css" rel="stylesheet" href="${request.static_url('kensaku:static/kensaku/css/bootstrap-theme.min.css')}" />
    <link type="text/css" rel="stylesheet" href="${request.static_url('kensaku:static/kensaku/css/style.css')}" />
</head>
<body>
<form id="kensaku-form" method="GET" action="localhost:3000/c" target="_blank" role="form">
    <div class="form-group">
        <div class="col-sm-10">
            <input id="kensaku" class="form-control" autofocus type="text" name="q" placeholder="Cari Promo Paket Umroh Murah" style="width:100%;max-width:600px;outline:0">
            <input type="hidden" id="arrPromo" name="arrPromo" />
        </div>
    </div>
    <div class="form-group">
        <div class="col-md-4">
            <input class="form-control dt-pick" id="startDate" name="startDate"/>
        </div>
    </div>
    <div class="form-group">
        <div class="col-md-4">
            <input class="form-control dt-pick" id="endDate" name="endDate"/>
        </div>
    </div>
    <div class="form-group">
        <div class="col-md-4">
            <select id="whatPrice" name="whatPrice" class="form-control">
                <option value=''>  - Pilih Kisaran Budget - </option>
                <option value='2000'> <= $2000</option>
                <option value='2001 ~ 2500'> $2001 ~ $2500</option>
                <option value='2501 ~ 3000'> $2501 ~ $3000</option>
                <option value='3001 ~ 4000'> $3001 ~ $4000</option>
                <option value='4000'> >= $4000</option>
            </select>
        </div>
    </div>
    <div class="form-group">
        <div class="col-md-6">
            <input class="btn btn-default" type="submit" id="btn-cari" name="btn-cari" style="width: 250px;" />
        </div>
    </div>
</form>

<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/jquery-1.11.1.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/jquery-ui.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/moment.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/handlebars-v2.0.0.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/handlebars-helpers.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/jquery.auto-complete.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/hilitor.js')}"></script>
<script id="acw" type="text/x-handlebars-template">
    <div class="autocomplete-suggestion"
         data-val="{{ResultText}} {{dateFormat startDate}} - {{dateFormat endDate}}"
         data-promo="{{ GroupOfPromo }}"
         data-sdate="{{startDate}}"
         data-edate="{{endDate}}">
        {{#IsTitle}}
        <span>{{Header}} <span class="align-right">Promo (<strong>{{NoOfPromo}}</strong>)</span></span>
        {{/IsTitle}}
        {{^IsTitle}}
        {{#HasImage}}
        <a class="anchor" tabindex="-1">
            <img src="{{Image}}" data-2x="{{RetinaImage}}" height="50" width="50" alt="">
            <ul class="list-plain align-left" >
                <li><strong id="autoCompleteText">{{ResultText}}</strong></li>
            </ul>
            <span>{{startDate}} - {{endDate}}</span><span class="align-right">Promo (<strong>{{NoOfPromo}}</strong>)</span>
        </a>
        {{/HasImage}}
        {{^HasImage}}
        <a class="anchor" tabindex="-1">
            <span class="align-left" id="autoCompleteText">{{ResultText}} {{dateFormat startDate}} - {{dateFormat endDate}}</span>
            <span class="align-right">Promo (<strong>{{NoOfPromo}}</strong>)</span>
        </a>
        {{/HasImage}}
        {{/IsTitle}}
    </div>
</script>
<script type="text/javascript">
    $(function(){
        var hightlander = new Hilitor('wacs');
        hightlander.setMatchType("left");
        $('#kensaku').autoComplete({
            minChars: 1,
            source: function(term, response){
                try { xhr.abort(); } catch(e){}
                var xhr = $.getJSON('${request.route_url('results')}', { q: term }, function(data){ response(data); });
            },
            renderItem: function (item, search){
                ##console.log(item);
                var tpl = $('#acw').html();
                ##Mustache.parse(tpl);
                var template = Handlebars.compile(tpl);
                ##return Mustache.render(tpl, item);
                return template(item);
            },
            onSelect: function(self, term, promo) {
                var countPromo = 1;
                console.log(promo);
                var splto = promo.toString().split(",");
                if(splto.length > 1 ) {
                    countPromo = splto.length;
                }

                console.log(self[0].dataset);
                $('#btn-cari').val('Total Promo: (' + countPromo + ')');
                $('#arrPromo').val(promo);
                console.log(moment(self[0].dataset.sdate).format("DD/MM/YYYY"));

                $('#startDate').datepicker('setDate', new Date(moment(self[0].dataset.sdate).format("MM/DD/YYYY")));
                $('#endDate').datepicker('setDate', new Date(moment(self[0].dataset.edate).format("MM/DD/YYYY")));
            },
            onShow: function(term) {
                console.log(term);
                hightlander.apply(term);
            }
        });
        $( ".dt-pick" ).datepicker({
            dateFormat: "dd-mm-yy",
            onClose: function( selectedDate ) {
                var arr = $('#arrPromo').val();
                $.getJSON('${request.route_url('valid')}',
                        { arrPromo: arr },
                        function(data){
                            console.log(data);
                            $('#btn-cari').val('Total Promo: (' + data.data.count + ')');
                        });
            }
        });


    });
</script>
</body>
</html>