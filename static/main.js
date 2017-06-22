/**
 * Created by yeti on 05.05.17.
 */
 
var levels = ['kraj', 'woj', 'okrag', 'gmina', 'obwod'];
var curLevel, curNum, searchUrl;
var new_num = 666, unpin_num = 667;

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

function canGoDown() {
    return curLevel < 3;
}

function isCommune() {
    return curLevel == 3;
}

function isDistrict() {
    return curLevel == 2;
}

function isVoivodeship() {
    return curLevel == 1;
}

function isCountry() {
    return curLevel == 0;
}

function canEdit(data) {
    return data.user != '';
}

function getDownLink(num) {
    if (curLevel > 3) {
        console.log("Can't go down!");
        return '';
    }
    return '/' + levels[curLevel + 1] + '/' + num;
}

function getBackLink(num) {
    if (!canGoDown()) {
        console.log("Can't go down!");
        return '';
    }
    return '/' + levels[curLevel + 1] + '/' + num;
}

function getCurLink() {
    if (isSearch) {
        return '/szukaj?' + curNum;
    }
    return '/' + levels[curLevel] + '/' + curNum;
}

function statusMessage(msg) {
    $('span#msg').text(msg);
}

function showLoading() {
    $('#loading').show();
}

function hideLoading() {
    $('#loading').hide();
}

