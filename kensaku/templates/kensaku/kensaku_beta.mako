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
                            <input id="kensaku" name="txtinput" type="text" class="form-control inputSearchForm" placeholder="Ketik paket umroh yang Anda inginkan" />
                            <!-- <input type="hidden" id="arrPromo" name="arrPromo" /> -->
                            <input type="hidden" id="q" name="q" />
                            <input type="hidden" id="type" name="type" />
                            <input type="hidden" id="match" name="match" />
                            <div class="resultBox autocomplete-suggestions"></div>
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
<script type="text/javascript" src="${request.static_url('kensaku:static/kensaku/plugins/bootstrap-datepicker.js')}"></script>
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
    <span class="autocomplete-suggestion acomSug acomZZ"
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
            <span class="align-left pull-left">{{Header}}</span>
            <span class="pull-right"><strong>{{NoOfPromo}} Paket</strong></span>
        </div>
        {{/IsTitle}}
        {{^IsTitle}}
        {{#HasImage}}
        <a class="anchor anchorLink acomZZXX" tabindex="-1">
            <img src="{{Image}}" data-2x="{{RetinaImage}}" height="50" width="50" alt="">
            <ul class="list-plain align-left">
                <li><strong id="autoCompleteText">{{{chain 'capitalizeEach' 'cahaya' ResultText term=term}}}, Harga mulai US${{startPrice}}, Diskon Hingga {{endDisc}}</strong></li>
            </ul>
            <span class="align-right"><strong class="pull-right">{{NoOfPromo}} Paket</strong></span>
        </a>
        {{/HasImage}}
        {{^HasImage}}
        {{#IsDefault}}
        <!-- autocomplete paket populer -->
        <a class="anchor anchorLink" tabindex="-1">
            <span class="pull-left">
                <i class="fa">
                    <img class="ideIcon" src="assets/newfrontend/images/biro-thumb/{{agent_slug}}.jpg" width="40px">
                </i>
                <span class="align-left autoBiro"><img src="assets/newfrontend/images/fa-{{airline_name}}.png" style="margin-top:3px;"></span>
                <span class="align-left autoBiro"><img src="assets/newfrontend/images/{{rates_hotel}}-star.png" style="margin-left: 35px;margin-top:3px;"></span>
            </span>
            <span class="align-left pull-left" id="autoCompleteText">{{{chain 'capitalizeEach' 'cahaya' ResultText term=term}}} </span>
            <span class="pull-right">Biaya umroh mulai <strong><small><s>US$ {{add startPrice endDisc}}</s></small></strong> <strong>US$ {{startPrice}}</strong>
            </span>
        </a>
        {{/IsDefault}}
        {{^IsDefault}}
        {{#is tagging 'PACKETS'}}
        <span class="pull-left">
            <i class="fa">
                <img class="ideIcon" src="assets/newfrontend/images/biro-thumb/{{agent_slug}}.jpg" width="40px"></i>
            <span class="align-left autoBiro"><img src="assets/newfrontend/images/fa-{{airline_name}}.png" style="margin-top:3px;"></span>
            <span class="align-left autoBiro"><img src="http://aux3.ikhram.com/assets/newfrontend/images/{{rates_hotel}}-star.png" style="margin-left: 35px;margin-top:3px;"></span>
        </span>
        {{else}}
        <span class="pull-left">
            <i class="fa"><img class="ideIcon" src="assets/newfrontend/images/biro-umroh-search.png"></i>
            <span class="align-left autoBiro" id="autoCompleteText">{{agent_city}}</span>
        </span>
        {{/is}}
        <span class="align-left pull-left" id="autoCompleteText">{{{chain 'capitalizeEach' 'cahaya' ResultText term=term}}} </span>
        <span class="pull-right">
                  <span style="padding-right:15px;">Biaya umroh mulai
                    <strong><small><s>US$ {{add startPrice endDisc}}</s></small></strong>
                    <strong>US$ {{startPrice}}</strong>
                  </span>
            <strong>{{NoOfPromo}} Paket</strong>
        </span>
    {{/IsDefault}}
    {{/HasImage}}
    {{/IsTitle}}
    </span>
</script>
<script type="text/javascript">
$.widget("ikhram.promoautocomplete", $.ui.autocomplete, {
    options: {
        headerWrapper: '',
        emptyWrapper: '',
        renderer: false,
        _term: '',
        suggest: false,
        _focusedItem: ''
    },
    _create: function() {
        this._super();
        this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
        this._term = '';
    },
    _renderMenu: function(ul, items) {
        var that = this;
        // set header auto complete unless term < 0
        if(0 >= that.options._term && 2 < items.length) ul.append(that.options.headerWrapper);
        // sett wrapper empty result
        console.log(items.length);
        if(2 < items.length) {
            that.options._focusedItem = items[1];
            $.each(items, function (i, item) {
                item = $.extend({}, item, {
                    label: item.ResultText || '',
                    value: item.ResultText || '',
                    term: that.options._term || ''
                });
                that._renderItemData(ul, item);
            });
        } else {
            that.options._focusedItem = '';
            ul.append(that.options.emptyWrapper);
            $.each(items, function (i, item) {
                item = $.extend({}, item, {
                    label: '',
                    value: that.options._term,
                    term: that.options._term || ''
                });
                that._renderItemData(ul, item);
            });
        }
    },
    _renderItem: function(ul, item) {
        var that = this,
            head = '',
            tpl = $('#acw').html(),
            template = Handlebars.compile(tpl);
        // set template
        if(item.IsTitle) head = 'ui-autocomplete-category';
        if(that.options._focusedItem == '') {
            return $( "<li>")
                    .css('display', 'none')
                    .append('')
                    .appendTo(ul);
        }
        return $( "<li>" )
                .addClass(head)
                .append( template(item) )
                .appendTo( ul );
    },
    close: function(event){
        var that = this;
        that._super(event);
    }
});
$(function(){
    var kensakuauto = $('#kensaku').promoautocomplete({
        query: '',
        headerWrapper: '<div class="ui-autocomplete-category header-acs"><img class="ideIcon" src="assets/newfrontend/images/ide.png"><span>Ketik paket umroh yang anda cari. <span class="contoh">Contoh: <b> Langsung madinah, Plus Turki, Garuda Indonesia, Mei 2015, Hari kejepit, Patuna Travel </b></span></span></div>',
        emptyWrapper: '<div class="ui-autocomplete-category header-acs">Kata Kunci Tidak ditemukan<div/>',
        minLength: 0,
        delay: 0,
        autoFocus: false,
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
            //console.log(ui);
        },
        focus: function(ev, ui) {
            console.log("--- focus --");
            var that = $(this).promoautocomplete("instance");
            console.log(that.options._focusedItem);
            if(ui.item) that.options._focusedItem = ui.item;
            //console.log(this._focusedItem);
        },
        select: function(ev, ui) {
            console.log("--- select ---");
            var that = $(this).promoautocomplete("instance"),
                    item = ui.item;
            setTimeout(function() {
                // set data di form
                that.options._pushData(item, that);
                //$(this).val(ui.item.ResultText);
            }, 10);
        },
        close: function(ev, ui) {
            console.log("--- close --");
        },
        open: function(ev, ui){
            console.log("--- open --");
            var that = $(this).promoautocomplete("instance"),
                    menu = that.widget().find('.ui-menu-item').eq(0);
            menu.addClass('ui-state-focus');
            that._trigger("focus", ev, ui);
        },
        // saat negara api mulai beranjak dewasa
        _pushData: function(item, self) {
            var that = $(this).promoautocomplete("instance");
            console.log("---_watch --");
            console.log(self.options._term);
            $('#numPrice').html('US$' + item.startPrice);
            $('#numPromo').html(item.NoOfPromo).trigger('numChanged');
            $('#q').val(self.options._term);
            $('#match').val(item.match);
            $('#type').val(item.type);

            sd.setValue(new Date(moment(item.startDate).format("YYYY-MM-DD")));
            ed.setValue(new Date(moment(item.endDate).format("YYYY-MM-DD")));

        }
    });
    var d = [
        kensaku.keyCode.UP, kensaku.keyCode.DOWN, kensaku.keyCode.LEFT,
        kensaku.keyCode.RIGHT, kensaku.keyCode.ESCAPE, kensaku.keyCode.ENTER,
        kensaku.keyCode.TAB, kensaku.keyCode.CONTROL, kensaku.keyCode.ALT,
        kensaku.keyCode.SHIFT, kensaku.keyCode.CAPS_LOCK, kensaku.keyCode.COMMAND,
        kensaku.keyCode.HOME, kensaku.keyCode.INSERT, kensaku.keyCode.WINDOWS

    ];
    kensakuauto.bind("keyup", function(ev) {
        var that = $(this).promoautocomplete("instance");
        0 <= d.indexOf(ev.keyCode) || (that.options._term = kensakuauto.val());
        console.log('ubind - bind : keyup' + that.options._term);
    });
    kensakuauto.bind("click", function() {
        console.log("---click---");
        var that = $(this).promoautocomplete("instance");
        $(this).promoautocomplete('search', that.options._term);
        that._value(that.options._term);
    });
    kensakuauto.bind("blur", function(ev) {
        var that = $(this).promoautocomplete("instance"),
                menu = $('.ui-menu-item .ui-state-focus'),
                item = that.options._focusedItem;
        if(typeof item === "object") {
            that._value(item.ResultText);
        } else that._value(item);
        that.options._pushData(item, that);
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
        var endDate = moment(new Date(edate)).format('DD-MM-YYYY');
        var price = $('#whatPrice').val();
        var match = $('#match').val();
        var type = $('#type').val();
        var input = $('#kensaku').val();
        var q = $('#q').val();

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