
function login() {
    showLoading();
    $.post('/auth/login', getFormData($('form#login')), function (data) {
        if (data.result == 'success') {
            $('span#username').text(data.user);
            $('input[name="username"]').val('');
            $('input[name="password"]').val('');
            $('span#logged_out').hide();
            $('span#logged_in').show();
            refresh('Pomyślne logowanie.');
        } else {
            statusMessage('Błąd przy logowaniu.');
            hideLoading();
        }
    });
}

function logout() {
    showLoading();
    $.post('/auth/logout', {}, function (data) {
        if (data.result == 'success') {
            $('span#logged_out').show();
            $('span#logged_in').hide();
            refresh('Pomyślne wylogowanie.');
        } else {
            statusMessage('Błąd przy wylogowaniu.');
            hideLoading();
        }
    });
}

function register() {
    showLoading();
    $.post('/auth/register', getFormData($('form#register')), function (data) {
        if (data.result == 'success') {
            $('span#username').text(data.user);
            $('input[name="username"]').val('');
            $('input[name="password"]').val('');
            $('span#logged_out').hide();
            $('span#logged_in').show();
            $('#register_form_shadow').hide();
            $('#register_form').hide();
            $('input').val('');
            refresh('Pomyślna rejestracja.');
        } else {
            statusMessage('Błąd przy rejestracji.');
            hideLoading();
        }
    });
}