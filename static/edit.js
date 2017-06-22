function edit_show(num) {
    var row = $('tr[data-num=' + num + ']');
    row.children('.edit-off').hide();
    row.children('.edit-on').show();
}

function getData(row) {
    var data = {};
    if (isCommune()) {
        data['address'] = row.find('input').val();
        if (curNum != -1)
            data['commune'] = curNum;
        row.find('input[type=number]').each(function (i, el) {
            data['votes_' + (i + 1)] = parseInt(el.value);
        });
    }
    else {
        data['name'] = row.find('input').val();
        if (curNum != -1) {
            if (isDistrict())
                data['district'] = curNum;
            else if (isVoivodeship())
                data['voivodeship'] = curNum;
        }
    }
    return data;
}

function edit_submit(num) {
    var row = $('tr[data-num=' + num + ']');
    showLoading();

    $.ajax({
        url: getDownLink(num), type: 'PUT', data: getData(row), dataType: 'json',
        success: function (data) {
            if (data.result == 'success') {
                refresh("Pomyślnia edycja.");
            }
            else {
                statusMessage("Błąd przy edycji: " + data.result);
                hideLoading();
            }
        }
    });
}

function edit_unpin(num) {
    var row = $('tr[data-num=' + num + ']');
    var data = {};
    showLoading();

    if (isCommune())
        data['commune'] = null;
    else if (isDistrict())
        data['district'] = null;
    else if (isVoivodeship())
        data['voivodeship'] = null;

    $.ajax({
        url: getDownLink(num), type: 'PUT', data: data, dataType: 'json',
        success: function (data) {
            if (data.result == 'success') {
                refresh("Pomyślnie odpięto.");
            }
            else {
                statusMessage("Błąd przy odpinaniu: " + data.result);
                hideLoading();
            }
        }
    });
}

function edit_pin(num) {
    var row = $('tr[data-num=' + num + ']');
    var data = {};
    showLoading();

    if (isCommune())
        data['commune'] = curNum;
    else if (isDistrict())
        data['district'] = curNum;
    else if (isVoivodeship())
        data['voivodeship'] = curNum;

    $.ajax({
        url: getDownLink(num), type: 'PUT', data: data, dataType: 'json',
        success: function (data) {
            if (data.result == 'success') {
                refresh("Pomyślnie przypięto.");
            }
            else {
                statusMessage("Błąd przy przypinaniu: " + data.result);
                hideLoading();
            }
        }
    });
}

function edit_add() {
    var row = $('tr[data-num=' + new_num + ']');
    showLoading();

    $.ajax({
        url: '/' + levels[curLevel + 1], type: 'PUT', data: getData(row), dataType: 'json',
        success: function (data) {
            if (data.result == 'success') {
                refresh("Pomyślnie dodano wpis.");
            }
            else {
                statusMessage("Błąd: " + data.result);
                hideLoading();
            }
        }, error: function () {
            statusMessage("Błąd.");
            hideLoading();
        }
    });
}

function edit_delete(num) {
    var row = $('tr[data-num=' + num + ']');
    showLoading();

    $.ajax({
        url: getDownLink(num), type: 'DELETE', dataType: 'json',
        success: function (data) {
            if (data.result == 'success') {
                refresh("Pomyślnie usunięto wpis.");
            }
            else {
                statusMessage("Błąd: " + data.result);
                hideLoading();
            }
        }
    });
}

function update_row(num) {
    var row = $('tr[data-num=' + num + ']');
    var x = 0;

    row.find('input[type=number]').each(function (i, el) {
        x += parseInt(el.value);
    });
    row.children('.total').text(x);
}