<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Kensaku | Ikhram</title>
    <meta name="description" content="A lightweight autocomplete plugin for jQuery.">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link type="text/css" rel="stylesheet" href="${request.static_url('kensaku:static/kensaku/css/bootstrap.min.css')}" />
    <link type="text/css" rel="stylesheet" href="${request.static_url('kensaku:static/kensaku/css/bootstrap-theme.min.css')}" />
    ##    <link type="text/css" rel="stylesheet" href="${request.static_url('kensaku:static/kensaku/css/style.css')}" />
        <link type="text/css" rel="stylesheet" href="${request.static_url('kensaku:static/kensaku/plugins/plugins.css')}" />
    <style>
        .ui-autocomplete {
            max-height: 250px;
            overflow-y: auto;
            /* prevent horizontal scrollbar */
            overflow-x: hidden;
        }
        /* IE 6 doesn't support max-height
         * we use height instead, but this forces the menu to always be this tall
         */
        * html .ui-autocomplete {
            height: 250px;
        }
        /* autocomplete adds the ui-autocomplete-loading class to the textbox when it is _busy_ */
        #kensaku.ui-autocomplete-loading {
            background-image: url(${request.static_url('kensaku:static/kensaku/plugins/images/loading.gif')});
            background-position: right center;
            background-repeat: no-repeat;
        }
        .ui-autocomplete-category {
            font-weight: bold;
            padding: .2em .4em;
            margin: .8em 0 .2em;
            line-height: 1.5;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="row">
        <div class="col-md-8 col-sm-8 col-xs-9 bhoechie-tab-container">
            <form id="kensaku-form" accept-charset="UTF-8" data-remote="true" method="get" class="form-horizontal" action="${request.route_url('home')}">
                <div class="row">
                    <div class="col-md-12">
                        <div class="input-group input-group-lg" style="padding-bottom: 30px;">
                            <span class="input-group-addon glyphicon glyphicon-search iconSearchForm"></span>
                            <input id="kensaku" name="q" type="text" class="form-control inputSearchForm" placeholder="Ketik paket umroh yang Anda inginkan" />
                            <!-- <input type="hidden" id="arrPromo" name="arrPromo" /> -->
                            <input type="hidden" id="type" name="type" />
                            <input type="hidden" id="match" name="match" />
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="input-daterange">
                            <div class="row">
                                <div class="col-md-3 h100">
                                    <div class="form-group form-group-lg form-group-icon-left"><i class="fa fa-calendar input-icon input-icon-highlight"></i>
                                        <label class="cl1b9fe0" style="margin-right: -60px;">Rencana Keberangkatan antara :</label>
                                        <div class="input-group bdbae1f5 col-md-11">
                                            <span class="input-group-addon bgWt"><i class="glyphicon glyphicon-calendar" style="color: #a7aeb8;"></i></span>
                                            <input id="startDate" name="startDate" type="text" class="form-control noBdRD noBdCL bdL" style="font-size:16px;">
                                        </div>
                                        <div class="rangSt">S/D</div>
                                    </div>
                                </div>
                                <div class="col-md-3 h100" style="border-right: 1px solid #bbc2c7;">
                                    <div class="form-group form-group-lg form-group-icon-left"><i class="fa fa-calendar input-icon input-icon-highlight"></i>
                                        <label> &nbsp; </label>
                                        <div class="input-group bdbae1f5 col-md-11">
                                            <span class="input-group-addon bgWt"><i class="glyphicon glyphicon-calendar" style="color: #a7aeb8;"></i></span>
                                            <input id="endDate" name="endDate" type="text" class="form-control noBdRD noBdCL bdL" style="font-size:16px;">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-3 h100" style="border-right: 1px solid #bbc2c7;">
                                    <div class="form-group custom-select form-group-lg form-group-select-plus">
                                        <label class="cl1b9fe0"> Biaya Umroh </label>
                                        <select id="whatPrice" name="whatPrice" class="form-control noBdRD bdbae1f5" style="font-size: 15px;">
                                            <option value=''>  - Pilih Kisaran Budget - </option>
                                            <option value=':2000'> <= $2000</option>
                                            <option value='2001 ~ 2500'> $2001 ~ $2500</option>
                                            <option value='2501 ~ 3000'> $2501 ~ $3000</option>
                                            <option value='3001 ~ 4000'> $3001 ~ $4000</option>
                                            <option value='4000:'> >= $4000</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="form-group form-group-lg form-group-select-plus">
                                        <div class="descSearchRight">
                                            <div class="avPack">Tersedia <span id="numPromo" class="numResult">0</span> paket umroh</div>
                                            <div class="avPack">Biaya Mulai <span id="numPrice" class="numResult">US $0</span></div>
                                        </div>
                                        <input class="btn btn-primary btnScFr pull-right" type="submit" id="btn-kensaku" name="btn-kensaku" value="Tampilkan Paket Umroh" disabled />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/plugins/jquery.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/plugins/jquery-ui.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/plugins/jquery-ui-datepicker.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/plugins/jquery-ui-autocomplete.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/moment.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/handlebars-v2.0.0.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/swag.min.js')}"></script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/js/libhelp.js')}"></script>
