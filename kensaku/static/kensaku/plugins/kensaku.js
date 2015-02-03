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
        // set wrapper empty result
        console.log(items.length);
        if(2 < items.length) {
            that.options._focusedItem = items[1];
            // set header all promo item
            // var tpl = $('#acw-header').html(),
            //     template = Handlebars.compile(tpl);
            //     ul.append(template(items[0]));
            //     fitem = items[0];
            //     itm = $.extend({}, fitem, {
            //         label: fitem.ResultText || '',
            //         value: fitem.ResultText || '',
            //         term: that.options._term || ''
            //     });
            //     that._renderItemData(ul, itm);
            // end set
            $.each(items, function (i, item) {
                item = $.extend({}, item, {
                    label: item.ResultText || '',
                    value: item.ResultText || '',
                    term: that.options._term || ''
                });
                that._renderItemData(ul, item);
            });
        } else {
            // empty wrapper
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
        headerWrapper: '<div class="ui-autocomplete-category header-acs">' +
            '<img class="ideIcon" src="assets/newfrontend/images/ide.png">' +
            '<span>Ketik paket umroh yang anda cari.<br /> <span class="contoh">Contoh: <b> ' +
            'Langsung madinah, Plus Turki, Garuda Indonesia, Mei 2015, Hari kejepit, ' +
            'Patuna Travel </b></span></span></div>',
        emptyWrapper: '<div class="ui-autocomplete-category header-acs">' +
            '<img class="ideIcon" src="assets/newfrontend/images/sadface.png">' +
            'Kata Kunci Tidak ditemukan<div/>',
        minLength: 0,
        delay: 0,
        autoFocus: false,
        source: function(request, response) {
            xhr.request({
                    url: "http://localhost:6543/api/v1/result",
                    method: "POST",
                    data: {
                        q: request.term,
                        match: '',
                        type: ''
                    }
                },
                function(rpcdata){
                    var json = easyXDM.getJSONObject().parse(rpcdata.data);
                    // console.log(rpcdata.data);
                    response(json);
                    // var xhr = $.getJSON('localhost:6543/results', { q: term }, function(data){ response(data);
                }, function(errors){});
        },
        search: function(ev, ui) {
            console.log('--- hail kensaku ---');
            //console.log(ui);
        },
        focus: function(ev, ui) {
            console.log("--- focus --");
            var that = $(this).promoautocomplete("instance");
            if(ui.item) that.options._focusedItem = ui.item;
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
        if(that.options._term !== that._value())that._value(that.options._term);
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