function getFormData(form) {
    var unindexed_array = form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function (n, i) {
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function updateLoginInfo(data) {
    if (data.user != '') {
        $('span#username').text(data.user);
        $('span#logged_out').hide();
        $('span#logged_in').show();
    } else {
        $('span#logged_out').show();
        $('span#logged_in').hide();
    }
}
 
function fillData(data) {
	$('table.candidates tbody').empty();
	$('table.regions thead tr th.thin').remove();
	$('table.regions tbody').empty();
	$('button#back').remove();
	$('button#refresh').remove();
	downLink = data.down;
	
	$.each(data.candidates, function(i, el){
		var row = $('<tr>');
		row.append('<td>' + el.name + '</td>');
		row.append('<td class="num">' + el.votes + '</td>');
		row.append('<td><div><div style="width:' + el.votes_percent + '; background-color:' + el.color + ';">' + el.votes_percent + '</div></div></td>');
		$('table.candidates tbody').append(row);

		$('table.regions thead tr').append('<th class="thin">' + el.name + '</th>');
	});
	
	$.each(data.regions, function(i, el){
	    var row = $('<tr data-num=' + el.n + '>');
		
		if (canGoDown())
		    row.append('<td class="edit-off"><button onclick="goTo(' + (curLevel + 1) + ', ' + el.n + ', \'\');">' + escapeHtml(el.name) + '</button></td>');
		else
		    row.append('<td class="edit-off">' + escapeHtml(el.name) + '</td>');

		row.append('<td class="edit-on"><input type="text" value="' + escapeHtml(el.name) + '"></td>');
		
		row.append('<td class="edit-off edit-on num total">' + el.total + '</td>');
		
		$.each(el.candidate_votes, function (i, v) {
            if (canGoDown())
                row.append('<td class="edit-off edit-on num thin">' + v + '</td>');
            else {
                row.append('<td class="edit-off num thin">' + v + '</td>');
                row.append('<td class="edit-on thin"><input type="number" oninput="update_row(' + el.n + ')" value="' + v + '"></td>');
            }
		});
		
		if (canEdit(data)) {
            if (!isCountry())
		        row.append('<td class="edit-off"><button onclick="edit_show(' + el.n + ')">Edytuj</button>' +
                           '<button onclick="edit_unpin(' + el.n + ')">Odepnij</button></td>');
            else
                row.append('<td class="edit-off"><button onclick="edit_show(' + el.n + ')">Edytuj</button></td>');

		    row.append('<td class="edit-on"><button onclick="edit_submit(' + el.n + ')">Zapisz</button>' +
                       '<button onclick="edit_delete(' + el.n + ')">Usuń</button></td>');
		}
		
		$('table.regions tbody').append(row);
		row.children('.edit-on').hide();
		row.children('.edit-off').show();
	});

	if (canEdit(data)) {
	    var row = $('<tr data-num=' + new_num + '>');
	    row.append('<td class="edit-on"><input type="text" value=""></td>');
	    row.append('<td class="edit-off edit-on num total">0</td>');
	    $.each(data.candidates, function (i, v) {
	        if (canGoDown())
	            row.append('<td class="edit-off edit-on num thin">0</td>');
	        else
	            row.append('<td class="edit-on thin"><input type="number" oninput="update_row(' + new_num + ')" value="0"></td>');
	    });
	    row.append('<td class="edit-on"><button onclick="edit_add(' + new_num + ')">Dodaj</button></td>');
	    $('table.regions tbody').append(row);
	}

	if (data.dangling && data.dangling.length > 0) {
	    $('table.regions tbody').append('<tr><td colspan=15>Zwisające:</td></tr>');
	    $.each(data.dangling, function (i, el) {
	        var row = $('<tr data-num=' + el.n + '>');

	        if (canGoDown())
	            row.append('<td class="edit-off"><button onclick="goTo(' + (curLevel + 1) + ', ' + el.n + ', \'\');">' + escapeHtml(el.name) + '</button></td>');
	        else
	            row.append('<td class="edit-off">' + escapeHtml(el.name) + '</td>');

	        row.append('<td class="edit-on"><input type="text" value="' + escapeHtml(el.name) + '"></td>');

	        row.append('<td class="edit-off edit-on num total">' + escapeHtml(el.name) + '</td>');

	        $.each(el.candidate_votes, function (i, v) {
	            if (canGoDown())
	                row.append('<td class="edit-off edit-on num thin">' + v + '</td>');
	            else {
	                row.append('<td class="edit-off num thin">' + v + '</td>');
	                row.append('<td class="edit-on thin"><input type="number" oninput="update_row(' + el.n + ')" value="' + v + '"></td>');
	            }
	        });

	        if (canEdit(data)) {
	            if (!isCountry())
	                row.append('<td class="edit-off"><button onclick="edit_show(' + el.n + ')">Edytuj</button>' +
                               '<button onclick="edit_pin(' + el.n + ')">Przypnij</button></td>');
	            else
	                row.append('<td class="edit-off"><button onclick="edit_show(' + el.n + ')">Edytuj</button></td>');

	            row.append('<td class="edit-on"><button onclick="edit_submit(' + el.n + ')">Zapisz</button>' +
                           '<button onclick="edit_delete(' + el.n + ')">Usuń</button></td>');
	        }

	        $('table.regions tbody').append(row);
	        row.children('.edit-on').hide();
	        row.children('.edit-off').show();
	    });
	}
	
	$('nav').prepend('<button id="refresh" style="float: left;" onclick="refresh(\'\');">Odśwież</button>');
	if (!isCountry())
	    $('nav').prepend('<button id="back" style="float: left;" onclick="goTo(' + (curLevel - 1) + ', ' + data.back + ', \'\');">Powrót</button>');
}

function refresh(text) {
    if (searchUrl) {
        search(searchUrl);
        statusMessage(text);
    }
    else
        goTo(curLevel, curNum, text)
}

function goTo(level, num, text) {
    var url = '/' + levels[level] + '/' + num;
    curLevel = level;
    curNum = num;
    searchUrl = null;
    showLoading();

	if (localStorage.getItem(url)) {
		fillData(JSON.parse(localStorage.getItem(url)));
	}
	$.getJSON(url, function(data, status){
		localStorage.setItem(url, JSON.stringify(data));
		fillData(data);
		hideLoading();
		statusMessage(text);
		updateLoginInfo(data);
	});
}

function search(url) {
    var selected = $('form#search').find('option:selected').val()
    if (!url)
        url = '/szukaj?type=' + selected + '&' + $('form#search').serialize();

    searchUrl = url;
    curLevel = levels.indexOf(selected) - 1;
    curNum = -1;
    $.getJSON(url, function (data, status) {
        if (data.result && data.result != 'success')
            statusMessage(data.result);
        else {
            fillData(data);
            hideLoading();
            statusMessage('Pomyślne wyszukiwanie.');
            updateLoginInfo(data);
            $('form#search input[name=q]').val('');
        }
    });
}
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    $.ajaxSetup({
        contentType: 'application/json',
        processData: false,
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        if (options.data) {
            options.data = JSON.stringify(options.data);
        }
    });

    $('form#login').children('input').keypress(function (e) {
        // Enter pressed?
        if (e.which == 10 || e.which == 13) {
            login();
        }
    });
    $('form#register').children('input').keypress(function (e) {
        // Enter pressed?
        if (e.which == 10 || e.which == 13) {
            register();
        }
    });

	goTo(0, 0, '');
});