<script>Swag.registerHelpers(Handlebars);</script>
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/xeasy/easyXDM.js')}"></script>
<script type="text/javascript">
    /**
     * Request the use of the JSON object
     */
    easyXDM.DomHelper.requiresJSON("kensaku/xeasy/json2.js");
    // this is really what you are after
    var xhr = new easyXDM.Rpc({
        // local: "../name.html",
        // swf: REMOTE + "/../easyxdm.swf",
        remote: "http://localhost:6543/static/kensaku/xeasy/cors/"
        // remoteHelper: "http://localhost:6543/static/kensaku/xeasy/name.html"
    }, {
        remote: {
            request: {}
        }
    });

</script>
<script id="acw" type="text/x-handlebars-template">
    <div class="autocomplete-suggestion acomSug acomZZ"
         data-val="{{ResultText}}"
         data-promo="{{ NoOfPromo }}"
         data-match="{{match}}"
         data-type="{{type}}"
         data-sdate="{{startDate}}"
         data-edate="{{endDate}}"
         data-price="{{startPrice}}"
            >
        {{#IsTitle}}
        <div class="headTit">
            <div class="align-left pull-left">{{Header}}</div>
            <div class="pull-right"> <strong>{{NoOfPromo}} Paket</strong></div>
        </div>

        {{/IsTitle}}
        {{^IsTitle}}
        {{#HasImage}}
        <a class="anchor anchorLink acomZZXX" tabindex="-1">
            <img src="{{Image}}" data-2x="{{RetinaImage}}" height="50" width="50" alt="">
            <ul class="list-plain align-left">
                <li><strong id="autoCompleteText">{{capitalizeEach ResultText}}, Harga mulai US${{startPrice}}, Diskon Hingga {{endDisc}}</strong></li>
            </ul>
            <span class="align-right"><strong class="pull-right">{{NoOfPromo}} Paket</strong></span>
        </a>
        {{/HasImage}}
        {{^HasImage}}
        {{#IsDefault}}
        <!-- autocomplete paket populer -->
        <a class="anchor anchorLink" tabindex="-1">
            <div class="pull-left">
                <i class="fa">
                    <img class="ideIcon" src="assets/newfrontend/images/biro-thumb/{{agent_slug}}.jpg" width="40px">
                </i>
                <span class="align-left autoBiro"><img src="assets/newfrontend/images/fa-{{airline_name}}.png" style="margin-top:3px;"></span>
                <span class="align-left autoBiro"><img src="assets/newfrontend/images/{{rates_hotel}}-star.png" style="margin-left: 35px;margin-top:3px;"></span>
            </div>
            <div class="align-left pull-left" id="autoCompleteText">{{capitalizeEach ResultText}} </div>
            <div class="pull-right">Biaya umroh mulai <strong><small><s>US$ {{add startPrice endDisc}}</small></s></strong> <strong>US$ {{startPrice}}</strong>
            </div>
        </a>
        {{/IsDefault}}
        {{^IsDefault}}
        {{#is tagging 'PACKETS'}}
        <div class="pull-left">
            <i class="fa">
                <img class="ideIcon" src="assets/newfrontend/images/biro-thumb/{{agent_slug}}.jpg" width="40px"></i>
            <span class="align-left autoBiro"><img src="assets/newfrontend/images/fa-{{airline_name}}.png" style="margin-top:3px;"></span>
            <span class="align-left autoBiro"><img src="http://aux3.ikhram.com/assets/newfrontend/images/{{rates_hotel}}-star.png" style="margin-left: 35px;margin-top:3px;"></span>
        </div>
        {{else}}
        <div class="pull-left">
            <i class="fa"><img class="ideIcon" src="assets/newfrontend/images/biro-umroh-search.png"></i>
            <span class="align-left autoBiro" id="autoCompleteText">{{agent_city}}</span>
        </div>
        {{/is}}
        <div class="align-left pull-left" id="autoCompleteText">{{capitalizeEach ResultText}}  </div>
        <div class="pull-right">
                  <span style="padding-right:15px;">Biaya umroh mulai
                    <strong><small><s>US$ {{add startPrice endDisc}}</s></small></strong>
                    <strong>US$ {{startPrice}}</strong>
                  </span>
            <strong>{{NoOfPromo}} Paket</strong>
        </div>
    </div>
    {{/IsDefault}}
    {{/HasImage}}
    {{/IsTitle}}
    </div>
</script>
<script type="text/javascript">
    $.widget("ikhram.promoautocomplete", $.ui.autocomplete, {
        options: {
            headerWrapper: '',
            renderer: false
        },
        _create: function() {
            this._super();
            this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
            this._term = '';
        },
        _renderMenu: function(ul, items) {
            var that = this;
            if($.isFunction(that.options.renderer)) {
                that.options.renderer(ul, items, that._renderItemData());
            }
            that._super(ul, items);
        },
        _renderItem: function(ul, item) {
##            var hl = item.ResultText.replace(new RegExp(".*(" + this.term + ").*", "i"),
##                    function(a, b, c, d) {
##                        return a.replace(new RegExp(b, "ig"),
##                                        '<span style="font-weight:bold;">' + b + "</span>")
##                    });
##
##            return $( "<li>" )
##                    .attr( "data-value", item.ResultText )
##                    .append( hl )
##                    .appendTo( ul );
        }
    });
    $(function(){
        var kensakuauto = $('#kensaku').promoautocomplete({
            _term: '',
            headerWrapper: '<div class="header-acs"><img class="ideIcon" src="assets/newfrontend/images/ide.png"><span>Ketik paket umroh yang anda cari. <span class="contoh">Contoh: <b> Langsung madinah, Plus Turki, Garuda Indonesia, Mei 2015, Hari kejepit, Patuna Travel </b></span></span></div>',
            minLength: 0,
            autoFocus: true,
            renderer: function(ul, items, data) {
                var that = this;
                console.log(that._term);
                // set header auto complete unless term < 0
                //if(0 >= that.term.toString().length) ul.append(that.options.headerWrapper);
                $.each(items, function(i, item){
                    item.value = item.ResultText;
                    console.log(item);
                    if(item.IsTitle) {
                        ul.append("<li class='ui-autocomplete-category'>"+ item.Header + "</li>");
                    } else data(ul, item);
                });

            },
            source: function(request, response) {
                $.ajax({
                    url: '${request.route_url('results_build')}',
                    method: 'POST',
                    data: {
                        q: request.term
                    },
                    dataType: "json",
                    success: function (data) {
                        response(data);
                    }
                });
            },
            search: function(ev, ui) {
                console.log('--- hail kensaku ---');
            },
            focus: function(ev, ui) {
                //console.log(ui.item);
                console.log("--- focus ---");
            },
            delay: 0,
            select: function(ev, ui) {
                console.log("--- select ---");
                var item = ui.item;
                this._selectedItem = item;
                setTimeout(function() {
                    // set data di form
                    //$(this).val(ui.item.ResultText);
                }, 10);

            },
            close: function(ev, ui) {
                $(this).promoautocomplete("close");
            }
        });
        kensakuauto.unbind("click").bind("click", function() {
            $(this).promoautocomplete('search', this._term);
        });
        var d = [
            kensaku.keyCode.UP, kensaku.keyCode.DOWN, kensaku.keyCode.LEFT,
            kensaku.keyCode.RIGHT, kensaku.keyCode.ESCAPE, kensaku.keyCode.ENTER,
            kensaku.keyCode.TAB, kensaku.keyCode.CONTROL, kensaku.keyCode.ALT,
            kensaku.keyCode.SHIFT, kensaku.keyCode.CAPS_LOCK, kensaku.keyCode.COMMAND,
            kensaku.keyCode.HOME, kensaku.keyCode.INSERT, kensaku.keyCode.WINDOWS,
            kensaku.keyCode.BACKSPACE
        ];
        kensakuauto.unbind("keyup").bind("keyup", function(ev) {
            0 <= d.indexOf(ev.keyCode) || (this._term = kensakuauto.val())
            console.log('ubind - bind : keyup' + this._term);
        });

        var nowTemp = new Date();
        var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);

        var sd = $( "#startDate" ).datepicker({
            format: "dd-mm-yyyy",
            onRender: function(date){
                return date.valueOf() < now.valueOf() ? 'disabled' : '';
            }
        }).on('changeDate', function(e) {
            var newDate = new Date(e.date)
            if (e.date.valueOf() > ed.date.valueOf()) {
                newDate.setDate(newDate.getDate() + 1);
                ed.setValue(newDate);
            }

            var startDate = e.date;
            var endDate = ed.date;
            console.log(startDate + ' // ' + moment(new Date(endDate)).format('DD-MM-YYYY'));
            sd.hide();
            $('#endDate')[0].focus();
            valid_button(startDate, endDate);
        }).data('datepicker');

        var ed =  $( "#endDate" ).datepicker({
            format: "dd-mm-yyyy",
            onRender: function(date){
                return date.valueOf() <= sd.date.valueOf() ? 'disabled' : '';
            }
        }).on('changeDate', function(e) {
            var startDate = sd.date;
            var endDate = e.date;
            ed.hide();
            valid_button(startDate, endDate);
        }).data('datepicker');

        $("#whatPrice").change(function() {
            var startDate = sd.date;
            var endDate = ed.date;
            valid_button(startDate, endDate);
        });

        var valid_button = function(sdate, edate) {
            var startDate = moment(new Date(sdate)).format('DD-MM-YYYY');
            var endDate = moment(new Date(edate)).format('DD-MM-YYYY');;
            var price = $('#whatPrice').val();
            var match = $('#match').val();
            var type = $('#type').val();
            var q = $('#kensaku').val().toString().split(',')[0];

            xhr.request({
                url: "http://localhost:6543/api/v1/valid",
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest"
                },
                data: {
                    q: q,
                    match: match,
                    type: type,
                    startDate: startDate,
                    endDate: endDate,
                    whatPrice: price
                }
            }, function(data){
                var json = easyXDM.getJSONObject().parse(data.data);
                // console.log(json);
                $('#numPrice').html('US$' + json.data.price);
                $('#numPromo').html(json.data.count).trigger('numChanged');
            });
        }
        var num = $('#numPromo');
        num.bind('numChanged', function(){
            var submitter = $('#btn-kensaku');
            if(submitter.is(":disabled")){
                submitter.removeAttr('disabled');
            }
            if(num.html() <= 0){
                $('#btn-kensaku').attr('disabled', 'disabled');
            }

        });
    });
</script>
</body>
</html>