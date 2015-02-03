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


 $(function(){
        var hightlander = new Hilitor('wacs');
        hightlander.setMatchType("left");
        $('#kensaku').autoComplete({
          minChars: 0,
          wrapperHeader: '<div class="header-acs"><img class="ideIcon" src="assets/newfrontend/images/ide.png"><span>Ketik paket umroh yang anda cari. <span class="contoh">Contoh: <b> Langsung madinah, Plus Turki, Garuda Indonesia, Mei 2015, Hari kejepit, Patuna Travel </b></span></span></div>',
          source: function(term, response){
                // try { xhr.abort(); } catch(e){}

                xhr.request({
                  url: "http://localhost:6543/api/v1/result",
                  method: "POST",
                  data: {
                    q: term,
                    match: '',
                    type: '',
                  }
                }, function(rpcdata){
                  var json = easyXDM.getJSONObject().parse(rpcdata.data);
                  // console.log(rpcdata.data);
                  response(json);
                  // var xhr = $.getJSON('localhost:6543/results', { q: term }, function(data){ response(data);
                  }, function(errors){

                  });
              },
              renderItem: function (item, search){
                // ##console.log(item);
                var tpl = $('#acw').html();
                // ##Mustache.parse(tpl);
                var template = Handlebars.compile(tpl);
                // ##return Mustache.render(tpl, item);
                return template(item);
              },
              onSelect: function(self, term, promo) {
                // var countPromo = 0;
                // var splto = promo.toString().split(",");
                // if(splto.length > 0 ) {
                //   countPromo = splto.length;
                // }

                $('#numPrice').html('US$' + self[0].dataset.price);
                $('#numPromo').html(promo).trigger('numChanged');
                // $('#arrPromo').val(promo);
                $('#match').val(self[0].dataset.match);
                $('#type').val(self[0].dataset.type);

                sd.setValue(new Date(moment(self[0].dataset.sdate).format("YYYY-MM-DD")));
                ed.setValue(new Date(moment(self[0].dataset.edate).format("YYYY-MM-DD")));
              },
              onShow: function(term) {
                hightlander.apply(term);
              },
              onKeydown: function(term){
                hightlander.apply(term);
              }
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
    // var arr = $('#arrPromo').val();
      //format date 'dd-MM-YYYY'
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
          // arrPromo: arr,
          q: q,
          match: match,
          type: type,
          startDate: startDate,
          endDate: endDate,
          whatPrice: price
        },
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

$('#remove-query').click(function(){

  var test = "oke je";

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

  $('#kensaku').val('');
  $('#numPrice').html('US$' + 0);
  $('#numPromo').html(0).trigger('numChanged');
  $('#arrPromo').val('');

  var date_now = moment(new Date()).format('DD-MM-YYYY');

  sd.setValue(now);
  ed.setValue(now);

  $('#startDate').val('');
  $('#endDate').val('');
  $('#kensaku').focus();
  $('#kensaku').removeClass("inputSearchRightForm");
  $('#remove-query').hide();
})
