document.searchcount = 0;

function update() {
    var q = $("#q");
    var r = $("#results");
    var qs = q.val();
    var oq = q.attr("data-oldq");
    console.log(q.val().length);
    var lan = q.val().length;

//    if (lan % 2 == 0 ) {
//        if (qs != oq) {
    q.attr("data-oldq", qs);
    $.ajax({
        url: "results",
        data: {"q": qs, "count": document.searchcount + 1}
    }).success(function (data, status, xhr) {
        var html = $(data);
        var count = Number(html.find("#count").val());
        if (count >= document.searchcount) {
            r.html(html);
            document.searchcount = count;
        }
    });
//        }
//    }
}

document.count = 0
$(document).ready(function() {
    $("#q").keypress(function(event){
        console.log("Key: " + event.which);
        if( event.which != 8 ){
            update();
        }
    });
    update();
});
