/**
 * Created by surya on 05/12/14.
 */

input.autoComplete({
    minChars: 1,
    source: function (term, suggest) {
        $.ajax({
            url: dateUrl,
            data: 'term=' + term,
            method: "GET",
            dataType: "jsonp",
            success: function (data, textStatus, jqXhr) {
                suggest(data);
            }
        });
    },
    renderItem: function (item, search) {
        var userInfo = userStore.get(item.user_id) || {},
            tpl = {
                status: userInfo.status || 'none',
                photo: item.photo || defaultImagePath,
                name: item.label || 'Unknown',
                groups: userInfo.group || ''
            };

        return '<div class="autocomplete-suggestion" data-val="' + tpl.name + '">' +
            '<div class="status status-' + tpl.status + '"></div>' +
            '<div class="image"><img src="' + tpl.photo + '"></div>' +
            '<div class="info">' +
            '<div class="name">' + tpl.name + '</div>' +
            '<div class="groups">' + tpl.groups + '</div>' +
            '</div>' +
            '</div>';
    }
});